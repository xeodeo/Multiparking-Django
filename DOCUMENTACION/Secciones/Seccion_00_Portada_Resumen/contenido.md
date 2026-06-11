# SECCIÓN 0 — Portada, Resumen/Abstract e Introducción
# Documento: Sistema de Información Web para la Gestión Integral de Parqueaderos Privados — MultiParking
# Programa: Análisis y Desarrollo de Software (ADSO) — SENA
# Norma de citación: APA 7ma edición

---

## INSTRUCCIONES DE FORMATO (para Claude Desktop al crear el Word)

- Fuente: Times New Roman 12pt para todo el cuerpo
- Interlineado: 2.0 (doble espacio) en todo el documento
- Márgenes: 2.54 cm (1 pulgada) en todos los lados
- Sangría de primera línea: 1.27 cm en cada párrafo del cuerpo
- Títulos de sección: Times New Roman 12pt, negrita, centrado, sin subrayar
- Subtítulos: Times New Roman 12pt, negrita, alineado a la izquierda
- Numeración de páginas: parte inferior derecha, en números arábigos desde la página de resumen
- La portada NO lleva número de página
- Todas las tablas y figuras deben llevar título en formato APA 7 (Tabla 1 / Figura 1 en negrita, descripción en cursiva en línea siguiente)

---

## 0.0 — PORTADA

```
[CENTRADO, SIN NÚMERO DE PÁGINA]

Sistema de Información Web para la Gestión Integral de Parqueaderos Privados

MultiParking




Integrantes:
Kevin Arley Grisales Ovalle
Kevin Santiago Pinto López




Análisis y Desarrollo de Software
Ficha: 3119175




Centro de Diseño y Metrología – SENA
Bogotá D.C., 2026
```

---

## 0.05 — ÍNDICE / TABLA DE CONTENIDO

**Título de sección:** Tabla de Contenido
*(Centrado, negrita, 12pt Times New Roman — página nueva después de la portada)*

**[INSTRUCCIÓN CLAUDE DESKTOP — ÍNDICE]**

Insertar aquí una Tabla de Contenido generada con el campo TOC de Word. Usar el siguiente código python-docx:

```python
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Título del índice
p_titulo = doc.add_paragraph()
p_titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_titulo.paragraph_format.first_line_indent = 0
run_tit = p_titulo.add_run('Tabla de Contenido')
run_tit.bold = True
run_tit.font.size = Pt(12)

doc.add_paragraph()  # espacio

# Campo TOC automático (Word lo actualiza con Ctrl+A → F9)
paragraph = doc.add_paragraph()
paragraph.paragraph_format.first_line_indent = 0
run = paragraph.add_run()
fldChar_begin = OxmlElement('w:fldChar')
fldChar_begin.set(qn('w:fldCharType'), 'begin')
run._r.append(fldChar_begin)
instrText = OxmlElement('w:instrText')
instrText.set(qn('xml:space'), 'preserve')
instrText.text = 'TOC \\o "1-3" \\h \\z \\u'
run._r.append(instrText)
fldChar_sep = OxmlElement('w:fldChar')
fldChar_sep.set(qn('w:fldCharType'), 'separate')
run._r.append(fldChar_sep)
fldChar_end = OxmlElement('w:fldChar')
fldChar_end.set(qn('w:fldCharType'), 'end')
run._r.append(fldChar_end)
```

**IMPORTANTE para evitar doble numeración:**
- Los estilos de encabezado en Word NO deben tener autonumeración de lista activada
- El número de sección (ej: "4.1") ya está incluido en el TEXTO del heading — NO usar Heading con lista numerada
- Usar estilo "Heading 1", "Heading 2", "Heading 3" sin modificar numeración automática
- En python-docx: `doc.add_heading('4.1. Identificación de procesos', level=2)` — el número va dentro del texto, no como propiedad del estilo
- Si el TOC muestra números dobles al abrirlo en Word, ir a Referencias → Tabla de contenido → Actualizar tabla → "Actualizar toda la tabla"

**Estilo del índice (APA 7 + SENA):**
- Título "Tabla de Contenido": centrado, negrita, 12pt
- Entradas del TOC: Times New Roman 12pt, alineación izquierda
- Número de página: derecha, separado por puntos (......... 5)
- Sin sangría para nivel 1 (secciones principales: 1, 2, 3...)
- Sangría 0.5 cm para nivel 2 (subsecciones: 1.1, 1.2...)
- Sangría 1.0 cm para nivel 3 (subsubsecciones: 1.1.1)
- Sin negrita en las entradas del TOC

---

## 0.1 — RESUMEN

**Título de sección:** Resumen
*(Centrado, negrita, sin cursiva, 12pt Times New Roman)*

MultiParking es un sistema de información web orientado a la automatización y gestión integral de parqueaderos privados de pequeña y mediana escala. La plataforma permite el registro de usuarios con tres roles diferenciados: administrador, vigilante y cliente; el control de vehículos propios y visitantes; la asignación y liberación de espacios en tiempo real sobre un plano interactivo por pisos; el cálculo automático de tarifas por minuto con redondeo a cien pesos colombianos; la generación y registro de pagos; la aplicación de cupones de descuento por porcentaje o valor fijo; la gestión de reservas anticipadas; el registro fotográfico de novedades operativas con notificación automática por correo electrónico; un sistema de fidelización mediante stickers acumulables canjeables por bonos de descuento; y la generación de reportes exportables en formato PDF y Excel. El sistema fue desarrollado en Python con el framework Django, empleando PostgreSQL como gestor de base de datos en el entorno de producción desplegado en Render.com, Tailwind CSS para el diseño responsivo, SendGrid para el envío de correos transaccionales y Gunicorn como servidor WSGI. La arquitectura sigue el patrón MVT (Modelo-Vista-Template) con autenticación por sesión propia y control de acceso basado en roles.

**Palabras clave:** parqueadero, sistema de información web, Django, PostgreSQL, gestión de espacios, fidelización, roles de usuario.

---

## 0.2 — ABSTRACT

**Título de sección:** Abstract
*(Centrado, negrita, sin cursiva, 12pt Times New Roman)*

MultiParking is a web-based information system designed for the comprehensive automation and management of small and medium-scale private parking lots. The platform supports user registration across three differentiated roles—administrator, security guard, and client—along with real-time parking space assignment and release on an interactive floor map, minute-based automatic fare calculation rounded to the nearest one hundred Colombian pesos, payment generation, percentage and fixed-value discount coupons, advance reservation management, photographic incident logging with automated email notifications, a loyalty sticker accumulation program redeemable for discount vouchers, and exportable reports in PDF and Excel formats. The system was built with Python and the Django framework, using PostgreSQL as the production database hosted on Render.com, Tailwind CSS for responsive design, SendGrid for transactional email delivery, and Gunicorn as the WSGI server. The architecture follows the MVT (Model-View-Template) pattern with custom session-based authentication and role-based access control.

**Keywords:** parking lot, web information system, Django, PostgreSQL, space management, loyalty program, role-based access.

---

## 0.3 — INTRODUCCIÓN

**Título de sección:** Introducción
*(Centrado, negrita, sin cursiva, 12pt Times New Roman)*

En la ciudad de Bogotá D.C., específicamente en la localidad de Suba, barrio Compartir, los parqueaderos privados de pequeña y mediana escala operan con métodos manuales que generan ineficiencias operativas: registros en papel, cálculos de tarifa imprecisos, ausencia de trazabilidad y nula visibilidad del estado de los espacios en tiempo real. Esta situación, observable también en numerosos establecimientos similares a nivel nacional, deriva en pérdida de ingresos, inconformidad de los usuarios y dificultad para tomar decisiones basadas en datos (García & Martínez, 2022).

	El proyecto MultiParking desarrolla una solución web que automatiza de forma integral la operación de parqueaderos privados. El sistema registra ingresos y salidas de vehículos, calcula tarifas en tiempo real, gestiona reservas anticipadas, emite notificaciones digitales, aplica descuentos mediante cupones y acumula beneficios de fidelización para los usuarios registrados.

	La arquitectura tecnológica se apoya en Django (Python 3.12), PostgreSQL en producción (Render.com), Tailwind CSS vía CDN, Chart.js para visualizaciones estadísticas, SendGrid como proveedor de correo transaccional y Gunicorn como servidor WSGI. La autenticación implementa un modelo de sesión propio —sin dependencia del módulo django.contrib.auth.User— con tres roles de acceso: ADMIN, VIGILANTE y CLIENTE, cada uno con vistas y permisos diferenciados.

	El presente documento sigue la estructura definida por el programa Análisis y Desarrollo de Software (ADSO) del Servicio Nacional de Aprendizaje (SENA) para el Trabajo Final del Proyecto Formativo (TFPF), y las normas de presentación y citación APA séptima edición (American Psychological Association, 2020).

---

## NOTAS PARA CLAUDE DESKTOP

1. La portada va en página 1 (sin número visible).
2. El Resumen inicia en página 2 con numeración visible desde aquí.
3. Cada sección nueva inicia en página nueva (salto de página obligatorio antes de cada título de sección principal).
4. Los párrafos del cuerpo llevan sangría de primera línea de 1.27 cm — en el .md están marcados con TAB al inicio.
5. No hay líneas en blanco entre párrafos — el doble espacio ya da la separación visual.
6. Las palabras clave van en párrafo separado con la etiqueta **Palabras clave:** en cursiva seguida de los términos en minúscula separados por coma.
7. El título del documento ("Sistema de Información Web...") va en negrita centrado en la portada.
8. "MultiParking" como subtítulo de la portada va en negrita, tamaño 14pt, centrado.
