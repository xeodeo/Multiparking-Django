const {
  Document, Packer, Paragraph, TextRun, ImageRun,
  AlignmentType, PageNumber, Footer, LevelFormat,
  HeadingLevel, SectionType, PageBreak,
  PositionalTab, PositionalTabAlignment,
  PositionalTabRelativeTo, PositionalTabLeader,
  Table, TableRow, TableCell, WidthType, BorderStyle,
  ShadingType, VerticalAlign
} = require('docx');
const fs = require('fs');
const path = require('path');

const CHARTS_04 = path.join(
  __dirname,
  "Secciones", "Seccion_04_Elicitacion_Requisitos", "charts"
);

const FONT   = "Times New Roman";
const PT12   = 24;
const PT10   = 20;
const PT14   = 28;
const DOUBLE = 480;
const SINGLE = 240;
const MARGIN = 1440;
const INDENT = 720;

// Columnas tabla riesgo (DXA), total 9360
const W3 = [400, 1680, 1500, 1590, 840, 650, 2700];

// Columnas tablas estadísticas encuesta
const WS = [3500, 1465, 1465, 1465, 1465];

const pageFooter = new Footer({
  children: [new Paragraph({
    children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: PT12 })],
    alignment: AlignmentType.RIGHT,
    spacing: { before: 0, after: 0 },
  })],
});

// ── Helpers ────────────────────────────────────────────────────────────────

function empty() {
  return new Paragraph({
    children: [new TextRun({ text: "", font: FONT, size: PT12 })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
  });
}

function coverLine(text, bold, size) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: size || PT12, bold: !!bold })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.CENTER,
  });
}

// HeadingLevel.HEADING_1 — centrado (Resumen, Abstract, Intro, títulos de sección)
function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun({ text, font: FONT, size: PT12, bold: true, color: "000000" })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.CENTER,
  });
}

// HeadingLevel.HEADING_2 — izquierda (subsecciones 1.1, 1.2 …)
function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    children: [new TextRun({ text, font: FONT, size: PT12, bold: true, color: "000000" })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.LEFT,
  });
}

// Párrafo sin sangría (primer párrafo tras encabezado y textos de resumen/abstract)
function pNoIndent(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12 })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.JUSTIFIED,
  });
}

// Párrafo con sangría de primera línea (TAB al inicio en el MD)
function p(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12 })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.JUSTIFIED,
    indent: { firstLine: INDENT },
  });
}

// Etiqueta de fase (negrita, sin sangría)
function fase(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12, bold: true })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.LEFT,
  });
}

// Párrafo negrita con sangría (lead-in de listas)
function pBold(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12, bold: true })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.JUSTIFIED,
    indent: { firstLine: INDENT },
  });
}

// Línea "Palabras clave:" / "Keywords:" con etiqueta en cursiva
function kwLine(label, terms) {
  return new Paragraph({
    children: [
      new TextRun({ text: label, font: FONT, size: PT12, italics: true }),
      new TextRun({ text: " " + terms, font: FONT, size: PT12 }),
    ],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
  });
}

// Pies de figura APA 7
function figLabel(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12, bold: true })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.LEFT,
    indent: { firstLine: 0 },
  });
}
function figItalic(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12, italics: true })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.LEFT,
    indent: { firstLine: 0 },
  });
}
function figNote(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12 })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.LEFT,
    indent: { firstLine: 0 },
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

// Salto de página
function pb() {
  return new Paragraph({ children: [new PageBreak()] });
}

// ── Helpers tabla APA ─────────────────────────────────────────────────────

function tabLabel(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12, bold: true })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.LEFT,
    indent: { firstLine: 0 },
  });
}

function tabItalic(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12, italics: true })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.LEFT,
    indent: { firstLine: 0 },
  });
}

function tabNote() {
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

function thCell(text, colIdx) {
  return new TableCell({
    children: [new Paragraph({
      children: [new TextRun({ text, font: FONT, size: PT10, bold: true })],
      spacing: { line: SINGLE, lineRule: "auto", before: 60, after: 60 },
      alignment: AlignmentType.CENTER,
    })],
    width: { size: W3[colIdx], type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, color: "auto", fill: "D9D9D9" },
    verticalAlign: VerticalAlign.CENTER,
    margins: { top: 60, bottom: 60, left: 80, right: 80 },
  });
}

function tdCell(text, colIdx, fill) {
  const cell = {
    children: [new Paragraph({
      children: [new TextRun({ text, font: FONT, size: PT10 })],
      spacing: { line: SINGLE, lineRule: "auto", before: 60, after: 60 },
      alignment: AlignmentType.LEFT,
    })],
    width: { size: W3[colIdx], type: WidthType.DXA },
    verticalAlign: VerticalAlign.CENTER,
    margins: { top: 60, bottom: 60, left: 80, right: 80 },
  };
  if (fill) cell.shading = { type: ShadingType.CLEAR, color: "auto", fill };
  return new TableCell(cell);
}

function nivelCell(text, fill, colIdx) {
  return new TableCell({
    children: [new Paragraph({
      children: [new TextRun({ text, font: FONT, size: PT10, bold: true })],
      spacing: { line: SINGLE, lineRule: "auto", before: 60, after: 60 },
      alignment: AlignmentType.CENTER,
    })],
    width: { size: W3[colIdx], type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, color: "auto", fill },
    verticalAlign: VerticalAlign.CENTER,
    margins: { top: 60, bottom: 60, left: 80, right: 80 },
  });
}

// ── Helpers stats tabla encuesta ──────────────────────────────────────────

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

function buildStatsTable(rows) {
  const BD = {
    top:     { style: BorderStyle.SINGLE, size: 4, color: "000000" },
    bottom:  { style: BorderStyle.SINGLE, size: 4, color: "000000" },
    left:    { style: BorderStyle.SINGLE, size: 4, color: "000000" },
    right:   { style: BorderStyle.SINGLE, size: 4, color: "000000" },
    insideH: { style: BorderStyle.SINGLE, size: 4, color: "000000" },
    insideV: { style: BorderStyle.SINGLE, size: 4, color: "000000" },
  };
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

function tabNoteCustom(noteText) {
  return new Paragraph({
    children: [
      new TextRun({ text: "Nota.", font: FONT, size: PT10, italics: true }),
      new TextRun({ text: " " + noteText, font: FONT, size: PT10 }),
    ],
    spacing: { line: SINGLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.LEFT,
    indent: { firstLine: 0 },
  });
}

function figImg(fname) {
  const buf = fs.readFileSync(path.join(CHARTS_04, fname));
  return new Paragraph({
    children: [new ImageRun({ data: buf, transformation: { width: 396, height: 324 } })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.CENTER,
  });
}

function figNoteStd() {
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

// pMixed — bold prefix + normal text en mismo párrafo con sangría
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

// pregunta — "Pregunta N:" bold + texto normal, sin sangría
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

// ── Datos tablas encuesta 2–13 ─────────────────────────────────────────────

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

const RIESGOS = [
  { n:"1", riesgo:"Retrasos en el desarrollo del sistema", causa:"Subestimación de tiempos o problemas técnicos imprevistos", impacto:"Aplazamiento en la entrega final del TFPF", prob:"Media", nivel:"Medio", fill:"FFF2CC", mitiga:"Cronograma ágil con revisión semanal de avances y redistribución de tareas." },
  { n:"2", riesgo:"Dificultades en la integración de pagos digitales", causa:"Problemas con APIs de pasarelas de pago externas", impacto:"No se podrán realizar cobros automatizados en línea", prob:"Media", nivel:"Medio", fill:"FFF2CC", mitiga:"Usar APIs documentadas (PayU, Wompi); en su defecto, registrar pagos manualmente." },
  { n:"3", riesgo:"Falta de conectividad en el entorno piloto (Suba)", causa:"Infraestructura deficiente de red en el parqueadero", impacto:"Fallos en el acceso o carga del sistema durante la operación", prob:"Alta", nivel:"Alto", fill:"FFCCCC", mitiga:"Verificar requisitos técnicos de conectividad del sitio previamente al despliegue." },
  { n:"4", riesgo:"Baja adopción por parte de los usuarios", causa:"Resistencia al cambio por parte del personal operativo", impacto:"Uso limitado del sistema y regreso a procesos manuales", prob:"Media", nivel:"Medio", fill:"FFF2CC", mitiga:"Capacitaciones prácticas y pruebas piloto con retroalimentación continua." },
  { n:"5", riesgo:"Pérdida de datos durante el uso", causa:"Fallos en el servidor o en la base de datos", impacto:"Pérdida de historial de parqueos y registros operativos", prob:"Baja", nivel:"Bajo", fill:"D9EAD3", mitiga:"Backups automáticos diarios en Render.com (pg_dump + snapshots)." },
  { n:"6", riesgo:"Cambios en los requerimientos del cliente", causa:"Nuevas necesidades descubiertas durante el desarrollo", impacto:"Re-trabajo o rediseño de módulos ya implementados", prob:"Media", nivel:"Medio", fill:"FFF2CC", mitiga:"Reuniones frecuentes con stakeholders y control de cambios documentado." },
  { n:"7", riesgo:"Salida de un integrante clave del equipo", causa:"Problemas personales o deserción académica", impacto:"Retrasos significativos o redistribución forzada de tareas", prob:"Baja", nivel:"Bajo", fill:"D9EAD3", mitiga:"Documentación compartida, repositorio Git con historial completo y roles cruzados." },
];

function buildTablaRiesgos() {
  const BORDERS = {
    top:     { style: BorderStyle.SINGLE, size: 4, color: "000000" },
    bottom:  { style: BorderStyle.SINGLE, size: 4, color: "000000" },
    left:    { style: BorderStyle.SINGLE, size: 4, color: "000000" },
    right:   { style: BorderStyle.SINGLE, size: 4, color: "000000" },
    insideH: { style: BorderStyle.SINGLE, size: 4, color: "000000" },
    insideV: { style: BorderStyle.SINGLE, size: 4, color: "000000" },
  };
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    borders: BORDERS,
    rows: [
      new TableRow({
        tableHeader: true,
        children: [
          thCell("Nº", 0), thCell("Riesgo", 1), thCell("Causa", 2),
          thCell("Impacto", 3), thCell("Probabilidad", 4),
          thCell("Nivel", 5), thCell("Estrategia de mitigación", 6),
        ],
      }),
      ...RIESGOS.map(r => new TableRow({
        children: [
          tdCell(r.n, 0), tdCell(r.riesgo, 1), tdCell(r.causa, 2),
          tdCell(r.impacto, 3), tdCell(r.prob, 4),
          nivelCell(r.nivel, r.fill, 5), tdCell(r.mitiga, 6),
        ],
      })),
    ],
  });
}

// Entrada del índice con líder de puntos
// level 0 = sección principal (negrita), level 1 = subsección (normal, sangría)
function tocEntry(text, pageNum, level) {
  return new Paragraph({
    children: [
      new TextRun({ text, font: FONT, size: PT12, bold: level === 0 }),
      new TextRun({
        children: [
          new PositionalTab({
            alignment: PositionalTabAlignment.RIGHT,
            relativeTo: PositionalTabRelativeTo.MARGIN,
            leader: PositionalTabLeader.DOT,
          }),
          String(pageNum),
        ],
        font: FONT, size: PT12,
      }),
    ],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    indent: level > 0 ? { left: 720 } : undefined,
  });
}

// ── Documento ──────────────────────────────────────────────────────────────

const doc = new Document({
  styles: {
    default: {
      document: { run: { font: FONT, size: PT12 } },
    },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1",
        basedOn: "Normal", next: "Normal", quickFormat: true,
        run:       { size: PT12, bold: true, font: FONT, color: "000000" },
        paragraph: { spacing: { line: DOUBLE, before: 0, after: 0 }, alignment: AlignmentType.CENTER, outlineLevel: 0 },
      },
      {
        id: "Heading2", name: "Heading 2",
        basedOn: "Normal", next: "Normal", quickFormat: true,
        run:       { size: PT12, bold: true, font: FONT, color: "000000" },
        paragraph: { spacing: { line: DOUBLE, before: 0, after: 0 }, alignment: AlignmentType.LEFT, outlineLevel: 1 },
      },
    ],
  },
  numbering: {
    config: [{
      reference: "bullets",
      levels: [{
        level: 0,
        format: LevelFormat.BULLET,
        text: "•",
        alignment: AlignmentType.LEFT,
        style: {
          paragraph: { indent: { left: 720, hanging: 360 } },
          run: { font: FONT, size: PT12 },
        },
      }],
    }],
  },

  sections: [

    // ══════════════════════════════════════════════════════════════════════
    // SECCIÓN 1 — PORTADA (sin numeración de página)
    // ══════════════════════════════════════════════════════════════════════
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN },
        },
      },
      children: [
        empty(), empty(), empty(), empty(), empty(),
        coverLine("Sistema de Información Web para la Gestión Integral de Parqueaderos Privados", true),
        empty(),
        coverLine("MultiParking", true, PT14),
        empty(), empty(), empty(), empty(),
        coverLine("Integrantes:"),
        coverLine("Kevin Arley Grisales Ovalle"),
        coverLine("Kevin Santiago Pinto López"),
        empty(), empty(), empty(),
        coverLine("Análisis y Desarrollo de Software"),
        coverLine("Ficha: 3119175"),
        empty(), empty(), empty(),
        coverLine("Centro de Diseño y Metrología – SENA"),
        coverLine("Bogotá D.C., 2026"),
      ],
    },

    // ══════════════════════════════════════════════════════════════════════
    // SECCIÓN 2 — TOC + TODO EL CONTENIDO (numeración visible desde aquí)
    // ══════════════════════════════════════════════════════════════════════
    {
      properties: {
        type: SectionType.NEXT_PAGE,
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN },
        },
      },
      footers: { default: pageFooter },
      children: [

        // ── Tabla de Contenido (índice estático con dot-leaders) ───────
        new Paragraph({
          children: [new TextRun({ text: "Tabla de Contenido", font: FONT, size: PT12, bold: true })],
          alignment: AlignmentType.CENTER,
          spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
        }),
        empty(),
        tocEntry("Resumen",                                          3, 0),
        tocEntry("Abstract",                                         4, 0),
        tocEntry("Introducción",                                     5, 0),
        tocEntry("1. Planteamiento y Justificación del Problema",    6, 0),
        tocEntry("1.1. Planteamiento del problema",                  6, 1),
        tocEntry("1.2. Árbol del problema",                          7, 1),
        tocEntry("1.3. Justificación",                               8, 1),
        tocEntry("1.4. Alcance del proyecto",                        9, 1),
        tocEntry("2. Objetivos del Trabajo Final de Proyecto Formativo (TFPF)", 10, 0),
        tocEntry("2.1. Objetivo general",                           10, 1),
        tocEntry("2.2. Objetivos específicos",                      11, 1),
        tocEntry("2.3. Alcance del proyecto",                       13, 1),
        tocEntry("3. Matriz de Riesgo",                            15, 0),
        tocEntry("4. Elicitación de Requisitos",                   16, 0),
        tocEntry("4.1. Identificación de procesos",                16, 1),
        tocEntry("4.2. Recolección de la información",             17, 1),
        tocEntry("4.3. Elección de la técnica",                    17, 1),
        tocEntry("4.4. Aplicación de la técnica",                  18, 1),
        tocEntry("4.5. Organización de la información",            18, 1),
        tocEntry("4.6. Informe de la recolección de datos",        26, 1),
        pb(),

        // ── Resumen ─────────────────────────────────────────────────────
        h1("Resumen"),
        pNoIndent(
          "MultiParking es un sistema de información web orientado a la automatización y " +
          "gestión integral de parqueaderos privados de pequeña y mediana escala. La plataforma " +
          "permite el registro de usuarios con tres roles diferenciados: administrador, vigilante " +
          "y cliente; el control de vehículos propios y visitantes; la asignación y liberación " +
          "de espacios en tiempo real sobre un plano interactivo por pisos; el cálculo automático " +
          "de tarifas por minuto con redondeo a cien pesos colombianos; la generación y registro " +
          "de pagos; la aplicación de cupones de descuento por porcentaje o valor fijo; la gestión " +
          "de reservas anticipadas; el registro fotográfico de novedades operativas con notificación " +
          "automática por correo electrónico; un sistema de fidelización mediante stickers " +
          "acumulables canjeables por bonos de descuento; y la generación de reportes exportables " +
          "en formato PDF y Excel. El sistema fue desarrollado en Python con el framework Django, " +
          "empleando PostgreSQL como gestor de base de datos en el entorno de producción desplegado " +
          "en Render.com, Tailwind CSS para el diseño responsivo, SendGrid para el envío de correos " +
          "transaccionales y Gunicorn como servidor WSGI. La arquitectura sigue el patrón " +
          "MVT (Modelo-Vista-Template) con autenticación por sesión propia y control de acceso " +
          "basado en roles."
        ),
        kwLine("Palabras clave:", "parqueadero, sistema de información web, Django, PostgreSQL, gestión de espacios, fidelización, roles de usuario."),
        pb(),

        // ── Abstract ────────────────────────────────────────────────────
        h1("Abstract"),
        pNoIndent(
          "MultiParking is a web-based information system designed for the comprehensive " +
          "automation and management of small and medium-scale private parking lots. The platform " +
          "supports user registration across three differentiated roles—administrator, security " +
          "guard, and client—along with real-time parking space assignment and release on an " +
          "interactive floor map, minute-based automatic fare calculation rounded to the nearest " +
          "one hundred Colombian pesos, payment generation, percentage and fixed-value discount " +
          "coupons, advance reservation management, photographic incident logging with automated " +
          "email notifications, a loyalty sticker accumulation program redeemable for discount " +
          "vouchers, and exportable reports in PDF and Excel formats. The system was built with " +
          "Python and the Django framework, using PostgreSQL as the production database hosted on " +
          "Render.com, Tailwind CSS for responsive design, SendGrid for transactional email " +
          "delivery, and Gunicorn as the WSGI server. The architecture follows the MVT " +
          "(Model-View-Template) pattern with custom session-based authentication and role-based " +
          "access control."
        ),
        kwLine("Keywords:", "parking lot, web information system, Django, PostgreSQL, space management, loyalty program, role-based access."),
        pb(),

        // ── Introducción ─────────────────────────────────────────────────
        h1("Introducción"),
        pNoIndent(
          "En la ciudad de Bogotá D.C., específicamente en la localidad de Suba, barrio " +
          "Compartir, los parqueaderos privados de pequeña y mediana escala operan con métodos " +
          "manuales que generan ineficiencias operativas: registros en papel, cálculos de tarifa " +
          "imprecisos, ausencia de trazabilidad y nula visibilidad del estado de los espacios en " +
          "tiempo real. Esta situación, observable también en numerosos establecimientos similares " +
          "a nivel nacional, deriva en pérdida de ingresos, inconformidad de los usuarios y " +
          "dificultad para tomar decisiones basadas en datos (García & Martínez, 2022)."
        ),
        p(
          "El proyecto MultiParking desarrolla una solución web que automatiza de forma integral " +
          "la operación de parqueaderos privados. El sistema registra ingresos y salidas de " +
          "vehículos, calcula tarifas en tiempo real, gestiona reservas anticipadas, emite " +
          "notificaciones digitales, aplica descuentos mediante cupones y acumula beneficios de " +
          "fidelización para los usuarios registrados."
        ),
        p(
          "La arquitectura tecnológica se apoya en Django (Python 3.12), PostgreSQL en " +
          "producción (Render.com), Tailwind CSS vía CDN, Chart.js para visualizaciones " +
          "estadísticas, SendGrid como proveedor de correo transaccional y Gunicorn como servidor " +
          "WSGI. La autenticación implementa un modelo de sesión propio —sin dependencia del " +
          "módulo django.contrib.auth.User— con tres roles de acceso: ADMIN, VIGILANTE y CLIENTE, " +
          "cada uno con vistas y permisos diferenciados."
        ),
        p(
          "El presente documento sigue la estructura definida por el programa Análisis y " +
          "Desarrollo de Software (ADSO) del Servicio Nacional de Aprendizaje (SENA) para el " +
          "Trabajo Final del Proyecto Formativo (TFPF), y las normas de presentación y citación " +
          "APA séptima edición (American Psychological Association, 2020)."
        ),
        pb(),

        // ══════════════════════════════════════════════════════════════════
        // 1. PLANTEAMIENTO Y JUSTIFICACIÓN DEL PROBLEMA
        // ══════════════════════════════════════════════════════════════════
        h1("1. Planteamiento y Justificación del Problema"),

        // 1.1
        h2("1.1. Planteamiento del problema"),
        pNoIndent(
          "En la ciudad de Bogotá D.C., específicamente en la localidad de Suba, barrio " +
          "Compartir, los parqueaderos privados de pequeña y mediana escala gestionan sus " +
          "operaciones mediante procesos completamente manuales. El control del ingreso y " +
          "salida de vehículos depende de planillas físicas, lo que impide contar con " +
          "trazabilidad confiable y genera inconsistencias frecuentes en los tiempos " +
          "registrados y los valores cobrados a los usuarios. La ausencia de un sistema " +
          "tecnológico centralizado limita la visibilidad en tiempo real de los espacios " +
          "disponibles, dificulta la conciliación de pagos y complica la detección oportuna " +
          "de errores o irregularidades operativas."
        ),
        p(
          "A esta problemática se suma la imposibilidad de realizar reservas anticipadas de " +
          "espacios, lo que reduce la satisfacción del usuario y la competitividad del " +
          "establecimiento frente a alternativas que sí ofrecen servicios digitales. Los " +
          "propietarios y administradores tampoco cuentan con herramientas que les permitan " +
          "generar reportes de ingresos, analizar la ocupación histórica o fidelizar a sus " +
          "clientes habituales mediante incentivos digitales."
        ),
        p(
          "De continuar esta situación, los establecimientos afectados seguirán incurriendo " +
          "en pérdidas económicas por cobros imprecisos, pérdida de clientes por deficiencias " +
          "en el servicio y exposición a fraudes internos por la falta de trazabilidad en los " +
          "registros operativos."
        ),

        // 1.2
        h2("1.2. Árbol del problema"),
        new Paragraph({
          children: [new ImageRun({
            type: "png",
            data: fs.readFileSync(
              "C:/Users/xeodeo/Desktop/Multiparking-Django/DOCUMENTACION/" +
              "Secciones/Seccion_01_Planteamiento_Problema/arbol_problema.png"
            ),
            transformation: { width: 600, height: 450 },
            altText: {
              title: "Árbol del problema",
              description: "Árbol del problema del sistema MultiParking",
              name: "arbol_problema",
            },
          })],
          alignment: AlignmentType.CENTER,
          spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
        }),
        figLabel("Figura 1"),
        figItalic("Árbol del problema del sistema MultiParking"),
        figNote("Nota. Elaboración propia (2026)."),

        // 1.3
        h2("1.3. Justificación"),
        pNoIndent(
          "En numerosos parqueaderos privados de pequeña y mediana escala en Bogotá, el " +
          "control manual de ingreso y salida de vehículos genera demoras, fallos en el cobro " +
          "y pérdida de información crítica. Estudios recientes señalan que la adopción de " +
          "sistemas digitales de gestión de aparcamientos mejora la eficiencia operativa, " +
          "reduce errores humanos y ofrece trazabilidad de datos en tiempo real (García & " +
          "Martínez, 2022). Así mismo, Garavito Albao et al. (2021) demuestran que los " +
          "sistemas de información en pequeñas empresas de servicios reducen el tiempo de " +
          "atención hasta en un 40 % y disminuyen los errores de registro en más del 60 %."
        ),
        p(
          "El desarrollo de MultiParking responde directamente a esta problemática al " +
          "proporcionar una plataforma centralizada que digitaliza todos los procesos " +
          "operativos del parqueadero. La solución beneficia directamente a tres perfiles de " +
          "usuarios: administradores, que obtienen visibilidad total del estado del parqueadero " +
          "y acceso a reportes de inteligencia operativa; vigilantes, que agilizan los procesos " +
          "de ingreso y salida mediante interfaces simplificadas; y clientes, que acceden a " +
          "reservas anticipadas, historial de parqueos y beneficios de fidelización acumulables."
        ),
        p(
          "Desde la perspectiva técnica, la implementación sobre Django (Python 3.12) con " +
          "PostgreSQL garantiza mantenibilidad a largo plazo, escalabilidad y seguridad de " +
          "datos. El despliegue en la plataforma Render.com permite disponibilidad continua " +
          "sin inversión en infraestructura propia, lo que hace la solución viable " +
          "económicamente para establecimientos de pequeña escala " +
          "(American Psychological Association, 2020)."
        ),

        // 1.4
        h2("1.4. Alcance del proyecto"),
        pNoIndent(
          "El proyecto consiste en desarrollar un sistema de información web denominado " +
          "MultiParking, orientado a automatizar la gestión integral de parqueaderos privados " +
          "de pequeña y mediana escala, tomando como contexto de referencia los " +
          "establecimientos de la localidad de Suba, barrio Compartir, en la ciudad de " +
          "Bogotá D.C. El sistema opera como plataforma web responsiva accesible desde " +
          "dispositivos móviles o computadores de escritorio, sin requerir hardware " +
          "especializado adicional."
        ),
        pBold("El alcance incluye:"),
        bul("Levantamiento y documentación de requerimientos funcionales y no funcionales."),
        bul("Diseño de la arquitectura del sistema y la base de datos relacional (PostgreSQL)."),
        bul(
          "Desarrollo de nueve módulos funcionales: usuarios, vehículos, pisos y espacios, " +
          "inventario de parqueos, tarifas, pagos, cupones de descuento, reservas, novedades " +
          "operativas, fidelización y reportes."
        ),
        bul("Notificaciones automáticas por correo electrónico mediante SendGrid."),
        bul("Exportación de reportes en formato PDF (reportlab) y Excel (openpyxl)."),
        bul("Despliegue y puesta en producción en Render.com con integración continua (CI/CD)."),
        bul("Documentación técnica completa del sistema."),

        pBold("Quedan fuera del alcance:"),
        bul("Integración con hardware automatizado (barreras vehiculares, sensores de presencia, cámaras de reconocimiento de placas)."),
        bul("Desarrollo de aplicación móvil nativa (iOS/Android)."),
        bul("Integración con pasarelas de pago en línea (contemplada para versiones futuras)."),
        bul("Módulo de facturación electrónica DIAN."),
        pb(),

        // ══════════════════════════════════════════════════════════════════
        // 2. OBJETIVOS DEL TRABAJO FINAL DE PROYECTO FORMATIVO (TFPF)
        // ══════════════════════════════════════════════════════════════════
        h1("2. Objetivos del Trabajo Final de Proyecto Formativo (TFPF)"),

        // 2.1
        h2("2.1. Objetivo general"),
        pNoIndent(
          "Desarrollar un sistema de información web que permita la gestión integral de " +
          "parqueaderos privados en la localidad de Suba, barrio Compartir, de la ciudad de " +
          "Bogotá D.C., optimizando el control de ingreso y salida de vehículos, la asignación " +
          "de espacios en tiempo real, el cálculo automático de tarifas, la gestión de reservas " +
          "anticipadas, el seguimiento de novedades operativas y la fidelización de usuarios " +
          "mediante una plataforma accesible, segura y escalable."
        ),

        // 2.2
        h2("2.2. Objetivos específicos"),

        fase("Fase de inicio:"),
        bul(
          "Analizar los procesos actuales de operación y control en parqueaderos privados de " +
          "la localidad de Suba para identificar los requerimientos funcionales y no " +
          "funcionales del sistema."
        ),
        bul(
          "Identificar las necesidades de los usuarios (administradores, vigilantes y clientes) " +
          "mediante la aplicación de encuestas digitales y observación directa en el entorno real."
        ),

        fase("Fase de planificación:"),
        bul(
          "Diseñar la arquitectura del sistema web bajo el patrón MVT (Modelo-Vista-Template), " +
          "definiendo la estructura de la base de datos relacional, los módulos funcionales y " +
          "las interfaces de usuario por rol."
        ),
        bul(
          "Elaborar los diagramas de análisis y diseño requeridos: casos de uso, actividades, " +
          "secuencias, clases y modelo entidad-relación."
        ),

        fase("Fase de ejecución:"),
        bul(
          "Desarrollar los nueve módulos principales del sistema: usuarios, vehículos, pisos y " +
          "espacios, inventario de parqueos, tarifas, pagos, cupones de descuento, reservas, " +
          "novedades operativas, programa de fidelización y reportes."
        ),
        bul(
          "Implementar el cálculo automático de tarifas por minuto, las notificaciones " +
          "automáticas por correo electrónico mediante SendGrid y la exportación de reportes " +
          "en formatos PDF y Excel."
        ),
        bul(
          "Garantizar la seguridad del sistema mediante autenticación por sesión propia, " +
          "control de acceso basado en roles (ADMIN, VIGILANTE, CLIENTE), política de " +
          "cabeceras CSP y protección CSRF."
        ),

        fase("Fase de implementación:"),
        bul(
          "Desplegar el sistema en la plataforma Render.com, configurando el entorno de " +
          "producción con PostgreSQL, variables de entorno seguras e integración continua (CI/CD)."
        ),
        bul(
          "Capacitar al personal operativo del parqueadero y realizar pruebas piloto con " +
          "datos reales antes de la puesta en marcha definitiva."
        ),
        bul(
          "Documentar el sistema conforme a la estructura del programa ADSO-SENA y las " +
          "normas de presentación APA séptima edición."
        ),

        // 2.3
        h2("2.3. Alcance del proyecto"),
        pNoIndent(
          "El sistema MultiParking está diseñado para dar solución a las necesidades operativas " +
          "de parqueaderos privados de pequeña y mediana escala, con especial referencia a los " +
          "establecimientos ubicados en la localidad de Suba, barrio Compartir, Bogotá D.C. " +
          "No obstante, la solución es generalizable a cualquier parqueadero privado con " +
          "características similares en el territorio nacional."
        ),

        pBold("El proyecto abarca las siguientes fases y entregables:"),
        bul(
          "Levantamiento y documentación de requerimientos funcionales (RF), no funcionales " +
          "(RNF), normativos y reglas de negocio."
        ),
        bul(
          "Diseño de la arquitectura del sistema y la base de datos relacional (PostgreSQL) " +
          "con su respectivo diccionario de datos, triggers y scripts SQL."
        ),
        bul(
          "Desarrollo e integración de nueve módulos funcionales con sus respectivas " +
          "interfaces web responsivas."
        ),
        bul(
          "Notificaciones automáticas por correo electrónico (SendGrid) para novedades " +
          "operativas y recuperación de contraseña."
        ),
        bul("Exportación de reportes en formato PDF (reportlab) y Excel (openpyxl)."),
        bul("Despliegue y puesta en producción en Render.com con configuración de CI/CD."),
        bul("Documentación técnica completa del sistema según estructura SENA ADSO."),

        pBold("Limitaciones y exclusiones del proyecto:"),
        bul(
          "No incluye integración con hardware automatizado (barreras vehiculares, sensores " +
          "de presencia, cámaras de reconocimiento de placas)."
        ),
        bul(
          "No contempla el desarrollo de aplicación móvil nativa (iOS/Android); el sistema " +
          "es web responsivo."
        ),
        bul(
          "No incluye integración con pasarelas de pago en línea (PSE, PayU, Wompi); los " +
          "pagos se registran manualmente en el sistema."
        ),
        bul("No incluye módulo de facturación electrónica DIAN."),
        bul(
          "Las funcionalidades descritas como \"versiones futuras\" en el documento quedan " +
          "fuera del alcance del presente trabajo formativo."
        ),
        pb(),

        // ══════════════════════════════════════════════════════════════════
        // 3. MATRIZ DE RIESGO
        // ══════════════════════════════════════════════════════════════════
        h1("3. Matriz de Riesgo"),
        pNoIndent(
          "Durante la fase de planificación del proyecto se identificaron los principales " +
          "riesgos que podrían afectar el desarrollo, la implementación y la operación del " +
          "sistema MultiParking. La Tabla 1 presenta cada riesgo con su causa, impacto " +
          "potencial, probabilidad de ocurrencia, nivel de riesgo resultante y la estrategia " +
          "de mitigación definida por el equipo de desarrollo."
        ),
        tabLabel("Tabla 1"),
        tabItalic("Matriz de Riesgos del Proyecto MultiParking"),
        buildTablaRiesgos(),
        tabNote(),
        pb(),

        // ══════════════════════════════════════════════════════════════════
        // 4. ELICITACIÓN DE REQUISITOS
        // ══════════════════════════════════════════════════════════════════
        h1("4. Elicitación de Requisitos"),

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

        h2("4.2. Recolección de la información del software a construir"),
        pNoIndent(
          "Para iniciar el desarrollo del sistema MultiParking se realizó una fase de " +
          "recolección de datos con el objetivo de comprender las necesidades reales de " +
          "propietarios, vigilantes y usuarios. La información se obtuvo a través de dos " +
          "técnicas principales: observación directa en parqueaderos privados de la localidad " +
          "de Suba, barrio Compartir, en la ciudad de Bogotá D.C., y encuestas digitales " +
          "dirigidas a usuarios habituales y administradores del sector."
        ),

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

        h2("4.4. Aplicación de la técnica de recolección de información"),
        p(
          "La encuesta se aplicó de forma digital a través de un formulario en línea " +
          "distribuido entre usuarios habituales y personal operativo de parqueaderos privados " +
          "de la localidad de Suba, barrio Compartir. La observación directa se efectuó en " +
          "los mismos establecimientos en días representativos de alta y baja afluencia " +
          "vehicular, registrando los procedimientos de ingreso y salida, los tiempos de " +
          "espera, las modalidades de cobro y las incidencias más frecuentes."
        ),

        h2("4.5. Organización de la información recolectada"),
        h2("4.5.1 Encuesta"),
        p("A continuación se presenta el análisis estadístico de la información recolectada en la encuesta aplicada (n = 13):"),

        pregunta("Pregunta 1:", "¿Con qué frecuencia utilizas parqueaderos públicos o privados?"),
        tabLabel("Tabla 2"), tabItalic("Frecuencia de uso de parqueaderos"),
        buildStatsTable(T2), tabNoteCustom("Elaboración propia (2026)."),
        figImg("fig02.png"), figLabel("Figura 2"), figItalic("Frecuencia de uso de parqueaderos (n = 13)"), figNoteStd(),

        pregunta("Pregunta 2:", "¿Qué medio usas actualmente para pagar en un parqueadero?"),
        tabLabel("Tabla 3"), tabItalic("Medio de pago actual en parqueaderos"),
        buildStatsTable(T3), tabNoteCustom("Elaboración propia (2026)."),
        figImg("fig03.png"), figLabel("Figura 3"), figItalic("Medio de pago actual en parqueaderos (n = 13)"), figNoteStd(),

        pregunta("Pregunta 3:", "¿Cuál es el aspecto que más te molesta al usar un parqueadero?"),
        tabLabel("Tabla 4"), tabItalic("Aspecto más molesto al usar un parqueadero"),
        buildStatsTable(T4), tabNoteCustom("Elaboración propia (2026)."),
        figImg("fig04.png"), figLabel("Figura 4"), figItalic("Aspecto más molesto al usar un parqueadero (n = 13)"), figNoteStd(),

        pregunta("Pregunta 4:", "¿Te gustaría poder ingresar al parqueadero escaneando un código QR?"),
        tabLabel("Tabla 5"), tabItalic("Disposición para ingresar con código QR"),
        buildStatsTable(T5), tabNoteCustom("Elaboración propia (2026)."),
        figImg("fig05.png"), figLabel("Figura 5"), figItalic("Disposición para ingreso con código QR (n = 13)"), figNoteStd(),

        pregunta("Pregunta 5:", "¿Te parecería útil poder ver el tiempo y costo acumulado en tiempo real?"),
        tabLabel("Tabla 6"), tabItalic("Utilidad de visualizar tiempo y costo en tiempo real"),
        buildStatsTable(T6), tabNoteCustom("Elaboración propia (2026)."),
        figImg("fig06.png"), figLabel("Figura 6"), figItalic("Utilidad de visualizar costo en tiempo real (n = 13)"), figNoteStd(),

        pregunta("Pregunta 6:", "¿Usarías una app para reservar espacio de parqueo antes de llegar?"),
        tabLabel("Tabla 7"), tabItalic("Disposición para reservar espacio de parqueo anticipadamente"),
        buildStatsTable(T7), tabNoteCustom("Elaboración propia (2026)."),
        figImg("fig07.png"), figLabel("Figura 7"), figItalic("Disposición para reserva anticipada de espacio (n = 13)"), figNoteStd(),

        pregunta("Pregunta 7:", "¿Cuál sería tu método de pago preferido para este sistema?"),
        tabLabel("Tabla 8"), tabItalic("Método de pago de preferencia para un sistema digital"),
        buildStatsTable(T8), tabNoteCustom("Elaboración propia (2026)."),
        figImg("fig08.png"), figLabel("Figura 8"), figItalic("Método de pago de preferencia para el sistema (n = 13)"), figNoteStd(),

        pregunta("Pregunta 8:", "¿Qué tanto te gustaría que el parqueadero reconociera tu historial para darte descuentos?"),
        tabLabel("Tabla 9"), tabItalic("Interés en que el parqueadero reconozca el historial del usuario para descuentos"),
        buildStatsTable(T9), tabNoteCustom("Elaboración propia (2026)."),
        figImg("fig09.png"), figLabel("Figura 9"), figItalic("Interés en fidelización por historial de uso (n = 13)"), figNoteStd(),

        pregunta("Pregunta 9:", "¿Consideras importante salir del parqueadero rápidamente sin interactuar con personal?"),
        tabLabel("Tabla 10"), tabItalic("Importancia de salir del parqueadero sin interactuar con personal"),
        buildStatsTable(T10), tabNoteCustom("Elaboración propia (2026)."),
        figImg("fig10.png"), figLabel("Figura 10"), figItalic("Importancia de la salida autónoma del parqueadero (n = 13)"), figNoteStd(),

        pregunta("Pregunta 10:", "¿Qué tan dispuesto estarías a usar un sistema de parqueadero completamente automatizado?"),
        tabLabel("Tabla 11"), tabItalic("Disposición para usar un sistema de parqueadero completamente automatizado"),
        buildStatsTable(T11), tabNoteCustom("Elaboración propia (2026)."),
        figImg("fig11.png"), figLabel("Figura 11"), figItalic("Disposición para usar sistema automatizado (n = 13)"), figNoteStd(),

        pregunta("Pregunta 11:", "¿Estarías dispuesto/a a pagar un poco más por un parqueadero automatizado?"),
        tabLabel("Tabla 12"), tabItalic("Disposición para pagar más por un parqueadero automatizado"),
        buildStatsTable(T12), tabNoteCustom("Elaboración propia (2026)."),
        figImg("fig12.png"), figLabel("Figura 12"), figItalic("Disposición de pago por sistema automatizado (n = 13)"), figNoteStd(),

        pregunta("Pregunta 12:", "¿Qué funcionalidad te gustaría que tuviera un parqueadero automatizado?"),
        tabLabel("Tabla 13"), tabItalic("Funcionalidades deseadas en un parqueadero automatizado"),
        buildStatsTable(T13), tabNoteCustom("Elaboración propia (2026)."),
        figImg("fig13.png"), figLabel("Figura 13"), figItalic("Funcionalidades deseadas en parqueadero automatizado (n = 13)"), figNoteStd(),

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
    },
  ],
});

const OUT = "C:/Users/xeodeo/Desktop/Multiparking-Django/DOCUMENTACION/MultiParking_Documentacion.docx";

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(OUT, buffer);
  console.log("OK: " + OUT);
}).catch(err => {
  console.error(err);
  process.exit(1);
});
