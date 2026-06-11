const {
  Document, Packer, Paragraph, TextRun, ImageRun,
  AlignmentType, PageNumber, Footer, LevelFormat
} = require('docx');
const fs = require('fs');

const FONT   = "Times New Roman";
const PT12   = 24;
const DOUBLE = 480;
const MARGIN = 1440;
const INDENT = 720;

const pageFooter = new Footer({
  children: [new Paragraph({
    children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: PT12 })],
    alignment: AlignmentType.RIGHT,
    spacing: { before: 0, after: 0 },
  })],
});

// ── Helpers ────────────────────────────────────────────────────────────────

// Título principal: negrita, centrado (APA nivel 1)
function h1(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12, bold: true })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.CENTER,
  });
}

// Subtítulo de subsección: negrita, izquierda (APA nivel 2)
function h2(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12, bold: true })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.LEFT,
  });
}

// Párrafo sin sangría (primer párrafo tras encabezado — sin TAB en el MD)
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

// Párrafo con sangría + texto en negrita (ej. "El alcance incluye:")
function pBold(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12, bold: true })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.JUSTIFIED,
    indent: { firstLine: INDENT },
  });
}

// Texto centrado (placeholder figura)
function pCenter(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12 })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.CENTER,
  });
}

// Líneas de pie de figura APA 7
function figLabel(text) {   // "Figura 1" — negrita
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12, bold: true })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
  });
}
function figTitle(text) {   // Título en cursiva
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12, italics: true })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
  });
}
function figNote(text) {    // Nota normal
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12 })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
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

// ── Documento ──────────────────────────────────────────────────────────────

const doc = new Document({
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
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN },
      },
    },
    footers: { default: pageFooter },
    children: [

      // ── Título principal ──────────────────────────────────────
      h1("1. Planteamiento y Justificación del Problema"),

      // ── 1.1 Planteamiento del problema ───────────────────────
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

      // ── 1.2 Árbol del problema ────────────────────────────────
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
      figTitle("Árbol del problema del sistema MultiParking"),
      figNote("Nota. Elaboración propia (2026)."),

      // ── 1.3 Justificación ─────────────────────────────────────
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

      // ── 1.4 Alcance del proyecto ──────────────────────────────
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
      bul(
        "Integración con hardware automatizado (barreras vehiculares, sensores de " +
        "presencia, cámaras de reconocimiento de placas)."
      ),
      bul("Desarrollo de aplicación móvil nativa (iOS/Android)."),
      bul("Integración con pasarelas de pago en línea (contemplada para versiones futuras)."),
      bul("Módulo de facturación electrónica DIAN."),
    ],
  }],
});

const OUT = "C:/Users/xeodeo/Desktop/Multiparking-Django/DOCUMENTACION/Secciones/" +
            "Seccion_01_Planteamiento_Problema/seccion_01_planteamiento_justificacion.docx";

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(OUT, buffer);
  console.log("OK: " + OUT);
}).catch(err => {
  console.error(err);
  process.exit(1);
});
