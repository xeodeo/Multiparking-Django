from datetime import date, time, timedelta

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.utils import timezone

from cupones.models import Cupon, CuponAplicado
from pagos.models import Pago
from parqueadero.models import Espacio, InventarioParqueo, Piso, TipoEspacio
from reservas.models import Reserva
from tarifas.models import Tarifa
from usuarios.models import Usuario
from vehiculos.models import Vehiculo


class Command(BaseCommand):
    help = 'Llena las tablas con datos de prueba coherentes'

    def handle(self, *args, **options):
        self.stdout.write('Limpiando datos anteriores...')
        CuponAplicado.objects.all().delete()
        Cupon.objects.all().delete()
        Pago.objects.all().delete()
        Reserva.objects.all().delete()
        InventarioParqueo.objects.all().delete()
        Tarifa.objects.all().delete()
        Espacio.objects.all().delete()
        TipoEspacio.objects.all().delete()
        Piso.objects.all().delete()
        Vehiculo.objects.all().delete()
        Usuario.objects.all().delete()

        # =============================================
        # 1. USUARIOS
        # =============================================
        self.stdout.write('Creando usuarios...')

        clave = make_password('password123')

        admin1 = Usuario.objects.create(
            usuDocumento='1001234567',
            usuNombreCompleto='Carlos Andrés Martínez López',
            usuCorreo='carlos.martinez@multiparking.com',
            usuTelefono='3101234567',
            usuClaveHash=clave,
            rolTipoRol='ADMIN',
            usuEstado=True,
        )

        admin2 = Usuario.objects.create(
            usuDocumento='1009876543',
            usuNombreCompleto='Laura Patricia Gómez Ruiz',
            usuCorreo='laura.gomez@multiparking.com',
            usuTelefono='3209876543',
            usuClaveHash=clave,
            rolTipoRol='ADMIN',
            usuEstado=True,
        )

        vig1 = Usuario.objects.create(
            usuDocumento='1012345678',
            usuNombreCompleto='Pedro José Ramírez Castro',
            usuCorreo='pedro.ramirez@multiparking.com',
            usuTelefono='3112345678',
            usuClaveHash=clave,
            rolTipoRol='VIGILANTE',
            usuEstado=True,
        )

        vig2 = Usuario.objects.create(
            usuDocumento='1023456789',
            usuNombreCompleto='María Fernanda Torres Díaz',
            usuCorreo='maria.torres@multiparking.com',
            usuTelefono='3153456789',
            usuClaveHash=clave,
            rolTipoRol='VIGILANTE',
            usuEstado=True,
        )

        vig3 = Usuario.objects.create(
            usuDocumento='1034567890',
            usuNombreCompleto='Jorge Luis Hernández Peña',
            usuCorreo='jorge.hernandez@multiparking.com',
            usuTelefono='3184567890',
            usuClaveHash=clave,
            rolTipoRol='VIGILANTE',
            usuEstado=False,  # Inactivo
        )

        cli1 = Usuario.objects.create(
            usuDocumento='1045678901',
            usuNombreCompleto='Andrea Sofía Vargas Mendoza',
            usuCorreo='andrea.vargas@gmail.com',
            usuTelefono='3005678901',
            usuClaveHash=clave,
            rolTipoRol='CLIENTE',
            usuEstado=True,
        )

        cli2 = Usuario.objects.create(
            usuDocumento='1056789012',
            usuNombreCompleto='Santiago David Morales Ríos',
            usuCorreo='santiago.morales@gmail.com',
            usuTelefono='3016789012',
            usuClaveHash=clave,
            rolTipoRol='CLIENTE',
            usuEstado=True,
        )

        cli3 = Usuario.objects.create(
            usuDocumento='1067890123',
            usuNombreCompleto='Valentina Restrepo Aguilar',
            usuCorreo='valentina.restrepo@hotmail.com',
            usuTelefono='3127890123',
            usuClaveHash=clave,
            rolTipoRol='CLIENTE',
            usuEstado=True,
        )

        cli4 = Usuario.objects.create(
            usuDocumento='1078901234',
            usuNombreCompleto='Daniel Felipe Ospina Cardona',
            usuCorreo='daniel.ospina@yahoo.com',
            usuTelefono='3148901234',
            usuClaveHash=clave,
            rolTipoRol='CLIENTE',
            usuEstado=True,
        )

        cli5 = Usuario.objects.create(
            usuDocumento='1089012345',
            usuNombreCompleto='Camila Alejandra Parra Suárez',
            usuCorreo='camila.parra@gmail.com',
            usuTelefono='3169012345',
            usuClaveHash=clave,
            rolTipoRol='CLIENTE',
            usuEstado=True,
        )

        cli6 = Usuario.objects.create(
            usuDocumento='1090123456',
            usuNombreCompleto='Nicolás Esteban Rojas Luna',
            usuCorreo='nicolas.rojas@outlook.com',
            usuTelefono='3190123456',
            usuClaveHash=clave,
            rolTipoRol='CLIENTE',
            usuEstado=False,  # Inactivo
        )

        # =============================================
        # 2. VEHICULOS
        # =============================================
        self.stdout.write('Creando vehículos...')

        v1 = Vehiculo.objects.create(
            vehPlaca='ABC123', vehTipo='Carro', vehColor='Blanco',
            vehMarca='Chevrolet', vehModelo='Spark GT', fkIdUsuario=cli1,
        )
        v2 = Vehiculo.objects.create(
            vehPlaca='DEF456', vehTipo='Carro', vehColor='Negro',
            vehMarca='Renault', vehModelo='Logan', fkIdUsuario=cli1,
        )
        v3 = Vehiculo.objects.create(
            vehPlaca='GHI789', vehTipo='Carro', vehColor='Rojo',
            vehMarca='Mazda', vehModelo='CX-5', fkIdUsuario=cli2,
        )
        v4 = Vehiculo.objects.create(
            vehPlaca='JKL012', vehTipo='Moto', vehColor='Negro',
            vehMarca='Yamaha', vehModelo='FZ 250', fkIdUsuario=cli2,
        )
        v5 = Vehiculo.objects.create(
            vehPlaca='MNO345', vehTipo='Carro', vehColor='Gris',
            vehMarca='Toyota', vehModelo='Corolla', fkIdUsuario=cli3,
        )
        v6 = Vehiculo.objects.create(
            vehPlaca='PQR678', vehTipo='Moto', vehColor='Azul',
            vehMarca='Honda', vehModelo='CB 160', fkIdUsuario=cli3,
        )
        v7 = Vehiculo.objects.create(
            vehPlaca='STU901', vehTipo='Carro', vehColor='Blanco',
            vehMarca='Kia', vehModelo='Picanto', fkIdUsuario=cli4,
        )
        v8 = Vehiculo.objects.create(
            vehPlaca='VWX234', vehTipo='Carro', vehColor='Plata',
            vehMarca='Hyundai', vehModelo='Tucson', fkIdUsuario=cli4,
        )
        v9 = Vehiculo.objects.create(
            vehPlaca='YZA567', vehTipo='Moto', vehColor='Rojo',
            vehMarca='Suzuki', vehModelo='Gixxer 150', fkIdUsuario=cli5,
        )
        v10 = Vehiculo.objects.create(
            vehPlaca='BCD890', vehTipo='Carro', vehColor='Azul',
            vehMarca='Ford', vehModelo='Escape', fkIdUsuario=cli5,
        )
        v11 = Vehiculo.objects.create(
            vehPlaca='EFG123', vehTipo='Carro', vehColor='Verde',
            vehMarca='Volkswagen', vehModelo='Gol', fkIdUsuario=cli6,
        )
        v12 = Vehiculo.objects.create(
            vehPlaca='HIJ456', vehTipo='Moto', vehColor='Negro',
            vehMarca='AKT', vehModelo='NKD 125', fkIdUsuario=cli6,
        )

        # =============================================
        # 3. PISOS
        # =============================================
        self.stdout.write('Creando pisos...')

        piso1 = Piso.objects.create(pisNombre='Piso 1 - Nivel Calle', pisEstado=True)
        piso2 = Piso.objects.create(pisNombre='Piso 2 - Subterráneo 1', pisEstado=True)
        piso3 = Piso.objects.create(pisNombre='Piso 3 - Subterráneo 2', pisEstado=True)
        piso4 = Piso.objects.create(pisNombre='Piso 4 - Terraza', pisEstado=False)  # Inactivo

        # =============================================
        # 4. TIPOS DE ESPACIO
        # =============================================
        self.stdout.write('Creando tipos de espacio...')

        tipo_carro = TipoEspacio.objects.create(nombre='CARRO')
        tipo_moto = TipoEspacio.objects.create(nombre='MOTO')
        tipo_discap = TipoEspacio.objects.create(nombre='DISCAPACITADOS')
        tipo_visit = TipoEspacio.objects.create(nombre='VISITANTE')

        # =============================================
        # 5. ESPACIOS
        # =============================================
        self.stdout.write('Creando espacios...')

        espacios = []

        # Piso 1: 10 carros + 5 motos + 2 discapacitados + 3 visitantes = 20
        for i in range(1, 11):
            espacios.append(Espacio(
                espNumero=f'P1-C{i:02d}', fkIdPiso=piso1,
                fkIdTipoEspacio=tipo_carro, espEstado='DISPONIBLE',
            ))
        for i in range(1, 6):
            espacios.append(Espacio(
                espNumero=f'P1-M{i:02d}', fkIdPiso=piso1,
                fkIdTipoEspacio=tipo_moto, espEstado='DISPONIBLE',
            ))
        for i in range(1, 3):
            espacios.append(Espacio(
                espNumero=f'P1-D{i:02d}', fkIdPiso=piso1,
                fkIdTipoEspacio=tipo_discap, espEstado='DISPONIBLE',
            ))
        for i in range(1, 4):
            espacios.append(Espacio(
                espNumero=f'P1-V{i:02d}', fkIdPiso=piso1,
                fkIdTipoEspacio=tipo_visit, espEstado='DISPONIBLE',
            ))

        # Piso 2: 12 carros + 8 motos = 20
        for i in range(1, 13):
            espacios.append(Espacio(
                espNumero=f'P2-C{i:02d}', fkIdPiso=piso2,
                fkIdTipoEspacio=tipo_carro, espEstado='DISPONIBLE',
            ))
        for i in range(1, 9):
            espacios.append(Espacio(
                espNumero=f'P2-M{i:02d}', fkIdPiso=piso2,
                fkIdTipoEspacio=tipo_moto, espEstado='DISPONIBLE',
            ))

        # Piso 3: 10 carros + 5 motos = 15
        for i in range(1, 11):
            espacios.append(Espacio(
                espNumero=f'P3-C{i:02d}', fkIdPiso=piso3,
                fkIdTipoEspacio=tipo_carro, espEstado='DISPONIBLE',
            ))
        for i in range(1, 6):
            espacios.append(Espacio(
                espNumero=f'P3-M{i:02d}', fkIdPiso=piso3,
                fkIdTipoEspacio=tipo_moto, espEstado='DISPONIBLE',
            ))

        Espacio.objects.bulk_create(espacios)

        # Marcar algunos como OCUPADO e INACTIVO
        Espacio.objects.filter(espNumero='P1-C01').update(espEstado='OCUPADO')
        Espacio.objects.filter(espNumero='P1-C02').update(espEstado='OCUPADO')
        Espacio.objects.filter(espNumero='P1-M01').update(espEstado='OCUPADO')
        Espacio.objects.filter(espNumero='P2-C01').update(espEstado='OCUPADO')
        Espacio.objects.filter(espNumero='P3-C10').update(espEstado='INACTIVO')
        Espacio.objects.filter(espNumero='P3-M05').update(espEstado='INACTIVO')

        # Refrescar referencias para FK
        esp_p1c01 = Espacio.objects.get(espNumero='P1-C01')
        esp_p1c02 = Espacio.objects.get(espNumero='P1-C02')
        esp_p1c03 = Espacio.objects.get(espNumero='P1-C03')
        esp_p1c05 = Espacio.objects.get(espNumero='P1-C05')
        esp_p1m01 = Espacio.objects.get(espNumero='P1-M01')
        esp_p1m02 = Espacio.objects.get(espNumero='P1-M02')
        esp_p1v01 = Espacio.objects.get(espNumero='P1-V01')
        esp_p2c01 = Espacio.objects.get(espNumero='P2-C01')
        esp_p2c02 = Espacio.objects.get(espNumero='P2-C02')
        esp_p2m01 = Espacio.objects.get(espNumero='P2-M01')
        esp_p3c01 = Espacio.objects.get(espNumero='P3-C01')

        # =============================================
        # 6. TARIFAS
        # =============================================
        self.stdout.write('Creando tarifas...')

        hoy = date.today()

        Tarifa.objects.create(
            nombre='Tarifa Carro Estándar',
            fkIdTipoEspacio=tipo_carro,
            precioHora=5000, precioDia=35000, precioMensual=450000,
            activa=True, fechaInicio=hoy - timedelta(days=90),
        )
        Tarifa.objects.create(
            nombre='Tarifa Moto Estándar',
            fkIdTipoEspacio=tipo_moto,
            precioHora=2500, precioDia=18000, precioMensual=220000,
            activa=True, fechaInicio=hoy - timedelta(days=90),
        )
        Tarifa.objects.create(
            nombre='Tarifa Discapacitados',
            fkIdTipoEspacio=tipo_discap,
            precioHora=3000, precioDia=20000, precioMensual=280000,
            activa=True, fechaInicio=hoy - timedelta(days=90),
        )
        Tarifa.objects.create(
            nombre='Tarifa Visitante',
            fkIdTipoEspacio=tipo_visit,
            precioHora=6000, precioDia=40000, precioMensual=500000,
            activa=True, fechaInicio=hoy - timedelta(days=90),
        )
        # Tarifa antigua (inactiva)
        Tarifa.objects.create(
            nombre='Tarifa Carro 2024',
            fkIdTipoEspacio=tipo_carro,
            precioHora=4000, precioDia=28000, precioMensual=380000,
            activa=False,
            fechaInicio=date(2024, 1, 1),
            fechaFin=hoy - timedelta(days=91),
        )
        Tarifa.objects.create(
            nombre='Tarifa Moto 2024',
            fkIdTipoEspacio=tipo_moto,
            precioHora=2000, precioDia=14000, precioMensual=180000,
            activa=False,
            fechaInicio=date(2024, 1, 1),
            fechaFin=hoy - timedelta(days=91),
        )

        # =============================================
        # 7. INVENTARIO PARQUEO
        # =============================================
        self.stdout.write('Creando registros de parqueo...')

        ahora = timezone.now()

        # --- Parqueos FINALIZADOS (con salida) ---
        ip1 = InventarioParqueo.objects.create(
            fkIdVehiculo=v1, fkIdEspacio=esp_p1c03,
        )
        InventarioParqueo.objects.filter(pk=ip1.pk).update(
            parHoraEntrada=ahora - timedelta(days=5, hours=8),
            parHoraSalida=ahora - timedelta(days=5, hours=5),
        )

        ip2 = InventarioParqueo.objects.create(
            fkIdVehiculo=v3, fkIdEspacio=esp_p1c05,
        )
        InventarioParqueo.objects.filter(pk=ip2.pk).update(
            parHoraEntrada=ahora - timedelta(days=3, hours=10),
            parHoraSalida=ahora - timedelta(days=3, hours=6),
        )

        ip3 = InventarioParqueo.objects.create(
            fkIdVehiculo=v4, fkIdEspacio=esp_p2m01,
        )
        InventarioParqueo.objects.filter(pk=ip3.pk).update(
            parHoraEntrada=ahora - timedelta(days=2, hours=6),
            parHoraSalida=ahora - timedelta(days=2, hours=2),
        )

        ip4 = InventarioParqueo.objects.create(
            fkIdVehiculo=v5, fkIdEspacio=esp_p2c02,
        )
        InventarioParqueo.objects.filter(pk=ip4.pk).update(
            parHoraEntrada=ahora - timedelta(days=1, hours=9),
            parHoraSalida=ahora - timedelta(days=1, hours=4),
        )

        ip5 = InventarioParqueo.objects.create(
            fkIdVehiculo=v7, fkIdEspacio=esp_p3c01,
        )
        InventarioParqueo.objects.filter(pk=ip5.pk).update(
            parHoraEntrada=ahora - timedelta(days=1, hours=5),
            parHoraSalida=ahora - timedelta(days=1, hours=2),
        )

        ip6 = InventarioParqueo.objects.create(
            fkIdVehiculo=v10, fkIdEspacio=esp_p1v01,
        )
        InventarioParqueo.objects.filter(pk=ip6.pk).update(
            parHoraEntrada=ahora - timedelta(hours=12),
            parHoraSalida=ahora - timedelta(hours=9),
        )

        # --- Parqueos ACTIVOS (sin salida) ---
        ip7 = InventarioParqueo.objects.create(
            fkIdVehiculo=v1, fkIdEspacio=esp_p1c01,
        )
        InventarioParqueo.objects.filter(pk=ip7.pk).update(
            parHoraEntrada=ahora - timedelta(hours=3),
        )

        ip8 = InventarioParqueo.objects.create(
            fkIdVehiculo=v5, fkIdEspacio=esp_p1c02,
        )
        InventarioParqueo.objects.filter(pk=ip8.pk).update(
            parHoraEntrada=ahora - timedelta(hours=2),
        )

        ip9 = InventarioParqueo.objects.create(
            fkIdVehiculo=v6, fkIdEspacio=esp_p1m01,
        )
        InventarioParqueo.objects.filter(pk=ip9.pk).update(
            parHoraEntrada=ahora - timedelta(hours=1),
        )

        ip10 = InventarioParqueo.objects.create(
            fkIdVehiculo=v8, fkIdEspacio=esp_p2c01,
        )
        InventarioParqueo.objects.filter(pk=ip10.pk).update(
            parHoraEntrada=ahora - timedelta(minutes=45),
        )

        # Refrescar para tener datos actualizados
        ip1.refresh_from_db()
        ip2.refresh_from_db()
        ip3.refresh_from_db()
        ip4.refresh_from_db()
        ip5.refresh_from_db()
        ip6.refresh_from_db()

        # =============================================
        # 8. PAGOS (solo de parqueos finalizados)
        # =============================================
        self.stdout.write('Creando pagos...')

        pago1 = Pago.objects.create(
            pagMonto=15000, pagMetodo='EFECTIVO',
            pagEstado='PAGADO', fkIdParqueo=ip1,
        )
        pago2 = Pago.objects.create(
            pagMonto=20000, pagMetodo='TARJETA',
            pagEstado='PAGADO', fkIdParqueo=ip2,
        )
        pago3 = Pago.objects.create(
            pagMonto=10000, pagMetodo='EFECTIVO',
            pagEstado='PAGADO', fkIdParqueo=ip3,
        )
        pago4 = Pago.objects.create(
            pagMonto=25000, pagMetodo='TRANSFERENCIA',
            pagEstado='PAGADO', fkIdParqueo=ip4,
        )
        pago5 = Pago.objects.create(
            pagMonto=15000, pagMetodo='TARJETA',
            pagEstado='PAGADO', fkIdParqueo=ip5,
        )
        pago6 = Pago.objects.create(
            pagMonto=18000, pagMetodo='EFECTIVO',
            pagEstado='PAGADO', fkIdParqueo=ip6,
        )
        # Pago anulado
        Pago.objects.create(
            pagMonto=5000, pagMetodo='EFECTIVO',
            pagEstado='ANULADO', fkIdParqueo=ip1,
        )

        # =============================================
        # 9. CUPONES
        # =============================================
        self.stdout.write('Creando cupones...')

        cup1 = Cupon.objects.create(
            cupNombre='BIENVENIDO20',
            cupTipo='PORCENTAJE', cupValor=20,
            cupDescripcion='20% de descuento para nuevos clientes',
            cupFechaInicio=hoy - timedelta(days=30),
            cupFechaFin=hoy + timedelta(days=60),
            cupActivo=True,
        )
        cup2 = Cupon.objects.create(
            cupNombre='DESCUENTO5000',
            cupTipo='VALOR_FIJO', cupValor=5000,
            cupDescripcion='$5.000 de descuento en cualquier servicio',
            cupFechaInicio=hoy - timedelta(days=15),
            cupFechaFin=hoy + timedelta(days=45),
            cupActivo=True,
        )
        cup3 = Cupon.objects.create(
            cupNombre='FIDELIDAD15',
            cupTipo='PORCENTAJE', cupValor=15,
            cupDescripcion='15% para clientes frecuentes',
            cupFechaInicio=hoy - timedelta(days=60),
            cupFechaFin=hoy + timedelta(days=30),
            cupActivo=True,
        )
        Cupon.objects.create(
            cupNombre='NAVIDAD2024',
            cupTipo='PORCENTAJE', cupValor=30,
            cupDescripcion='Promoción navideña 2024',
            cupFechaInicio=date(2024, 12, 1),
            cupFechaFin=date(2024, 12, 31),
            cupActivo=False,  # Expirado
        )
        Cupon.objects.create(
            cupNombre='DESCUENTO10000',
            cupTipo='VALOR_FIJO', cupValor=10000,
            cupDescripcion='$10.000 de descuento - Aniversario',
            cupFechaInicio=hoy + timedelta(days=10),
            cupFechaFin=hoy + timedelta(days=40),
            cupActivo=True,  # Activo pero aún no vigente
        )

        # =============================================
        # 10. CUPONES APLICADOS
        # =============================================
        self.stdout.write('Creando cupones aplicados...')

        CuponAplicado.objects.create(
            fkIdPago=pago2, fkIdCupon=cup1, montoDescontado=4000,
        )
        CuponAplicado.objects.create(
            fkIdPago=pago4, fkIdCupon=cup2, montoDescontado=5000,
        )
        CuponAplicado.objects.create(
            fkIdPago=pago6, fkIdCupon=cup3, montoDescontado=2700,
        )

        # =============================================
        # 11. RESERVAS
        # =============================================
        self.stdout.write('Creando reservas...')

        manana = hoy + timedelta(days=1)
        pasado = hoy + timedelta(days=2)

        esp_p1c04 = Espacio.objects.get(espNumero='P1-C04')
        esp_p1c06 = Espacio.objects.get(espNumero='P1-C06')
        esp_p2c03 = Espacio.objects.get(espNumero='P2-C03')
        esp_p2m02 = Espacio.objects.get(espNumero='P2-M02')
        esp_p1m03 = Espacio.objects.get(espNumero='P1-M03')

        Reserva.objects.create(
            resFechaReserva=manana,
            resHoraInicio=time(8, 0), resHoraFin=time(12, 0),
            resEstado='CONFIRMADA',
            fkIdEspacio=esp_p1c04, fkIdVehiculo=v3,
        )
        Reserva.objects.create(
            resFechaReserva=manana,
            resHoraInicio=time(9, 0), resHoraFin=time(17, 0),
            resEstado='PENDIENTE',
            fkIdEspacio=esp_p2c03, fkIdVehiculo=v7,
        )
        Reserva.objects.create(
            resFechaReserva=manana,
            resHoraInicio=time(14, 0), resHoraFin=time(18, 0),
            resEstado='CONFIRMADA',
            fkIdEspacio=esp_p2m02, fkIdVehiculo=v9,
        )
        Reserva.objects.create(
            resFechaReserva=pasado,
            resHoraInicio=time(7, 0), resHoraFin=time(19, 0),
            resEstado='PENDIENTE',
            fkIdEspacio=esp_p1c06, fkIdVehiculo=v10,
        )
        # Reserva cancelada
        Reserva.objects.create(
            resFechaReserva=hoy,
            resHoraInicio=time(10, 0), resHoraFin=time(14, 0),
            resEstado='CANCELADA',
            fkIdEspacio=esp_p1m03, fkIdVehiculo=v4,
        )
        # Reserva completada (de ayer)
        Reserva.objects.create(
            resFechaReserva=hoy - timedelta(days=1),
            resHoraInicio=time(8, 0), resHoraFin=time(13, 0),
            resEstado='COMPLETADA',
            fkIdEspacio=esp_p3c01, fkIdVehiculo=v7,
        )

        # =============================================
        # RESUMEN
        # =============================================
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=== Datos de prueba creados ==='))
        self.stdout.write(f'  Usuarios:           {Usuario.objects.count()}')
        self.stdout.write(f'  Vehículos:          {Vehiculo.objects.count()}')
        self.stdout.write(f'  Pisos:              {Piso.objects.count()}')
        self.stdout.write(f'  Tipos de Espacio:   {TipoEspacio.objects.count()}')
        self.stdout.write(f'  Espacios:           {Espacio.objects.count()}')
        self.stdout.write(f'  Tarifas:            {Tarifa.objects.count()}')
        self.stdout.write(f'  Parqueos:           {InventarioParqueo.objects.count()}')
        self.stdout.write(f'  Pagos:              {Pago.objects.count()}')
        self.stdout.write(f'  Cupones:            {Cupon.objects.count()}')
        self.stdout.write(f'  Cupones Aplicados:  {CuponAplicado.objects.count()}')
        self.stdout.write(f'  Reservas:           {Reserva.objects.count()}')
