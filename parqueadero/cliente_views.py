from decimal import Decimal
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.utils import timezone

from parqueadero.models import Espacio, InventarioParqueo
from parqueadero.views import ClienteRequiredMixin
from pagos.models import Pago
from cupones.models import Cupon, CuponAplicado
from tarifas.models import Tarifa


class ClienteSalidaView(ClienteRequiredMixin, View):
    """Vista para procesar la salida del vehículo del parqueadero"""

    def get(self, request):
        usuario_id = request.session.get('usuario_id')

        # Buscar vehículo dentro del parqueadero
        registro = InventarioParqueo.objects.filter(
            fkIdVehiculo__fkIdUsuario_id=usuario_id,
            parHoraSalida__isnull=True
        ).select_related(
            'fkIdVehiculo',
            'fkIdEspacio__fkIdPiso',
            'fkIdEspacio__fkIdTipoEspacio'
        ).first()

        if not registro:
            messages.error(request, 'No tienes ningún vehículo dentro del parqueadero.')
            return redirect('dashboard')

        # Calcular costo
        ahora = timezone.now()
        entrada = registro.parHoraEntrada
        duracion = ahora - entrada

        dias = duracion.days
        segundos = duracion.seconds
        horas = segundos // 3600
        minutos = (segundos % 3600) // 60

        duracion_str = ""
        if dias > 0:
            duracion_str += f"{dias}d "
        if horas > 0:
            duracion_str += f"{horas}h "
        duracion_str += f"{minutos}m"
        if not duracion_str:
            duracion_str = "Menos de 1m"

        # Obtener tarifa
        tarifa = Tarifa.objects.filter(
            fkIdTipoEspacio=registro.fkIdEspacio.fkIdTipoEspacio,
            activa=True
        ).first()

        monto_total = Decimal('0')
        tarifa_info = None

        if tarifa:
            horas_totales = dias * 24 + horas + (1 if minutos > 0 else 0)
            if horas_totales == 0 and dias == 0:
                horas_totales = 1
            monto_total = tarifa.precioHora * horas_totales
            tarifa_info = {
                'precio_hora': tarifa.precioHora,
                'horas_totales': horas_totales
            }

        # Obtener cupones activos
        hoy = timezone.now().date()
        cupones_disponibles = Cupon.objects.filter(
            cupActivo=True,
            cupFechaInicio__lte=hoy,
            cupFechaFin__gte=hoy
        )

        return render(request, 'cliente/salida_pago.html', {
            'registro': registro,
            'duracion': duracion_str,
            'tarifa_info': tarifa_info,
            'monto_total': monto_total,
            'cupones': cupones_disponibles,
        })

    def post(self, request):
        usuario_id = request.session.get('usuario_id')

        # Buscar vehículo dentro del parqueadero
        registro = InventarioParqueo.objects.filter(
            fkIdVehiculo__fkIdUsuario_id=usuario_id,
            parHoraSalida__isnull=True
        ).select_related(
            'fkIdVehiculo',
            'fkIdEspacio__fkIdTipoEspacio'
        ).first()

        if not registro:
            messages.error(request, 'No tienes ningún vehículo dentro del parqueadero.')
            return redirect('dashboard')

        # Obtener datos del formulario
        metodo_pago = request.POST.get('metodo_pago', 'EFECTIVO')
        codigo_cupon = request.POST.get('codigo_cupon', '').strip()

        # Calcular costo
        ahora = timezone.now()
        duracion = ahora - registro.parHoraEntrada

        dias = duracion.days
        segundos = duracion.seconds
        horas = segundos // 3600
        minutos = (segundos % 3600) // 60

        # Obtener tarifa
        tarifa = Tarifa.objects.filter(
            fkIdTipoEspacio=registro.fkIdEspacio.fkIdTipoEspacio,
            activa=True
        ).first()

        monto_total = Decimal('0')

        if tarifa:
            horas_totales = dias * 24 + horas + (1 if minutos > 0 else 0)
            if horas_totales == 0 and dias == 0:
                horas_totales = 1
            monto_total = tarifa.precioHora * horas_totales

        # Aplicar cupón si existe
        cupon = None
        monto_descuento = Decimal('0')

        if codigo_cupon:
            try:
                hoy = timezone.now().date()
                cupon = Cupon.objects.get(
                    cupNombre__iexact=codigo_cupon,
                    cupActivo=True,
                    cupFechaInicio__lte=hoy,
                    cupFechaFin__gte=hoy
                )

                if cupon.cupTipo == 'PORCENTAJE':
                    monto_descuento = (monto_total * cupon.cupValor) / 100
                else:  # VALOR_FIJO
                    monto_descuento = min(cupon.cupValor, monto_total)

            except Cupon.DoesNotExist:
                messages.warning(request, f'El cupón "{codigo_cupon}" no es válido o ha expirado.')

        # Calcular monto final
        monto_final = max(monto_total - monto_descuento, Decimal('0'))

        # Marcar salida
        registro.parHoraSalida = ahora
        registro.save()

        # Crear registro de pago
        if metodo_pago == 'EFECTIVO':
            estado_pago = 'PENDIENTE'
            mensaje = f'Pago registrado: ${monto_final:,.0f} COP en efectivo (PENDIENTE). Dirígete a caja para completar el pago.'
        else:  # PSE
            estado_pago = 'PAGADO'
            mensaje = f'Pago procesado exitosamente: ${monto_final:,.0f} COP vía PSE. ¡Gracias por tu preferencia!'

        pago = Pago.objects.create(
            pagMonto=monto_final,
            pagMetodo=metodo_pago,
            pagEstado=estado_pago,
            fkIdParqueo=registro
        )

        # Aplicar cupón al pago si existe
        if cupon and monto_descuento > 0:
            CuponAplicado.objects.create(
                fkIdPago=pago,
                fkIdCupon=cupon,
                montoDescontado=monto_descuento
            )

        # Liberar espacio
        espacio = registro.fkIdEspacio
        espacio.espEstado = 'DISPONIBLE'
        espacio.save()

        # Agregar mensaje de tiempo límite
        messages.success(request, mensaje)
        messages.info(request, '⚠️ IMPORTANTE: Tienes 10 minutos para salir del parqueadero y evitar sanciones.')

        return redirect('dashboard')
