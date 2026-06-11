const {
  Document, Packer, Paragraph, TextRun,
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

// Primer párrafo tras encabezado — sin sangría
function pNoIndent(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12 })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.JUSTIFIED,
  });
}

// Párrafo con sangría de primera línea
function p(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12 })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.JUSTIFIED,
    indent: { firstLine: INDENT },
  });
}

// Etiqueta de fase — negrita, sin sangría (Fase de inicio:, etc.)
function fase(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12, bold: true })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.LEFT,
  });
}

// Lead-in con sangría + negrita (El proyecto abarca..., Limitaciones...)
function pBold(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: PT12, bold: true })],
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

      // ── Título principal ──────────────────────────────────────────────
      h1("2. Objetivos del Trabajo Final de Proyecto Formativo (TFPF)"),

      // ── 2.1 Objetivo general ─────────────────────────────────────────
      h2("2.1. Objetivo general"),
      pNoIndent(
        "Desarrollar un sistema de información web que permita la gestión integral de " +
        "parqueaderos privados en la localidad de Suba, barrio Compartir, de la ciudad de " +
        "Bogotá D.C., optimizando el control de ingreso y salida de vehículos, la asignación " +
        "de espacios en tiempo real, el cálculo automático de tarifas, la gestión de reservas " +
        "anticipadas, el seguimiento de novedades operativas y la fidelización de usuarios " +
        "mediante una plataforma accesible, segura y escalable."
      ),

      // ── 2.2 Objetivos específicos ─────────────────────────────────────
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

      // ── 2.3 Alcance del proyecto ──────────────────────────────────────
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
    ],
  }],
});

const OUT = "C:/Users/xeodeo/Desktop/Multiparking-Django/DOCUMENTACION/Secciones/" +
            "Seccion_02_Objetivos/seccion_02_objetivos.docx";

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(OUT, buffer);
  console.log("OK: " + OUT);
}).catch(err => { console.error(err); process.exit(1); });
