# SECCIÓN 4 — Elicitación de Requisitos
# Documento: MultiParking — SENA ADSO · Ficha 3119175
# Norma: APA 7ma edición

---

## INSTRUCCIONES DE FORMATO

- Esta sección inicia en página nueva
- Título principal: "4. Elicitación de Requisitos" — negrita, centrado, 12pt Times New Roman
- Subtítulos (4.1, 4.2, etc.): negrita, alineado izquierda, 12pt
- Las tablas estadísticas de la encuesta llevan título APA 7 ANTES:
  - Línea 1: **Tabla N** (negrita)
  - Línea 2: *Descripción de la tabla* (cursiva)
  - Después: *Nota.* Elaboración propia (2026).
- Las figuras (gráficas) llevan leyenda APA 7 DEBAJO de la imagen, NUNCA centrada:
  - Línea 1: **Figura N** — negrita, alineada al margen izquierdo, sin sangría
  - Línea 2: *Descripción en cursiva, alineada al margen izquierdo, sin sangría*
  - Línea 3: *Nota.* Elaboración propia (2026). — "Nota." en cursiva, resto normal, flush left, sin sangría
  - IMPORTANTE: La IMAGEN se centra; la LEYENDA (etiqueta + título + nota) va flush left, sin sangría de primera línea
- Tablas en 10pt para que quepan en la página
- Encabezados de tabla en negrita
- Párrafos del cuerpo con sangría de primera línea 1.27 cm — esta sangría NO aplica a leyendas de figura ni a notas de tabla
- Doble espacio en todo

---

## INSTRUCCIONES PARA GENERACIÓN DE GRÁFICAS (Claude Desktop)

Cada marca `[GRÁFICA N]` indica que debes generar una imagen con matplotlib y embeberla en el documento Word con `doc.add_picture()`. Plantilla base:

```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

def crear_grafica_barras_v(categorias, valores, titulo, nombre_archivo):
    fig, ax = plt.subplots(figsize=(6, 3.5))
    bars = ax.bar(categorias, valores, color='#2E6DA4', edgecolor='white')
    ax.set_ylabel('Frecuencia Absoluta')
    ax.set_ylim(0, max(valores) + 2)
    ax.set_title(titulo, fontsize=10, pad=8)
    for bar, val in zip(bars, valores):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                str(val), ha='center', va='bottom', fontsize=9)
    plt.xticks(fontsize=8, wrap=True)
    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150)
    buf.seek(0)
    plt.close(fig)
    return buf

def crear_grafica_barras_h(categorias, valores, titulo):
    fig, ax = plt.subplots(figsize=(6, 3.5))
    bars = ax.barh(categorias, valores, color='#2E6DA4', edgecolor='white')
    ax.set_xlabel('Frecuencia Absoluta')
    ax.set_xlim(0, max(valores) + 2)
    ax.set_title(titulo, fontsize=10, pad=8)
    for bar, val in zip(bars, valores):
        ax.text(val + 0.05, bar.get_y() + bar.get_height()/2,
                str(val), ha='left', va='center', fontsize=9)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150)
    buf.seek(0)
    plt.close(fig)
    return buf
```

Para insertar en el documento: `doc.add_picture(buf, width=Inches(5.5))`
Luego agregar el párrafo de título de figura en negrita + cursiva según APA 7.

---

## 4.1 — IDENTIFICACIÓN DE PROCESOS

**Título:** 4.1. Identificación de procesos

Los procesos principales identificados en los parqueaderos privados de la localidad de Suba, barrio Compartir, durante la fase de observación y recolección de datos son los siguientes:

- Registro de ingreso de vehículo con asignación automática de espacio disponible.
- Cálculo de tiempo de permanencia y tarifa al momento de la salida del vehículo.
- Gestión de pagos y aplicación de descuentos mediante cupones.
- Reserva anticipada de espacios por parte de clientes registrados.
- Registro de novedades operativas con notificación al usuario afectado.
- Generación de reportes de ingresos, ocupación y actividad del parqueadero.

---

## 4.2 — RECOLECCIÓN DE LA INFORMACIÓN DEL SOFTWARE A CONSTRUIR

**Título:** 4.2. Recolección de la información del software a construir

Para iniciar el desarrollo del sistema MultiParking se realizó una fase de recolección de datos con el objetivo de comprender las necesidades reales de propietarios, vigilantes y usuarios. La información se obtuvo a través de dos técnicas principales: observación directa en parqueaderos privados de la localidad de Suba, barrio Compartir, en la ciudad de Bogotá D.C., y encuestas digitales dirigidas a usuarios habituales y administradores del sector.

---

## 4.3 — ELECCIÓN DE LA TÉCNICA DE RECOLECCIÓN DE LA INFORMACIÓN

**Título:** 4.3. Elección de la técnica de recolección de la información

	Para el proyecto se optó por utilizar las siguientes técnicas de recolección de información:

	**Encuesta digital:** Aplicada a 13 usuarios y administradores de parqueaderos de la localidad de Suba, con 13 preguntas de selección múltiple sobre su experiencia actual y sus expectativas frente a un sistema tecnológico. La encuesta digital permite obtener datos cuantificables de forma rápida y sistemática, facilitando el análisis estadístico de frecuencias absolutas y relativas.

	**Observación directa:** Empleada para registrar de forma sistemática el comportamiento de los procesos operativos en parqueaderos de pequeño y mediano tamaño en días de alta y baja afluencia. Esta técnica complementó los datos de la encuesta al permitir verificar en campo las problemáticas declaradas por los participantes.

---

## 4.4 — APLICACIÓN DE LA TÉCNICA DE RECOLECCIÓN DE INFORMACIÓN

**Título:** 4.4. Aplicación de la técnica de recolección de información

	La encuesta se aplicó de forma digital a través de un formulario en línea distribuido entre usuarios habituales y personal operativo de parqueaderos privados de la localidad de Suba, barrio Compartir. La observación directa se efectuó en los mismos establecimientos en días representativos de alta y baja afluencia vehicular, registrando los procedimientos de ingreso y salida, los tiempos de espera, las modalidades de cobro y las incidencias más frecuentes.

---

## 4.5 — ORGANIZACIÓN DE LA INFORMACIÓN RECOLECTADA

**Título:** 4.5. Organización de la información recolectada

### 4.5.1 Encuesta

	A continuación se presenta el análisis estadístico de la información recolectada en la encuesta aplicada (n = 13):

¿Con qué frecuencia utilizas parqueaderos públicos o privados?

**Tabla 2**
*Frecuencia de uso de parqueaderos*

| Variable | Frecuencia Absoluta | FA Acumulada | Frecuencia Relativa | FR Acumulada |
|---|---|---|---|---|
| Todos los días | 4 | 4 | 0,308 | 0,308 |
| Varias veces a la semana | 3 | 7 | 0,231 | 0,539 |
| Ocasionalmente | 3 | 10 | 0,231 | 0,770 |
| Casi nunca | 3 | 13 | 0,231 | 1,000 |
| **Muestra** | **13** | | | |

*Nota.* Elaboración propia (2026).

[⚙ CREAR FIGURA 2]

**Figura 2**
*Frecuencia de uso de parqueaderos (n = 13)*
*Nota.* Elaboración propia (2026).

¿Qué medio usas actualmente para pagar en un parqueadero?

**Tabla 3**
*Medio de pago actual en parqueaderos*

| Variable | Frecuencia Absoluta | FA Acumulada | Frecuencia Relativa | FR Acumulada |
|---|---|---|---|---|
| Efectivo | 11 | 11 | 0,846 | 0,846 |
| Tarjeta débito/crédito | 1 | 12 | 0,077 | 0,923 |
| App o sistema digital | 1 | 13 | 0,077 | 1,000 |
| **Muestra** | **13** | | | |

*Nota.* Elaboración propia (2026).

[⚙ CREAR FIGURA 3]

**Figura 3**
*Medio de pago actual en parqueaderos (n = 13)*
*Nota.* Elaboración propia (2026).

¿Cuál es el aspecto que más te molesta al usar un parqueadero?

**Tabla 4**
*Aspecto más molesto al usar un parqueadero*

| Variable | Frecuencia Absoluta | FA Acumulada | Frecuencia Relativa | FR Acumulada |
|---|---|---|---|---|
| Pago solo en efectivo | 4 | 4 | 0,308 | 0,308 |
| Largos tiempos de espera | 2 | 6 | 0,154 | 0,462 |
| Tarifas poco claras | 2 | 8 | 0,154 | 0,615 |
| Filas para entrar o salir | 2 | 10 | 0,154 | 0,769 |
| Falta de espacios disponibles | 2 | 12 | 0,154 | 0,923 |
| Pérdida de tiquetes | 1 | 13 | 0,077 | 1,000 |
| **Muestra** | **13** | | | |

*Nota.* Elaboración propia (2026).

[⚙ CREAR FIGURA 4]

**Figura 4**
*Aspecto más molesto al usar un parqueadero (n = 13)*
*Nota.* Elaboración propia (2026).

¿Te gustaría poder ingresar al parqueadero escaneando un código QR?

**Tabla 5**
*Disposición para ingresar con código QR*

| Variable | Frecuencia Absoluta | FA Acumulada | Frecuencia Relativa | FR Acumulada |
|---|---|---|---|---|
| Sí | 5 | 5 | 0,385 | 0,385 |
| Tal vez | 8 | 13 | 0,615 | 1,000 |
| No | 0 | 13 | 0,000 | 1,000 |
| **Muestra** | **13** | | | |

*Nota.* Elaboración propia (2026).

[⚙ CREAR FIGURA 5]

**Figura 5**
*Disposición para ingreso con código QR (n = 13)*
*Nota.* Elaboración propia (2026).

¿Te parecería útil poder ver el tiempo y costo acumulado en tiempo real?

**Tabla 6**
*Utilidad de visualizar tiempo y costo en tiempo real*

| Variable | Frecuencia Absoluta | FA Acumulada | Frecuencia Relativa | FR Acumulada |
|---|---|---|---|---|
| Sí, muy útil | 12 | 12 | 0,923 | 0,923 |
| Me es indiferente | 0 | 12 | 0,000 | 0,923 |
| No lo necesito | 1 | 13 | 0,077 | 1,000 |
| **Muestra** | **13** | | | |

*Nota.* Elaboración propia (2026).

[⚙ CREAR FIGURA 6]

**Figura 6**
*Utilidad de visualizar costo en tiempo real (n = 13)*
*Nota.* Elaboración propia (2026).

¿Usarías una app para reservar espacio de parqueo antes de llegar?

**Tabla 7**
*Disposición para reservar espacio de parqueo anticipadamente*

| Variable | Frecuencia Absoluta | FA Acumulada | Frecuencia Relativa | FR Acumulada |
|---|---|---|---|---|
| Sí | 8 | 8 | 0,615 | 0,615 |
| Tal vez | 4 | 12 | 0,308 | 0,923 |
| No | 1 | 13 | 0,077 | 1,000 |
| **Muestra** | **13** | | | |

*Nota.* Elaboración propia (2026).

[⚙ CREAR FIGURA 7]

**Figura 7**
*Disposición para reserva anticipada de espacio (n = 13)*
*Nota.* Elaboración propia (2026).

¿Cuál sería tu método de pago preferido para este sistema?

**Tabla 8**
*Método de pago de preferencia para un sistema digital*

| Variable | Frecuencia Absoluta | FA Acumulada | Frecuencia Relativa | FR Acumulada |
|---|---|---|---|---|
| Transferencia digital / billetera | 4 | 4 | 0,308 | 0,308 |
| Tarjeta débito/crédito | 4 | 8 | 0,308 | 0,615 |
| Efectivo | 3 | 11 | 0,231 | 0,846 |
| Pago por código QR | 2 | 13 | 0,154 | 1,000 |
| **Muestra** | **13** | | | |

*Nota.* Elaboración propia (2026).

[⚙ CREAR FIGURA 8]

**Figura 8**
*Método de pago de preferencia para el sistema (n = 13)*
*Nota.* Elaboración propia (2026).

¿Qué tanto te gustaría que el parqueadero reconociera tu historial para darte descuentos?

**Tabla 9**
*Interés en que el parqueadero reconozca el historial del usuario para descuentos*

| Variable | Frecuencia Absoluta | FA Acumulada | Frecuencia Relativa | FR Acumulada |
|---|---|---|---|---|
| Me gustaría mucho | 6 | 6 | 0,462 | 0,462 |
| Es algo interesante | 5 | 11 | 0,385 | 0,847 |
| No me interesa | 2 | 13 | 0,154 | 1,000 |
| **Muestra** | **13** | | | |

*Nota.* Elaboración propia (2026).

[⚙ CREAR FIGURA 9]

**Figura 9**
*Interés en fidelización por historial de uso (n = 13)*
*Nota.* Elaboración propia (2026).

¿Consideras importante salir del parqueadero rápidamente sin interactuar con personal?

**Tabla 10**
*Importancia de salir del parqueadero sin interactuar con personal*

| Variable | Frecuencia Absoluta | FA Acumulada | Frecuencia Relativa | FR Acumulada |
|---|---|---|---|---|
| Moderadamente importante | 6 | 6 | 0,462 | 0,462 |
| Muy importante | 5 | 11 | 0,385 | 0,847 |
| No es importante | 2 | 13 | 0,154 | 1,000 |
| **Muestra** | **13** | | | |

*Nota.* Elaboración propia (2026).

[⚙ CREAR FIGURA 10]

**Figura 10**
*Importancia de la salida autónoma del parqueadero (n = 13)*
*Nota.* Elaboración propia (2026).

¿Qué tan dispuesto estarías a usar un sistema de parqueadero completamente automatizado?

**Tabla 11**
*Disposición para usar un sistema de parqueadero completamente automatizado*

| Variable | Frecuencia Absoluta | FA Acumulada | Frecuencia Relativa | FR Acumulada |
|---|---|---|---|---|
| Muy dispuesto | 7 | 7 | 0,538 | 0,538 |
| Algo dispuesto | 6 | 13 | 0,462 | 1,000 |
| No dispuesto | 0 | 13 | 0,000 | 1,000 |
| **Muestra** | **13** | | | |

*Nota.* Elaboración propia (2026).

[⚙ CREAR FIGURA 11]

**Figura 11**
*Disposición para usar sistema automatizado (n = 13)*
*Nota.* Elaboración propia (2026).

¿Estarías dispuesto/a a pagar un poco más por un parqueadero automatizado?

**Tabla 12**
*Disposición para pagar más por un parqueadero automatizado*

| Variable | Frecuencia Absoluta | FA Acumulada | Frecuencia Relativa | FR Acumulada |
|---|---|---|---|---|
| Solo si el precio es igual al tradicional | 7 | 7 | 0,538 | 0,538 |
| Sí | 6 | 13 | 0,462 | 1,000 |
| No | 0 | 13 | 0,000 | 1,000 |
| **Muestra** | **13** | | | |

*Nota.* Elaboración propia (2026).

[⚙ CREAR FIGURA 12]

**Figura 12**
*Disposición de pago por sistema automatizado (n = 13)*
*Nota.* Elaboración propia (2026).

¿Qué funcionalidad te gustaría que tuviera un parqueadero automatizado?

**Tabla 13**
*Funcionalidades deseadas en un parqueadero automatizado*

| Variable | Frecuencia Absoluta | FA Acumulada | Frecuencia Relativa | FR Acumulada |
|---|---|---|---|---|
| Poder reservar | 3 | 3 | 0,231 | 0,231 |
| Pagar al ingresar, no al salir | 2 | 5 | 0,154 | 0,385 |
| Garantizar seguridad del vehículo | 3 | 8 | 0,231 | 0,615 |
| Notificación del vencimiento del parqueo | 3 | 11 | 0,231 | 0,846 |
| Parqueadero más amplio | 2 | 13 | 0,154 | 1,000 |
| **Muestra** | **13** | | | |

*Nota.* Elaboración propia (2026).

[⚙ CREAR FIGURA 13]

**Figura 13**
*Funcionalidades deseadas en parqueadero automatizado (n = 13)*
*Nota.* Elaboración propia (2026).



### 4.5.2 Observación directa

	Se llevaron a cabo observaciones directas en parqueaderos privados de tamaño pequeño y mediano ubicados en la localidad de Suba, barrio Compartir, en días con alta y baja afluencia vehicular. Se registraron los procedimientos de entrada y salida de vehículos, la asignación de espacios, los tiempos de espera, las formas de cobro y las incidencias más frecuentes. Los hallazgos confirmaron de manera directa las problemáticas reportadas en la encuesta: control manual mediante planillas físicas, ausencia de visibilidad del estado de espacios en tiempo real, cobros imprecisos por cálculos manuales y largos tiempos de atención en horas de alta demanda. Estos resultados sustentan la necesidad de digitalizar el control de acceso, el cobro y la comunicación con los usuarios (Elaboración propia, 2026).

---

## 4.6 — INFORME DE LA RECOLECCIÓN DE DATOS

**Título:** 4.6. Informe de la recolección de datos

	Los resultados de la encuesta y la observación directa realizada en los parqueaderos de la localidad de Suba, barrio Compartir, evidencian de manera contundente la necesidad de una solución tecnológica. El 84,6 % de los encuestados señaló que el efectivo es el único medio de pago aceptado; el 92,3 % consideró muy útil poder ver el tiempo de permanencia y el costo acumulado en tiempo real; el 100 % se mostró abierto al uso de tecnología QR para el ingreso; y el 61,5 % usaría un sistema de reserva anticipada. Adicionalmente, el 100 % de los participantes declaró estar dispuesto a usar un sistema automatizado (53,8 % muy dispuesto; 46,2 % algo dispuesto), y ninguno se mostró en contra de la automatización.

	Estos hallazgos confirman la viabilidad y pertinencia del sistema MultiParking como respuesta tecnológica a las necesidades identificadas. Los módulos de reservas, fidelización, visualización de tarifas en tiempo real, pagos digitales y notificaciones automáticas responden directamente a las preferencias expresadas por los usuarios encuestados. La observación directa verificó en campo que las problemáticas declaradas son reales y persistentes en el entorno del parqueadero de referencia (Elaboración propia, 2026).

---

## NOTA PARA CLAUDE DESKTOP

### Tablas estadísticas
- Tablas 2–13: 5 columnas (Variable | Frecuencia Absoluta | FA Acumulada | Frecuencia Relativa | FR Acumulada)
- Valores de FR con coma decimal (0,308 — norma colombiana)
- Tablas en 10pt; texto del cuerpo en 12pt
- Encabezados de tabla en negrita

Código APA 7 para título de tabla (va ANTES de la tabla, flush left, sin sangría):
```python
# Línea 1: "Tabla N" — negrita, flush left, sin sangría, 12pt
p_tnum = doc.add_paragraph()
p_tnum.alignment = WD_ALIGN_PARAGRAPH.LEFT
p_tnum.paragraph_format.first_line_indent = 0
p_tnum.paragraph_format.space_after = Pt(0)
run_tnum = p_tnum.add_run(f'Tabla {n}')
run_tnum.bold = True
run_tnum.font.size = Pt(12)

# Línea 2: título en cursiva — flush left, sin sangría, 12pt
p_ttit = doc.add_paragraph()
p_ttit.alignment = WD_ALIGN_PARAGRAPH.LEFT
p_ttit.paragraph_format.first_line_indent = 0
p_ttit.paragraph_format.space_after = Pt(3)
run_ttit = p_ttit.add_run('Descripción de la tabla')
run_ttit.italic = True
run_ttit.font.size = Pt(12)
```

Código APA 7 para *Nota.* de tabla (va DESPUÉS de la tabla, flush left, sin sangría):
```python
p_tnota = doc.add_paragraph()
p_tnota.alignment = WD_ALIGN_PARAGRAPH.LEFT
p_tnota.paragraph_format.first_line_indent = 0
p_tnota.paragraph_format.space_before = Pt(3)
run_nl = p_tnota.add_run('Nota. ')
run_nl.italic = True
run_nl.font.size = Pt(10)
run_nr = p_tnota.add_run('Elaboración propia (2026).')
run_nr.font.size = Pt(10)
```

### Generación de gráficas con matplotlib
Cada marcador `[⚙ CREAR FIGURA N]` en el documento indica que debes generar una imagen y embeberla en ese punto. Parámetros por figura:

| Figura | Tipo | Categorías | Valores |
|---|---|---|---|
| 2 | barras_v | "Todos los días", "Varias veces a la semana", "Ocasionalmente", "Casi nunca" | 4, 3, 3, 3 |
| 3 | barras_v | "Efectivo", "Tarjeta débito/crédito", "App o sistema digital" | 11, 1, 1 |
| 4 | barras_h | "Pérdida de tiquetes", "Falta de espacios", "Filas entrar/salir", "Tarifas poco claras", "Tiempos de espera", "Pago solo efectivo" | 1, 2, 2, 2, 2, 4 |
| 5 | barras_v | "Sí", "Tal vez", "No" | 5, 8, 0 |
| 6 | barras_v | "Sí, muy útil", "Me es indiferente", "No lo necesito" | 12, 0, 1 |
| 7 | barras_v | "Sí", "Tal vez", "No" | 8, 4, 1 |
| 8 | barras_h | "Pago por código QR", "Efectivo", "Tarjeta débito/crédito", "Transferencia/billetera" | 2, 3, 4, 4 |
| 9 | barras_v | "Me gustaría mucho", "Es algo interesante", "No me interesa" | 6, 5, 2 |
| 10 | barras_v | "Moderadamente importante", "Muy importante", "No es importante" | 6, 5, 2 |
| 11 | barras_v | "Muy dispuesto", "Algo dispuesto", "No dispuesto" | 7, 6, 0 |
| 12 | barras_v | "Solo si precio igual", "Sí", "No" | 7, 6, 0 |
| 13 | barras_h | "Parqueadero más amplio", "Pagar al ingresar", "Garantizar seguridad", "Poder reservar", "Notif. vencimiento" | 2, 2, 3, 3, 3 |

El marcador `[⚙ CREAR FIGURA N]` NO debe aparecer en el documento Word — es solo una instrucción interna. Reemplazarlo por la imagen generada.

Pasos para cada gráfica:
1. Llamar la función correspondiente con los datos del marcador
2. Obtener el buffer PNG
3. Insertar la imagen centrada: `p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; run = p.add_run(); run.add_picture(buf, width=Inches(5.5))`
4. Agregar párrafo para **Figura N**: alineación IZQUIERDA (WD_ALIGN_PARAGRAPH.LEFT), sin sangría de primera línea (paragraph_format.first_line_indent = 0), texto en negrita, 10pt
5. Agregar párrafo para el título en cursiva: misma alineación IZQUIERDA, sin sangría, texto en cursiva, 10pt
6. Agregar párrafo para la nota: alineación IZQUIERDA, sin sangría, "Nota." en cursiva seguido del resto en normal, 10pt

Ejemplo de código para la leyenda:
```python
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Inches
from docx.oxml.ns import qn
import docx.oxml as oxml

# Párrafo Figura N
p_num = doc.add_paragraph()
p_num.alignment = WD_ALIGN_PARAGRAPH.LEFT
p_num.paragraph_format.first_line_indent = 0
p_num.paragraph_format.space_before = Pt(0)
run_num = p_num.add_run(f'Figura {n}')
run_num.bold = True
run_num.font.size = Pt(10)

# Párrafo título
p_tit = doc.add_paragraph()
p_tit.alignment = WD_ALIGN_PARAGRAPH.LEFT
p_tit.paragraph_format.first_line_indent = 0
run_tit = p_tit.add_run(titulo_figura)
run_tit.italic = True
run_tit.font.size = Pt(10)

# Párrafo Nota
p_nota = doc.add_paragraph()
p_nota.alignment = WD_ALIGN_PARAGRAPH.LEFT
p_nota.paragraph_format.first_line_indent = 0
run_nota_label = p_nota.add_run('Nota. ')
run_nota_label.italic = True
run_nota_label.font.size = Pt(10)
run_nota_resto = p_nota.add_run('Elaboración propia (2026).')
run_nota_resto.font.size = Pt(10)
```

### Color de las barras
- Color principal: `#2E6DA4` (azul institucional)
- Sin gradientes, sin 3D

### Numeración continua del documento
- Figura 1 = árbol del problema (sección 1.2)
- Tabla 1 = matriz de riesgos (sección 3)
- Esta sección: Tablas 2–13 y Figuras 2–13

### Estructura de subsecciones
- 4.5.1 y 4.5.2 son sub-etiquetas en negrita, alineadas a la izquierda
- No hay página nueva entre 4.5.1 y 4.5.2 — continúa en el mismo flujo
- La sección 5 sí inicia en página nueva
