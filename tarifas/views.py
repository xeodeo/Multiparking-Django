from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from parqueadero.models import TipoEspacio
from usuarios.mixins import AdminRequiredMixin

from .models import Tarifa


class TarifaListView(AdminRequiredMixin, View):
    def get(self, request):
        tarifas = Tarifa.objects.select_related('fkIdTipoEspacio').order_by('nombre')
        activas = tarifas.filter(activa=True).count()
        tipos_count = TipoEspacio.objects.count()
        return render(request, 'admin_panel/tarifas/list.html', {
            'active_page': 'tarifas',
            'tarifas': tarifas,
            'activas': activas,
            'tipos_count': tipos_count,
            'total_tarifas': tarifas.count(),
        })


class TarifaCreateView(AdminRequiredMixin, View):
    def get(self, request):
        return render(request, 'admin_panel/tarifas/form.html', {
            'active_page': 'tarifas',
            'title': 'Nueva Tarifa',
            'tipos': TipoEspacio.objects.order_by('nombre'),
        })

    def post(self, request):
        nombre = request.POST.get('nombre', '').strip()
        tipo_id = request.POST.get('fkIdTipoEspacio', '')
        precio_hora = request.POST.get('precioHora', '')
        precio_hora_visitante = request.POST.get('precioHoraVisitante', '') or 0  # Opcional; 0 si no se ingresa
        precio_dia = request.POST.get('precioDia', '')
        precio_mensual = request.POST.get('precioMensual', '')
        activa = 'activa' in request.POST
        fecha_inicio = request.POST.get('fechaInicio', '')
        fecha_fin = request.POST.get('fechaFin', '') or None  # Opcional; None = tarifa vigente indefinidamente

        ctx = {
            'active_page': 'tarifas',
            'title': 'Nueva Tarifa',
            'tipos': TipoEspacio.objects.order_by('nombre'),
            'tarifa': {
                'nombre': nombre,
                'fkIdTipoEspacio_id': tipo_id,
                'precioHora': precio_hora,
                'precioHoraVisitante': precio_hora_visitante,
                'precioDia': precio_dia,
                'precioMensual': precio_mensual,
                'activa': activa,
                'fechaInicio': fecha_inicio,
                'fechaFin': fecha_fin,
            },
        }

        if not all([nombre, tipo_id, precio_hora, precio_dia, precio_mensual, fecha_inicio]):
            messages.error(request, 'Todos los campos obligatorios deben estar llenos.')
            return render(request, 'admin_panel/tarifas/form.html', ctx)

        try:
            # Decimal(str(...)) convierte el string de forma segura; evita errores de float con valores grandes
            for campo, valor_str in [('Precio hora', precio_hora), ('Precio día', precio_dia),
                                      ('Precio mensual', precio_mensual)]:
                if Decimal(str(valor_str)) < 0:
                    messages.error(request, f'{campo} no puede ser negativo.')
                    return render(request, 'admin_panel/tarifas/form.html', ctx)
            if precio_hora_visitante and Decimal(str(precio_hora_visitante)) < 0:
                messages.error(request, 'Precio hora visitante no puede ser negativo.')
                return render(request, 'admin_panel/tarifas/form.html', ctx)
        except (InvalidOperation, ValueError):
            messages.error(request, 'Los precios deben ser números válidos.')
            return render(request, 'admin_panel/tarifas/form.html', ctx)

        Tarifa.objects.create(
            nombre=nombre,
            fkIdTipoEspacio_id=tipo_id,
            precioHora=precio_hora,
            precioHoraVisitante=precio_hora_visitante,
            precioDia=precio_dia,
            precioMensual=precio_mensual,
            activa=activa,
            fechaInicio=fecha_inicio,
            fechaFin=fecha_fin,
        )
        messages.success(request, 'Tarifa creada exitosamente.')
        return redirect('admin_tarifas')


class TarifaUpdateView(AdminRequiredMixin, View):
    def get(self, request, pk):
        tarifa = get_object_or_404(Tarifa, pk=pk)
        return render(request, 'admin_panel/tarifas/form.html', {
            'active_page': 'tarifas',
            'title': 'Editar Tarifa',
            'tarifa': tarifa,
            'tipos': TipoEspacio.objects.order_by('nombre'),
        })

    def post(self, request, pk):
        tarifa = get_object_or_404(Tarifa, pk=pk)
        tarifa.nombre = request.POST.get('nombre', '').strip()
        tarifa.fkIdTipoEspacio_id = request.POST.get('fkIdTipoEspacio', '')
        tarifa.precioHora = request.POST.get('precioHora', '')
        tarifa.precioHoraVisitante = request.POST.get('precioHoraVisitante', '') or 0
        tarifa.precioDia = request.POST.get('precioDia', '')
        tarifa.precioMensual = request.POST.get('precioMensual', '')
        tarifa.activa = 'activa' in request.POST
        tarifa.fechaInicio = request.POST.get('fechaInicio', '')
        tarifa.fechaFin = request.POST.get('fechaFin', '') or None

        if not all([tarifa.nombre, tarifa.fkIdTipoEspacio_id, tarifa.precioHora,
                    tarifa.precioDia, tarifa.precioMensual, tarifa.fechaInicio]):
            messages.error(request, 'Todos los campos obligatorios deben estar llenos.')
            return render(request, 'admin_panel/tarifas/form.html', {
                'active_page': 'tarifas',
                'title': 'Editar Tarifa',
                'tarifa': tarifa,
                'tipos': TipoEspacio.objects.order_by('nombre'),
            })

        edit_ctx = {
            'active_page': 'tarifas',
            'title': 'Editar Tarifa',
            'tarifa': tarifa,
            'tipos': TipoEspacio.objects.order_by('nombre'),
        }
        try:
            for campo, val in [('Precio hora', tarifa.precioHora), ('Precio día', tarifa.precioDia),
                                ('Precio mensual', tarifa.precioMensual)]:
                if Decimal(str(val)) < 0:
                    messages.error(request, f'{campo} no puede ser negativo.')
                    return render(request, 'admin_panel/tarifas/form.html', edit_ctx)
            if tarifa.precioHoraVisitante and Decimal(str(tarifa.precioHoraVisitante)) < 0:
                messages.error(request, 'Precio hora visitante no puede ser negativo.')
                return render(request, 'admin_panel/tarifas/form.html', edit_ctx)
        except (InvalidOperation, ValueError):
            messages.error(request, 'Los precios deben ser números válidos.')
            return render(request, 'admin_panel/tarifas/form.html', edit_ctx)

        tarifa.save()
        messages.success(request, 'Tarifa actualizada.')
        return redirect('admin_tarifas')


class TarifaToggleView(AdminRequiredMixin, View):
    """Activar/desactivar tarifa vía POST (AJAX o normal)."""
    def post(self, request, pk):
        tarifa = get_object_or_404(Tarifa, pk=pk)
        tarifa.activa = not tarifa.activa
        tarifa.save()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'ok': True, 'activa': tarifa.activa})
        messages.success(request, f'Tarifa {"activada" if tarifa.activa else "desactivada"}.')
        return redirect('admin_tarifas')


class TarifaDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        tarifa = get_object_or_404(Tarifa, pk=pk)
        tarifa.delete()
        messages.success(request, 'Tarifa eliminada.')
        return redirect('admin_tarifas')
