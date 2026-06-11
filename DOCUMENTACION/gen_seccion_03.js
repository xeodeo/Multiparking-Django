const {
  Document, Packer, Paragraph, TextRun,
  AlignmentType, PageNumber, Footer,
  Table, TableRow, TableCell, WidthType, BorderStyle,
  ShadingType, VerticalAlign
} = require('docx');
const fs = require('fs');

const FONT   = "Times New Roman";
const PT12   = 24;
const PT10   = 20;
const DOUBLE = 480;
const SINGLE = 240;
const MARGIN = 1440;

// Columna widths (DXA), total = 9360
const W = [400, 1680, 1500, 1590, 840, 650, 2700];

const pageFooter = new Footer({
  children: [new Paragraph({
    children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: PT12 })],
    alignment: AlignmentType.RIGHT,
    spacing: { before: 0, after: 0 },
  })],
});

// ── Helpers ────────────────────────────────────────────────────────────────

function h1(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12, bold: true })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.CENTER,
  });
}

function pNoIndent(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12 })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.JUSTIFIED,
  });
}

function tabLabel(text) {   // "Tabla 1" — negrita, izquierda
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12, bold: true })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.LEFT,
  });
}

function tabTitle(text) {   // Título en cursiva
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12, italics: true })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.LEFT,
  });
}

// Nota debajo de tabla — 10pt, cursiva "Nota." + texto normal
function tabNote() {
  return new Paragraph({
    children: [
      new TextRun({ text: "Nota.", font: FONT, size: PT10, italics: true }),
      new TextRun({ text: " Elaboración propia (2026).", font: FONT, size: PT10 }),
    ],
    spacing: { line: SINGLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.LEFT,
  });
}

// Celda de cabecera
function thCell(text, colIdx) {
  return new TableCell({
    children: [new Paragraph({
      children: [new TextRun({ text, font: FONT, size: PT10, bold: true })],
      spacing: { line: SINGLE, lineRule: "auto", before: 60, after: 60 },
      alignment: AlignmentType.CENTER,
    })],
    width: { size: W[colIdx], type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, color: "auto", fill: "D9D9D9" },
    verticalAlign: VerticalAlign.CENTER,
    margins: { top: 60, bottom: 60, left: 80, right: 80 },
  });
}

// Celda de dato con color opcional
function tdCell(text, colIdx, fill, bold) {
  const runs = bold
    ? [new TextRun({ text, font: FONT, size: PT10, bold: true })]
    : [new TextRun({ text, font: FONT, size: PT10 })];
  const cell = {
    children: [new Paragraph({
      children: runs,
      spacing: { line: SINGLE, lineRule: "auto", before: 60, after: 60 },
      alignment: AlignmentType.LEFT,
    })],
    width: { size: W[colIdx], type: WidthType.DXA },
    verticalAlign: VerticalAlign.CENTER,
    margins: { top: 60, bottom: 60, left: 80, right: 80 },
  };
  if (fill) cell.shading = { type: ShadingType.CLEAR, color: "auto", fill };
  return new TableCell(cell);
}

// Nivel (centrado + color)
function nivelCell(text, fill, colIdx) {
  return new TableCell({
    children: [new Paragraph({
      children: [new TextRun({ text, font: FONT, size: PT10, bold: true })],
      spacing: { line: SINGLE, lineRule: "auto", before: 60, after: 60 },
      alignment: AlignmentType.CENTER,
    })],
    width: { size: W[colIdx], type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, color: "auto", fill },
    verticalAlign: VerticalAlign.CENTER,
    margins: { top: 60, bottom: 60, left: 80, right: 80 },
  });
}

// ── Datos ──────────────────────────────────────────────────────────────────

const ROWS = [
  {
    n: "1",
    riesgo: "Retrasos en el desarrollo del sistema",
    causa:  "Subestimación de tiempos o problemas técnicos imprevistos",
    impacto:"Aplazamiento en la entrega final del TFPF",
    prob:   "Media",
    nivel:  "Medio",
    fill:   "FFF2CC",
    mitiga: "Cronograma ágil con revisión semanal de avances y redistribución de tareas.",
  },
  {
    n: "2",
    riesgo: "Dificultades en la integración de pagos digitales",
    causa:  "Problemas con APIs de pasarelas de pago externas",
    impacto:"No se podrán realizar cobros automatizados en línea",
    prob:   "Media",
    nivel:  "Medio",
    fill:   "FFF2CC",
    mitiga: "Usar APIs documentadas (PayU, Wompi); en su defecto, registrar pagos manualmente.",
  },
  {
    n: "3",
    riesgo: "Falta de conectividad en el entorno piloto (Suba)",
    causa:  "Infraestructura deficiente de red en el parqueadero",
    impacto:"Fallos en el acceso o carga del sistema durante la operación",
    prob:   "Alta",
    nivel:  "Alto",
    fill:   "FFCCCC",
    mitiga: "Verificar requisitos técnicos de conectividad del sitio previamente al despliegue.",
  },
  {
    n: "4",
    riesgo: "Baja adopción por parte de los usuarios",
    causa:  "Resistencia al cambio por parte del personal operativo",
    impacto:"Uso limitado del sistema y regreso a procesos manuales",
    prob:   "Media",
    nivel:  "Medio",
    fill:   "FFF2CC",
    mitiga: "Capacitaciones prácticas y pruebas piloto con retroalimentación continua.",
  },
  {
    n: "5",
    riesgo: "Pérdida de datos durante el uso",
    causa:  "Fallos en el servidor o en la base de datos",
    impacto:"Pérdida de historial de parqueos y registros operativos",
    prob:   "Baja",
    nivel:  "Bajo",
    fill:   "D9EAD3",
    mitiga: "Backups automáticos diarios en Render.com (pg_dump + snapshots).",
  },
  {
    n: "6",
    riesgo: "Cambios en los requerimientos del cliente",
    causa:  "Nuevas necesidades descubiertas durante el desarrollo",
    impacto:"Re-trabajo o rediseño de módulos ya implementados",
    prob:   "Media",
    nivel:  "Medio",
    fill:   "FFF2CC",
    mitiga: "Reuniones frecuentes con stakeholders y control de cambios documentado.",
  },
  {
    n: "7",
    riesgo: "Salida de un integrante clave del equipo",
    causa:  "Problemas personales o deserción académica",
    impacto:"Retrasos significativos o redistribución forzada de tareas",
    prob:   "Baja",
    nivel:  "Bajo",
    fill:   "D9EAD3",
    mitiga: "Documentación compartida, repositorio Git con historial completo y roles cruzados.",
  },
];

// ── Tabla ──────────────────────────────────────────────────────────────────

const headerRow = new TableRow({
  tableHeader: true,
  children: [
    thCell("Nº",          0),
    thCell("Riesgo",      1),
    thCell("Causa",       2),
    thCell("Impacto",     3),
    thCell("Probabilidad",4),
    thCell("Nivel",       5),
    thCell("Estrategia de mitigación", 6),
  ],
});

const dataRows = ROWS.map(r => new TableRow({
  children: [
    tdCell(r.n,       0),
    tdCell(r.riesgo,  1),
    tdCell(r.causa,   2),
    tdCell(r.impacto, 3),
    tdCell(r.prob,    4),
    nivelCell(r.nivel, r.fill, 5),
    tdCell(r.mitiga,  6),
  ],
}));

const table = new Table({
  width: { size: 9360, type: WidthType.DXA },
  rows: [headerRow, ...dataRows],
  borders: {
    top:           { style: BorderStyle.SINGLE, size: 4, color: "000000" },
    bottom:        { style: BorderStyle.SINGLE, size: 4, color: "000000" },
    left:          { style: BorderStyle.SINGLE, size: 4, color: "000000" },
    right:         { style: BorderStyle.SINGLE, size: 4, color: "000000" },
    insideH:       { style: BorderStyle.SINGLE, size: 4, color: "000000" },
    insideV:       { style: BorderStyle.SINGLE, size: 4, color: "000000" },
  },
});

// ── Documento ──────────────────────────────────────────────────────────────

const doc = new Document({
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN },
      },
    },
    footers: { default: pageFooter },
    children: [
      h1("3. Matriz de Riesgo"),
      pNoIndent(
        "Durante la fase de planificación del proyecto se identificaron los principales " +
        "riesgos que podrían afectar el desarrollo, la implementación y la operación del " +
        "sistema MultiParking. La Tabla 1 presenta cada riesgo con su causa, impacto " +
        "potencial, probabilidad de ocurrencia, nivel de riesgo resultante y la estrategia " +
        "de mitigación definida por el equipo de desarrollo."
      ),
      tabLabel("Tabla 1"),
      tabTitle("Matriz de Riesgos del Proyecto MultiParking"),
      table,
      tabNote(),
    ],
  }],
});

const OUT = "C:/Users/xeodeo/Desktop/Multiparking-Django/DOCUMENTACION/Secciones/" +
            "Seccion_03_Matriz_Riesgo/seccion_03_matriz_riesgo.docx";

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(OUT, buffer);
  console.log("OK: " + OUT);
}).catch(err => { console.error(err); process.exit(1); });
