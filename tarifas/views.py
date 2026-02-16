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
        precio_dia = request.POST.get('precioDia', '')
        precio_mensual = request.POST.get('precioMensual', '')
        activa = 'activa' in request.POST
        fecha_inicio = request.POST.get('fechaInicio', '')
        fecha_fin = request.POST.get('fechaFin', '') or None

        ctx = {
            'active_page': 'tarifas',
            'title': 'Nueva Tarifa',
            'tipos': TipoEspacio.objects.order_by('nombre'),
            'tarifa': {
                'nombre': nombre,
                'fkIdTipoEspacio_id': tipo_id,
                'precioHora': precio_hora,
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

        Tarifa.objects.create(
            nombre=nombre,
            fkIdTipoEspacio_id=tipo_id,
            precioHora=precio_hora,
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
