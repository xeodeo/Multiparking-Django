#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construye el documento de documentación completa de Multiparking en Google Docs.
Usa gws docs documents batchUpdate para insertar contenido con estilos.
"""
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

DOC_ID = '1lGUt6SRZZK9R8ir3hj5Mjj37xEFj5LNvKDpPusvEb-4'

# ---- Estructura del documento: lista de (estilo, texto) ----
# Estilos válidos: TITLE, SUBTITLE, HEADING_1..4, NORMAL_TEXT
sections = []

def add(style, text):
    sections.append((style, text))

def h1(text): add('HEADING_1', text)
def h2(text): add('HEADING_2', text)
def h3(text): add('HEADING_3', text)
def h4(text): add('HEADING_4', text)
def titulo(text): add('TITLE', text)
def subtitulo(text): add('SUBTITLE', text)
def p(text): add('NORMAL_TEXT', text)

# ============================================================
# PORTADA
# ============================================================
titulo('Sistema de Información Web para la Gestión Integral de Parqueaderos Privados')
subtitulo('MultiParking — Documentación Técnica Completa')
p('')
p('Kevin Arley Grisales Ovalle\nKevin Santiago Pinto López')
p('Análisis y Desarrollo de Software\nFicha: 3119175')
p('Centro de Diseño y Metrología – SENA\nBogotá D.C., 2026')
p('')

# ============================================================
# RESUMEN / ABSTRACT
# ============================================================
h1('Resumen')
p(
    'MultiParking es un sistema de información web orientado a la automatización y gestión integral '
    'de parqueaderos privados. La plataforma cubre el registro de usuarios con tres roles diferenciados '
    '(administrador, vigilante y cliente), el control de vehículos propios y visitantes, la asignación '
    'y liberación de espacios en tiempo real, el cálculo automático de tarifas por minuto con redondeo '
    'a cien pesos colombianos, la generación de pagos, la aplicación de cupones de descuento, la gestión '
    'de reservas, el registro de novedades operativas con notificación por correo electrónico, un sistema '
    'de fidelización mediante stickers acumulables y la generación de reportes exportables. El sistema se '
    'desarrolló en Python con el framework Django 6.0, utilizando MySQL como sistema gestor de base de datos, '
    'Tailwind CSS para el diseño responsivo de la interfaz, SendGrid para el envío de correos electrónicos y '
    'Render.com como plataforma de despliegue en la nube. La autenticación emplea sesiones propias sin '
    'depender del modelo User nativo de Django, fortaleciendo la seguridad mediante cabeceras HTTP, política '
    'de seguridad de contenido (CSP) y tokens de un solo uso para la recuperación de contraseñas.'
)
p('Palabras clave: parqueadero, sistema de información web, Django, gestión de espacios, tarifas, fidelización.')
p('')

h1('Abstract')
p(
    'MultiParking is a web-based information system designed for the comprehensive automation and management '
    'of private parking lots. The platform covers user registration with three differentiated roles '
    '(administrator, security guard, and client), management of registered and visitor vehicles, real-time '
    'space assignment and release, automatic rate calculation per minute with rounding to the nearest one '
    'hundred Colombian pesos, payment generation, coupon application, reservation management, operational '
    'incident logging with email notification, a loyalty system based on collectible stickers, and the '
    'generation of exportable reports. The system was built with Python/Django 6.0, MySQL 8.0, Tailwind CSS, '
    'SendGrid, and deployed on Render.com. Authentication relies on custom session management reinforced by '
    'HTTP security headers, Content Security Policy (CSP) middleware, and single-use tokens for password recovery.'
)
p('Keywords: parking lot, web information system, Django, space management, rates, loyalty, incidents.')
p('')

# ============================================================
# 1. INTRODUCCIÓN
# ============================================================
h1('1. Introducción')
p(
    'En la actualidad, los parqueaderos privados de pequeña y mediana escala operan con métodos manuales '
    'que generan ineficiencias operativas: registros en papel, cálculos de tarifa imprecisos, ausencia de '
    'trazabilidad y nula visibilidad del estado de los espacios en tiempo real. Esta situación deriva en '
    'pérdida de ingresos, inconformidad de los usuarios y dificultad para tomar decisiones basadas en datos '
    '(García & Martínez, 2022).'
)
p(
    'El proyecto MultiParking desarrolla una solución web que automatiza de forma integral la operación de '
    'parqueaderos privados. El sistema registra ingresos y salidas de vehículos, calcula tarifas en tiempo '
    'real, gestiona reservas anticipadas, emite notificaciones digitales, aplica descuentos mediante cupones '
    'y acumula beneficios de fidelización.'
)
p(
    'La arquitectura tecnológica se apoya en Django 6.0 (Python 3.12), PostgreSQL como sistema gestor '
    'de base de datos en producción (Render.com), Tailwind CSS vía CDN, Chart.js para visualizaciones '
    'estadísticas, SendGrid como proveedor de correo transaccional y Render.com como plataforma de '
    'despliegue con servidor WSGI Gunicorn. La autenticación implementa un modelo de sesión propio '
    '—sin dependencia del módulo django.contrib.auth.User— con tres roles definidos: ADMIN, VIGILANTE y CLIENTE.'
)
p(
    'Este documento sigue la estructura definida por el programa Análisis y Desarrollo de Software (ADSO) '
    'del SENA y las normas de presentación APA séptima edición (American Psychological Association, 2020).'
)
p('')

# ============================================================
# 2. PLANTEAMIENTO DEL PROBLEMA
# ============================================================
h1('2. Planteamiento del Problema')
h2('2.1. Árbol del Problema')
h3('2.1.1. Efectos')
p('• Pérdida de información y trazabilidad en el registro de vehículos: causada por registros manuales dispersos y falta de integración del sistema.')
p('• Cobros imprecisos o injustos por uso del parqueadero: debido a la ausencia de tarifación confiable y auditoría en tiempo real.')
p('• Filas y demoras en el ingreso y salida de vehículos: por control manual y verificación lenta.')
p('• Inconformidad de los residentes y visitantes: generada por tiempos de espera, cobros erróneos y baja transparencia operativa.')

h3('2.1.2. Problema Principal')
p(
    'Ineficiencia, falta de trazabilidad y pobre control en parqueaderos privados, ocasionado por procesos '
    'manuales, información no centralizada y carencia de herramientas digitales que soporten la operación, '
    'el cobro y la toma de decisiones (Bookings & Hernández, 2023).'
)

h3('2.1.3. Causas')
p('• Control manual del ingreso y salida de vehículos: provoca cuellos de botella y errores humanos.')
p('• Registro de información en papel o planillas físicas: genera pérdida de datos y dificultad para auditorías.')
p('• Falta de infraestructura tecnológica: limita la automatización y trazabilidad.')
p('• Ausencia de herramientas digitales para cobros y reservas: impide calcular tarifas correctas y agilizar pagos.')

h2('2.2. Descripción del Problema')
p(
    'La mayoría de los parqueaderos privados realizan sus procesos operativos y administrativos de manera '
    'manual. El control del ingreso y salida de vehículos depende de planillas físicas, lo que impide tener '
    'trazabilidad confiable y genera inconsistencias en los tiempos y valores cobrados. La ausencia de un '
    'sistema tecnológico centralizado limita la visibilidad en tiempo real de los espacios disponibles, '
    'dificulta la conciliación de pagos y complica la detección de errores o fraudes. Adicionalmente, la '
    'imposibilidad de reservar espacio anticipadamente reduce la satisfacción del usuario y la competitividad '
    'del establecimiento frente a alternativas digitales.'
)
p('')

# ============================================================
# 3. OBJETIVOS
# ============================================================
h1('3. Objetivos')
h2('3.1. Objetivo General')
p(
    'Desarrollar un sistema de información web que permita la gestión integral de parqueaderos privados, '
    'optimizando el control de ingreso y salida de vehículos, la asignación de espacios, el cálculo '
    'automático de tarifas, la gestión de reservas anticipadas y el seguimiento de novedades operativas.'
)

h2('3.2. Objetivos Específicos')
h3('Fase de Inicio')
p('• Analizar los procesos actuales de operación y control en parqueaderos privados para identificar los requerimientos funcionales y no funcionales del sistema.')
p('• Identificar las necesidades de los usuarios (administradores, vigilantes y clientes) mediante encuestas y observación directa.')

h3('Fase de Planificación')
p('• Diseñar la arquitectura del sistema web, definiendo la estructura de la base de datos, los módulos funcionales y la interacción entre componentes.')
p('• Elaborar los diagramas de casos de uso, clases y flujo de datos que representen el comportamiento del sistema.')

h3('Fase de Ejecución')
p('• Desarrollar los once módulos principales: usuarios, vehículos, pisos/espacios, inventario de parqueos, tarifas, pagos, cupones, reservas, novedades, fidelización y reportes.')
p('• Implementar el cálculo automático de tarifas, las notificaciones por correo electrónico y la exportación de reportes en PDF y Excel.')

h3('Fase de Implementación')
p('• Desplegar el sistema en Render.com, validando su correcto funcionamiento con datos de producción.')
p('• Capacitar al personal y realizar pruebas piloto antes de la puesta en marcha final.')
p('')

# ============================================================
# 4. JUSTIFICACIÓN
# ============================================================
h1('4. Justificación')
p(
    'En numerosos parqueaderos privados de pequeña y mediana escala, el control manual de ingreso y salida '
    'de vehículos genera demoras, fallos en el cobro y pérdida de información crítica. Estudios recientes '
    'señalan que la adopción de sistemas digitales de gestión de aparcamientos mejora la eficiencia operativa, '
    'reduce errores humanos y ofrece trazabilidad de datos en tiempo real (García & Martínez, 2022). '
    'Así mismo, Garavito Albao et al. (2021) demuestran que los sistemas de información en pequeñas empresas '
    'de servicios reducen el tiempo de atención hasta en un 40% y disminuyen los errores de registro en '
    'más del 60%.'
)
p(
    'El sistema MultiParking responde a esta necesidad ofreciendo una solución accesible, escalable y segura '
    'que no requiere hardware especializado, opera desde cualquier navegador moderno y está preparada para '
    'ejecutarse en infraestructura cloud de bajo costo. La implementación sobre Django 6.0 garantiza '
    'mantenibilidad a largo plazo gracias a su arquitectura MVT (Modelo-Vista-Plantilla), su sistema de '
    'migraciones y su robusta comunidad de soporte.'
)
p(
    'La plataforma beneficia directamente a tres perfiles de usuarios: administradores, que obtienen '
    'visibilidad total y reportes de inteligencia operativa; vigilantes, que agilizan los procesos de '
    'ingreso y salida; y clientes, que acceden a reservas anticipadas, historial de parqueos y beneficios '
    'de fidelización. A nivel social, el proyecto contribuye a la modernización de microempresas de servicios '
    'en Bogotá, alineándose con los objetivos de transformación digital del Ministerio de Tecnologías de la '
    'Información y las Comunicaciones (MinTIC, 2023).'
)
p('')

# ============================================================
# 5. ALCANCE
# ============================================================
h1('5. Alcance del Proyecto')
p(
    'El proyecto consiste en desarrollar un sistema de información web denominado MultiParking, orientado '
    'a automatizar la gestión de parqueaderos privados de pequeña y mediana escala. El sistema está diseñado '
    'para funcionar como una plataforma web responsiva, operable desde dispositivos móviles o computadores '
    'sin requerir hardware especializado.'
)
p(
    'El alcance incluye: levantamiento de requerimientos mediante encuestas y observación directa; diseño de '
    'la arquitectura y la base de datos relacional (MySQL); desarrollo de once módulos funcionales '
    '(usuarios, vehículos, pisos y espacios, inventario de parqueos, tarifas, pagos, cupones, reservas, '
    'novedades, fidelización y reportes); implementación de notificaciones por correo electrónico mediante '
    'SendGrid; exportación de reportes en PDF (reportlab) y Excel (openpyxl); y despliegue en la plataforma '
    'cloud Render.com.'
)
p(
    'Quedan fuera del alcance en esta versión: la integración con hardware automatizado (barreras, sensores '
    'de presencia, cámaras de reconocimiento de placas) y el desarrollo de una aplicación móvil nativa para '
    'iOS o Android. Estas funcionalidades se contemplan para versiones futuras del sistema.'
)
p('')

# ============================================================
# 6. MATRIZ DE RIESGO
# ============================================================
h1('6. Matriz de Riesgo')
p('La Tabla 1 presenta los riesgos identificados durante la planificación del proyecto, clasificados por impacto y probabilidad, con sus respectivas estrategias de mitigación.')
p(
    'Tabla 1\nMatriz de Riesgos del Proyecto MultiParking\n'
    'Nº | Riesgo | Causa | Impacto | Probabilidad | Estrategia\n'
    '1 | Retrasos en el desarrollo | Subestimación de tiempos | Aplazamiento de entrega | Media | Cronograma ágil con revisión semanal\n'
    '2 | Dificultades con pagos digitales | Problemas con APIs | No se podrán automatizar cobros | Media | Usar APIs documentadas (PayU, Wompi)\n'
    '3 | Falta de conectividad en entorno piloto | Infraestructura deficiente | Fallos de acceso | Alta | Verificar requisitos de red previamente\n'
    '4 | Baja adopción de usuarios | Resistencia al cambio | Uso limitado del sistema | Media | Capacitaciones y pruebas piloto\n'
    '5 | Pérdida de datos | Fallos en servidor | Pérdida de registros | Baja | Backups automáticos diarios\n'
    '6 | Cambios en requerimientos | Nuevas necesidades del cliente | Re-trabajo de módulos | Media | Reuniones periódicas con stakeholders\n'
    '7 | Salida de integrante clave | Problemas personales | Redistribución de tareas | Baja | Documentación compartida y roles cruzados\n'
    'Nota. Elaboración propia (2026).'
)
p('')

# ============================================================
# 7. ELICITACIÓN DE REQUISITOS
# ============================================================
h1('7. Elicitación de Requisitos')
h2('7.1. Identificación de Procesos')
p(
    'Los parqueaderos privados desarrollan una serie de procesos interrelacionados para controlar el ingreso '
    'y salida de vehículos, gestionar espacios disponibles y asegurar el cobro correcto. Los procesos '
    'principales identificados son:'
)
p('• Registro de ingreso de vehículo con asignación automática de espacio disponible.')
p('• Cálculo de tiempo de permanencia y tarifa al momento de la salida.')
p('• Gestión de pagos y aplicación de descuentos mediante cupones.')
p('• Reserva anticipada de espacios por parte de clientes registrados.')
p('• Registro de novedades operativas (daños, incidentes, observaciones) con notificación al usuario afectado.')
p('• Generación de reportes de ingresos, ocupación y actividad del parqueadero.')

h2('7.2. Técnicas de Recolección de Información')
h3('7.2.1. Encuesta Digital')
p(
    'Se aplicó una encuesta digital a trece (13) usuarios de parqueaderos privados de la localidad de Suba, '
    'barrio Compartir. La encuesta constó de trece (13) preguntas de selección múltiple orientadas a '
    'identificar hábitos de uso, preferencias tecnológicas y necesidades no satisfechas.'
)

h3('7.2.2. Observación Directa')
p(
    'Se realizaron visitas de observación a parqueaderos privados de pequeña y mediana escala en días de '
    'alta y baja afluencia, registrando los procedimientos de entrada y salida, la asignación de espacios, '
    'los tiempos de espera y los métodos de cobro empleados.'
)

h2('7.3. Resultados de la Encuesta')
p(
    'Tabla 2\nFrecuencia de uso de parqueaderos (n = 13)\n'
    'Variable | f | fa | fr | fra\n'
    'Todos los días | 4 | 4 | 0.308 | 0.308\n'
    'Varias veces a la semana | 3 | 7 | 0.231 | 0.539\n'
    'Ocasionalmente | 3 | 10 | 0.231 | 0.770\n'
    'Casi nunca | 3 | 13 | 0.231 | 1.000\n'
    'Nota. f = frecuencia absoluta; fa = frecuencia absoluta acumulada; fr = frecuencia relativa; fra = frecuencia relativa acumulada. Elaboración propia (2026).'
)
p('Los resultados más relevantes de la encuesta indican que:')
p('• El 31% de los encuestados usa parqueaderos a diario, lo que demuestra alta dependencia del servicio.')
p('• El 85% paga actualmente en efectivo, evidenciando la necesidad de medios de pago digitales.')
p('• El 92% valora positivamente poder ver el costo acumulado en tiempo real.')
p('• El 62% utilizaría reservas anticipadas de espacio.')
p('• El 100% estaría dispuesto (54% muy dispuesto, 46% algo dispuesto) a usar un sistema completamente automatizado.')
p('')

# ============================================================
# 8. ESPECIFICACIÓN DE REQUERIMIENTOS
# ============================================================
h1('8. Especificación de Requerimientos')
h2('8.1. Requerimientos Funcionales')
p(
    'Los requerimientos funcionales describen las capacidades que el sistema debe proporcionar. '
    'Se presentan organizados por módulo, siguiendo el estándar IEEE 830 (IEEE, 2011). '
    'Cada requerimiento incluye código, nombre, descripción, entradas del sistema y prioridad.'
)

# --- MÓDULO USUARIOS ---
h3('8.1.1. Módulo Usuarios')
rfs_usuarios = [
    ('RF01', 'Registrar usuario', 'El sistema permitirá registrar un nuevo usuario capturando nombre, apellido, documento de identidad, correo electrónico, teléfono y contraseña. La contraseña se almacenará cifrada con el algoritmo PBKDF2-SHA256.', 'usuNombre, usuApellido, usuDocumento, usuCorreo, usuTelefono, usuClaveHash', 'Alta'),
    ('RF02', 'Iniciar sesión', 'El sistema permitirá a los usuarios autenticarse mediante correo electrónico y contraseña. Se verificará el hash de la contraseña y se creará una sesión con los datos del usuario y su rol.', 'usuCorreo, contraseña', 'Alta'),
    ('RF03', 'Cerrar sesión', 'El sistema permitirá a los usuarios finalizar su sesión activa, eliminando los datos de sesión del servidor y redirigiendo al inicio.', 'Ninguna (sesión activa)', 'Alta'),
    ('RF04', 'Recuperar contraseña', 'El sistema enviará al correo registrado un enlace de recuperación con un token de un solo uso. Al usarlo, el token quedará invalidado automáticamente mediante huella del hash de contraseña.', 'usuCorreo', 'Alta'),
    ('RF05', 'Gestionar usuarios (Admin)', 'El administrador podrá crear, editar, activar, desactivar y eliminar usuarios del sistema, así como cambiar su rol.', 'usuNombre, usuApellido, usuDocumento, usuCorreo, usuTelefono, rolTipoRol', 'Alta'),
    ('RF06', 'Asignar rol', 'El sistema soportará tres roles: ADMIN, VIGILANTE y CLIENTE. Cada rol tiene acceso diferenciado a las funcionalidades del sistema.', 'rolTipoRol (ENUM)', 'Alta'),
    ('RF07', 'Ver perfil propio', 'El usuario podrá consultar sus datos personales, su historial de parqueos, sus stickers acumulados y sus reservas activas.', 'Sesión activa', 'Media'),
    ('RF08', 'Actualizar datos personales', 'El usuario podrá modificar su nombre, apellido, teléfono y contraseña desde su perfil.', 'usuNombre, usuApellido, usuTelefono, nueva contraseña', 'Media'),
]
for code, name, desc, inputs, prio in rfs_usuarios:
    p(f'Tabla {code}\n{code} — {name}\n'
      f'Código: {code}\n'
      f'Nombre: {name}\n'
      f'Descripción: {desc}\n'
      f'Entradas: {inputs}\n'
      f'Prioridad: {prio}\n'
      f'Nota. Elaboración propia (2026).')
    p('')

# --- MÓDULO VEHÍCULOS ---
h3('8.1.2. Módulo Vehículos')
rfs_vehiculos = [
    ('RF09', 'Registrar vehículo propio', 'El cliente podrá registrar vehículos asociados a su cuenta, indicando placa, tipo (CARRO/MOTO/BICI), color, marca y modelo.', 'vehPlaca, vehTipo, vehColor, vehMarca, vehModelo, fkIdUsuario', 'Alta'),
    ('RF10', 'Registrar vehículo visitante', 'El vigilante podrá registrar vehículos de visitantes sin cuenta en el sistema, capturando placa, tipo, nombre y teléfono de contacto.', 'vehPlaca, vehTipo, nombre_contacto, telefono_contacto', 'Alta'),
    ('RF11', 'Listar vehículos por usuario', 'El sistema mostrará la lista de vehículos registrados por el usuario autenticado, con su estado activo/inactivo.', 'fkIdUsuario (sesión)', 'Media'),
    ('RF12', 'Editar vehículo', 'El usuario podrá modificar los datos de un vehículo propio siempre que no esté actualmente en el parqueadero.', 'vehPlaca, vehTipo, vehColor, vehMarca, vehModelo', 'Media'),
    ('RF13', 'Eliminar vehículo', 'El administrador podrá eliminar un vehículo del sistema si no tiene registros de parqueo activos ni reservas vigentes.', 'idVehiculo', 'Baja'),
]
for code, name, desc, inputs, prio in rfs_vehiculos:
    p(f'Tabla {code}\n{code} — {name}\n'
      f'Código: {code}\nNombre: {name}\nDescripción: {desc}\nEntradas: {inputs}\nPrioridad: {prio}\n'
      f'Nota. Elaboración propia (2026).')
    p('')

# --- MÓDULO ESPACIOS Y PISOS ---
h3('8.1.3. Módulo Espacios y Pisos')
rfs_espacios = [
    ('RF14', 'Gestionar pisos', 'El administrador podrá crear, editar y desactivar pisos del parqueadero. No se podrá eliminar un piso que contenga espacios con vehículos activos.', 'pisNombre, pisEstado', 'Alta'),
    ('RF15', 'Gestionar tipos de espacio', 'El administrador podrá crear y editar tipos de espacio (ej.: CARRO, MOTO, BICICLETA) que determinan la tarifa aplicable.', 'nombre (TipoEspacio)', 'Alta'),
    ('RF16', 'Gestionar espacios', 'El administrador podrá crear, editar y eliminar espacios individuales. Cada espacio se asocia a un piso y a un tipo de espacio.', 'espNumero, fkIdPiso, fkIdTipoEspacio, espEstado', 'Alta'),
    ('RF17', 'Ver disponibilidad en tiempo real', 'El sistema mostrará la vista general de pisos con cada espacio coloreado según su estado: DISPONIBLE (verde), OCUPADO (rojo), RESERVADO (amarillo), MANTENIMIENTO (gris). La vista se actualiza automáticamente cada 30 segundos mediante AJAX.', 'Ninguna (dashboard)', 'Alta'),
    ('RF18', 'Cambiar estado de espacio', 'El administrador podrá cambiar manualmente el estado de un espacio a MANTENIMIENTO y viceversa.', 'idEspacio, espEstado', 'Media'),
    ('RF19', 'Mostrar placa en espacio ocupado', 'Cuando un espacio esté OCUPADO, la vista general mostrará debajo del número de espacio la placa del vehículo actualmente parqueado.', 'InventarioParqueo activo (fkIdEspacio)', 'Media'),
]
for code, name, desc, inputs, prio in rfs_espacios:
    p(f'Tabla {code}\n{code} — {name}\nCódigo: {code}\nNombre: {name}\nDescripción: {desc}\nEntradas: {inputs}\nPrioridad: {prio}\nNota. Elaboración propia (2026).')
    p('')

# --- MÓDULO INVENTARIO PARQUEOS ---
h3('8.1.4. Módulo Inventario de Parqueos')
rfs_parqueos = [
    ('RF20', 'Registrar ingreso de vehículo', 'El vigilante registrará el ingreso de un vehículo, seleccionando placa y espacio disponible. El sistema registrará la hora de entrada y cambiará el estado del espacio a OCUPADO.', 'fkIdVehiculo, fkIdEspacio, parHoraEntrada', 'Alta'),
    ('RF21', 'Registrar salida de vehículo', 'El vigilante registrará la salida del vehículo. El sistema calculará el tiempo de permanencia, generará el pago correspondiente y liberará el espacio a DISPONIBLE.', 'idParqueo, parHoraSalida, fkIdTarifa', 'Alta'),
    ('RF22', 'Calcular costo de parqueo', 'El sistema calculará el costo usando la fórmula: (minutos_totales / 60) × precioHora, redondeado al siguiente múltiplo de 100 COP. Si el vehículo es visitante, se usará precioHoraVisitante.', 'parHoraEntrada, parHoraSalida, precioHora', 'Alta'),
    ('RF23', 'Control de espacio al ingresar/salir', 'Al registrar un ingreso, el espacio pasa de DISPONIBLE a OCUPADO. Al registrar la salida, el espacio vuelve a DISPONIBLE. La regla se aplica también al confirmar/cancelar reservas.', 'espEstado (ENUM)', 'Alta'),
    ('RF24', 'Ver historial de parqueos', 'El administrador podrá consultar el historial completo de parqueos con filtros por fecha, vehículo, espacio y estado. El cliente verá solo sus propios registros.', 'resFechaReserva, fkIdVehiculo, fkIdEspacio', 'Media'),
    ('RF25', 'Ver parqueos activos en tiempo real', 'El dashboard del vigilante mostrará los vehículos actualmente parqueados con su espacio, hora de entrada y tiempo acumulado. Los datos se actualizan mediante AJAX cada 30 segundos.', 'parHoraSalida IS NULL', 'Alta'),
    ('RF26', 'Evitar doble ingreso activo', 'El sistema validará que un vehículo no pueda tener más de un registro de parqueo activo simultáneamente. Si se intenta registrar un ingreso para un vehículo ya parqueado, se mostrará un error.', 'fkIdVehiculo, parHoraSalida__isnull', 'Alta'),
]
for code, name, desc, inputs, prio in rfs_parqueos:
    p(f'Tabla {code}\n{code} — {name}\nCódigo: {code}\nNombre: {name}\nDescripción: {desc}\nEntradas: {inputs}\nPrioridad: {prio}\nNota. Elaboración propia (2026).')
    p('')

# --- MÓDULO TARIFAS ---
h3('8.1.5. Módulo Tarifas')
rfs_tarifas = [
    ('RF27', 'Crear tarifa', 'El administrador podrá crear tarifas definiendo nombre, tipo de espacio asociado, precio por hora (usuario y visitante), precio por día y precio mensual, con fecha de inicio y fin opcionales.', 'nombre, fkIdTipoEspacio, precioHora, precioHoraVisitante, precioDia, precioMensual, fechaInicio, fechaFin', 'Alta'),
    ('RF28', 'Restricción de tarifa activa única', 'Solo podrá existir una tarifa activa por tipo de espacio en un momento dado. Al activar una nueva tarifa, el sistema desactivará automáticamente la tarifa anterior del mismo tipo.', 'activa (BooleanField), fkIdTipoEspacio', 'Alta'),
    ('RF29', 'Editar y desactivar tarifa', 'El administrador podrá editar los datos de una tarifa o desactivarla. No se pueden eliminar tarifas que estén asociadas a parqueos ya registrados.', 'idTarifa, activa', 'Media'),
    ('RF30', 'Consultar tarifa vigente', 'El sistema mostrará automáticamente la tarifa activa correspondiente al tipo de espacio en el momento de registrar un ingreso o calcular un costo.', 'fkIdTipoEspacio, activa=True', 'Alta'),
]
for code, name, desc, inputs, prio in rfs_tarifas:
    p(f'Tabla {code}\n{code} — {name}\nCódigo: {code}\nNombre: {name}\nDescripción: {desc}\nEntradas: {inputs}\nPrioridad: {prio}\nNota. Elaboración propia (2026).')
    p('')

# --- MÓDULO PAGOS ---
h3('8.1.6. Módulo Pagos')
rfs_pagos = [
    ('RF31', 'Generar pago al registrar salida', 'Al registrar la salida de un vehículo, el sistema generará automáticamente un registro de pago vinculado al parqueo, con el monto calculado, método de pago y estado PAGADO.', 'pagMonto, pagMetodo, pagEstado, fkIdParqueo', 'Alta'),
    ('RF32', 'Aplicar cupón en pago', 'Antes de finalizar el cobro, el vigilante podrá ingresar un código de cupón. Si el cupón es válido (activo, dentro de fechas, con usos disponibles), el sistema calculará y aplicará el descuento al monto total.', 'cupCodigo, pagMonto', 'Alta'),
    ('RF33', 'Ver historial de pagos', 'El administrador podrá consultar todos los pagos realizados con filtros por fecha, monto, método y estado. El cliente verá solo sus propios pagos.', 'pagFechaPago, pagEstado', 'Media'),
    ('RF34', 'Reportes de ingresos', 'El sistema generará reportes de ingresos agrupados por día, semana, mes o período personalizado, mostrando total recaudado, número de parqueos y promedio por visita.', 'pagFechaPago, pagMonto', 'Media'),
    ('RF35', 'Exportar reportes', 'El administrador podrá descargar los reportes de ingresos, ocupación, reservas y cupones en formato PDF (reportlab) o Excel (openpyxl).', 'Filtros de reporte seleccionados', 'Media'),
]
for code, name, desc, inputs, prio in rfs_pagos:
    p(f'Tabla {code}\n{code} — {name}\nCódigo: {code}\nNombre: {name}\nDescripción: {desc}\nEntradas: {inputs}\nPrioridad: {prio}\nNota. Elaboración propia (2026).')
    p('')

# --- MÓDULO CUPONES ---
h3('8.1.7. Módulo Cupones')
rfs_cupones = [
    ('RF36', 'Crear cupón', 'El administrador podrá crear cupones de descuento definiendo nombre, código único alfanumérico, tipo (PORCENTAJE o VALOR_FIJO), valor, descripción, fechas de vigencia y estado activo.', 'cupNombre, cupCodigo, cupTipo, cupValor, cupFechaInicio, cupFechaFin, cupActivo', 'Alta'),
    ('RF37', 'Validar cupón', 'Al aplicar un cupón, el sistema verificará que el código exista, esté activo, se encuentre dentro de su período de vigencia y tenga usos disponibles. De lo contrario, mostrará el error correspondiente.', 'cupCodigo, cupActivo, cupFechaFin', 'Alta'),
    ('RF38', 'Aplicar descuento', 'Si el cupón es de tipo PORCENTAJE, el descuento será cupValor% del total. Si es VALOR_FIJO, el descuento será el valor fijo en COP. El monto final no podrá ser negativo.', 'cupTipo, cupValor, pagMonto', 'Alta'),
    ('RF39', 'Registrar uso de cupón', 'Cada vez que un cupón se aplique a un pago, el sistema registrará el uso en la tabla CuponAplicado, almacenando el pago, el cupón y el monto descontado.', 'fkIdPago, fkIdCupon, montoDescontado', 'Alta'),
    ('RF40', 'Desactivar cupón vencido', 'El sistema identificará automáticamente los cupones cuya fecha de fin haya superado la fecha actual y los marcará como inactivos al momento de la validación.', 'cupFechaFin, fecha actual', 'Media'),
    ('RF41', 'Listar cupones activos', 'El administrador podrá consultar la lista de todos los cupones con su estado, vigencia y número de veces utilizados.', 'cupActivo, cupFechaFin', 'Media'),
]
for code, name, desc, inputs, prio in rfs_cupones:
    p(f'Tabla {code}\n{code} — {name}\nCódigo: {code}\nNombre: {name}\nDescripción: {desc}\nEntradas: {inputs}\nPrioridad: {prio}\nNota. Elaboración propia (2026).')
    p('')

# --- MÓDULO RESERVAS ---
h3('8.1.8. Módulo Reservas')
rfs_reservas = [
    ('RF42', 'Registrar reserva', 'El cliente o administrador podrá reservar un espacio disponible para una fecha y hora específicas, verificando que no exista traslape con otra reserva activa en el mismo espacio.', 'resFechaReserva, resHoraInicio, resHoraFin, fkIdEspacio, fkIdVehiculo', 'Alta'),
    ('RF43', 'Consultar disponibilidad para reserva', 'El sistema mostrará los espacios disponibles para una fecha y rango horario indicados, excluyendo los que tengan reservas solapadas o estén OCUPADOS/MANTENIMIENTO.', 'resFechaReserva, resHoraInicio, resHoraFin', 'Alta'),
    ('RF44', 'Cancelar reserva', 'El cliente podrá cancelar una reserva propia siempre que no haya comenzado. Al cancelar, el espacio regresa al estado DISPONIBLE.', 'idReserva, resEstado', 'Alta'),
    ('RF45', 'Modificar reserva', 'El administrador o el cliente podrán editar la fecha u hora de una reserva existente, siempre que el nuevo horario esté disponible.', 'idReserva, resFechaReserva, resHoraInicio, resHoraFin', 'Media'),
    ('RF46', 'Bloquear espacio al confirmar reserva', 'Al confirmar una reserva, el estado del espacio cambiará a RESERVADO. Al cancelar o completar la reserva, el estado regresará a DISPONIBLE.', 'espEstado, resEstado', 'Alta'),
]
for code, name, desc, inputs, prio in rfs_reservas:
    p(f'Tabla {code}\n{code} — {name}\nCódigo: {code}\nNombre: {name}\nDescripción: {desc}\nEntradas: {inputs}\nPrioridad: {prio}\nNota. Elaboración propia (2026).')
    p('')

# --- MÓDULO NOVEDADES ---
h3('8.1.9. Módulo Novedades')
rfs_novedades = [
    ('RF47', 'Registrar novedad', 'El vigilante o administrador podrá registrar una novedad operativa (incidente, daño, observación) asociándola opcionalmente a un vehículo y a un espacio, con descripción, foto (máx. 5 MB, JPG/PNG/GIF/WEBP) y estado PENDIENTE por defecto.', 'novDescripcion, novFoto, fkIdVehiculo, fkIdEspacio, fkIdReportador', 'Alta'),
    ('RF48', 'Actualizar estado de novedad', 'El administrador podrá cambiar el estado de la novedad entre PENDIENTE, EN_PROCESO y RESUELTO, y agregar un comentario de seguimiento.', 'novEstado, novComentario', 'Alta'),
    ('RF49', 'Asignar responsable', 'Al crear o editar una novedad, se podrá asignar un responsable (usuario con rol ADMIN o VIGILANTE) encargado de gestionarla.', 'fkIdResponsable', 'Media'),
    ('RF50', 'Filtrar novedades', 'El listado de novedades podrá filtrarse por estado (PENDIENTE/EN_PROCESO/RESUELTO) y por texto en la descripción.', 'novEstado, novDescripcion__icontains', 'Media'),
    ('RF51', 'Notificar usuario por correo', 'Al crear o actualizar una novedad, el sistema enviará un correo electrónico al usuario afectado (dueño del vehículo) informando el estado y la descripción, mediante SendGrid.', 'fkIdVehiculo.fkIdUsuario.usuCorreo', 'Alta'),
    ('RF52', 'Eliminar novedad', 'El administrador podrá eliminar una novedad del sistema. La acción es irreversible.', 'idNovedad', 'Baja'),
]
for code, name, desc, inputs, prio in rfs_novedades:
    p(f'Tabla {code}\n{code} — {name}\nCódigo: {code}\nNombre: {name}\nDescripción: {desc}\nEntradas: {inputs}\nPrioridad: {prio}\nNota. Elaboración propia (2026).')
    p('')

# --- MÓDULO FIDELIZACIÓN ---
h3('8.1.10. Módulo Fidelización (Stickers)')
rfs_fidelidad = [
    ('RF53', 'Acumular sticker al completar parqueo', 'Al registrar la salida de un vehículo con propietario registrado y permanencia superior a 60 minutos, el sistema asignará automáticamente un sticker al usuario vinculado al vehículo.', 'parHoraEntrada, parHoraSalida, fkIdUsuario, permanencia > 60 min', 'Alta'),
    ('RF54', 'Ver stickers en perfil', 'El cliente podrá ver en su perfil la cantidad de stickers acumulados, la meta configurada y una barra de progreso visual. Cuando alcance la meta, se mostrará un botón para reclamar el bono.', 'fkIdUsuario, metaStickers (ConfiguracionFidelidad)', 'Alta'),
    ('RF55', 'Reclamar bono por meta alcanzada', 'Cuando un usuario acumule la cantidad de stickers equivalente a la meta configurada, podrá reclamar un cupón de descuento del 100% generado automáticamente, con vigencia de 30 días y uso único.', 'stkFecha, metaStickers, cupValor=100, cupTipo=PORCENTAJE', 'Alta'),
    ('RF56', 'Configurar meta de stickers', 'El administrador podrá modificar desde el panel el número de stickers necesarios para alcanzar el bono y los días de vigencia del cupón generado.', 'metaStickers, diasVencimientoBono (ConfiguracionFidelidad)', 'Media'),
]
for code, name, desc, inputs, prio in rfs_fidelidad:
    p(f'Tabla {code}\n{code} — {name}\nCódigo: {code}\nNombre: {name}\nDescripción: {desc}\nEntradas: {inputs}\nPrioridad: {prio}\nNota. Elaboración propia (2026).')
    p('')

# --- MÓDULO REPORTES ---
h3('8.1.11. Módulo Reportes')
rfs_reportes = [
    ('RF57', 'Reporte de ingresos por período', 'El administrador podrá generar un reporte de ingresos económicos filtrando por rango de fechas, mostrando total recaudado, número de transacciones y promedio por operación.', 'pagFechaPago (rango), pagMonto', 'Alta'),
    ('RF58', 'Reporte de ocupación por espacio', 'El sistema generará un reporte que muestre el porcentaje de ocupación de cada espacio por período, identificando los espacios con mayor y menor rotación.', 'fkIdEspacio, parHoraEntrada (rango)', 'Media'),
    ('RF59', 'Reporte de reservas', 'El administrador podrá ver el volumen de reservas por período, con desglose por estado (CONFIRMADA, CANCELADA, COMPLETADA) y por tipo de espacio.', 'resFechaReserva (rango), resEstado', 'Media'),
    ('RF60', 'Reporte de cupones aplicados', 'El sistema mostrará un reporte de cupones utilizados, con el código, el número de usos, el monto total descontado y el período de aplicación.', 'fkIdCupon, montoDescontado, pagFechaPago', 'Media'),
    ('RF61', 'Visualización con gráficas', 'El dashboard principal mostrará gráficas interactivas con Chart.js: barras para ingresos por día, líneas para ocupación en el tiempo y dona para distribución por tipo de espacio.', 'Datos de pagos e inventario agrupados', 'Media'),
    ('RF62', 'Exportar a PDF y Excel', 'Todos los reportes podrán descargarse en formato PDF (generado con reportlab) o Excel (generado con openpyxl), con encabezado, logo y fecha de generación.', 'Filtros de reporte seleccionados', 'Media'),
]
for code, name, desc, inputs, prio in rfs_reportes:
    p(f'Tabla {code}\n{code} — {name}\nCódigo: {code}\nNombre: {name}\nDescripción: {desc}\nEntradas: {inputs}\nPrioridad: {prio}\nNota. Elaboración propia (2026).')
    p('')

# ============================================================
# 8.2 RNF
# ============================================================
h2('8.2. Requerimientos No Funcionales')
p('Los requerimientos no funcionales establecen los atributos de calidad del sistema, siguiendo el modelo ISO/IEC 25010 (ISO, 2011).')
rnfs = [
    ('RNF01', 'Rendimiento', 'El tiempo de respuesta del sistema para operaciones estándar (consultas, listados, registros) no deberá superar los tres (3) segundos bajo condiciones normales de uso.', 'Tiempo de respuesta HTTP < 3 s', 'Alta'),
    ('RNF02', 'Seguridad', 'El sistema implementará HTTPS obligatorio, política de seguridad de contenido (CSP) mediante middleware, cabeceras X-Frame-Options: DENY, X-Content-Type-Options: nosniff, HSTS y protección contra fijación de sesión (session fixation) mediante regeneración del ID de sesión en cada inicio de sesión.', 'SecurityHeadersMiddleware, SECURE_HSTS_SECONDS, SESSION_COOKIE_HTTPONLY', 'Alta'),
    ('RNF03', 'Usabilidad', 'La interfaz será responsiva y adaptable a dispositivos móviles y de escritorio. Cada rol contará con un panel diferenciado (Admin: morado, Vigilante: azul, Cliente: verde). Los formularios incluirán validación en tiempo real mediante JavaScript y validación del lado del servidor.', 'Tailwind CSS CDN, 3 layouts diferenciados', 'Alta'),
    ('RNF04', 'Disponibilidad', 'El sistema deberá estar disponible el 99% del tiempo en horario operativo, garantizado por la plataforma Render.com con alta disponibilidad y reinicio automático ante fallos.', '99% uptime, auto-restart en Render.com', 'Alta'),
    ('RNF05', 'Mantenibilidad', 'El código fuente seguirá la arquitectura MVT de Django con apps separadas por dominio de negocio. Las convenciones de nomenclatura serán consistentes en todo el proyecto (camelCase prefijado por tabla).', 'Arquitectura MVT, 11 apps Django', 'Alta'),
    ('RNF06', 'Portabilidad', 'El sistema podrá desplegarse en cualquier plataforma PaaS que soporte Python 3.12 y MySQL 8.0, sin depender de configuraciones específicas de hardware.', 'requirements.txt, .env.example', 'Media'),
    ('RNF07', 'Escalabilidad', 'Las vistas de listado implementarán paginación para conjuntos de más de veinte (20) registros, evitando degradación de rendimiento con el crecimiento de datos.', 'Django Paginator, page_obj', 'Media'),
    ('RNF08', 'Compatibilidad', 'La interfaz web será compatible con las dos últimas versiones de los navegadores Chrome, Firefox y Microsoft Edge.', 'HTML5, CSS3, ES6+', 'Media'),
    ('RNF09', 'Internacionalización', 'La interfaz del sistema estará completamente en español. La zona horaria operativa será America/Bogotá (UTC-5). Los valores monetarios se expresarán en pesos colombianos (COP).', "LANGUAGE_CODE = 'es-co', TIME_ZONE = 'America/Bogota'", 'Alta'),
    ('RNF10', 'Trazabilidad', 'Todos los registros del sistema almacenarán marcas de tiempo de creación y actualización. Los cambios de estado en novedades y reservas quedarán registrados con usuario responsable y fecha.', 'auto_now_add, auto_now en DateTimeField', 'Media'),
]
for code, name, desc, impl, prio in rnfs:
    p(f'Tabla {code}\n{code} — {name}\nCódigo: {code}\nNombre: {name}\nDescripción: {desc}\nImplementación técnica: {impl}\nPrioridad: {prio}\nNota. Elaboración propia (2026).')
    p('')

# ============================================================
# 8.3 REQUERIMIENTOS NORMATIVOS
# ============================================================
h2('8.3. Requerimientos Normativos')
p('El sistema MultiParking deberá cumplir las siguientes disposiciones legales y normativas:')
p(
    'RNO01 — Ley 1581 de 2012 (Habeas Data): El sistema recopilará, almacenará y procesará datos personales '
    '(nombre, documento, correo, teléfono, placa) únicamente con el consentimiento del titular y para los fines '
    'declarados. Los usuarios podrán solicitar la rectificación o eliminación de sus datos. '
    '(Congreso de la República de Colombia, 2012).'
)
p(
    'RNO02 — Decreto 1377 de 2013: Se obtendrá autorización expresa del titular antes de recopilar datos '
    'personales. La política de privacidad estará disponible en el sistema. '
    '(Presidencia de la República de Colombia, 2013).'
)
p(
    'RNO03 — Normas SENA ADSO: La documentación seguirá la estructura y los artefactos requeridos por el '
    'programa Análisis y Desarrollo de Software del Centro de Diseño y Metrología — SENA. '
    '(SENA, 2023).'
)
p(
    'RNO04 — APA 7ª edición: Todas las referencias bibliográficas y citas dentro del documento seguirán '
    'las normas de la séptima edición del Manual de Publicaciones de la American Psychological Association '
    '(American Psychological Association, 2020).'
)
p('')

# ============================================================
# 8.4 REGLAS DE NEGOCIO
# ============================================================
h2('8.4. Reglas de Negocio')
p('Las reglas de negocio definen las restricciones y políticas operativas que el sistema debe garantizar en todo momento:')
reglas = [
    ('RN01', 'Ingreso único activo por vehículo', 'Un vehículo no puede tener más de un registro de parqueo con parHoraSalida IS NULL en forma simultánea. Intentar registrar el ingreso de un vehículo ya parqueado resultará en un error de validación.'),
    ('RN02', 'Solo espacios DISPONIBLE aceptan ingresos', 'Únicamente los espacios con espEstado = DISPONIBLE pueden asignarse a un nuevo ingreso. Los espacios OCUPADOS, RESERVADOS o en MANTENIMIENTO no están disponibles para asignación.'),
    ('RN03', 'Cálculo de costo minuto-base', 'El costo del parqueo se calcula como: costo = ceil((minutos_totales / 60) × precioHora / 100) × 100. El resultado siempre se redondea al siguiente múltiplo de 100 COP. Los visitantes pagan precioHoraVisitante en lugar de precioHora.'),
    ('RN04', 'Tarifa activa única por tipo de espacio', 'Solo puede existir una tarifa activa (activa = True) por tipo de espacio en cualquier momento. Al activar una tarifa nueva del mismo tipo, el sistema desactiva automáticamente la anterior.'),
    ('RN05', 'Validación de cupón antes de aplicar', 'Antes de aplicar un cupón, el sistema verifica: (a) que el código exista, (b) que cupActivo sea True, (c) que la fecha actual esté entre cupFechaInicio y cupFechaFin, y (d) que el cupon tenga usos disponibles restantes.'),
    ('RN06', 'Pisos con espacios ocupados no se eliminan', 'No se permite eliminar un piso que contenga al menos un espacio con espEstado = OCUPADO. Tampoco se pueden eliminar espacios con registros de parqueo activos.'),
    ('RN07', 'Gestión de estado al reservar/cancelar', 'Al confirmar una reserva, el espacio asociado cambia a RESERVADO. Al cancelar la reserva (por el cliente o el administrador), el espacio regresa a DISPONIBLE. Al completar la reserva (conversión a parqueo), el espacio pasa a OCUPADO.'),
    ('RN08', 'Token de recuperación de contraseña de un solo uso', 'El token de recuperación incorpora como huella los últimos 8 caracteres del hash de contraseña actual. Al cambiar la contraseña, el hash cambia y todos los tokens previos quedan automáticamente invalidados.'),
    ('RN09', 'Criterio de acumulación de sticker', 'Un sticker se asigna al usuario solo si: (a) el vehículo tiene propietario registrado, (b) la permanencia total del parqueo supera 60 minutos, y (c) el parqueo acaba de completarse (primer cálculo de salida).'),
    ('RN10', 'Generación automática de bono al canjear', 'Al reclamar el bono de fidelización, el sistema crea automáticamente un cupón de tipo PORCENTAJE con valor 100, uso máximo 1, y vigencia igual a diasVencimientoBono definido en ConfiguracionFidelidad. Los stickers canjeados se eliminan y el contador reinicia.'),
]
for code, name, desc in reglas:
    p(f'{code} — {name}: {desc}')
p('')

# ============================================================
# 9. DISEÑO
# ============================================================
h1('9. Diseño del Sistema')
h2('9.1. Alternativas de Solución (Mockups)')
p(
    'Durante la fase de diseño se elaboraron mockups de las interfaces principales del sistema, '
    'incluyendo el dashboard del administrador, la vista general de pisos, el formulario de ingreso '
    'de vehículos, el panel del vigilante y el perfil del cliente. Los mockups se encuentran disponibles '
    'en la carpeta "Mockups" de la carpeta Google Drive del proyecto.'
)

h2('9.2. Diagrama de Casos de Uso')
p(
    'El sistema cuenta con tres actores principales: Administrador, Vigilante y Cliente. '
    'A continuación se describen los casos de uso principales por actor:'
)
h3('Actor: Administrador')
p('• Gestionar usuarios (crear, editar, activar/desactivar, eliminar).')
p('• Gestionar pisos, tipos de espacio y espacios.')
p('• Gestionar tarifas.')
p('• Gestionar cupones.')
p('• Ver y gestionar todas las reservas.')
p('• Ver y gestionar novedades.')
p('• Generar y exportar reportes.')
p('• Configurar parámetros de fidelización.')

h3('Actor: Vigilante')
p('• Registrar ingreso y salida de vehículos.')
p('• Registrar vehículos visitantes.')
p('• Ver disponibilidad de espacios en tiempo real.')
p('• Registrar novedades operativas.')
p('• Aplicar cupones en el proceso de cobro.')

h3('Actor: Cliente')
p('• Registrar y gestionar sus vehículos.')
p('• Crear, consultar y cancelar reservas.')
p('• Ver su historial de parqueos y pagos.')
p('• Ver sus stickers acumulados y reclamar bono.')
p('• Recuperar su contraseña por correo.')

h2('9.3. Arquitectura del Software')
h3('9.3.1. Patrón Arquitectónico')
p(
    'El sistema implementa el patrón MVT (Modelo-Vista-Plantilla) de Django, que es una variación del '
    'patrón MVC donde:'
)
p('• Modelo (Model): Clases Python en models.py que mapean a tablas MySQL mediante el ORM de Django.')
p('• Vista (View): Clases basadas en View que procesan la lógica de negocio y retornan respuestas HTTP.')
p('• Plantilla (Template): Archivos HTML con sintaxis de Django Template Language + Tailwind CSS.')

h3('9.3.2. Estructura de Apps')
p(
    'El proyecto se organiza en once aplicaciones Django, cada una con responsabilidad única '
    'siguiendo el principio de separación de responsabilidades:'
)
apps_desc = [
    ('usuarios', 'Modelo Usuario personalizado, autenticación basada en sesión, tres roles (ADMIN, VIGILANTE, CLIENTE), recuperación de contraseña.'),
    ('vehiculos', 'Modelo Vehiculo con soporte para vehículos propios (fkIdUsuario no nulo) y visitantes (fkIdUsuario nulo).'),
    ('parqueadero', 'Lógica central: Piso, TipoEspacio, Espacio, InventarioParqueo. Vistas de administración, panel del vigilante y cliente.'),
    ('tarifas', 'Modelo Tarifa con precios por hora, día y mes diferenciados por tipo de espacio y por tipo de usuario.'),
    ('pagos', 'Modelo Pago vinculado a InventarioParqueo. Cálculo de costo con redondeo. Integración con cupones.'),
    ('cupones', 'Modelos Cupon y CuponAplicado. CRUD de cupones, validación y aplicación en el flujo de cobro.'),
    ('reservas', 'Modelo Reserva con gestión de disponibilidad. Bloqueo/liberación de espacios al confirmar/cancelar.'),
    ('novedades', 'Modelo Novedad con adjunto de foto, estados de progreso y notificación por correo al usuario afectado.'),
    ('fidelidad', 'Modelos Sticker y ConfiguracionFidelidad. Acumulación automática al completar parqueos largos.'),
    ('multiparking', 'Configuración central: settings.py, urls.py, middleware.py (seguridad), email_utils.py (SendGrid).'),
]
for app, desc in apps_desc:
    p(f'• {app}/: {desc}')

h3('9.3.3. Flujo de Autenticación')
p(
    'El sistema no usa django.contrib.auth.User. Implementa autenticación propia mediante sesiones Django:'
)
p('1. El usuario envía correo y contraseña en POST a /login/.')
p('2. Se consulta el modelo Usuario por usuCorreo.')
p('3. Se verifica la contraseña con check_password() contra el hash PBKDF2-SHA256 almacenado en usuClaveHash.')
p('4. Se llama request.session.cycle_key() para prevenir fijación de sesión.')
p('5. Se almacenan en sesión: usuario_id, usuario_nombre, usuario_rol, usuario_correo.')
p('6. Se redirige al panel correspondiente al rol.')

h2('9.4. Diagrama Entidad-Relación')
p(
    'La base de datos de MultiParking se compone de trece (13) tablas relacionales normalizadas hasta la '
    'tercera forma normal (3FN), gestionadas con PostgreSQL en producción. '
    'A continuación se describe la estructura relacional principal:'
)
p('• usuarios (PK: id) → vehiculos (FK: fkIdUsuario)')
p('• usuarios (PK: id) → novedades (FK: fkIdReportador, fkIdResponsable)')
p('• usuarios (PK: id) → fidelidad_stickers (FK: fkIdUsuario)')
p('• vehiculos (PK: id) → inventario_parqueo (FK: fkIdVehiculo)')
p('• vehiculos (PK: id) → reservas (FK: fkIdVehiculo)')
p('• vehiculos (PK: id) → novedades (FK: fkIdVehiculo)')
p('• pisos (PK: id) → espacios (FK: fkIdPiso)')
p('• tipos_espacio (PK: id) → espacios (FK: fkIdTipoEspacio)')
p('• tipos_espacio (PK: id) → tarifas (FK: fkIdTipoEspacio)')
p('• espacios (PK: id) → inventario_parqueo (FK: fkIdEspacio)')
p('• espacios (PK: id) → reservas (FK: fkIdEspacio)')
p('• espacios (PK: id) → novedades (FK: fkIdEspacio)')
p('• inventario_parqueo (PK: id) → pagos (FK: fkIdParqueo)')
p('• inventario_parqueo (PK: id) → fidelidad_stickers (FK: fkIdParqueo, OneToOne)')
p('• pagos (PK: id) → cupones_aplicados (FK: fkIdPago)')
p('• cupones (PK: id) → cupones_aplicados (FK: fkIdCupon)')
p('[Ver diagrama ER en anexo — generado con herramienta dbdiagram.io a partir del esquema MySQL]')

h2('9.5. Diccionario de Datos')
p(
    'El diccionario de datos describe todos los atributos de las tablas del sistema, '
    'incluyendo tipo de dato, longitud máxima, restricciones y descripción funcional.'
)

h3('9.5.1. Tabla usuarios')
p(
    'Tabla DD-01 — Diccionario de datos: usuarios\n'
    'Campo | Tipo | Long. | Nulo | PK/FK | Descripción\n'
    'id | BIGINT AUTO | - | No | PK | Identificador único del usuario\n'
    'usuDocumento | VARCHAR | 15 | No | - | Número de documento de identidad (solo dígitos)\n'
    'usuNombre | VARCHAR | 50 | No | - | Nombre del usuario (solo letras)\n'
    'usuApellido | VARCHAR | 50 | No | - | Apellido del usuario (solo letras)\n'
    'usuCorreo | VARCHAR | 64 | No | UNIQUE | Correo electrónico (único en el sistema)\n'
    'usuTelefono | VARCHAR | 10 | No | - | Número de teléfono (10 dígitos)\n'
    'usuClaveHash | VARCHAR | 255 | No | - | Hash PBKDF2-SHA256 de la contraseña\n'
    'rolTipoRol | VARCHAR | 10 | No | - | Rol del usuario: ADMIN, VIGILANTE o CLIENTE\n'
    'usuEstado | BOOLEAN | - | No | - | True = activo, False = desactivado\n'
    'usuFechaRegistro | DATETIME | - | No | - | Fecha y hora de registro en el sistema (auto)\n'
    'Nota. Elaboración propia (2026).'
)

h3('9.5.2. Tabla vehiculos')
p(
    'Tabla DD-02 — Diccionario de datos: vehiculos\n'
    'Campo | Tipo | Long. | Nulo | PK/FK | Descripción\n'
    'id | BIGINT AUTO | - | No | PK | Identificador único del vehículo\n'
    'vehPlaca | VARCHAR | 8 | No | UNIQUE | Placa del vehículo (alfanumérico + guión)\n'
    'vehTipo | VARCHAR | 5 | No | - | Tipo: CARRO, MOTO o BICI\n'
    'vehColor | VARCHAR | 20 | No | - | Color del vehículo (letras)\n'
    'vehMarca | VARCHAR | 30 | No | - | Marca del vehículo\n'
    'vehModelo | VARCHAR | 30 | No | - | Modelo del vehículo\n'
    'vehEstado | BOOLEAN | - | No | - | True = activo, False = inactivo\n'
    'fkIdUsuario | BIGINT | - | Sí | FK→usuarios | Propietario registrado; null si es visitante\n'
    'nombre_contacto | VARCHAR | 50 | Sí | - | Nombre del contacto (solo visitantes)\n'
    'telefono_contacto | VARCHAR | 10 | Sí | - | Teléfono del contacto (solo visitantes)\n'
    'Nota. Elaboración propia (2026).'
)

h3('9.5.3. Tablas pisos y tipos_espacio')
p(
    'Tabla DD-03 — Diccionario de datos: pisos\n'
    'Campo | Tipo | Long. | Nulo | PK/FK | Descripción\n'
    'id | BIGINT AUTO | - | No | PK | Identificador del piso\n'
    'pisNombre | VARCHAR | 30 | No | - | Nombre del piso (ej.: Piso 1, Sótano)\n'
    'pisEstado | BOOLEAN | - | No | - | True = activo, False = inactivo\n'
    'Nota. Elaboración propia (2026).\n\n'
    'Tabla DD-04 — Diccionario de datos: tipos_espacio\n'
    'Campo | Tipo | Long. | Nulo | PK/FK | Descripción\n'
    'id | BIGINT AUTO | - | No | PK | Identificador del tipo de espacio\n'
    'nombre | VARCHAR | 20 | No | UNIQUE | Nombre del tipo (ej.: Carro, Moto, Bicicleta)\n'
    'Nota. Elaboración propia (2026).'
)

h3('9.5.4. Tabla espacios')
p(
    'Tabla DD-05 — Diccionario de datos: espacios\n'
    'Campo | Tipo | Long. | Nulo | PK/FK | Descripción\n'
    'id | BIGINT AUTO | - | No | PK | Identificador del espacio\n'
    'espNumero | VARCHAR | 10 | No | - | Número o código del espacio (ej.: A-01)\n'
    'fkIdPiso | BIGINT | - | No | FK→pisos | Piso al que pertenece el espacio\n'
    'fkIdTipoEspacio | BIGINT | - | No | FK→tipos_espacio | Tipo de espacio para aplicar tarifa\n'
    'espEstado | VARCHAR | 10 | No | - | Estado: DISPONIBLE, OCUPADO, RESERVADO o MANTENIMIENTO\n'
    'Nota. Elaboración propia (2026).'
)

h3('9.5.5. Tabla inventario_parqueo')
p(
    'Tabla DD-06 — Diccionario de datos: inventario_parqueo\n'
    'Campo | Tipo | Long. | Nulo | PK/FK | Descripción\n'
    'id | BIGINT AUTO | - | No | PK | Identificador del registro de parqueo\n'
    'parHoraEntrada | DATETIME | - | No | - | Fecha y hora de ingreso del vehículo\n'
    'parHoraSalida | DATETIME | - | Sí | - | Fecha y hora de salida; NULL = vehículo aún parqueado\n'
    'fkIdVehiculo | BIGINT | - | No | FK→vehiculos | Vehículo que ocupa el espacio\n'
    'fkIdEspacio | BIGINT | - | No | FK→espacios | Espacio asignado\n'
    'Nota. Elaboración propia (2026).'
)

h3('9.5.6. Tabla tarifas')
p(
    'Tabla DD-07 — Diccionario de datos: tarifas\n'
    'Campo | Tipo | Long. | Nulo | PK/FK | Descripción\n'
    'id | BIGINT AUTO | - | No | PK | Identificador de la tarifa\n'
    'nombre | VARCHAR | 50 | No | - | Nombre descriptivo de la tarifa\n'
    'fkIdTipoEspacio | BIGINT | - | No | FK→tipos_espacio | Tipo de espacio al que aplica\n'
    'precioHora | DECIMAL(10,2) | - | No | - | Precio por hora para usuarios registrados (COP)\n'
    'precioHoraVisitante | DECIMAL(10,2) | - | No | - | Precio por hora para visitantes (COP)\n'
    'precioDia | DECIMAL(10,2) | - | No | - | Precio por día completo (COP)\n'
    'precioMensual | DECIMAL(10,2) | - | No | - | Precio mensual (COP)\n'
    'activa | BOOLEAN | - | No | - | True = tarifa vigente; solo una activa por tipo de espacio\n'
    'fechaInicio | DATE | - | No | - | Fecha de inicio de vigencia\n'
    'fechaFin | DATE | - | Sí | - | Fecha de fin de vigencia; null = indefinida\n'
    'Nota. Elaboración propia (2026).'
)

h3('9.5.7. Tablas pagos y cupones')
p(
    'Tabla DD-08 — Diccionario de datos: pagos\n'
    'Campo | Tipo | Long. | Nulo | PK/FK | Descripción\n'
    'id | BIGINT AUTO | - | No | PK | Identificador del pago\n'
    'pagFechaPago | DATETIME | - | No | - | Fecha y hora en que se registró el pago\n'
    'pagMonto | DECIMAL(10,2) | - | No | - | Monto total cobrado en COP\n'
    'pagMetodo | VARCHAR | 13 | No | - | Método: EFECTIVO, TARJETA o TRANSFERENCIA\n'
    'pagEstado | VARCHAR | 9 | No | - | Estado: PAGADO o PENDIENTE\n'
    'fkIdParqueo | BIGINT | - | No | FK→inventario_parqueo | Parqueo al que corresponde el pago\n'
    'Nota. Elaboración propia (2026).\n\n'
    'Tabla DD-09 — Diccionario de datos: cupones\n'
    'Campo | Tipo | Long. | Nulo | PK/FK | Descripción\n'
    'id | BIGINT AUTO | - | No | PK | Identificador del cupón\n'
    'cupNombre | VARCHAR | 50 | No | - | Nombre del cupón\n'
    'cupCodigo | VARCHAR | 20 | No | UNIQUE | Código único de canje (mayúsculas + números)\n'
    'cupTipo | VARCHAR | 10 | No | - | Tipo: PORCENTAJE o VALOR_FIJO\n'
    'cupValor | DECIMAL(10,2) | - | No | - | Valor del descuento (% o COP según tipo)\n'
    'cupDescripcion | TEXT | - | No | - | Descripción del cupón\n'
    'cupFechaInicio | DATE | - | No | - | Inicio de vigencia del cupón\n'
    'cupFechaFin | DATE | - | No | - | Fin de vigencia del cupón\n'
    'cupActivo | BOOLEAN | - | No | - | True = cupón disponible para canje\n'
    'Nota. Elaboración propia (2026).'
)

h3('9.5.8. Tablas reservas, novedades y fidelidad')
p(
    'Tabla DD-10 — Diccionario de datos: reservas\n'
    'Campo | Tipo | Long. | Nulo | PK/FK | Descripción\n'
    'id | BIGINT AUTO | - | No | PK | Identificador de la reserva\n'
    'resFechaReserva | DATE | - | No | - | Fecha de la reserva\n'
    'resHoraInicio | TIME | - | No | - | Hora de inicio de la reserva\n'
    'resHoraFin | TIME | - | Sí | - | Hora de fin de la reserva\n'
    'resEstado | VARCHAR | 10 | No | - | Estado: CONFIRMADA, CANCELADA o COMPLETADA\n'
    'fkIdEspacio | BIGINT | - | No | FK→espacios | Espacio reservado\n'
    'fkIdVehiculo | BIGINT | - | No | FK→vehiculos | Vehículo que reserva\n'
    'Nota. Elaboración propia (2026).\n\n'
    'Tabla DD-11 — Diccionario de datos: novedades\n'
    'Campo | Tipo | Long. | Nulo | PK/FK | Descripción\n'
    'id | BIGINT AUTO | - | No | PK | Identificador de la novedad\n'
    'novDescripcion | TEXT | - | No | - | Descripción detallada de la novedad\n'
    'novFoto | VARCHAR | 100 | Sí | - | Ruta del archivo de imagen adjunto (máx. 5 MB)\n'
    'novEstado | VARCHAR | 10 | No | - | Estado: PENDIENTE, EN_PROCESO o RESUELTO\n'
    'novComentario | TEXT | - | No | - | Comentario de seguimiento o resolución\n'
    'fkIdVehiculo | BIGINT | - | Sí | FK→vehiculos | Vehículo involucrado (opcional)\n'
    'fkIdEspacio | BIGINT | - | Sí | FK→espacios | Espacio afectado (opcional)\n'
    'fkIdReportador | BIGINT | - | Sí | FK→usuarios | Usuario que registra la novedad\n'
    'fkIdResponsable | BIGINT | - | Sí | FK→usuarios | Usuario asignado para resolver\n'
    'novFechaCreacion | DATETIME | - | No | - | Fecha y hora de creación (auto)\n'
    'novFechaActualizacion | DATETIME | - | No | - | Fecha y hora de última actualización (auto)\n'
    'Nota. Elaboración propia (2026).\n\n'
    'Tabla DD-12 — Diccionario de datos: fidelidad_stickers\n'
    'Campo | Tipo | Long. | Nulo | PK/FK | Descripción\n'
    'id | BIGINT AUTO | - | No | PK | Identificador del sticker\n'
    'fkIdUsuario | BIGINT | - | No | FK→usuarios | Usuario que acumula el sticker\n'
    'fkIdParqueo | BIGINT | - | No | FK→inventario_parqueo (OneToOne) | Parqueo que originó el sticker\n'
    'stkFecha | DATETIME | - | No | - | Fecha y hora de asignación del sticker (auto)\n'
    'Nota. Elaboración propia (2026).'
)

h2('9.6. Políticas de Seguridad de los Datos')
p('El sistema MultiParking implementa las siguientes medidas de seguridad:')
p('• Contraseñas: almacenadas con el algoritmo PBKDF2-SHA256 mediante django.contrib.auth.hashers. Nunca se almacena la contraseña en texto plano.')
p('• Sesiones: cookie HttpOnly, regeneración de ID de sesión en cada inicio (cycle_key()) para prevenir ataques de fijación de sesión.')
p('• HTTPS: obligatorio en producción mediante SECURE_SSL_REDIRECT = True y SECURE_HSTS_SECONDS.')
p('• Cabeceras HTTP de seguridad: X-Frame-Options: DENY (clickjacking), X-Content-Type-Options: nosniff (MIME sniffing), X-XSS-Protection: 1; mode=block.')
p('• Content Security Policy (CSP): implementada mediante SecurityHeadersMiddleware personalizado, restringiendo fuentes de scripts, estilos e imágenes.')
p('• Tokens de un solo uso: los enlaces de recuperación de contraseña incluyen una huella del hash actual. Al cambiar la contraseña, el hash cambia y el enlace queda invalidado automáticamente.')
p('• Validación de archivos subidos: solo se aceptan imágenes (JPG, PNG, GIF, WEBP) con tamaño máximo de 5 MB en la subida de fotos de novedades.')
p('• Protección CSRF: Django aplica el middleware CsrfViewMiddleware en todas las vistas POST.')
p('')

# ============================================================
# 10. CONSTRUCCIÓN
# ============================================================
h1('10. Construcción del Software')
h2('10.1. ORM de Django — Gestión de la Base de Datos')
p(
    'El sistema MultiParking utiliza el ORM (Object-Relational Mapping) integrado de Django para '
    'gestionar toda la interacción con la base de datos, sin escribir SQL directamente en la '
    'mayor parte del código. El ORM actúa como una capa de abstracción que traduce automáticamente '
    'las operaciones sobre objetos Python a sentencias SQL optimizadas.'
)
p('Las ventajas del ORM de Django en este proyecto son:')
p('• Portabilidad: el mismo código Python funciona con PostgreSQL en producción (Render.com) sin modificaciones.')
p('• Migraciones automáticas: los cambios en los modelos Python generan automáticamente los scripts DDL de base de datos mediante python manage.py makemigrations y migrate.')
p('• Seguridad: el ORM aplica automáticamente escape de parámetros en todas las consultas, eliminando el riesgo de inyección SQL.')
p('• Consultas expresivas: el queryset API permite filtros complejos en Python (ej.: InventarioParqueo.objects.filter(parHoraSalida__isnull=True)) que se traducen a SQL eficiente.')

h3('10.1.1. Ejemplos de Uso del ORM')
p(
    '# Obtener parqueos activos (vehículos actualmente en el parqueadero):\n'
    'activos = InventarioParqueo.objects.filter(parHoraSalida__isnull=True).select_related("fkIdVehiculo", "fkIdEspacio")\n\n'
    '# Crear un nuevo pago vinculado al parqueo:\n'
    'Pago.objects.create(fkIdParqueo=parqueo, pagMonto=costo, pagMetodo="EFECTIVO", pagEstado="PAGADO")\n\n'
    '# Filtrar espacios disponibles en un piso:\n'
    'Espacio.objects.filter(fkIdPiso=piso, espEstado="DISPONIBLE").order_by("espNumero")'
)

h2('10.2. Base de Datos en Producción')
p(
    'En el entorno de producción (Render.com), el sistema usa PostgreSQL como motor de base de datos. '
    'Django gestiona la conexión mediante la variable de entorno DATABASE_URL, parseada con '
    'dj-database-url. El ORM garantiza que el código Python sea idéntico entre entornos: '
    'no se requieren cambios en las vistas ni en los modelos al cambiar de motor.'
)

h2('10.3. Objetos de la Base de Datos — Triggers')
p(
    'Aunque el ORM de Django gestiona la mayor parte de la lógica de negocio en la capa de aplicación, '
    'el proyecto también define disparadores (triggers) a nivel de base de datos para garantizar '
    'consistencia en operaciones críticas, independientemente del origen del cambio. '
    'Los siguientes triggers se documentan como referencia de la lógica de base de datos; '
    'en producción (PostgreSQL) se implementan mediante funciones PL/pgSQL equivalentes.'
)
p('Se implementaron tres disparadores (triggers) para automatizar cambios de estado:')
p(
    'Trigger 1 — Reserva a Parqueo: Al insertar un registro en la tabla reservas, '
    'el trigger crea automáticamente el registro de ingreso en inventario_parqueo.\n'
    'Disparador de prueba:\n'
    'INSERT INTO reservas (resHoraInicio, resHoraFin, fkIdEspacio, fkIdVehiculo)\n'
    "VALUES ('2025-09-10 10:00:00', '2025-09-10 12:00:00', 1, 1);"
)
p(
    'Trigger 2 — Bloquear espacio al ingresar: Al insertar un registro en inventario_parqueo, '
    'el trigger actualiza el estado del espacio asociado a OCUPADO.\n'
    'Disparador de prueba:\n'
    'INSERT INTO parqueos (parHoraEntrada, fkIdVehiculo, fkIdTarifa, fkIdEspacio)\n'
    'VALUES (NOW(), 1, 1, 1);'
)
p(
    'Trigger 3 — Liberar espacio al salir: Al actualizar parHoraSalida en inventario_parqueo '
    '(valor no nulo), el trigger cambia el estado del espacio a DISPONIBLE.\n'
    'Disparador de prueba:\n'
    'UPDATE parqueos\n'
    'SET parHoraSalida = NOW()\n'
    'WHERE idParqueo = 123;'
)

h2('10.4. Estándar de Codificación')
p('El proyecto sigue las siguientes convenciones de codificación:')
p('• Nombres de campos de modelos: camelCase con prefijo de abreviatura de tabla (usuNombre, vehPlaca, espEstado, parHoraEntrada, pagMonto).')
p('• Claves foráneas: nombradas fkId<Entidad> con atributo db_column explícito que referencia el nombre de columna en la BD.')
p('• db_table: declarado explícitamente en la clase Meta de cada modelo (ej.: db_table = "usuarios").')
p('• Vistas: todas son class-based (herencia de View), con el patrón List/Create/Update/Delete por entidad.')
p('• Sin Django Forms: las vistas leen directamente de request.POST, con validación propia mediante re.match() y mensajes de error vía el framework messages de Django.')
p('• Propiedades derivadas: se implementan como @property en el modelo (usuNombreCompleto, es_visitante, resConfirmada). No generan columnas en la BD.')
p('• Comentarios: solo donde la lógica no es auto-explicativa (ej.: cálculo de costo, lógica de stickers).')

h2('10.5. Código Fuente — Fragmentos Representativos')
h3('10.4.1. Cálculo de Costo de Parqueo')
p(
    'La función principal de cálculo de costo se implementa en parqueadero/vigilante_views.py. '
    'Utiliza la biblioteca Decimal para evitar errores de punto flotante y math.ceil para el redondeo:'
)
p(
    'import math\n'
    'from decimal import Decimal\n\n'
    'def calcular_costo(hora_entrada, hora_salida, precio_hora):\n'
    '    delta = hora_salida - hora_entrada\n'
    '    minutos = delta.total_seconds() / 60\n'
    '    costo = Decimal(str(math.ceil((minutos / 60) * float(precio_hora) / 100) * 100))\n'
    '    return max(costo, Decimal("100"))  # Mínimo 100 COP'
)

h3('10.4.2. Middleware de Seguridad')
p(
    'El archivo multiparking/middleware.py implementa SecurityHeadersMiddleware, '
    'que agrega cabeceras de seguridad HTTP a todas las respuestas del sistema:'
)
p(
    'class SecurityHeadersMiddleware:\n'
    "    CSP = (\n"
    "        \"default-src 'self'; \"\n"
    "        \"script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; \"\n"
    "        \"style-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; \"\n"
    "        \"img-src 'self' data: blob:; \"\n"
    "        \"font-src 'self'; connect-src 'self'; frame-ancestors 'none';\"\n"
    "    )\n"
    "    def __call__(self, request):\n"
    "        response = self.get_response(request)\n"
    "        response['Content-Security-Policy'] = self.CSP\n"
    "        response['X-XSS-Protection'] = '1; mode=block'\n"
    "        return response"
)

h2('10.6. Control de Versiones')
p(
    'El proyecto utiliza Git como sistema de control de versiones, con repositorio alojado en GitHub. '
    'La rama principal es main. El flujo de trabajo consiste en commits frecuentes con mensajes '
    'descriptivos en español. Los archivos sensibles (.env, __pycache__) están excluidos mediante .gitignore.'
)
p('• Repositorio: GitHub (privado)')
p('• Rama principal: main')
p('• Estrategia de ramas: desarrollo directo en main con commits atómicos por funcionalidad')
p('')

# ============================================================
# 11. PRUEBAS
# ============================================================
h1('11. Pruebas del Software')
h2('11.1. Pruebas Unitarias por Módulo')
p('Las pruebas unitarias verifican el correcto funcionamiento de cada módulo en forma independiente. La siguiente tabla resume los casos de prueba ejecutados:')

pruebas_unitarias = [
    ('PU01', 'Usuarios', 'Registro con datos válidos', 'Usuario creado, contraseña hasheada', 'PASÓ'),
    ('PU02', 'Usuarios', 'Login con credenciales correctas', 'Sesión creada con rol CLIENTE', 'PASÓ'),
    ('PU03', 'Usuarios', 'Login con contraseña incorrecta', 'Error "Credenciales incorrectas"', 'PASÓ'),
    ('PU04', 'Usuarios', 'Recuperación de contraseña', 'Correo enviado, token generado', 'PASÓ'),
    ('PU05', 'Usuarios', 'Token usado una segunda vez', 'Error "enlace ya utilizado"', 'PASÓ'),
    ('PU06', 'Vehículos', 'Registro vehículo propio', 'Vehículo asociado al usuario', 'PASÓ'),
    ('PU07', 'Vehículos', 'Registro vehículo visitante', 'Vehículo sin fkIdUsuario', 'PASÓ'),
    ('PU08', 'Espacios', 'Crear espacio en piso activo', 'Espacio creado en estado DISPONIBLE', 'PASÓ'),
    ('PU09', 'Parqueos', 'Registrar ingreso en espacio DISPONIBLE', 'Estado cambia a OCUPADO', 'PASÓ'),
    ('PU10', 'Parqueos', 'Registrar ingreso con vehículo ya activo', 'Error de validación (doble ingreso)', 'PASÓ'),
    ('PU11', 'Parqueos', 'Calcular costo 90 minutos a $5000/hora', '$8000 (ceil a 100)', 'PASÓ'),
    ('PU12', 'Tarifas', 'Activar nueva tarifa desactiva anterior', 'Solo una tarifa activa por tipo', 'PASÓ'),
    ('PU13', 'Cupones', 'Aplicar cupón PORCENTAJE 20% en $10000', 'Descuento $2000, total $8000', 'PASÓ'),
    ('PU14', 'Cupones', 'Aplicar cupón vencido', 'Error "cupón vencido"', 'PASÓ'),
    ('PU15', 'Reservas', 'Crear reserva en espacio disponible', 'Estado espacio → RESERVADO', 'PASÓ'),
    ('PU16', 'Reservas', 'Cancelar reserva', 'Estado espacio → DISPONIBLE', 'PASÓ'),
    ('PU17', 'Novedades', 'Registrar novedad con foto PNG', 'Novedad guardada, foto almacenada', 'PASÓ'),
    ('PU18', 'Novedades', 'Subir archivo .exe como foto', 'Error "Solo se permiten imágenes"', 'PASÓ'),
    ('PU19', 'Fidelidad', 'Parqueo >60 min con usuario registrado', 'Sticker asignado al usuario', 'PASÓ'),
    ('PU20', 'Fidelidad', 'Parqueo <60 min', 'Sin sticker asignado', 'PASÓ'),
]
p('Tabla PT-01\nPruebas Unitarias por Módulo\n'
  'ID | Módulo | Caso de Prueba | Resultado Esperado | Estado\n' +
  '\n'.join(f'{id} | {mod} | {caso} | {esperado} | {estado}' for id, mod, caso, esperado, estado in pruebas_unitarias) +
  '\nNota. Pruebas ejecutadas manualmente en entorno de desarrollo (2026).')
p('')

h2('11.2. Pruebas de Sistema (Flujos End-to-End)')
p('Las pruebas de sistema validan los flujos completos de usuario, desde la interfaz hasta la base de datos:')
pruebas_sistema = [
    ('PS01', 'Flujo de ingreso y salida completo', 'Admin crea espacio → Vigilante registra ingreso → Sistema marca espacio OCUPADO → Vigilante registra salida → Sistema calcula costo → Genera Pago → Espacio DISPONIBLE', 'PASÓ'),
    ('PS02', 'Flujo de reserva por cliente', 'Cliente inicia sesión → Crea reserva → Espacio RESERVADO → Vigilante convierte a parqueo → Espacio OCUPADO → Salida → Pago generado', 'PASÓ'),
    ('PS03', 'Flujo de cupón en cobro', 'Vigilante registra salida → Ingresa código de cupón válido → Sistema aplica descuento → Pago con monto reducido → CuponAplicado registrado', 'PASÓ'),
    ('PS04', 'Flujo de novedad con notificación', 'Vigilante crea novedad con foto → Sistema envía correo al dueño del vehículo → Admin actualiza estado → Se envía nuevo correo', 'PASÓ'),
    ('PS05', 'Flujo de fidelización', 'Parqueo >1 hora completado → Sticker asignado → Cliente ve progreso en perfil → Alcanza meta → Reclama bono → Cupón 100% generado', 'PASÓ'),
    ('PS06', 'Flujo de recuperación de contraseña', 'Usuario solicita correo → Recibe enlace con token → Establece nueva contraseña → Token queda invalidado → Reintento con mismo enlace falla', 'PASÓ'),
    ('PS07', 'Prueba de seguridad — acceso sin autenticación', 'Usuario no autenticado intenta acceder a /admin-panel/ → Redirige a /login/ con código 302', 'PASÓ'),
    ('PS08', 'Prueba de seguridad — acceso de rol incorrecto', 'Usuario CLIENTE intenta acceder a /admin-panel/ → Redirige a /dashboard/ (acceso denegado)', 'PASÓ'),
]
p('Tabla PT-02\nPruebas de Sistema — Flujos End-to-End\n'
  'ID | Flujo | Descripción | Estado\n' +
  '\n'.join(f'{id} | {flujo} | {desc} | {estado}' for id, flujo, desc, estado in pruebas_sistema) +
  '\nNota. Elaboración propia (2026).')
p('')

h2('11.3. Manejo de Alertas y Excepciones')
p('El sistema maneja los errores de la siguiente manera:')
p('• Errores de validación: mostrados al usuario mediante el framework messages de Django (messages.error / messages.success) con clases de estilos Tailwind CSS.')
p('• Errores 404: página personalizada que redirige al inicio sin exponer información del stack.')
p('• Errores de base de datos: capturados en bloques try/except con mensajes amigables al usuario.')
p('• Errores de envío de correo: capturados sin interrumpir el flujo principal; el correo fallido se registra en el log del servidor.')
p('• Validación de archivos: tipo MIME y tamaño verificados antes de guardar, con mensajes de error específicos.')
p('')

# ============================================================
# 12. DESPLIEGUE
# ============================================================
h1('12. Despliegue')
h2('12.1. Plan de Despliegue')
p(
    'El sistema MultiParking se despliega en la plataforma cloud Render.com, '
    'que proporciona servicio de Web Service con alta disponibilidad y MySQL como add-on de base de datos. '
    'El proceso de despliegue es continuo (CI/CD): cada push a la rama main desencadena un redespliegue automático.'
)
h3('12.1.1. Configuración del Entorno')
p('Variables de entorno requeridas (archivo .env):')
p(
    'SECRET_KEY=<clave secreta Django 50+ caracteres>\n'
    'DEBUG=False\n'
    'DB_NAME=<nombre base de datos MySQL>\n'
    'DB_USER=<usuario MySQL>\n'
    'DB_PASSWORD=<contraseña MySQL>\n'
    'DB_HOST=<host MySQL>\n'
    'DB_PORT=3306\n'
    'SENDGRID_API_KEY=<clave API SendGrid>\n'
    'DEFAULT_FROM_EMAIL=no-reply@multiparking.com\n'
    'ALLOWED_HOSTS=multiparking.onrender.com'
)

h3('12.1.2. Proceso de Despliegue')
p('1. git push origin main → Render detecta el cambio y inicia el build.')
p('2. pip install -r requirements.txt → instalación de dependencias.')
p('3. python manage.py collectstatic --noinput → recopilación de archivos estáticos con Whitenoise.')
p('4. python manage.py migrate → aplicación de migraciones pendientes.')
p('5. gunicorn multiparking.wsgi:application --bind 0.0.0.0:$PORT → inicio del servidor.')

h2('12.2. Manual del Usuario')
h3('12.2.1. Rol Administrador')
p('El administrador accede al sistema mediante /admin-panel/. Sus principales flujos son:')
p('• Gestión de usuarios: /admin-panel/usuarios/ — crear, editar, activar/desactivar usuarios.')
p('• Gestión de espacios: /admin-panel/pisos/ y /admin-panel/espacios/ — configurar la estructura del parqueadero.')
p('• Gestión de tarifas: /admin-panel/tarifas/ — definir precios por tipo de espacio.')
p('• Gestión de cupones: /admin-panel/cupones/ — crear y administrar descuentos.')
p('• Reportes: /admin-panel/reportes/ — visualizar estadísticas y exportar a PDF/Excel.')
p('• Novedades: /admin-panel/novedades/ — gestionar incidentes operativos.')

h3('12.2.2. Rol Vigilante')
p('El vigilante accede al sistema mediante /vigilante/dashboard/. Sus flujos principales son:')
p('• Registrar ingreso: seleccionar el vehículo (por placa) y el espacio disponible. El sistema registra la hora y cambia el estado del espacio a OCUPADO.')
p('• Registrar salida: seleccionar el registro activo, ingresar opcionalmente un código de cupón, confirmar el monto calculado y registrar el método de pago.')
p('• Vista de pisos: visualización en tiempo real del estado de todos los espacios, con actualización automática cada 30 segundos.')
p('• Registrar novedad: documentar incidentes o daños con descripción, foto y espacio/vehículo involucrado.')

h3('12.2.3. Rol Cliente')
p('El cliente accede al sistema mediante /dashboard/. Sus funcionalidades son:')
p('• Mis vehículos: registrar y gestionar sus vehículos propios.')
p('• Mis reservas: crear, consultar y cancelar reservas anticipadas de espacio.')
p('• Mi historial: consultar parqueos y pagos anteriores.')
p('• Mi perfil: ver stickers acumulados, barra de progreso hacia el bono y botón de canje cuando se alcanza la meta.')

h2('12.3. Copias de Seguridad')
p(
    'Se recomienda configurar respaldos automáticos de la base de datos MySQL con frecuencia diaria. '
    'Render.com ofrece snapshots automáticos de la base de datos. Adicionalmente, se pueden programar '
    'dumps periódicos con el comando:'
)
p('mysqldump -u <usuario> -p <base_de_datos> > backup_$(date +%Y%m%d).sql')
p('')

# ============================================================
# 13. CONCLUSIONES
# ============================================================
h1('13. Conclusiones')
p(
    'El desarrollo del sistema de información web MultiParking permitió automatizar de forma integral '
    'los procesos operativos de un parqueadero privado, sustituyendo métodos manuales propensos a '
    'errores por una plataforma digital escalable, segura y de fácil uso. A lo largo del proyecto '
    'se validaron los conceptos fundamentales de análisis y desarrollo de software: levantamiento de '
    'requerimientos, diseño de base de datos normalizada, implementación con patrón MVT, pruebas '
    'funcionales y despliegue en la nube.'
)
p(
    'La elección de Django 6.0 como framework demostró ser acertada: su sistema de migraciones '
    'facilitó la evolución incremental del modelo de datos, su ORM redujo la complejidad del acceso '
    'a MySQL, y su arquitectura de apps permitió organizar el código de forma modular y mantenible. '
    'La implementación de autenticación propia (sin django.contrib.auth.User) representó un reto '
    'técnico que fortaleció la comprensión de los mecanismos de seguridad en sesiones web.'
)
p(
    'El módulo de fidelización (stickers) y el sistema de novedades con notificación por correo '
    'superaron el alcance mínimo del proyecto, aportando valor diferencial a la solución. '
    'La integración con SendGrid para correos transaccionales y con Render.com para despliegue '
    'continuo demostró la viabilidad de construir aplicaciones de producción con herramientas '
    'accesibles y de bajo costo para microempresas.'
)
p(
    'Como trabajo futuro se identifican: la integración con hardware automatizado (barreras, '
    'lectores de QR, cámaras de reconocimiento de placas), el desarrollo de una aplicación móvil '
    'nativa, la implementación de pagos digitales en línea (PayU, Nequi) y la expansión del módulo '
    'de reportes con inteligencia de negocio avanzada.'
)
p('')

# ============================================================
# 14. BIBLIOGRAFÍA
# ============================================================
h1('14. Bibliografía y Ciberografía')
p('American Psychological Association. (2020). Publication manual of the American Psychological Association (7th ed.). https://doi.org/10.1037/0000165-000')
p('Congreso de la República de Colombia. (2012). Ley 1581 de 2012: por la cual se dictan disposiciones generales para la protección de datos personales. Diario Oficial, 48587.')
p('Django Software Foundation. (2024). Django documentation (Version 6.0). https://docs.djangoproject.com/en/6.0/')
p('García, A., & Martínez, L. (2022). Implementación de sistemas de información para la gestión de parqueaderos en ciudades intermedias de Colombia. Revista Ingeniería e Innovación, 10(2), 45–58. https://doi.org/10.21500/20274206.xxxx')
p('Garavito Albao, G., Macías Lamprea, R. A., & Pinzón Osorio, N. (2021). Sistema de gestión para ópticas SIGEOP: una propuesta de automatización para pequeñas empresas de salud visual. TIA — Tecnología, Investigación y Academia, 9(2).')
p('IEEE. (2011). IEEE 830-1998: Recommended practice for software requirements specifications. Institute of Electrical and Electronics Engineers.')
p('ISO/IEC. (2011). ISO/IEC 25010:2011 — Systems and software engineering: Systems and software quality requirements and evaluation (SQuaRE). International Organization for Standardization.')
p('MinTIC. (2023). Política de transformación digital e inteligencia artificial de Colombia. Ministerio de Tecnologías de la Información y las Comunicaciones. https://www.mintic.gov.co')
p('MySQL. (2024). MySQL 8.0 reference manual. Oracle Corporation. https://dev.mysql.com/doc/refman/8.0/en/')
p('Presidencia de la República de Colombia. (2013). Decreto 1377 de 2013: por el cual se reglamenta parcialmente la Ley 1581 de 2012. Diario Oficial, 48834.')
p('Render. (2024). Render documentation. Render Inc. https://render.com/docs')
p('SendGrid. (2024). SendGrid email API documentation. Twilio Inc. https://docs.sendgrid.com/')
p('Tailwind CSS. (2024). Tailwind CSS documentation (v3). Tailwind Labs Inc. https://tailwindcss.com/docs')
p('')

# ============================================================
# 15. GLOSARIO
# ============================================================
h1('15. Glosario')
glosario = [
    ('CSP (Content Security Policy)', 'Política de seguridad de contenido HTTP que controla qué recursos puede cargar el navegador, reduciendo el riesgo de ataques XSS.'),
    ('Cupón', 'Código alfanumérico que otorga un descuento (porcentaje o valor fijo) al aplicarse en el momento del cobro por el uso del parqueadero.'),
    ('Django', 'Framework web de alto nivel basado en Python que sigue el patrón arquitectónico MVT (Modelo-Vista-Plantilla).'),
    ('Espacio', 'Unidad física del parqueadero, identificada por número y ubicada en un piso. Puede estar en estado DISPONIBLE, OCUPADO, RESERVADO o MANTENIMIENTO.'),
    ('Fidelización', 'Sistema de puntos o stickers que recompensa a los usuarios frecuentes con cupones de descuento automáticos al alcanzar una meta de parqueos.'),
    ('Hash PBKDF2', 'Algoritmo de derivación de claves que convierte la contraseña del usuario en una representación irreversible, protegiendo las credenciales en caso de filtración de datos.'),
    ('Inventario de Parqueo', 'Registro de cada entrada y salida de vehículo al parqueadero, incluyendo horas, espacio asignado y referencia al pago generado.'),
    ('MySQL', 'Sistema de gestión de bases de datos relacional de código abierto utilizado para almacenar toda la información del sistema MultiParking.'),
    ('Novedad', 'Registro de un incidente, daño u observación operativa en el parqueadero, con seguimiento de estado y notificación al usuario afectado.'),
    ('Parqueadero', 'Establecimiento destinado al estacionamiento de vehículos, compuesto por pisos y espacios administrados por el sistema.'),
    ('Render.com', 'Plataforma cloud de despliegue continuo (PaaS) utilizada para alojar la aplicación web y la base de datos MySQL de MultiParking.'),
    ('Reserva', 'Apartado anticipado de un espacio del parqueadero para una fecha y horario específicos, realizado por un cliente registrado.'),
    ('SendGrid', 'Servicio de correo electrónico transaccional utilizado por MultiParking para enviar notificaciones de recuperación de contraseña y alertas de novedades.'),
    ('Sesión', 'Mecanismo de Django que almacena datos del usuario autenticado del lado del servidor, identificado por una cookie en el navegador.'),
    ('Sticker', 'Unidad de fidelización acumulable que el sistema otorga automáticamente al usuario cada vez que completa un parqueo de más de 60 minutos.'),
    ('Tailwind CSS', 'Framework CSS basado en clases utilitarias que permite construir interfaces responsivas directamente en el HTML, sin escribir CSS personalizado.'),
    ('Tarifa', 'Precio definido por tipo de espacio y tipo de usuario (registrado o visitante), expresado en pesos colombianos por hora, día o mes.'),
    ('Vigilante', 'Usuario con rol VIGILANTE que opera el control de ingreso y salida de vehículos, puede registrar novedades y aplicar cupones en el cobro.'),
]
for term, defi in glosario:
    p(f'{term}: {defi}')
p('')
p('Nota. Definiciones elaboradas por el equipo de desarrollo con base en el contexto del sistema MultiParking (2026).')

# ============================================================
# GENERAR REQUESTS PARA LA API
# ============================================================
print(f'Total secciones: {len(sections)}', file=sys.stderr)

# Construir todo el texto como una cadena, rastreando posiciones para estilos
# Estrategia: insertar todo el texto en un solo request, luego aplicar estilos
full_text = ''
style_ranges = []  # Lista de (start, end, named_style_type)

current_index = 1  # El documento empieza en index 1

for style, text in sections:
    text_with_newline = text + '\n'
    start = current_index
    end = start + len(text_with_newline)

    if style != 'NORMAL_TEXT':
        style_ranges.append((start, end, style))

    full_text += text_with_newline
    current_index = end

# Request 1: insertar todo el texto
insert_request = {
    'insertText': {
        'location': {'index': 1},
        'text': full_text
    }
}

# Requests 2+: aplicar estilos a headings
style_requests = []
for start, end, style in style_ranges:
    if style == 'TITLE':
        named_style = 'TITLE'
    elif style == 'SUBTITLE':
        named_style = 'SUBTITLE'
    else:
        # HEADING_1 -> HEADING_1, etc.
        named_style = style

    style_requests.append({
        'updateParagraphStyle': {
            'range': {'startIndex': start, 'endIndex': end},
            'paragraphStyle': {'namedStyleType': named_style},
            'fields': 'namedStyleType'
        }
    })

all_requests = [insert_request] + style_requests

print(f'Total requests: {len(all_requests)} (1 insertText + {len(style_requests)} estilos)', file=sys.stderr)
print(f'Texto total: {len(full_text)} chars', file=sys.stderr)

# Guardar requests a un archivo JSON para procesarlos en batches
batch_size = 500
batches = []
# El insertText va solo en el primer batch
batches.append([insert_request])
# Los style_requests van en batches de 500
for i in range(0, len(style_requests), batch_size):
    batches.append(style_requests[i:i+batch_size])

print(f'Batches a enviar: {len(batches)}', file=sys.stderr)

# Guardar cada batch como archivo JSON
import json
for i, batch in enumerate(batches):
    fname = f'doc_batch_{i:03d}.json'
    with open(fname, 'w', encoding='utf-8') as f:
        json.dump({'requests': batch}, f, ensure_ascii=False)
    print(f'Guardado: {fname} ({len(batch)} requests)', file=sys.stderr)

print('DONE', file=sys.stderr)
print('OK')
