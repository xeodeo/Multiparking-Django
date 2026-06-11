const {
  Document, Packer, Paragraph, TextRun, ImageRun,
  AlignmentType, PageNumber, Footer, LevelFormat,
  Table, TableRow, TableCell, WidthType, BorderStyle,
  ShadingType, VerticalAlign
} = require('docx');
const fs = require('fs');
const path = require('path');

const FONT   = "Times New Roman";
const PT12   = 24;
const PT10   = 20;
const DOUBLE = 480;
const SINGLE = 240;
const MARGIN = 1440;
const INDENT = 720;

const CHARTS = path.join(
  __dirname,
  "Secciones", "Seccion_04_Elicitacion_Requisitos", "charts"
);

// Columnas tablas estadísticas
const WS = [3500, 1465, 1465, 1465, 1465];

const pageFooter = new Footer({
  children: [new Paragraph({
    children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: PT12 })],
    alignment: AlignmentType.RIGHT,
    spacing: { before: 0, after: 0 },
  })],
});

// ── Helpers párrafos ───────────────────────────────────────────────────────

function h1(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12, bold: true })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.CENTER,
  });
}

function h2(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12, bold: true })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.LEFT,
  });
}

// Primer párrafo tras título — sin sangría
function pNoIndent(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12 })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.JUSTIFIED,
  });
}

// Párrafo con sangría
function p(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12 })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.JUSTIFIED,
    indent: { firstLine: INDENT },
  });
}

// Párrafo con sangría: bold prefix + normal text en el mismo párrafo
// Ej: "Encuesta digital:" en negrita + " Aplicada a..." normal
function pMixed(boldPart, normalPart) {
  return new Paragraph({
    children: [
      new TextRun({ text: boldPart, font: FONT, size: PT12, bold: true }),
      new TextRun({ text: " " + normalPart, font: FONT, size: PT12 }),
    ],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.JUSTIFIED,
    indent: { firstLine: INDENT },
  });
}

// Viñeta
function bul(text) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    children: [new TextRun({ text, font: FONT, size: PT12 })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
  });
}

// Label de pregunta: "Pregunta N:" en negrita + texto en normal, sin sangría
function pregunta(numLabel, questionText) {
  return new Paragraph({
    children: [
      new TextRun({ text: numLabel, font: FONT, size: PT12, bold: true }),
      new TextRun({ text: " " + questionText, font: FONT, size: PT12 }),
    ],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.LEFT,
  });
}

// ── Helpers APA tabla ──────────────────────────────────────────────────────

function tabLabel(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12, bold: true })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.LEFT,
    indent: { firstLine: 0 },
  });
}

function tabTitle(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12, italics: true })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.LEFT,
    indent: { firstLine: 0 },
  });
}

function tabNote(noteText) {
  const isCustom = noteText && noteText !== "std";
  return new Paragraph({
    children: isCustom
      ? [
          new TextRun({ text: "Nota.", font: FONT, size: PT10, italics: true }),
          new TextRun({ text: " " + noteText, font: FONT, size: PT10 }),
        ]
      : [
          new TextRun({ text: "Nota.", font: FONT, size: PT10, italics: true }),
          new TextRun({ text: " Elaboración propia (2026).", font: FONT, size: PT10 }),
        ],
    spacing: { line: SINGLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.LEFT,
    indent: { firstLine: 0 },
  });
}

// ── Helpers APA figura ─────────────────────────────────────────────────────

function figImg(fname) {
  const buf = fs.readFileSync(path.join(CHARTS, fname));
  return new Paragraph({
    children: [new ImageRun({ data: buf, transformation: { width: 396, height: 324 } })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.CENTER,
  });
}

function figLabel(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12, bold: true })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.LEFT,
    indent: { firstLine: 0 },
  });
}

function figTitle(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12, italics: true })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.LEFT,
    indent: { firstLine: 0 },
  });
}

function figNote() {
  return new Paragraph({
    children: [
      new TextRun({ text: "Nota.", font: FONT, size: PT10, italics: true }),
      new TextRun({ text: " Elaboración propia (2026).", font: FONT, size: PT10 }),
    ],
    spacing: { line: SINGLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.LEFT,
    indent: { firstLine: 0 },
  });
}

// ── Builder tabla estadística ──────────────────────────────────────────────

const BD = {
  top:     { style: BorderStyle.SINGLE, size: 4, color: "000000" },
  bottom:  { style: BorderStyle.SINGLE, size: 4, color: "000000" },
  left:    { style: BorderStyle.SINGLE, size: 4, color: "000000" },
  right:   { style: BorderStyle.SINGLE, size: 4, color: "000000" },
  insideH: { style: BorderStyle.SINGLE, size: 4, color: "000000" },
  insideV: { style: BorderStyle.SINGLE, size: 4, color: "000000" },
};

function thStat(text, colIdx) {
  return new TableCell({
    children: [new Paragraph({
      children: [new TextRun({ text, font: FONT, size: PT10, bold: true })],
      spacing: { line: SINGLE, lineRule: "auto", before: 60, after: 60 },
      alignment: AlignmentType.CENTER,
    })],
    width: { size: WS[colIdx], type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, color: "auto", fill: "D9D9D9" },
    verticalAlign: VerticalAlign.CENTER,
    margins: { top: 60, bottom: 60, left: 80, right: 80 },
  });
}

function tdStat(text, colIdx, bold) {
  return new TableCell({
    children: [new Paragraph({
      children: [new TextRun({ text, font: FONT, size: PT10, bold: !!bold })],
      spacing: { line: SINGLE, lineRule: "auto", before: 60, after: 60 },
      alignment: colIdx === 0 ? AlignmentType.LEFT : AlignmentType.CENTER,
    })],
    width: { size: WS[colIdx], type: WidthType.DXA },
    verticalAlign: VerticalAlign.CENTER,
    margins: { top: 60, bottom: 60, left: 80, right: 80 },
  });
}

// rows: [[variable, fa, faAcum, fr, frAcum, isBold?], ...]
function buildStatsTable(rows) {
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    borders: BD,
    rows: [
      new TableRow({
        tableHeader: true,
        children: [
          thStat("Variable", 0), thStat("Frecuencia Absoluta", 1),
          thStat("FA Acumulada", 2), thStat("Frecuencia Relativa", 3),
          thStat("FR Acumulada", 4),
        ],
      }),
      ...rows.map(r => new TableRow({
        children: [
          tdStat(r[0], 0, r[5]), tdStat(r[1], 1, r[5]),
          tdStat(r[2], 2, r[5]), tdStat(r[3], 3, r[5]),
          tdStat(r[4], 4, r[5]),
        ],
      })),
    ],
  });
}

// ── Datos tablas 2–13 ──────────────────────────────────────────────────────

const T2  = [["Todos los días","4","4","0,308","0,308"],["Varias veces a la semana","3","7","0,231","0,539"],["Ocasionalmente","3","10","0,231","0,770"],["Casi nunca","3","13","0,231","1,000"],["Muestra","13","","","",true]];
const T3  = [["Efectivo","11","11","0,846","0,846"],["Tarjeta débito/crédito","1","12","0,077","0,923"],["App o sistema digital","1","13","0,077","1,000"],["Muestra","13","","","",true]];
const T4  = [["Pago solo en efectivo","4","4","0,308","0,308"],["Largos tiempos de espera","2","6","0,154","0,462"],["Tarifas poco claras","2","8","0,154","0,615"],["Filas para entrar o salir","2","10","0,154","0,769"],["Falta de espacios disponibles","2","12","0,154","0,923"],["Pérdida de tiquetes","1","13","0,077","1,000"],["Muestra","13","","","",true]];
const T5  = [["Sí","5","5","0,385","0,385"],["Tal vez","8","13","0,615","1,000"],["No","0","13","0,000","1,000"],["Muestra","13","","","",true]];
const T6  = [["Sí, muy útil","12","12","0,923","0,923"],["Me es indiferente","0","12","0,000","0,923"],["No lo necesito","1","13","0,077","1,000"],["Muestra","13","","","",true]];
const T7  = [["Sí","8","8","0,615","0,615"],["Tal vez","4","12","0,308","0,923"],["No","1","13","0,077","1,000"],["Muestra","13","","","",true]];
const T8  = [["Transferencia digital / billetera","4","4","0,308","0,308"],["Tarjeta débito/crédito","4","8","0,308","0,615"],["Efectivo","3","11","0,231","0,846"],["Pago por código QR","2","13","0,154","1,000"],["Muestra","13","","","",true]];
const T9  = [["Me gustaría mucho","6","6","0,462","0,462"],["Es algo interesante","5","11","0,385","0,847"],["No me interesa","2","13","0,154","1,000"],["Muestra","13","","","",true]];
const T10 = [["Moderadamente importante","6","6","0,462","0,462"],["Muy importante","5","11","0,385","0,847"],["No es importante","2","13","0,154","1,000"],["Muestra","13","","","",true]];
const T11 = [["Muy dispuesto","7","7","0,538","0,538"],["Algo dispuesto","6","13","0,462","1,000"],["No dispuesto","0","13","0,000","1,000"],["Muestra","13","","","",true]];
const T12 = [["Solo si el precio es igual al tradicional","7","7","0,538","0,538"],["Sí","6","13","0,462","1,000"],["No","0","13","0,000","1,000"],["Muestra","13","","","",true]];
const T13 = [["Poder reservar","3","3","0,231","0,231"],["Pagar al ingresar, no al salir","2","5","0,154","0,385"],["Garantizar seguridad del vehículo","3","8","0,231","0,615"],["Notificación del vencimiento del parqueo","3","11","0,231","0,846"],["Parqueadero más amplio","2","13","0,154","1,000"],["Muestra","13","","","",true]];

// ── Documento ──────────────────────────────────────────────────────────────

const doc = new Document({
  numbering: {
    config: [{
      reference: "bullets",
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: "•",
        alignment: AlignmentType.LEFT,
        style: {
          paragraph: { indent: { left: 720, hanging: 360 } },
          run: { font: FONT, size: PT12 },
        },
      }],
    }],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN },
      },
    },
    footers: { default: pageFooter },
    children: [

      h1("4. Elicitación de Requisitos"),

      // ── 4.1 ──────────────────────────────────────────────────────────
      h2("4.1. Identificación de procesos"),
      pNoIndent(
        "Los procesos principales identificados en los parqueaderos privados de la localidad " +
        "de Suba, barrio Compartir, durante la fase de observación y recolección de datos " +
        "son los siguientes:"
      ),
      bul("Registro de ingreso de vehículo con asignación automática de espacio disponible."),
      bul("Cálculo de tiempo de permanencia y tarifa al momento de la salida del vehículo."),
      bul("Gestión de pagos y aplicación de descuentos mediante cupones."),
      bul("Reserva anticipada de espacios por parte de clientes registrados."),
      bul("Registro de novedades operativas con notificación al usuario afectado."),
      bul("Generación de reportes de ingresos, ocupación y actividad del parqueadero."),

      // ── 4.2 ──────────────────────────────────────────────────────────
      h2("4.2. Recolección de la información del software a construir"),
      pNoIndent(
        "Para iniciar el desarrollo del sistema MultiParking se realizó una fase de " +
        "recolección de datos con el objetivo de comprender las necesidades reales de " +
        "propietarios, vigilantes y usuarios. La información se obtuvo a través de dos " +
        "técnicas principales: observación directa en parqueaderos privados de la localidad " +
        "de Suba, barrio Compartir, en la ciudad de Bogotá D.C., y encuestas digitales " +
        "dirigidas a usuarios habituales y administradores del sector."
      ),

      // ── 4.3 ──────────────────────────────────────────────────────────
      h2("4.3. Elección de la técnica de recolección de la información"),
      p("Para el proyecto se optó por utilizar las siguientes técnicas de recolección de información:"),
      pMixed(
        "Encuesta digital:",
        "Aplicada a 13 usuarios y administradores de parqueaderos de la localidad de Suba, " +
        "con 13 preguntas de selección múltiple sobre su experiencia actual y sus expectativas " +
        "frente a un sistema tecnológico. La encuesta digital permite obtener datos " +
        "cuantificables de forma rápida y sistemática, facilitando el análisis estadístico " +
        "de frecuencias absolutas y relativas."
      ),
      pMixed(
        "Observación directa:",
        "Empleada para registrar de forma sistemática el comportamiento de los procesos " +
        "operativos en parqueaderos de pequeño y mediano tamaño en días de alta y baja " +
        "afluencia. Esta técnica complementó los datos de la encuesta al permitir verificar " +
        "en campo las problemáticas declaradas por los participantes."
      ),

      // ── 4.4 ──────────────────────────────────────────────────────────
      h2("4.4. Aplicación de la técnica de recolección de información"),
      p(
        "La encuesta se aplicó de forma digital a través de un formulario en línea " +
        "distribuido entre usuarios habituales y personal operativo de parqueaderos privados " +
        "de la localidad de Suba, barrio Compartir. La observación directa se efectuó en " +
        "los mismos establecimientos en días representativos de alta y baja afluencia " +
        "vehicular, registrando los procedimientos de ingreso y salida, los tiempos de " +
        "espera, las modalidades de cobro y las incidencias más frecuentes."
      ),

      // ── 4.5 ──────────────────────────────────────────────────────────
      h2("4.5. Organización de la información recolectada"),
      h2("4.5.1 Encuesta"),
      p("A continuación se presenta el análisis estadístico de la información recolectada en la encuesta aplicada (n = 13):"),

      // ── Pregunta 1 / Tabla 2 ───
      pregunta("Pregunta 1:", "¿Con qué frecuencia utilizas parqueaderos públicos o privados?"),
      tabLabel("Tabla 2"),
      tabTitle("Frecuencia de uso de parqueaderos"),
      buildStatsTable(T2),
      tabNote("std"),
      figImg("fig02.png"),
      figLabel("Figura 2"),
      figTitle("Frecuencia de uso de parqueaderos (n = 13)"),
      figNote(),

      // ── Pregunta 2 / Tabla 3 ───
      pregunta("Pregunta 2:", "¿Qué medio usas actualmente para pagar en un parqueadero?"),
      tabLabel("Tabla 3"),
      tabTitle("Medio de pago actual en parqueaderos"),
      buildStatsTable(T3),
      tabNote("std"),
      figImg("fig03.png"),
      figLabel("Figura 3"),
      figTitle("Medio de pago actual en parqueaderos (n = 13)"),
      figNote(),

      // ── Pregunta 3 / Tabla 4 ───
      pregunta("Pregunta 3:", "¿Cuál es el aspecto que más te molesta al usar un parqueadero?"),
      tabLabel("Tabla 4"),
      tabTitle("Aspecto más molesto al usar un parqueadero"),
      buildStatsTable(T4),
      tabNote("std"),
      figImg("fig04.png"),
      figLabel("Figura 4"),
      figTitle("Aspecto más molesto al usar un parqueadero (n = 13)"),
      figNote(),

      // ── Pregunta 4 / Tabla 5 ───
      pregunta("Pregunta 4:", "¿Te gustaría poder ingresar al parqueadero escaneando un código QR?"),
      tabLabel("Tabla 5"),
      tabTitle("Disposición para ingresar con código QR"),
      buildStatsTable(T5),
      tabNote("std"),
      figImg("fig05.png"),
      figLabel("Figura 5"),
      figTitle("Disposición para ingreso con código QR (n = 13)"),
      figNote(),

      // ── Pregunta 5 / Tabla 6 ───
      pregunta("Pregunta 5:", "¿Te parecería útil poder ver el tiempo y costo acumulado en tiempo real?"),
      tabLabel("Tabla 6"),
      tabTitle("Utilidad de visualizar tiempo y costo en tiempo real"),
      buildStatsTable(T6),
      tabNote("std"),
      figImg("fig06.png"),
      figLabel("Figura 6"),
      figTitle("Utilidad de visualizar costo en tiempo real (n = 13)"),
      figNote(),

      // ── Pregunta 6 / Tabla 7 ───
      pregunta("Pregunta 6:", "¿Usarías una app para reservar espacio de parqueo antes de llegar?"),
      tabLabel("Tabla 7"),
      tabTitle("Disposición para reservar espacio de parqueo anticipadamente"),
      buildStatsTable(T7),
      tabNote("std"),
      figImg("fig07.png"),
      figLabel("Figura 7"),
      figTitle("Disposición para reserva anticipada de espacio (n = 13)"),
      figNote(),

      // ── Pregunta 7 / Tabla 8 ───
      pregunta("Pregunta 7:", "¿Cuál sería tu método de pago preferido para este sistema?"),
      tabLabel("Tabla 8"),
      tabTitle("Método de pago de preferencia para un sistema digital"),
      buildStatsTable(T8),
      tabNote("std"),
      figImg("fig08.png"),
      figLabel("Figura 8"),
      figTitle("Método de pago de preferencia para el sistema (n = 13)"),
      figNote(),

      // ── Pregunta 8 / Tabla 9 ───
      pregunta("Pregunta 8:", "¿Qué tanto te gustaría que el parqueadero reconociera tu historial para darte descuentos?"),
      tabLabel("Tabla 9"),
      tabTitle("Interés en que el parqueadero reconozca el historial del usuario para descuentos"),
      buildStatsTable(T9),
      tabNote("std"),
      figImg("fig09.png"),
      figLabel("Figura 9"),
      figTitle("Interés en fidelización por historial de uso (n = 13)"),
      figNote(),

      // ── Pregunta 9 / Tabla 10 ───
      pregunta("Pregunta 9:", "¿Consideras importante salir del parqueadero rápidamente sin interactuar con personal?"),
      tabLabel("Tabla 10"),
      tabTitle("Importancia de salir del parqueadero sin interactuar con personal"),
      buildStatsTable(T10),
      tabNote("std"),
      figImg("fig10.png"),
      figLabel("Figura 10"),
      figTitle("Importancia de la salida autónoma del parqueadero (n = 13)"),
      figNote(),

      // ── Pregunta 10 / Tabla 11 ───
      pregunta("Pregunta 10:", "¿Qué tan dispuesto estarías a usar un sistema de parqueadero completamente automatizado?"),
      tabLabel("Tabla 11"),
      tabTitle("Disposición para usar un sistema de parqueadero completamente automatizado"),
      buildStatsTable(T11),
      tabNote("std"),
      figImg("fig11.png"),
      figLabel("Figura 11"),
      figTitle("Disposición para usar sistema automatizado (n = 13)"),
      figNote(),

      // ── Pregunta 11 / Tabla 12 ───
      pregunta("Pregunta 11:", "¿Estarías dispuesto/a a pagar un poco más por un parqueadero automatizado?"),
      tabLabel("Tabla 12"),
      tabTitle("Disposición para pagar más por un parqueadero automatizado"),
      buildStatsTable(T12),
      tabNote("std"),
      figImg("fig12.png"),
      figLabel("Figura 12"),
      figTitle("Disposición de pago por sistema automatizado (n = 13)"),
      figNote(),

      // ── Pregunta 12 / Tabla 13 ───
      pregunta("Pregunta 12:", "¿Qué funcionalidad te gustaría que tuviera un parqueadero automatizado?"),
      tabLabel("Tabla 13"),
      tabTitle("Funcionalidades deseadas en un parqueadero automatizado"),
      buildStatsTable(T13),
      tabNote("std"),
      figImg("fig13.png"),
      figLabel("Figura 13"),
      figTitle("Funcionalidades deseadas en parqueadero automatizado (n = 13)"),
      figNote(),

      // ── 4.5.2 ─────────────────────────────────────────────────────────
      h2("4.5.2 Observación directa"),
      p(
        "Se llevaron a cabo observaciones directas en parqueaderos privados de tamaño pequeño " +
        "y mediano ubicados en la localidad de Suba, barrio Compartir, en días con alta y baja " +
        "afluencia vehicular. Se registraron los procedimientos de entrada y salida de " +
        "vehículos, la asignación de espacios, los tiempos de espera, las formas de cobro y " +
        "las incidencias más frecuentes. Los hallazgos confirmaron de manera directa las " +
        "problemáticas reportadas en la encuesta: control manual mediante planillas físicas, " +
        "ausencia de visibilidad del estado de espacios en tiempo real, cobros imprecisos por " +
        "cálculos manuales y largos tiempos de atención en horas de alta demanda. Estos " +
        "resultados sustentan la necesidad de digitalizar el control de acceso, el cobro y la " +
        "comunicación con los usuarios (Elaboración propia, 2026)."
      ),

      // ── 4.6 ──────────────────────────────────────────────────────────
      h2("4.6. Informe de la recolección de datos"),
      p(
        "Los resultados de la encuesta y la observación directa realizada en los parqueaderos " +
        "de la localidad de Suba, barrio Compartir, evidencian de manera contundente la " +
        "necesidad de una solución tecnológica. El 84,6 % de los encuestados señaló que el " +
        "efectivo es el único medio de pago aceptado; el 92,3 % consideró muy útil poder ver " +
        "el tiempo de permanencia y el costo acumulado en tiempo real; el 100 % se mostró " +
        "abierto al uso de tecnología QR para el ingreso; y el 61,5 % usaría un sistema de " +
        "reserva anticipada. Adicionalmente, el 100 % de los participantes declaró estar " +
        "dispuesto a usar un sistema automatizado (53,8 % muy dispuesto; 46,2 % algo " +
        "dispuesto), y ninguno se mostró en contra de la automatización."
      ),
      p(
        "Estos hallazgos confirman la viabilidad y pertinencia del sistema MultiParking como " +
        "respuesta tecnológica a las necesidades identificadas. Los módulos de reservas, " +
        "fidelización, visualización de tarifas en tiempo real, pagos digitales y " +
        "notificaciones automáticas responden directamente a las preferencias expresadas por " +
        "los usuarios encuestados. La observación directa verificó en campo que las " +
        "problemáticas declaradas son reales y persistentes en el entorno del parqueadero de " +
        "referencia (Elaboración propia, 2026)."
      ),
    ],
  }],
});

const OUT = "C:/Users/xeodeo/Desktop/Multiparking-Django/DOCUMENTACION/Secciones/" +
            "Seccion_04_Elicitacion_Requisitos/seccion_04_elicitacion_requisitos.docx";

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(OUT, buffer);
  console.log("OK: " + OUT);
}).catch(err => { console.error(err); process.exit(1); });
