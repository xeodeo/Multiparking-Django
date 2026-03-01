import re
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from usuarios.mixins import AdminRequiredMixin

from .models import Cupon

RE_CODIGO_CUPON = re.compile(r'^[A-Z0-9]+$')


class CuponListView(AdminRequiredMixin, View):
    def get(self, request):
        cupones = Cupon.objects.order_by('-cupActivo', 'cupNombre')
        activos = cupones.filter(cupActivo=True).count()
        total = cupones.count()
        return render(request, 'admin_panel/cupones/list.html', {
            'active_page': 'cupones',
            'cupones': cupones,
            'activos': activos,
            'inactivos': total - activos,
            'total': total,
        })


class CuponCreateView(AdminRequiredMixin, View):
    def get(self, request):
        return render(request, 'admin_panel/cupones/form.html', {
            'active_page': 'cupones',
            'title': 'Nuevo Cupón',
        })

    def post(self, request):
        nombre = request.POST.get('cupNombre', '').strip()
        codigo = request.POST.get('cupCodigo', '').strip().upper()
        tipo = request.POST.get('cupTipo', '')
        valor = request.POST.get('cupValor', '')
        descripcion = request.POST.get('cupDescripcion', '').strip()
        fecha_inicio = request.POST.get('cupFechaInicio', '')
        fecha_fin = request.POST.get('cupFechaFin', '')
        activo = 'cupActivo' in request.POST

        ctx = {
            'active_page': 'cupones',
            'title': 'Nuevo Cupón',
            'cupon': {
                'cupNombre': nombre,
                'cupCodigo': codigo,
                'cupTipo': tipo,
                'cupValor': valor,
                'cupDescripcion': descripcion,
                'cupFechaInicio': fecha_inicio,
                'cupFechaFin': fecha_fin,
                'cupActivo': activo,
            },
        }

        if not all([nombre, codigo, tipo, valor, fecha_inicio, fecha_fin]):
            messages.error(request, 'Todos los campos obligatorios deben estar llenos.')
            return render(request, 'admin_panel/cupones/form.html', ctx)

        if not RE_CODIGO_CUPON.match(codigo):
            messages.error(request, 'El código solo acepta letras mayúsculas y números.')
            return render(request, 'admin_panel/cupones/form.html', ctx)

        try:
            valor_decimal = Decimal(valor)
            if valor_decimal < 0:
                messages.error(request, 'El valor no puede ser negativo.')
                return render(request, 'admin_panel/cupones/form.html', ctx)
        except (InvalidOperation, ValueError):
            messages.error(request, 'El valor debe ser un número válido.')
            return render(request, 'admin_panel/cupones/form.html', ctx)

        if Cupon.objects.filter(cupCodigo__iexact=codigo).exists():
            messages.error(request, f'Ya existe un cupón con el código "{codigo}".')
            return render(request, 'admin_panel/cupones/form.html', ctx)

        Cupon.objects.create(
            cupNombre=nombre,
            cupCodigo=codigo,
            cupTipo=tipo,
            cupValor=valor,
            cupDescripcion=descripcion,
            cupFechaInicio=fecha_inicio,
            cupFechaFin=fecha_fin,
            cupActivo=activo,
        )
        messages.success(request, 'Cupón creado exitosamente.')
        return redirect('admin_cupones')


class CuponUpdateView(AdminRequiredMixin, View):
    def get(self, request, pk):
        cupon = get_object_or_404(Cupon, pk=pk)
        return render(request, 'admin_panel/cupones/form.html', {
            'active_page': 'cupones',
            'title': 'Editar Cupón',
            'cupon': cupon,
        })

    def post(self, request, pk):
        cupon = get_object_or_404(Cupon, pk=pk)
        cupon.cupNombre = request.POST.get('cupNombre', '').strip()
        cupon.cupCodigo = request.POST.get('cupCodigo', '').strip().upper()
        cupon.cupTipo = request.POST.get('cupTipo', '')
        cupon.cupValor = request.POST.get('cupValor', '')
        cupon.cupDescripcion = request.POST.get('cupDescripcion', '').strip()
        cupon.cupFechaInicio = request.POST.get('cupFechaInicio', '')
        cupon.cupFechaFin = request.POST.get('cupFechaFin', '')
        cupon.cupActivo = 'cupActivo' in request.POST

        if not all([cupon.cupNombre, cupon.cupCodigo, cupon.cupTipo, cupon.cupValor,
                    cupon.cupFechaInicio, cupon.cupFechaFin]):
            messages.error(request, 'Todos los campos obligatorios deben estar llenos.')
            return render(request, 'admin_panel/cupones/form.html', {
                'active_page': 'cupones',
                'title': 'Editar Cupón',
                'cupon': cupon,
            })

        edit_ctx = {'active_page': 'cupones', 'title': 'Editar Cupón', 'cupon': cupon}

        if not RE_CODIGO_CUPON.match(cupon.cupCodigo):
            messages.error(request, 'El código solo acepta letras mayúsculas y números.')
            return render(request, 'admin_panel/cupones/form.html', edit_ctx)

        try:
            valor_decimal = Decimal(str(cupon.cupValor))
            if valor_decimal < 0:
                messages.error(request, 'El valor no puede ser negativo.')
                return render(request, 'admin_panel/cupones/form.html', edit_ctx)
        except (InvalidOperation, ValueError):
            messages.error(request, 'El valor debe ser un número válido.')
            return render(request, 'admin_panel/cupones/form.html', edit_ctx)

        # Verificar que el código no exista en otro cupón
        duplicado = Cupon.objects.filter(cupCodigo__iexact=cupon.cupCodigo).exclude(pk=pk).exists()
        if duplicado:
            messages.error(request, f'Ya existe otro cupón con el código "{cupon.cupCodigo}".')
            return render(request, 'admin_panel/cupones/form.html', {
                'active_page': 'cupones',
                'title': 'Editar Cupón',
                'cupon': cupon,
            })

        cupon.save()
        messages.success(request, 'Cupón actualizado.')
        return redirect('admin_cupones')


class CuponDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        cupon = get_object_or_404(Cupon, pk=pk)
        cupon.delete()
        messages.success(request, 'Cupón eliminado.')
        return redirect('admin_cupones')
