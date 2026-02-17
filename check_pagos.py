import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multiparking.settings')
django.setup()

from django.utils import timezone
from datetime import timedelta
from pagos.models import Pago

# Ver todos los pagos
pagos = Pago.objects.all()
print(f'Total pagos en BD: {pagos.count()}')

if pagos.exists():
    print('\nPrimeros 5 pagos:')
    for p in pagos[:5]:
        print(f'  ID: {p.pk}, Monto: {p.pagMonto}, Fecha: {p.pagFechaPago}, Estado: {p.pagEstado}')

    # Ver rango de fechas
    now = timezone.now()
    hoy_local = timezone.localtime(now).date()
    hace_7_dias = hoy_local - timedelta(days=6)
    print(f'\nRango de búsqueda (gráfica):')
    print(f'  Hoy: {hoy_local}')
    print(f'  Hace 7 días: {hace_7_dias}')

    # Ver pagos en ese rango
    pagos_semana = Pago.objects.filter(
        pagFechaPago__date__gte=hace_7_dias,
        pagFechaPago__date__lte=hoy_local,
        pagEstado='PAGADO',
    )
    print(f'\nPagos últimos 7 días (PAGADO): {pagos_semana.count()}')

    if pagos_semana.exists():
        for p in pagos_semana:
            fecha_local = timezone.localtime(p.pagFechaPago).date()
            print(f'  {fecha_local}: ${p.pagMonto}')
    else:
        print('  No hay pagos en los últimos 7 días.')

        # Ver cuándo fue el pago más reciente
        ultimo_pago = Pago.objects.order_by('-pagFechaPago').first()
        if ultimo_pago:
            fecha_ultimo = timezone.localtime(ultimo_pago.pagFechaPago).date()
            print(f'\n  El pago más reciente fue: {fecha_ultimo}')
            print(f'  Está fuera del rango de 7 días.')
else:
    print('\n❌ No hay pagos en la base de datos.')
    print('\n📝 Para ver datos en la gráfica, necesitas:')
    print('  1. Crear al menos un piso y espacio')
    print('  2. Configurar una tarifa activa')
    print('  3. Registrar entrada de un vehículo')
    print('  4. Registrar salida del vehículo')
    print('  5. Esto creará automáticamente un Pago')
