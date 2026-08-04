#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera Manual_Despliegue_Multiparking.docx replicando EXACTAMENTE el formato
(fuentes, tamaños, colores, bordes y sombreado de tablas) extraído de
Manual_Despliegue_OptiLuxe.docx:

  - Fuente base: Arial 10pt, color negro (000000)
  - Título portada: Arial 24pt bold color 1F4E79 / subtítulo 16pt bold 2E6DB4
  - Heading 1: Arial 14pt bold color 1F4E79
  - Heading 2: Arial 12pt bold color 2E6DB4
  - Tablas: borde exterior sencillo, celdas con borde 1pt negro,
    fila de cabecera con relleno #404040 y texto blanco bold centrado,
    filas de datos alternadas #FFFFFF / #F2F2F2, texto 9pt no-bold
  - Página carta (8.5x11in), márgenes 0.75in

Contenido adaptado al entorno real de MultiParking (Render.com + PostgreSQL
managed), sin la sección de migración a VPS/Dokploy del manual original.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from docx import Document
from docx.shared import Pt, Inches, Twips, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

FONT = 'Arial'
COLOR_BODY = '000000'
COLOR_H1 = '1F4E79'
COLOR_H2 = '2E6DB4'
COLOR_HEADER_FILL = '404040'
COLOR_ALT_FILL = 'F2F2F2'
COLOR_WHITE = 'FFFFFF'

doc = Document()

# ── Página carta, márgenes 0.75in (igual al manual OptiLuxe) ─────────────────
for section in doc.sections:
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)

# ── helpers de formato ────────────────────────────────────────────────────────
def set_run_font(run, size_pt, bold=False, italic=False, color=COLOR_BODY, font=FONT):
    run.font.name = font
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor.from_string(color)
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    for attr in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rFonts.set(qn(attr), font)

def add_para(text='', size=10, bold=False, italic=False, color=COLOR_BODY,
             align=None, before=0, after=7):
    para = doc.add_paragraph()
    pf = para.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    if align is not None:
        para.alignment = align
    if text:
        run = para.add_run(text)
        set_run_font(run, size, bold=bold, italic=italic, color=color)
    return para

def h1(text):
    return add_para(text, size=14, bold=True, color=COLOR_H1, before=20, after=8)

def h2(text):
    return add_para(text, size=12, bold=True, color=COLOR_H2, before=14, after=6)

def body(text):
    return add_para(text, size=10, bold=False, color=COLOR_BODY, before=0, after=7)

def cover_line(text, size=11, bold=False, color=COLOR_BODY, before=0, after=4):
    return add_para(text, size=size, bold=bold, color=color,
                     align=WD_ALIGN_PARAGRAPH.CENTER, before=before, after=after)

def spacer(after=3):
    return add_para('', before=0, after=after)

# ── helpers de tabla (bordes, sombreado, márgenes) ───────────────────────────
def _set_cell_borders(cell, sz=1, color='000000'):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right'):
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), str(sz))
        el.set(qn('w:color'), color)
        borders.append(el)
    tcPr.append(borders)

def _shade_cell(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:fill'), fill)
    tcPr.append(shd)

def _set_cell_margins(cell, top, bottom, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    mar = OxmlElement('w:tcMar')
    for edge, val in (('top', top), ('left', left), ('bottom', bottom), ('right', right)):
        node = OxmlElement(f'w:{edge}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        mar.append(node)
    tcPr.append(mar)

def _set_cell_valign_center(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    va = OxmlElement('w:vAlign')
    va.set(qn('w:val'), 'center')
    tcPr.append(va)

def _set_cell_text(cell, text, bold, color, align, size=9):
    para = cell.paragraphs[0]
    for run in list(para.runs):
        run._element.getparent().remove(run._element)
    if align is not None:
        para.alignment = align
    run = para.add_run(text)
    set_run_font(run, size, bold=bold, color=color)

def _mark_header_row(table):
    trPr = table.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement('w:tblHeader')
    trPr.append(th)

# Anchos de columna extraídos de Manual_Despliegue_OptiLuxe.docx (dxa)
COL_WIDTHS = {2: (3060, 9180), 3: (2040, 5100, 5100)}

def table(headers, rows, titulo=None):
    if titulo:
        add_para(titulo, size=10, bold=True, before=0, after=2)
    n = len(headers)
    col_widths = COL_WIDTHS[n]
    tbl = doc.add_table(rows=1 + len(rows), cols=n)
    tbl.autofit = False

    tblPr = tbl._tbl.tblPr
    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:type'), 'dxa')
    tblW.set(qn('w:w'), '12240')
    tblPr.append(tblW)
    borders = OxmlElement('w:tblBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), '4')
        el.set(qn('w:color'), 'auto')
        borders.append(el)
    tblPr.append(borders)

    grid = tbl._tbl.find(qn('w:tblGrid'))
    for gridCol, w in zip(grid.findall(qn('w:gridCol')), col_widths):
        gridCol.set(qn('w:w'), str(w))
    for i, w in enumerate(col_widths):
        for cell in tbl.columns[i].cells:
            cell.width = Twips(w)

    _mark_header_row(tbl)
    for i, htext in enumerate(headers):
        cell = tbl.rows[0].cells[i]
        _shade_cell(cell, COLOR_HEADER_FILL)
        _set_cell_borders(cell)
        _set_cell_margins(cell, top=80, bottom=80)
        _set_cell_valign_center(cell)
        _set_cell_text(cell, htext, bold=True, color=COLOR_WHITE, align=WD_ALIGN_PARAGRAPH.CENTER)

    for r_idx, row_data in enumerate(rows):
        fill = COLOR_WHITE if r_idx % 2 == 0 else COLOR_ALT_FILL
        row = tbl.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            _shade_cell(cell, fill)
            _set_cell_borders(cell)
            _set_cell_margins(cell, top=60, bottom=60)
            _set_cell_valign_center(cell)
            _set_cell_text(cell, str(val), bold=False, color=COLOR_BODY, align=None)
    return tbl

# ═══════════════════════════════════════════════════════════════════════════
# PORTADA
# ═══════════════════════════════════════════════════════════════════════════
cover_line('Manual de Despliegue', size=24, bold=True, color=COLOR_H1, before=72, after=10)
cover_line('Sistema de Información MultiParking', size=16, bold=True, color=COLOR_H2, after=6)
cover_line('Gestión Integral de Parqueaderos Privados', size=11, after=4)
spacer()
cover_line('Integrantes:', size=11, bold=True, after=4)
cover_line('Kevin Arley Grisales Ovalle', size=11, after=0)
cover_line('Kevin Santiago Pinto López', size=11, after=0)
spacer()
cover_line('Análisis y Desarrollo de Software – Ficha 3119175', size=11, after=0)
cover_line('Centro de Diseño y Metrología – SENA', size=11, after=0)
cover_line('Bogotá D.C. – 2026', size=11, after=0)
doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════
# 1. DEFINICIÓN DEL ENTORNO TÉCNICO
# ═══════════════════════════════════════════════════════════════════════════
h1('1. Definición del entorno técnico')
body(
    'Esta sección describe los componentes tecnológicos que conforman el sistema MultiParking '
    'desplegado en Render.com, y su equivalencia con el entorno de desarrollo local. A diferencia '
    'de proyectos que migran a un VPS propio, MultiParking opera de forma permanente sobre la '
    'infraestructura administrada de Render, por lo que este manual no contempla un entorno de '
    'servidor autogestionado.'
)

h2('1.1 Componentes del entorno de producción (Render.com)')
table(
    ['Componente', 'Descripción'],
    [
        ['Sistema Operativo', 'Gestionado por Render (contenedor Linux interno, no configurable directamente)'],
        ['Runtime', 'Python 3.12+ / Django 6.0'],
        ['Servidor de aplicación (WSGI)', 'Gunicorn (gunicorn multiparking.wsgi:application)'],
        ['Servidor web / proxy', 'Interno de Render (TLS terminado por Render, sin Nginx configurable por el equipo)'],
        ['Base de datos', 'PostgreSQL 16 (Render Managed Database), conexión vía DATABASE_URL (dj-database-url)'],
        ['Archivos estáticos', 'Whitenoise (CompressedManifestStaticFilesStorage), servidos por el propio proceso Django'],
        ['Frontend', 'Django Templates + Tailwind CSS (CDN), renderizado del lado del servidor'],
        ['Gestor de despliegue', 'Render (CI/CD automático desde GitHub, sin configuración de servidor)'],
        ['Repositorio', 'github.com/xeodeo/Multiparking-Django'],
        ['Dominio', 'multiparking-django.onrender.com (dominio gratuito de Render)'],
        ['SSL/HTTPS', 'Automático, gestionado por Render'],
        ['Correo transaccional', 'Resend (prioritario) o SendGrid HTTP API (fallback) — evita bloqueo de puertos SMTP salientes'],
        ['Costo mensual', 'Plan Free: $0 USD, con suspensión por inactividad; Plan Starter: desde ~$7 USD/mes para disponibilidad continua'],
    ],
)
body('Nota. Elaboración propia (2026), a partir de la configuración vigente en multiparking/settings.py y build.sh.')

h2('1.2 Entorno local (desarrollo) vs. producción (Render)')
table(
    ['Componente', 'Entorno local (desarrollo)', 'Producción (Render)'],
    [
        ['Base de datos', 'MySQL 8.0 (utf8mb4), vía DB_NAME/DB_USER/DB_PASSWORD/DB_HOST/DB_PORT en .env', 'PostgreSQL 16, vía DATABASE_URL inyectada por Render'],
        ['Servidor', 'python manage.py runserver', 'gunicorn multiparking.wsgi:application'],
        ['DEBUG', 'True (por defecto)', 'False — se desactiva automáticamente si existe la variable RENDER'],
        ['Archivos estáticos', 'Servidor de desarrollo de Django', 'Whitenoise con compresión y versionado de archivos'],
        ['Dominio', 'http://localhost:8000', 'https://multiparking-django.onrender.com'],
        ['Variables de entorno', 'Archivo .env (python-dotenv)', 'Panel de Render → pestaña Environment'],
        ['Datos de prueba', 'scripts/reiniciar_base_datos.py (datos demo completos)', 'scripts/render_datos_prueba.py (compatible con PostgreSQL)'],
    ],
)

# ═══════════════════════════════════════════════════════════════════════════
# 2. PROTOCOLO DE ACCESO Y DESPLIEGUE
# ═══════════════════════════════════════════════════════════════════════════
h1('2. Protocolo de acceso y despliegue')
body(
    'El despliegue de MultiParking en Render se realiza de forma automática al conectar el repositorio '
    'de GitHub con la plataforma. No se requiere acceso SSH, configuración de servidor ni gestión manual '
    'de contenedores.'
)

h2('2.1 Despliegue automático en Render')
table(
    ['Paso', 'Descripción'],
    [
        ['Paso 1', 'Ingresar al dashboard de Render (render.com) con la cuenta del proyecto.'],
        ['Paso 2', 'Verificar que el Web Service esté conectado al repositorio github.com/xeodeo/Multiparking-Django.'],
        ['Paso 3', 'Confirmar que el Build Command sea bash build.sh y el Start Command sea gunicorn multiparking.wsgi:application.'],
        ['Paso 4', 'Realizar git push origin main con los cambios ya probados localmente.'],
        ['Paso 5', 'Render detecta el push y ejecuta build.sh: instala dependencias, corre collectstatic, aplica migraciones y carga datos iniciales si aplica.'],
        ['Paso 6', 'Verificar en el dashboard de Render (pestañas Events y Logs) que el despliegue finalizó como "Live" sin errores.'],
        ['Paso 7', 'Acceder a https://multiparking-django.onrender.com y validar login, dashboard y flujo de entrada/salida de vehículos.'],
    ],
)

h2('2.2 Script de construcción (build.sh)')
body('Render ejecuta el siguiente script en cada despliegue:')
body('pip install -r requirements.txt')
body('python manage.py collectstatic --no-input')
body('python manage.py migrate')
body('python scripts/cargar_datos_iniciales.py')

h2('2.3 Variables de entorno en Render')
table(
    ['Variable', 'Descripción'],
    [
        ['SECRET_KEY', 'Clave secreta de Django (50+ caracteres aleatorios). Nunca reutilizar la de desarrollo.'],
        ['DATABASE_URL', 'Cadena de conexión PostgreSQL provista automáticamente por Render al vincular la base de datos managed.'],
        ['RENDER', 'Variable inyectada automáticamente por la plataforma; el sistema la usa para desactivar DEBUG en producción.'],
        ['RENDER_EXTERNAL_HOSTNAME', 'Inyectada automáticamente por Render; se agrega a ALLOWED_HOSTS sin configuración manual.'],
        ['SENDGRID_API_KEY', 'Clave de la API HTTP de SendGrid, usada como proveedor de correo si no hay RESEND_API_KEY.'],
        ['RESEND_API_KEY', 'Clave de Resend (django-anymail). Si está definida, tiene prioridad sobre SendGrid.'],
        ['EMAIL_FROM', 'Remitente por defecto de los correos transaccionales, ej. "Multiparking <no-reply@multiparking.com>".'],
        ['GMAIL_USER / GMAIL_APP_PASSWORD', 'Opcional. Uso principalmente en pruebas locales; en producción se recomienda Resend o SendGrid.'],
    ],
)
body('Nota. Ninguna variable de conexión a MySQL (DB_HOST, DB_USER, etc.) aplica en Render: la base de datos de producción se resuelve completamente a través de DATABASE_URL.')

h2('2.4 Estrategia de ramas y pruebas')
table(
    ['Componente', 'Descripción'],
    [
        ['Rama de producción', 'main — único punto de despliegue. Cada push a main dispara el redespliegue automático en Render.'],
        ['Rama de integración', 'No existe una rama develop remota; el rol de "integración" lo cumple el entorno local de cada desarrollador.'],
        ['Estrategia', 'Todo cambio se desarrolla y prueba primero en local (manage.py runserver + MySQL) antes de subir a main. El push a main equivale al "merge a develop → producción" del flujo tradicional: no hay ambiente intermedio en la nube.'],
        ['Checklist antes de push a main', '1) Migraciones generadas y aplicadas localmente sin errores. 2) Pruebas manuales del flujo afectado. 3) python manage.py check sin advertencias críticas. 4) Verificar que no se suban credenciales (.env) al repositorio.'],
    ],
)

# ═══════════════════════════════════════════════════════════════════════════
# 3. GESTIÓN DE LA BASE DE DATOS
# ═══════════════════════════════════════════════════════════════════════════
h1('3. Gestión de la base de datos')

h2('3.1 Inicialización de la base de datos')
table(
    ['Componente', 'Descripción'],
    [
        ['Entorno local', 'python manage.py makemigrations seguido de python manage.py migrate sobre MySQL.'],
        ['Entorno de producción (Render)', 'python manage.py migrate se ejecuta automáticamente dentro de build.sh contra la base PostgreSQL managed.'],
        ['Carga de datos iniciales', 'scripts/cargar_datos_iniciales.py se ejecuta al final de build.sh (roles, configuración de fidelidad, etc.).'],
        ['Usuario administrador', 'scripts/create_admin.py crea admin@multiparking.com / admin123 (cambiar la contraseña tras el primer acceso).'],
        ['Reinicio completo con datos demo', 'python scripts/reiniciar_base_datos.py (uso exclusivo en entorno local/MySQL).'],
        ['Datos de prueba compatibles con Render', 'python scripts/render_datos_prueba.py (PostgreSQL).'],
        ['Verificación', 'python manage.py dbshell, o cliente PostgreSQL (DBeaver, psql) usando la DATABASE_URL externa de Render.'],
    ],
)

h2('3.2 Limpieza de la base de datos respetando claves foráneas')
body(
    'En caso de necesitar limpiar la base de datos sin romper integridad referencial, se debe seguir el '
    'orden exacto implementado en scripts/reiniciar_base_datos.py, que elimina primero las tablas hijas '
    'y termina en las tablas padre:'
)
table(
    ['Orden', 'Tabla (modelo)'],
    [
        ['1', 'fidelidad_stickers (Sticker)'],
        ['2', 'novedades (Novedad)'],
        ['3', 'cupones_aplicados (CuponAplicado)'],
        ['4', 'cupones (Cupon)'],
        ['5', 'reservas (Reserva)'],
        ['6', 'pagos (Pago)'],
        ['7', 'inventario_parqueo (InventarioParqueo)'],
        ['8', 'espacios (Espacio)'],
        ['9', 'tarifas (Tarifa)'],
        ['10', 'tipos_espacio (TipoEspacio)'],
        ['11', 'pisos (Piso)'],
        ['12', 'vehiculos (Vehiculo)'],
        ['13', 'usuarios (Usuario)'],
        ['14', 'fidelidad_configuracion (ConfiguracionFidelidad)'],
    ],
)
body('Nota. En producción, esta limpieza solo debe ejecutarse con un backup verificado y, de ser posible, en horario de bajo tráfico.')

# ═══════════════════════════════════════════════════════════════════════════
# 4. PLAN DE CONTINGENCIA Y ROLLBACK
# ═══════════════════════════════════════════════════════════════════════════
h1('4. Plan de contingencia y rollback')

h2('4.1 Política de backup obligatorio')
body(
    'Antes de ejecutar cualquier migración destructiva (renombrar/eliminar campos, cambios de tipo) o '
    'cualquier limpieza masiva de datos en producción, es obligatorio generar un respaldo completo de '
    'la base de datos PostgreSQL de Render. No se debe ejecutar ningún despliegue con cambios de este '
    'tipo sin contar con un backup verificado.'
)

h2('4.2 Procedimiento de backup')
table(
    ['Componente', 'Descripción'],
    [
        ['Origen de la conexión', 'Copiar la "External Database URL" desde el panel de la base de datos en Render (Dashboard → Base de datos → Connections).'],
        ['Comando de backup', 'pg_dump "postgresql://usuario:password@host/db" > backup_$(date +%Y%m%d_%H%M%S).sql'],
        ['Almacenamiento', 'Guardar el archivo .sql localmente y adicionalmente en un almacenamiento externo (Google Drive u otro repositorio de respaldos).'],
        ['Frecuencia recomendada', 'Antes de cada despliegue con cambios de esquema, y de forma manual periódica (semanal) mientras no exista backup automático propio.'],
        ['Verificación del backup', 'Restaurar en una base local de prueba: psql -U postgres -d multiparking_test < backup.sql'],
        ['Tiempo estimado de backup', '1 a 3 minutos, dado el volumen de datos actual del proyecto.'],
    ],
)

h2('4.3 Plan de rollback — paso a paso')
body(
    'Render no expone una interfaz de contenedores como Dokploy, pero sí conserva el historial de '
    'despliegues previos. Si un despliegue falla o introduce errores críticos en producción:'
)
table(
    ['Paso', 'Descripción'],
    [
        ['Paso 1 — Detectar la falla', 'Revisar la pestaña Logs del servicio en Render inmediatamente después del despliegue.'],
        ['Paso 2 — Rollback rápido vía Render', 'En Render Dashboard → pestaña Deploys, seleccionar el despliegue estable anterior y usar la opción "Redeploy" sobre ese commit.'],
        ['Paso 3 — Revertir en GitHub (alternativa)', 'Si se requiere revertir también el historial: git revert HEAD (preferido) o, si es imprescindible, git reset --hard <commit_anterior> seguido de push a main.'],
        ['Paso 4 — Redespliegue', 'Render detecta el nuevo estado de main (o el redeploy manual) y publica la versión anterior automáticamente.'],
        ['Paso 5 — Restaurar base de datos si aplica', 'Si el despliegue fallido incluyó migraciones destructivas: psql "<DATABASE_URL>" < backup_anterior.sql'],
        ['Paso 6 — Verificación', 'Probar las funcionalidades críticas: login, registro de ingreso/salida, cálculo de tarifa, generación de pago y envío de correo.'],
        ['Paso 7 — Notificación', 'Informar a los interesados sobre el incidente, la causa raíz y el tiempo de recuperación.'],
    ],
)
body('Nota importante. git reset --hard reescribe el historial de la rama main; usarlo solo si el equipo está de acuerdo y nadie más tiene cambios pendientes basados en esos commits. git revert es la opción segura por defecto.')

h2('4.4 Tiempos estimados de rollback')
table(
    ['Escenario', 'Tiempo estimado'],
    [
        ['Redeploy de un despliegue anterior (sin cambios en BD)', '3 a 6 minutos (tiempo de build de Render)'],
        ['Revertir código en GitHub + redeploy', '5 a 10 minutos'],
        ['Restaurar base de datos (backup < 500 MB)', '5 a 10 minutos'],
        ['Rollback completo (código + base de datos)', '10 a 20 minutos'],
        ['Tiempo máximo de inactividad aceptable', '30 minutos'],
    ],
)

# ═══════════════════════════════════════════════════════════════════════════
# 5. VERIFICACIÓN Y PRUEBAS
# ═══════════════════════════════════════════════════════════════════════════
h1('5. Verificación y pruebas')

h2('5.1 Pruebas previas al despliegue (en local)')
table(
    ['Verificación', 'Descripción'],
    [
        ['Migraciones al día', 'python manage.py makemigrations --check --dry-run no debe reportar migraciones faltantes.'],
        ['Variables de entorno', 'Confirmar que .env local refleja las mismas claves que se configurarán en Render (sección 2.3), sin subir el archivo al repositorio.'],
        ['Prueba de flujo completo', 'Registrar ingreso y salida de un vehículo, verificar cálculo de tarifa, aplicación de cupón y generación de pago.'],
        ['Prueba de autenticación', 'Verificar login/logout para los tres roles: ADMIN, VIGILANTE y CLIENTE.'],
        ['Prueba de notificaciones', 'Confirmar envío de correo (recuperación de contraseña o novedad) usando /admin-panel/ → herramienta de prueba de correo.'],
        ['Revisión de checks de Django', 'python manage.py check --deploy antes de subir cambios de configuración de seguridad.'],
    ],
)

h2('5.2 Plan de revisión post-despliegue')
table(
    ['Componente', 'Descripción'],
    [
        ['Monitoreo de logs', 'Revisar los logs del servicio en Render durante las primeras 24 horas tras el despliegue.'],
        ['Disponibilidad', 'Configurar un monitor externo gratuito (ej. UptimeRobot) apuntando a https://multiparking-django.onrender.com para alertas de caída.'],
        ['Uso de la base de datos', 'Revisar en el panel de Render el consumo de almacenamiento y conexiones de la base PostgreSQL managed.'],
        ['Cold start (plan Free)', 'Verificar que el primer acceso tras inactividad (spin-down) cargue correctamente, ya que el plan gratuito suspende el servicio sin tráfico.'],
        ['Revisión semanal', 'Revisar el crecimiento de datos (vehículos, parqueos, pagos) y los correos fallidos en el proveedor de email.'],
    ],
)

h2('5.3 Checklist de despliegue exitoso')
table(
    ['Ítem', 'Detalle'],
    [
        ['Backup realizado (si hubo cambios de esquema)', 'Obligatorio antes de migraciones destructivas.'],
        ['Variables de entorno configuradas', 'Todas las de la sección 2.3 presentes en el panel de Render.'],
        ['Migraciones aplicadas', 'Sin errores en el paso python manage.py migrate del build.'],
        ['Sitio accesible vía HTTPS', 'https://multiparking-django.onrender.com carga correctamente.'],
        ['Login funcional', 'Los tres roles (ADMIN, VIGILANTE, CLIENTE) autentican correctamente.'],
        ['Flujo de ingreso/salida operativo', 'Se puede registrar un vehículo, calcular tarifa y generar el pago.'],
        ['Correo transaccional operativo', 'Prueba de envío exitosa (Resend o SendGrid).'],
        ['Logs sin errores críticos', 'Revisados en Render durante las primeras horas post-despliegue.'],
    ],
)

# ═══════════════════════════════════════════════════════════════════════════
# 6. REFERENCIAS
# ═══════════════════════════════════════════════════════════════════════════
h1('Referencias')
for ref in [
    'Django Software Foundation. (2024). Deploying Django. https://docs.djangoproject.com/en/6.0/howto/deployment/',
    'PostgreSQL Global Development Group. (2024). PostgreSQL 16 documentation. https://www.postgresql.org/docs/16/',
    'Render. (2024). Render documentation. https://render.com/docs',
    'SendGrid. (2024). SendGrid email API documentation. https://docs.sendgrid.com/',
    'Resend. (2024). Resend documentation. https://resend.com/docs',
    'WhiteNoise. (2024). WhiteNoise documentation. https://whitenoise.readthedocs.io/',
]:
    body(ref)

# ═══════════════════════════════════════════════════════════════════════════
# GUARDAR
# ═══════════════════════════════════════════════════════════════════════════
out_path = 'Manual_Despliegue_Multiparking.docx'
doc.save(out_path)
print(f'Guardado: {out_path}')
