const {
  Document, Packer, Paragraph, TextRun,
  AlignmentType, PageNumber, Footer, SectionType, PageBreak
} = require('docx');
const fs = require('fs');

const FONT  = "Times New Roman";
const PT12  = 24;
const PT14  = 28;
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

function empty() {
  return new Paragraph({
    children: [new TextRun({ text: "", font: FONT, size: PT12 })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
  });
}

function coverLine(text, bold, size) {
  return new Paragraph({
    children: [new TextRun({ text: text, font: FONT, size: size || PT12, bold: !!bold })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.CENTER,
  });
}

function secTitle(text) {
  return new Paragraph({
    children: [new TextRun({ text: text, font: FONT, size: PT12, bold: true })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.CENTER,
  });
}

function bodyPara(text) {
  return new Paragraph({
    children: [new TextRun({ text: text, font: FONT, size: PT12 })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.JUSTIFIED,
    indent: { firstLine: INDENT },
  });
}

function abstractPara(text) {
  return new Paragraph({
    children: [new TextRun({ text: text, font: FONT, size: PT12 })],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
    alignment: AlignmentType.JUSTIFIED,
  });
}

function kwLine(label, terms) {
  return new Paragraph({
    children: [
      new TextRun({ text: label, font: FONT, size: PT12, italics: true }),
      new TextRun({ text: " " + terms, font: FONT, size: PT12 }),
    ],
    spacing: { line: DOUBLE, lineRule: "auto", before: 0, after: 0 },
  });
}

function pb() {
  return new Paragraph({ children: [new PageBreak()] });
}

const doc = new Document({
  sections: [

    // ──────────────────────────────────────────
    // SECCIÓN 1 — PORTADA (sin numeración)
    // ──────────────────────────────────────────
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN },
        },
      },
      children: [
        // Espacio vertical ~2 pulgadas antes del título
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

    // ──────────────────────────────────────────
    // SECCIÓN 2 — RESUMEN · ABSTRACT · INTRODUCCIÓN
    // (numeración desde página 1)
    // ──────────────────────────────────────────
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

        // ── RESUMEN ──
        secTitle("Resumen"),
        empty(),
        abstractPara(
          "MultiParking es un sistema de información web orientado a la automatización y " +
          "gestión integral de parqueaderos privados de pequeña y mediana escala. La plataforma " +
          "permite el registro de usuarios con tres roles diferenciados: administrador, vigilante " +
          "y cliente; el control de vehículos propios y visitantes; la asignación y liberación de " +
          "espacios en tiempo real sobre un plano interactivo por pisos; el cálculo automático de " +
          "tarifas por minuto con redondeo a cien pesos colombianos; la generación y registro de " +
          "pagos; la aplicación de cupones de descuento por porcentaje o valor fijo; la gestión de " +
          "reservas anticipadas; el registro fotográfico de novedades operativas con notificación " +
          "automática por correo electrónico; un sistema de fidelización mediante stickers " +
          "acumulables canjeables por bonos de descuento; y la generación de reportes exportables " +
          "en formato PDF y Excel. El sistema fue desarrollado en Python con el framework Django, " +
          "empleando PostgreSQL como gestor de base de datos en el entorno de producción desplegado " +
          "en Render.com, Tailwind CSS para el diseño responsivo, SendGrid para el envío de correos " +
          "transaccionales y Gunicorn como servidor WSGI. La arquitectura sigue el patrón " +
          "MVT (Modelo-Vista-Template) con autenticación por sesión propia y control de acceso " +
          "basado en roles."
        ),
        empty(),
        kwLine("Palabras clave:", "parqueadero, sistema de información web, Django, PostgreSQL, gestión de espacios, fidelización, roles de usuario."),

        pb(),

        // ── ABSTRACT ──
        secTitle("Abstract"),
        empty(),
        abstractPara(
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
        empty(),
        kwLine("Keywords:", "parking lot, web information system, Django, PostgreSQL, space management, loyalty program, role-based access."),

        pb(),

        // ── INTRODUCCIÓN ──
        // Párrafo 1: sin sangría (no lleva TAB en el MD)
        // Párrafos 2-4: con sangría de primera línea (llevan TAB en el MD)
        secTitle("Introducción"),
        abstractPara(
          "En la ciudad de Bogotá D.C., específicamente en la localidad de Suba, barrio " +
          "Compartir, los parqueaderos privados de pequeña y mediana escala operan con métodos " +
          "manuales que generan ineficiencias operativas: registros en papel, cálculos de tarifa " +
          "imprecisos, ausencia de trazabilidad y nula visibilidad del estado de los espacios en " +
          "tiempo real. Esta situación, observable también en numerosos establecimientos similares " +
          "a nivel nacional, deriva en pérdida de ingresos, inconformidad de los usuarios y " +
          "dificultad para tomar decisiones basadas en datos (García & Martínez, 2022)."
        ),
        bodyPara(
          "El proyecto MultiParking desarrolla una solución web que automatiza de forma integral " +
          "la operación de parqueaderos privados. El sistema registra ingresos y salidas de " +
          "vehículos, calcula tarifas en tiempo real, gestiona reservas anticipadas, emite " +
          "notificaciones digitales, aplica descuentos mediante cupones y acumula beneficios de " +
          "fidelización para los usuarios registrados."
        ),
        bodyPara(
          "La arquitectura tecnológica se apoya en Django (Python 3.12), PostgreSQL en producción " +
          "(Render.com), Tailwind CSS vía CDN, Chart.js para visualizaciones estadísticas, " +
          "SendGrid como proveedor de correo transaccional y Gunicorn como servidor WSGI. La " +
          "autenticación implementa un modelo de sesión propio —sin dependencia del módulo " +
          "django.contrib.auth.User— con tres roles de acceso: ADMIN, VIGILANTE y CLIENTE, " +
          "cada uno con vistas y permisos diferenciados."
        ),
        bodyPara(
          "El presente documento sigue la estructura definida por el programa Análisis y " +
          "Desarrollo de Software (ADSO) del Servicio Nacional de Aprendizaje (SENA) para el " +
          "Trabajo Final del Proyecto Formativo (TFPF), y las normas de presentación y citación " +
          "APA séptima edición (American Psychological Association, 2020)."
        ),
      ],
    },
  ],
});

const OUT = "C:/Users/xeodeo/Desktop/Multiparking-Django/DOCUMENTACION/Secciones/Seccion_00_Portada_Resumen/seccion_00_portada_resumen_abstract_introduccion.docx";

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(OUT, buffer);
  console.log("OK: " + OUT);
}).catch(err => {
  console.error(err);
  process.exit(1);
});
