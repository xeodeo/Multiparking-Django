from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.db.models import Q

from usuarios.mixins import AdminRequiredMixin
from .models import Vehiculo
from .validators import validar_datos_vehiculo, RE_SOLO_LETRAS, RE_SOLO_NUMEROS
from usuarios.models import Usuario


class VehiculoListView(AdminRequiredMixin, View):
    def get(self, request):
        qs = Vehiculo.objects.select_related('fkIdUsuario').order_by('-pk')

        q = request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(vehPlaca__icontains=q) |
                Q(vehMarca__icontains=q) |
                Q(fkIdUsuario__usuNombre__icontains=q) |
                Q(fkIdUsuario__usuApellido__icontains=q) |
                Q(nombre_contacto__icontains=q)
            )

        total = Vehiculo.objects.count()
        registrados = Vehiculo.objects.filter(fkIdUsuario__isnull=False).count()
        visitantes = Vehiculo.objects.filter(fkIdUsuario__isnull=True).count()

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
            'usuarios': Usuario.objects.filter(usuEstado=True).order_by('usuNombre', 'usuApellido'),
        })

    def post(self, request):
        placa = request.POST.get('vehPlaca', '').strip().upper()
        tipo = request.POST.get('vehTipo', 'Carro')
        color = request.POST.get('vehColor', '').strip()
        marca = request.POST.get('vehMarca', '').strip()
        modelo = request.POST.get('vehModelo', '').strip()
        estado = request.POST.get('vehEstado') == 'on'
        usuario_id = request.POST.get('fkIdUsuario', '')
        nombre_contacto = request.POST.get('nombre_contacto', '').strip()
        telefono_contacto = request.POST.get('telefono_contacto', '').strip()

        ctx = {
            'active_page': 'vehiculos',
            'title': 'Nuevo Vehículo',
            'usuarios': Usuario.objects.filter(usuEstado=True).order_by('usuNombre', 'usuApellido'),
            'vehiculo': {
                'vehPlaca': placa, 'vehTipo': tipo, 'vehColor': color,
                'vehMarca': marca, 'vehModelo': modelo, 'vehEstado': estado,
                'nombre_contacto': nombre_contacto,
                'telefono_contacto': telefono_contacto,
            },
        }

        err = validar_datos_vehiculo(placa, tipo, color, marca, modelo,
                                    nombre_contacto, telefono_contacto)
        if err:
            messages.error(request, err)
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
            vehEstado=estado if estado else True,
            fkIdUsuario_id=usuario_id if usuario_id else None,  # null si es un visitante sin cuenta
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
            'usuarios': Usuario.objects.filter(usuEstado=True).order_by('usuNombre', 'usuApellido'),
        })

    def post(self, request, pk):
        vehiculo = get_object_or_404(Vehiculo, pk=pk)
        placa = request.POST.get('vehPlaca', '').strip().upper()
        vehiculo.vehTipo = request.POST.get('vehTipo', 'Carro')
        vehiculo.vehColor = request.POST.get('vehColor', '').strip()
        vehiculo.vehMarca = request.POST.get('vehMarca', '').strip()
        vehiculo.vehModelo = request.POST.get('vehModelo', '').strip()
        vehiculo.vehEstado = request.POST.get('vehEstado') == 'on'
        usuario_id = request.POST.get('fkIdUsuario', '')
        vehiculo.nombre_contacto = request.POST.get('nombre_contacto', '').strip()
        vehiculo.telefono_contacto = request.POST.get('telefono_contacto', '').strip()

        ctx = {
            'active_page': 'vehiculos',
            'title': 'Editar Vehículo',
            'vehiculo': vehiculo,
            'usuarios': Usuario.objects.filter(usuEstado=True).order_by('usuNombre', 'usuApellido'),
        }

        err = validar_datos_vehiculo(placa, vehiculo.vehTipo, vehiculo.vehColor,
                                    vehiculo.vehMarca, vehiculo.vehModelo,
                                    vehiculo.nombre_contacto, vehiculo.telefono_contacto)
        if err:
            messages.error(request, err)
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
        # No se puede eliminar si el vehículo tiene un registro activo (parHoraSalida IS NULL = aún estacionado)
        if InventarioParqueo.objects.filter(fkIdVehiculo=vehiculo, parHoraSalida__isnull=True).exists():
            messages.error(request, 'No se puede eliminar un vehículo que está actualmente parqueado.')
            return redirect('admin_vehiculos')
        vehiculo.delete()
        messages.success(request, 'Vehículo eliminado.')
        return redirect('admin_vehiculos')
