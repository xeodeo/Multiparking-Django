"""
Vistas para que los clientes gestionen sus propios vehículos
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View

from usuarios.models import Usuario
from vehiculos.models import Vehiculo


class ClienteRequiredMixin:
    """Mixin para requerir que el usuario sea un cliente autenticado"""
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            messages.error(request, 'Debes iniciar sesión.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class ClienteCrearVehiculoView(ClienteRequiredMixin, View):
    """Vista para que un cliente cree su propio vehículo"""

    def get(self, request):
        return render(request, 'cliente/vehiculo_form.html', {
            'title': 'Agregar Vehículo',
        })

    def post(self, request):
        usuario_id = request.session.get('usuario_id')
        usuario = Usuario.objects.get(pk=usuario_id)

        placa = request.POST.get('vehPlaca', '').strip().upper()
        tipo = request.POST.get('vehTipo', 'CARRO')
        marca = request.POST.get('vehMarca', '').strip()
        modelo = request.POST.get('vehModelo', '').strip()
        color = request.POST.get('vehColor', '').strip()
        estado = request.POST.get('vehEstado') == 'on'

        # Validaciones
        if not placa:
            messages.error(request, 'La placa es obligatoria.')
            return render(request, 'cliente/vehiculo_form.html', {
                'title': 'Agregar Vehículo',
                'placa': placa,
                'tipo': tipo,
                'marca': marca,
                'modelo': modelo,
                'color': color,
                'estado': estado,
            })

        # Verificar si el vehículo ya existe
        vehiculo_existente = Vehiculo.objects.filter(vehPlaca=placa).first()

        if vehiculo_existente:
            # Si existe y es visitante, permitir que el usuario lo reclame
            if vehiculo_existente.es_visitante:
                # Convertir de visitante a vehículo registrado
                vehiculo_existente.es_visitante = False
                vehiculo_existente.fkIdUsuario = usuario
                vehiculo_existente.vehTipo = tipo
                vehiculo_existente.vehMarca = marca or vehiculo_existente.vehMarca
                vehiculo_existente.vehModelo = modelo or vehiculo_existente.vehModelo
                vehiculo_existente.vehColor = color or vehiculo_existente.vehColor
                vehiculo_existente.vehEstado = estado if estado else True
                vehiculo_existente.nombre_contacto = None
                vehiculo_existente.telefono_contacto = None
                vehiculo_existente.save()

                messages.success(request, f'Vehículo {placa} registrado exitosamente. Era un vehículo visitante y ahora es tuyo.')
                return redirect('dashboard')
            else:
                # Si existe y ya tiene dueño
                messages.error(request, f'La placa {placa} ya está registrada por otro usuario.')
                return render(request, 'cliente/vehiculo_form.html', {
                    'title': 'Agregar Vehículo',
                    'placa': placa,
                    'tipo': tipo,
                    'marca': marca,
                    'modelo': modelo,
                    'color': color,
                    'estado': estado,
                })

        # Crear nuevo vehículo
        Vehiculo.objects.create(
            vehPlaca=placa,
            vehTipo=tipo,
            vehMarca=marca,
            vehModelo=modelo,
            vehColor=color,
            vehEstado=estado if estado else True,
            es_visitante=False,
            fkIdUsuario=usuario
        )

        messages.success(request, f'Vehículo {placa} agregado exitosamente.')
        return redirect('dashboard')


class ClienteEditarVehiculoView(ClienteRequiredMixin, View):
    """Vista para que un cliente edite su propio vehículo"""

    def get(self, request, pk):
        usuario_id = request.session.get('usuario_id')
        vehiculo = get_object_or_404(Vehiculo, pk=pk, fkIdUsuario__pk=usuario_id, es_visitante=False)

        return render(request, 'cliente/vehiculo_form.html', {
            'title': 'Editar Vehículo',
            'vehiculo': vehiculo,
        })

    def post(self, request, pk):
        usuario_id = request.session.get('usuario_id')
        vehiculo = get_object_or_404(Vehiculo, pk=pk, fkIdUsuario__pk=usuario_id, es_visitante=False)

        placa = request.POST.get('vehPlaca', '').strip().upper()
        tipo = request.POST.get('vehTipo', 'CARRO')
        marca = request.POST.get('vehMarca', '').strip()
        modelo = request.POST.get('vehModelo', '').strip()
        color = request.POST.get('vehColor', '').strip()
        estado = request.POST.get('vehEstado') == 'on'

        # Validaciones
        if not placa:
            messages.error(request, 'La placa es obligatoria.')
            return render(request, 'cliente/vehiculo_form.html', {
                'title': 'Editar Vehículo',
                'vehiculo': vehiculo,
            })

        # Verificar que la placa no exista en otro vehículo
        if Vehiculo.objects.filter(vehPlaca=placa).exclude(pk=pk).exists():
            messages.error(request, f'Ya existe otro vehículo con la placa {placa}.')
            return render(request, 'cliente/vehiculo_form.html', {
                'title': 'Editar Vehículo',
                'vehiculo': vehiculo,
            })

        # Actualizar vehículo
        vehiculo.vehPlaca = placa
        vehiculo.vehTipo = tipo
        vehiculo.vehMarca = marca
        vehiculo.vehModelo = modelo
        vehiculo.vehColor = color
        vehiculo.vehEstado = estado
        vehiculo.save()

        messages.success(request, f'Vehículo {placa} actualizado exitosamente.')
        return redirect('dashboard')
