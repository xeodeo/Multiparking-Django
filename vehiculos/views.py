from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.db.models import Q

from usuarios.mixins import AdminRequiredMixin
from .models import Vehiculo
from usuarios.models import Usuario


class VehiculoListView(AdminRequiredMixin, View):
    def get(self, request):
        qs = Vehiculo.objects.select_related('fkIdUsuario').order_by('-pk')

        q = request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(vehPlaca__icontains=q) |
                Q(vehMarca__icontains=q) |
                Q(fkIdUsuario__usuNombreCompleto__icontains=q) |
                Q(nombre_contacto__icontains=q)
            )

        total = Vehiculo.objects.count()
        registrados = Vehiculo.objects.filter(es_visitante=False).count()
        visitantes = Vehiculo.objects.filter(es_visitante=True).count()

        return render(request, 'admin_panel/vehiculos/list.html', {
            'active_page': 'vehiculos',
            'vehiculos': qs,
            'q': q,
            'total': total,
            'registrados': registrados,
            'visitantes': visitantes,
        })


class VehiculoCreateView(AdminRequiredMixin, View):
    def get(self, request):
        return render(request, 'admin_panel/vehiculos/form.html', {
            'active_page': 'vehiculos',
            'title': 'Nuevo Vehículo',
            'usuarios': Usuario.objects.filter(usuEstado=True).order_by('usuNombreCompleto'),
        })

    def post(self, request):
        placa = request.POST.get('vehPlaca', '').strip().upper()
        tipo = request.POST.get('vehTipo', '').strip()
        color = request.POST.get('vehColor', '').strip()
        marca = request.POST.get('vehMarca', '').strip()
        modelo = request.POST.get('vehModelo', '').strip()
        usuario_id = request.POST.get('fkIdUsuario', '')
        es_visitante = request.POST.get('es_visitante') == 'on'
        nombre_contacto = request.POST.get('nombre_contacto', '').strip()
        telefono_contacto = request.POST.get('telefono_contacto', '').strip()

        ctx = {
            'active_page': 'vehiculos',
            'title': 'Nuevo Vehículo',
            'usuarios': Usuario.objects.filter(usuEstado=True).order_by('usuNombreCompleto'),
            'vehiculo': {
                'vehPlaca': placa, 'vehTipo': tipo, 'vehColor': color,
                'vehMarca': marca, 'vehModelo': modelo,
                'es_visitante': es_visitante,
                'nombre_contacto': nombre_contacto,
                'telefono_contacto': telefono_contacto,
            },
        }

        if not all([placa, tipo]):
            messages.error(request, 'Placa y tipo son obligatorios.')
            return render(request, 'admin_panel/vehiculos/form.html', ctx)

        if Vehiculo.objects.filter(vehPlaca=placa).exists():
            messages.error(request, f'Ya existe un vehículo con placa {placa}.')
            return render(request, 'admin_panel/vehiculos/form.html', ctx)

        Vehiculo.objects.create(
            vehPlaca=placa,
            vehTipo=tipo,
            vehColor=color,
            vehMarca=marca,
            vehModelo=modelo,
            fkIdUsuario_id=usuario_id if usuario_id else None,
            es_visitante=es_visitante or not usuario_id,
            nombre_contacto=nombre_contacto,
            telefono_contacto=telefono_contacto,
        )
        messages.success(request, 'Vehículo creado exitosamente.')
        return redirect('admin_vehiculos')


class VehiculoUpdateView(AdminRequiredMixin, View):
    def get(self, request, pk):
        vehiculo = get_object_or_404(Vehiculo, pk=pk)
        return render(request, 'admin_panel/vehiculos/form.html', {
            'active_page': 'vehiculos',
            'title': 'Editar Vehículo',
            'vehiculo': vehiculo,
            'usuarios': Usuario.objects.filter(usuEstado=True).order_by('usuNombreCompleto'),
        })

    def post(self, request, pk):
        vehiculo = get_object_or_404(Vehiculo, pk=pk)
        placa = request.POST.get('vehPlaca', '').strip().upper()
        vehiculo.vehTipo = request.POST.get('vehTipo', '').strip()
        vehiculo.vehColor = request.POST.get('vehColor', '').strip()
        vehiculo.vehMarca = request.POST.get('vehMarca', '').strip()
        vehiculo.vehModelo = request.POST.get('vehModelo', '').strip()
        usuario_id = request.POST.get('fkIdUsuario', '')
        vehiculo.es_visitante = request.POST.get('es_visitante') == 'on' or not usuario_id
        vehiculo.nombre_contacto = request.POST.get('nombre_contacto', '').strip()
        vehiculo.telefono_contacto = request.POST.get('telefono_contacto', '').strip()

        ctx = {
            'active_page': 'vehiculos',
            'title': 'Editar Vehículo',
            'vehiculo': vehiculo,
            'usuarios': Usuario.objects.filter(usuEstado=True).order_by('usuNombreCompleto'),
        }

        if not all([placa, vehiculo.vehTipo]):
            messages.error(request, 'Placa y tipo son obligatorios.')
            return render(request, 'admin_panel/vehiculos/form.html', ctx)

        if Vehiculo.objects.filter(vehPlaca=placa).exclude(pk=pk).exists():
            messages.error(request, f'Ya existe otro vehículo con placa {placa}.')
            return render(request, 'admin_panel/vehiculos/form.html', ctx)

        vehiculo.vehPlaca = placa
        vehiculo.fkIdUsuario_id = usuario_id if usuario_id else None
        vehiculo.save()
        messages.success(request, 'Vehículo actualizado.')
        return redirect('admin_vehiculos')


class VehiculoDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        vehiculo = get_object_or_404(Vehiculo, pk=pk)
        from parqueadero.models import InventarioParqueo
        if InventarioParqueo.objects.filter(fkIdVehiculo=vehiculo, parHoraSalida__isnull=True).exists():
            messages.error(request, 'No se puede eliminar un vehículo que está actualmente parqueado.')
            return redirect('admin_vehiculos')
        vehiculo.delete()
        messages.success(request, 'Vehículo eliminado.')
        return redirect('admin_vehiculos')
