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
        es_visitante = registro.fkIdVehiculo.es_visitante

        if tarifa:
            horas_totales = dias * 24 + horas + (1 if minutos > 0 else 0)
            if horas_totales == 0 and dias == 0:
                horas_totales = 1
            # Usar tarifa visitante si aplica
            precio_hora = tarifa.precioHoraVisitante if es_visitante and tarifa.precioHoraVisitante > 0 else tarifa.precioHora
            monto_total = precio_hora * horas_totales
            tarifa_info = {
                'precio_hora': precio_hora,
                'horas_totales': horas_totales,
                'es_visitante': es_visitante,
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
        es_visitante = registro.fkIdVehiculo.es_visitante

        if tarifa:
            horas_totales = dias * 24 + horas + (1 if minutos > 0 else 0)
            if horas_totales == 0 and dias == 0:
                horas_totales = 1
            precio_hora = tarifa.precioHoraVisitante if es_visitante and tarifa.precioHoraVisitante > 0 else tarifa.precioHora
            monto_total = precio_hora * horas_totales

        # Aplicar cupón si existe
        cupon = None
        monto_descuento = Decimal('0')

        if codigo_cupon:
            try:
                hoy = timezone.now().date()
                cupon = Cupon.objects.get(
                    cupCodigo__iexact=codigo_cupon,
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

        # Crear registro de pago
        if metodo_pago == 'EFECTIVO':
            estado_pago = 'PENDIENTE'
        else:  # PSE
            estado_pago = 'PAGADO'

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

        if metodo_pago == 'EFECTIVO':
            # EFECTIVO: NO liberar espacio aún, se marca salida desde Vista General
            # Solo registrar el pago pendiente
            return render(request, 'cliente/salida_efectivo.html', {
                'registro': registro,
                'monto_final': monto_final,
                'pago': pago,
            })
        else:
            # PSE: Marcar salida y liberar espacio inmediatamente
            registro.parHoraSalida = ahora
            registro.save()

            espacio = registro.fkIdEspacio
            espacio.espEstado = 'DISPONIBLE'
            espacio.save()

            return render(request, 'cliente/salida_exitosa.html', {
                'registro': registro,
                'monto_final': monto_final,
                'metodo': 'PSE',
            })
