from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from multiparking import email_utils
from usuarios.mixins import AdminRequiredMixin
from usuarios.models import Usuario
from vehiculos.models import Vehiculo
from parqueadero.models import Espacio

from .models import Novedad


def _validar_foto(foto):
    """Valida tipo y tamaño de la foto. Devuelve (True, None) o (False, msg_error)."""
    allowed_types = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}
    if foto.content_type not in allowed_types:
        return False, 'Solo se permiten imágenes (JPG, PNG, GIF, WEBP).'
    if foto.size > 5 * 1024 * 1024:
        return False, 'La imagen no puede superar 5 MB.'
    return True, None


class NovedadListView(AdminRequiredMixin, View):
    def get(self, request):
        novedades = Novedad.objects.select_related(
            'fkIdVehiculo', 'fkIdEspacio', 'fkIdReportador', 'fkIdResponsable'
        )

        estado = request.GET.get('estado', '')
        if estado:
            novedades = novedades.filter(novEstado=estado)

        q = request.GET.get('q', '').strip()
        if q:
            novedades = novedades.filter(novDescripcion__icontains=q)

        counts = {
            item['novEstado']: item['c']
            for item in Novedad.objects.values('novEstado').annotate(c=Count('pk'))
        }
        return render(request, 'admin_panel/novedades/list.html', {
            'active_page': 'novedades',
            'novedades': novedades,
            'estado_sel': estado,
            'q': q,
            'total': novedades.count(),
            'pendientes': counts.get('PENDIENTE', 0),
            'en_proceso': counts.get('EN_PROCESO', 0),
            'resueltos': counts.get('RESUELTO', 0),
        })


class NovedadCreateView(AdminRequiredMixin, View):
    def get(self, request):
        vehiculos = Vehiculo.objects.filter(vehEstado=True).select_related('fkIdUsuario')
        espacios = Espacio.objects.select_related('fkIdPiso')
        responsables = Usuario.objects.filter(
            rolTipoRol__in=['ADMIN', 'VIGILANTE'], usuEstado=True
        )
        # Pre-selección desde Vista General de Pisos (?espacio_id=X&vehiculo_id=Y)
        preselect_espacio = request.GET.get('espacio_id') or ''
        preselect_vehiculo = request.GET.get('vehiculo_id') or ''
        return render(request, 'admin_panel/novedades/form.html', {
            'active_page': 'novedades',
            'title': 'Registrar Novedad',
            'vehiculos': vehiculos,
            'espacios': espacios,
            'responsables': responsables,
            'preselect_espacio': preselect_espacio,
            'preselect_vehiculo': preselect_vehiculo,
        })

    def post(self, request):
        descripcion = request.POST.get('descripcion', '').strip()
        vehiculo_id = request.POST.get('vehiculo_id') or None
        espacio_id = request.POST.get('espacio_id') or None
        responsable_id = request.POST.get('responsable_id') or None
        foto = request.FILES.get('foto')

        if not descripcion:
            messages.error(request, 'La descripción es obligatoria.')
            return redirect('admin_novedades_crear')

        if foto:
            ok, err = _validar_foto(foto)
            if not ok:
                messages.error(request, err)
                return redirect('admin_novedades_crear')

        reportador = Usuario.objects.filter(pk=request.session.get('usuario_id')).first()

        novedad = Novedad(
            novDescripcion=descripcion,
            novEstado='PENDIENTE',
            fkIdReportador=reportador,
        )
        if vehiculo_id:
            novedad.fkIdVehiculo_id = vehiculo_id
        if espacio_id:
            novedad.fkIdEspacio_id = espacio_id
        if responsable_id:
            novedad.fkIdResponsable_id = responsable_id
        if foto:
            novedad.novFoto = foto
        novedad.save()

        # Notificar al usuario afectado
        email_utils.enviar_novedad(novedad)

        messages.success(request, 'Novedad registrada.')
        return redirect('admin_novedades')


class NovedadUpdateView(AdminRequiredMixin, View):
    def get(self, request, pk):
        novedad = get_object_or_404(Novedad, pk=pk)
        vehiculos = Vehiculo.objects.filter(vehEstado=True).select_related('fkIdUsuario')
        espacios = Espacio.objects.select_related('fkIdPiso')
        responsables = Usuario.objects.filter(
            rolTipoRol__in=['ADMIN', 'VIGILANTE'], usuEstado=True
        )
        return render(request, 'admin_panel/novedades/form.html', {
            'active_page': 'novedades',
            'title': 'Gestionar Novedad',
            'novedad': novedad,
            'vehiculos': vehiculos,
            'espacios': espacios,
            'responsables': responsables,
        })

    def post(self, request, pk):
        novedad = get_object_or_404(Novedad, pk=pk)

        novedad.novDescripcion = request.POST.get('descripcion', novedad.novDescripcion).strip()
        novedad.novEstado = request.POST.get('estado', novedad.novEstado)
        novedad.novComentario = request.POST.get('comentario', '').strip()

        vehiculo_id = request.POST.get('vehiculo_id') or None
        espacio_id = request.POST.get('espacio_id') or None
        responsable_id = request.POST.get('responsable_id') or None
        foto = request.FILES.get('foto')

        if foto:
            ok, err = _validar_foto(foto)
            if not ok:
                messages.error(request, err)
                return redirect('admin_novedades_editar', pk=pk)

        novedad.fkIdVehiculo_id = vehiculo_id
        novedad.fkIdEspacio_id = espacio_id
        novedad.fkIdResponsable_id = responsable_id
        if foto:
            novedad.novFoto = foto
        novedad.save()

        # Notificar al usuario sobre el cambio de estado
        email_utils.enviar_novedad(novedad)

        messages.success(request, f'Novedad #{novedad.pk} actualizada.')
        return redirect('admin_novedades')


class NovedadDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        novedad = get_object_or_404(Novedad, pk=pk)
        novedad.delete()
        messages.success(request, 'Novedad eliminada.')
        return redirect('admin_novedades')
