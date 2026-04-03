import secrets
from datetime import date, timedelta

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from multiparking import email_utils
from usuarios.mixins import AdminRequiredMixin
from usuarios.models import Usuario
from cupones.models import Cupon

from .models import ConfiguracionFidelidad, Sticker


class FidelidadConfigView(AdminRequiredMixin, View):
    """Panel admin para configurar la meta de stickers."""

    def get(self, request):
        config = ConfiguracionFidelidad.get()
        return render(request, 'admin_panel/fidelidad/config.html', {
            'active_page': 'fidelidad',
            'config': config,
        })

    def post(self, request):
        config = ConfiguracionFidelidad.get()
        try:
            config.metaStickers = int(request.POST.get('meta_stickers', 10))
            config.diasVencimientoBono = int(request.POST.get('dias_vencimiento', 30))
            if config.metaStickers < 1 or config.diasVencimientoBono < 1:
                raise ValueError
            config.save()
            messages.success(request, 'Configuración guardada.')
        except (ValueError, TypeError):
            messages.error(request, 'Valores inválidos.')
        return redirect('admin_fidelidad')


class PerfilClienteView(View):
    """Perfil del cliente con stickers y bono."""

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        usuario = Usuario.objects.get(pk=request.session['usuario_id'])
        config = ConfiguracionFidelidad.get()
        stickers_count = Sticker.objects.filter(fkIdUsuario=usuario).count()
        meta = config.metaStickers
        progreso = min(int((stickers_count / meta) * 100), 100) if meta > 0 else 0
        puede_reclamar = stickers_count >= meta

        # Buscar si el usuario tiene un cupón bono activo y sin usar
        bono_activo = Cupon.objects.filter(
            cupCodigo__startswith='BONO',
            cupActivo=True,
            cupFechaFin__gte=date.today(),
            cupNombre__icontains=usuario.usuNombreCompleto,
        ).exclude(aplicaciones__isnull=False).first()

        return render(request, 'cliente/perfil.html', {
            'usuario': usuario,
            'stickers': stickers_count,
            'meta': meta,
            'progreso': progreso,
            'puede_reclamar': puede_reclamar,
            'bono_activo': bono_activo,
        })


class ReclamarBonoView(View):
    """El cliente reclama su bono cuando tiene suficientes stickers."""

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        usuario = Usuario.objects.get(pk=request.session['usuario_id'])
        config = ConfiguracionFidelidad.get()
        stickers_count = Sticker.objects.filter(fkIdUsuario=usuario).count()

        if stickers_count < config.metaStickers:
            messages.error(request, f'Necesitas {config.metaStickers} stickers. Tienes {stickers_count}.')
            return redirect('cliente_perfil')

        # Generar código único para el cupón bono
        codigo = f'BONO{secrets.token_hex(4).upper()}'
        hoy = date.today()
        vencimiento = hoy + timedelta(days=config.diasVencimientoBono)

        cupon = Cupon.objects.create(
            cupNombre=f'Bono Fidelidad — {usuario.usuNombreCompleto}',
            cupCodigo=codigo,
            cupTipo='PORCENTAJE',
            cupValor=100,
            cupDescripcion=f'Bono 100% canjeado por {config.metaStickers} stickers acumulados.',
            cupFechaInicio=hoy,
            cupFechaFin=vencimiento,
            cupActivo=True,
        )

        # Eliminar los stickers consumidos
        Sticker.objects.filter(fkIdUsuario=usuario).delete()

        # Notificar al usuario
        email_utils.enviar_bono_stickers(usuario, cupon)

        messages.success(
            request,
            f'¡Bono reclamado! Tu código es {codigo}, válido hasta el {vencimiento.strftime("%d/%m/%Y")}.'
        )
        return redirect('cliente_perfil')
