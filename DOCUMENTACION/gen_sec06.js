const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, WidthType, BorderStyle, ShadingType, ImageRun, PageBreak
} = require('docx');
const fs = require('fs');
const path = require('path');

const IMG_DIR = 'C:\\Users\\xeodeo\\Desktop\\Multiparking-Django\\DOCUMENTACION\\Secciones\\Seccion_06_Analisis_Especificacion';
const OUT = path.join(IMG_DIR, 'Seccion_06_Analisis_Especificacion.docx');
const PAGE_W = 9026;

const BORDER = { style: BorderStyle.SINGLE, size: 4, color: '999999' };
const CB = { top: BORDER, bottom: BORDER, left: BORDER, right: BORDER };

function para(text, opts = {}) {
  const { bold = false, italic = false, size = 24, align = AlignmentType.LEFT, spacing = { before: 80, after: 80 } } = opts;
  return new Paragraph({
    alignment: align, indent: { firstLine: 0 }, spacing,
    children: [new TextRun({ text, bold, italic, size, font: 'Times New Roman' })]
  });
}

function heading1(text) {
  return new Paragraph({
    alignment: AlignmentType.LEFT, indent: { firstLine: 0 },
    spacing: { before: 360, after: 120 },
    children: [new TextRun({ text, bold: true, size: 28, font: 'Times New Roman' })]
  });
}

function heading2(text) {
  return new Paragraph({
    alignment: AlignmentType.LEFT, indent: { firstLine: 0 },
    spacing: { before: 240, after: 80 },
    keepNext: true,
    children: [new TextRun({ text, bold: true, size: 26, font: 'Times New Roman' })]
  });
}

function heading3(text) {
  return new Paragraph({
    alignment: AlignmentType.LEFT, indent: { firstLine: 0 },
    spacing: { before: 200, after: 60 },
    keepNext: true,
    children: [new TextRun({ text, bold: true, italic: true, size: 24, font: 'Times New Roman' })]
  });
}

function hCell(text, w) {
  return new TableCell({
    width: { size: w, type: WidthType.DXA }, borders: CB,
    shading: { fill: 'D9D9D9', type: ShadingType.CLEAR },
    margins: { top: 60, bottom: 60, left: 80, right: 80 },
    children: [new Paragraph({ indent: { firstLine: 0 }, spacing: { before: 40, after: 40 },
      children: [new TextRun({ text, bold: true, size: 18, font: 'Times New Roman' })] })]
  });
}

function dCell(text, w, fill = 'FFFFFF', sm = false) {
  return new TableCell({
    width: { size: w, type: WidthType.DXA }, borders: CB,
    shading: { fill: fill || 'FFFFFF', type: ShadingType.CLEAR },
    margins: { top: 60, bottom: 60, left: 80, right: 80 },
    children: [new Paragraph({ indent: { firstLine: 0 }, spacing: { before: 40, after: 40 },
      children: [new TextRun({ text, size: sm ? 16 : 18, font: 'Times New Roman' })] })]
  });
}

function tLabel(n, title) {
  return [
    new Paragraph({ alignment: AlignmentType.LEFT, indent: { firstLine: 0 }, spacing: { before: 240, after: 0 },
      children: [new TextRun({ text: `Tabla ${n}`, bold: true, size: 24, font: 'Times New Roman' })] }),
    new Paragraph({ alignment: AlignmentType.LEFT, indent: { firstLine: 0 }, spacing: { before: 0, after: 80 },
      children: [new TextRun({ text: title, italic: true, size: 24, font: 'Times New Roman' })] })
  ];
}

function tNote(extra = '') {
  return new Paragraph({
    alignment: AlignmentType.LEFT, indent: { firstLine: 0 }, spacing: { before: 80, after: 200 },
    children: [
      new TextRun({ text: 'Nota. ', italic: true, size: 20, font: 'Times New Roman' }),
      new TextRun({ text: (extra || 'Elaboración propia (2026).'), size: 20, font: 'Times New Roman' })
    ]
  });
}

function figLabel(n, title) {
  return new Paragraph({
    alignment: AlignmentType.CENTER, indent: { firstLine: 0 }, spacing: { before: 0, after: 0 },
    keepNext: true,
    children: [new TextRun({ text: `Figura ${n}`, bold: true, size: 22, font: 'Times New Roman' })]
  });
}

function figTitle(title) {
  return new Paragraph({
    alignment: AlignmentType.CENTER, indent: { firstLine: 0 }, spacing: { before: 0, after: 60 },
    keepNext: true,
    children: [new TextRun({ text: title, italic: true, size: 22, font: 'Times New Roman' })]
  });
}

function figNote(extra = '') {
  return new Paragraph({
    alignment: AlignmentType.LEFT, indent: { firstLine: 0 }, spacing: { before: 40, after: 200 },
    children: [
      new TextRun({ text: 'Nota. ', italic: true, size: 20, font: 'Times New Roman' }),
      new TextRun({ text: extra || 'Elaboración propia mediante PlantUML (2026).', size: 20, font: 'Times New Roman' })
    ]
  });
}

function imgPara(filename, w, h) {
  const imgPath = path.join(IMG_DIR, filename);
  if (!fs.existsSync(imgPath)) {
    return new Paragraph({ indent: { firstLine: 0 },
      children: [new TextRun({ text: `[Imagen no encontrada: ${filename}]`, italic: true, size: 20, font: 'Times New Roman', color: 'FF0000' })] });
  }
  const data = fs.readFileSync(imgPath);
  const ext = path.extname(filename).toLowerCase();
  const type = (ext === '.jpg' || ext === '.jpeg') ? 'jpg' : 'png';
  return new Paragraph({
    alignment: AlignmentType.CENTER, indent: { firstLine: 0 }, spacing: { before: 120, after: 40 },
    keepNext: true,
    children: [new ImageRun({ data, transformation: { width: w, height: h }, type })]
  });
}

function priColor(pri) {
  if (pri === 'Alta') return 'FFCCCC';
  if (pri === 'Media') return 'FFF2CC';
  return 'FFFFFF';
}

// HU Table builder
// cols: [ID, Rol, Historia, Criterios, Prioridad]
// W: [500, 700, 2800, 3626, 700] total = PAGE_W ~ 9026? adjust: 500+700+2600+3726+700=8226... let me recalc
// HU_W: ID=500, Rol=800, Historia=2400, Criterios=3826, Pri=700 = 8226... hmm, let me use: 500+700+2500+4026+700=8426
// Actually use simpler: [500, 700, 2200, 3826, 800] = 8026

const HU_W = [500, 700, 2500, 4426, 700]; // ID, Rol, Historia, Criterios, Prioridad ~ 8826

function huTable(rows) {
  const header = new TableRow({
    tableHeader: true,
    children: [
      hCell('ID', HU_W[0]),
      hCell('Rol', HU_W[1]),
      hCell('Historia de Usuario', HU_W[2]),
      hCell('Criterios de Aceptación', HU_W[3]),
      hCell('Prioridad', HU_W[4])
    ]
  });
  const dataRows = rows.map(([id, rol, historia, criterios, pri]) =>
    new TableRow({ children: [
      dCell(id, HU_W[0]),
      dCell(rol, HU_W[1]),
      dCell(historia, HU_W[2]),
      dCell(criterios, HU_W[3], priColor(pri)),
      dCell(pri, HU_W[4], priColor(pri))
    ]})
  );
  return new Table({ rows: [header, ...dataRows], width: { size: PAGE_W, type: WidthType.DXA } });
}

// Relation table builder
const REL_W = [1200, 800, 6826]; // Relación, Tipo, Descripción

function relTable(rows) {
  const header = new TableRow({
    tableHeader: true,
    children: [hCell('Relación', REL_W[0]), hCell('Tipo', REL_W[1]), hCell('Descripción', REL_W[2])]
  });
  const dataRows = rows.map(([rel, tipo, desc]) =>
    new TableRow({ children: [dCell(rel, REL_W[0], null, true), dCell(tipo, REL_W[1], null, true), dCell(desc, REL_W[2], null, true)] })
  );
  return new Table({ rows: [header, ...dataRows], width: { size: PAGE_W, type: WidthType.DXA } });
}

// Simple 2-col table
function simpleTable(headers, rows, widths) {
  const header = new TableRow({ tableHeader: true, children: headers.map((h, i) => hCell(h, widths[i])) });
  const dataRows = rows.map(row =>
    new TableRow({ children: row.map((c, i) => dCell(c, widths[i], null, true)) })
  );
  return new Table({ rows: [header, ...dataRows], width: { size: PAGE_W, type: WidthType.DXA } });
}

// ===========================================================
// BUILD DOCUMENT
// ===========================================================
const children = [];

// ---- SECTION HEADING ----
children.push(heading1('6. ANÁLISIS Y ESPECIFICACIÓN DEL SISTEMA'));

// ---- 6.1 MOCKUPS ----
children.push(heading2('6.1 Mockups / Interfaces del Sistema'));
children.push(para('Dado que el sistema MultiParking fue desarrollado e implementado en su totalidad, las pantallas que se presentan a continuación corresponden a las interfaces finales del sistema, las cuales fueron concebidas durante la fase de diseño conceptual y materializadas en la implementación con Django Templates y Tailwind CSS.'));
children.push(para('El sistema cuenta con tres módulos de interfaz diferenciados por rol, cada uno con rutas y vistas específicas:'));

children.push(...tLabel(35, 'Módulos de Interfaz del Sistema MultiParking por Rol'));
children.push(simpleTable(
  ['Módulo', 'URL Base', 'Descripción'],
  [
    ['Panel Administrador', '/admin-panel/', 'CRUD completo de todos los módulos, reportes y mapa interactivo de espacios'],
    ['Panel Vigilante', '/guardia/', 'Registro de ingreso, salida de vehículos y confirmación de pago en efectivo'],
    ['Panel Cliente', '/dashboard/ y /cliente/', 'Consulta de vehículos, reservas anticipadas, perfil y bono de fidelidad'],
    ['Autenticación', '/login/, /register/', 'Inicio de sesión con rol, registro de nuevos usuarios y recuperación de contraseña']
  ],
  [1800, 1600, 5426]
));
children.push(tNote('Las interfaces siguen diseño responsive con Tailwind CSS (CDN). El administrador accede al mapa interactivo de espacios que muestra el estado de cada espacio en tiempo real con codificación de colores (verde: DISPONIBLE, rojo: OCUPADO, azul: RESERVADO, gris: INACTIVO). Elaboración propia (2026).'));

children.push(para('A continuación se presentan los mockups de las interfaces principales del sistema, elaborados durante la fase de diseño y que sirvieron como guía para la implementación final.'));

const MOCK_images = [
  ['MOCK_home.jpeg',    480, 360, '6.1.1', 'Página de Inicio — MultiParking',
   'Pantalla pública de bienvenida con acceso al inicio de sesión. Presenta las tres características principales del sistema: ingreso con código QR, pagos digitales y acceso diferenciado por roles.'],
  ['MOCK_admin_1.jpeg', 520, 410, '6.1.2', 'Panel Administrador — Dashboard Principal',
   'Vista principal del administrador. Muestra indicadores clave: total de espacios (120), espacios disponibles (34), ganancias del día ($62.400) y reservas activas (8). Incluye el resumen de pisos con el estado visual de cada espacio (disponible, ocupado, reservado).'],
  ['MOCK_admin_2.jpeg', 520, 410, '6.1.3', 'Panel Administrador — Resumen de Reservas',
   'Vista de gestión de reservas activas del administrador. Presenta una tabla con piso, usuario, vehículo, hora, duración, valor y estado de cada reserva. Incluye gráficos de ocupación por hora e ingresos por turno (día, tarde, noche).'],
  ['MOCK_guardia.jpeg', 560, 307, '6.1.4', 'Panel Vigilante — Solicitudes de Entrada y Salida',
   'Interfaz del vigilante (celador). Muestra los contadores de entradas pendientes, salidas pendientes, pagos pendientes y parqueaderos activos. Las secciones principales permiten verificar y autorizar solicitudes de entrada, así como autorizar salidas y pagos de los vehículos activos.'],
  ['MOCK_usuario.jpeg', 560, 347, '6.1.5', 'Panel Cliente — Dashboard del Usuario',
   'Panel de autoservicio del cliente registrado. Accesos rápidos a: entrar al parqueadero (QR), gestionar vehículos, hacer reservación y marcar salida. Muestra los vehículos registrados con su estado, las reservas activas con fecha de confirmación y el historial de pagos con monto, placa, duración y método de pago.']
];

for (const [filename, w, h, figNum, figTitleText, desc] of MOCK_images) {
  children.push(figLabel(figNum, figTitleText));
  children.push(figTitle(figTitleText));
  children.push(imgPara(filename, w, h));
  children.push(figNote(`Mockup de interfaz — ${figTitleText}. Elaboración propia (2026).`));
  children.push(para(desc, { size: 22, spacing: { before: 60, after: 160 } }));
}

// ---- 6.2 HISTORIAS DE USUARIO ----
children.push(heading2('6.2 Historias de Usuario'));
children.push(para('Las historias de usuario del proyecto MultiParking se gestionan en el tablero Trello del equipo, organizadas por sprints de desarrollo. El tablero está disponible en: https://trello.com/b/nL1GvfLi/multiparking'));
children.push(para('El desarrollo se estructuró en 9 sprints (Sprint 0 al Sprint 8), cada uno con tarjetas que representan funcionalidades en formato de historia de usuario: Como [rol], quiero [acción], para [beneficio].'));

children.push(...tLabel(36, 'Sprints y Módulos Cubiertos en el Tablero Trello — MultiParking'));
children.push(simpleTable(
  ['Sprint', 'Nombre', 'Módulos / Funcionalidades Cubiertas', 'Estado'],
  [
    ['Sprint 0', 'Infraestructura Base', 'Configuración Django, base de datos MySQL/PostgreSQL, autenticación por sesión, sistema de roles', 'Completado'],
    ['Sprint 1', 'Usuarios, Vehículos y Espacios', 'CRUD usuarios (3 roles), registro/edición de vehículos y visitantes, gestión de pisos y espacios', 'Completado'],
    ['Sprint 2', 'Inventario, Tarifas, Pagos y Cupones', 'Registro ingreso/salida, cálculo de tarifas por tipo, creación de pagos, gestión de cupones', 'Completado'],
    ['Sprint 3', 'Flujo Principal Finalizado', 'Integración y pruebas del flujo completo ingreso-salida-pago', 'Completado'],
    ['Sprint 4', 'Pagos Avanzados y Cupones', 'Aplicación de cupones al pago, tipos PORCENTAJE y VALOR_FIJO, registro CuponAplicado', 'Completado'],
    ['Sprint 5', 'Reservas y Puntos de Fidelidad', 'Reservas anticipadas con validación de conflictos, sistema de stickers, reclamación de bono', 'Completado'],
    ['Sprint 6', 'Novedades y Reportes', 'Registro de incidencias con foto, gestión de estados de novedad, reportes PDF y Excel', 'Completado'],
    ['Sprint 7', 'Auditoría, Perfil y UX', 'Mapa interactivo de espacios, panel cliente, ingreso por código QR, mejoras de interfaz', 'Completado'],
    ['Sprint 8', 'Seguridad, Calidad y Cierre', 'Middleware de seguridad (CSP, no-cache), validaciones multicapa, pruebas y despliegue Render.com', 'En Progreso']
  ],
  [600, 1600, 5026, 900]
));
children.push(tNote('Las historias de usuario detalladas por sprint están disponibles en el tablero Trello del proyecto: https://trello.com/b/nL1GvfLi/multiparking. Elaboración propia (2026).'));

// ---- 6.3 DIAGRAMAS DE CASOS DE USO ----
children.push(heading2('6.3 Diagramas UML de Casos de Uso'));
children.push(para('Los diagramas de casos de uso describen las interacciones entre los actores del sistema y los módulos funcionales. Los actores identificados son: Administrador, Vigilante, Usuario/Cliente y Sistema de Correo (SendGrid). Se presentan 11 diagramas organizados por módulo funcional.'));

const CU_images = [
  ['caso_uso_V3_img6.png', 520, 310, '6.3.1', 'Módulo Usuarios'],
  ['caso_uso_V3_img2.png', 520, 310, '6.3.2', 'Módulo Vehículos'],
  ['CU_09_parqueos.png',   520, 280, '6.3.3', 'Módulo Parqueos (Ingreso)'],
  ['CU_03_salida_pagos.png', 520, 300, '6.3.4', 'Módulo Salida y Pagos'],
  ['caso_uso_V3_img10.png', 520, 310, '6.3.5', 'Módulo Espacios y Tarifas'],
  ['caso_uso_V3_img5.png',  520, 280, '6.3.6', 'Módulo Reservas'],
  ['caso_uso_V3_img8.png',  480, 240, '6.3.7', 'Módulo Descuentos (Cupones)'],
  ['CU_11_fidelidad.png',   520, 300, '6.3.8', 'Módulo Fidelidad (Stickers)'],
  ['CU_12_novedades.png',   520, 320, '6.3.9', 'Módulo Novedades'],
  ['caso_uso_V3_img1.png',  520, 260, '6.3.10', 'Módulo Vigilante'],
  ['caso_uso_V3_img4.png',  480, 240, '6.3.11', 'Módulo Auditoría y Reportes']
];

for (const [filename, w, h, figNum, figTitleText] of CU_images) {
  children.push(figLabel(figNum, figTitleText));
  children.push(figTitle(figTitleText));
  children.push(imgPara(filename, w, h));
  children.push(figNote(`Diagrama UML de casos de uso — ${figTitleText}. Elaboración propia mediante PlantUML (2026).`));
}

// ---- 6.4 DIAGRAMAS DE ACTIVIDADES ----
children.push(heading2('6.4 Diagramas de Actividades'));
children.push(para('Los diagramas de actividades describen el flujo de ejecución de los procesos principales del sistema MultiParking. Se presentan cuatro diagramas que cubren los flujos críticos de negocio.'));

const ACT_images = [
  ['ACT_01_ingreso.png', 520, 480, '6.4.1', 'Registro de Ingreso de Vehículo',
   'El vigilante o usuario busca el vehículo por placa o QR. Si no existe, se registra como visitante. El sistema verifica que no tenga un ingreso activo y que exista espacio disponible. Al confirmar, crea el InventarioParqueo con la hora de entrada y cambia el espacio a OCUPADO.'],
  ['ACT_02_salida_pago.png', 520, 700, '6.4.2', 'Registro de Salida y Pago',
   'El sistema localiza el registro activo del vehículo y calcula la duración. Aplica la tarifa vigente (precioHoraVisitante para visitantes). Opcionalmente se aplica un cupón. Se registra hora de salida, se crea el Pago, se libera el espacio y se verifica si corresponde otorgar un Sticker. El monto se calcula como (minutos / 60) × precioHora, redondeado al múltiplo de 100 COP.'],
  ['ACT_03_reserva.png', 520, 600, '6.4.3', 'Proceso de Reserva Anticipada',
   'El cliente selecciona su vehículo y el horario deseado. El sistema verifica disponibilidad y detecta conflictos con otras reservas del mismo vehículo. Al no haber conflictos, crea la Reserva en PENDIENTE. El cliente puede confirmarla (CONFIRMADA, espacio a RESERVADO) o cancelarla (libera el espacio).'],
  ['ACT_04_fidelidad.png', 520, 520, '6.4.4', 'Reclamar Bono de Fidelidad',
   'El cliente consulta sus stickers acumulados. Si alcanzó la metaStickers configurada y no tiene un bono activo sin usar, puede reclamar un cupón de descuento del 100% con vigencia de diasVencimientoBono días a partir de la fecha de reclamación.']
];

for (const [filename, w, h, figNum, figTitleText, desc] of ACT_images) {
  children.push(figLabel(figNum, figTitleText));
  children.push(figTitle(figTitleText));
  children.push(imgPara(filename, w, h));
  children.push(figNote(`Diagrama de actividad UML — ${figTitleText}. Elaboración propia mediante PlantUML (2026).`));
  children.push(para(desc, { size: 22, spacing: { before: 60, after: 120 } }));
}

// ---- 6.5 DIAGRAMAS DE SECUENCIAS ----
children.push(heading2('6.5 Diagramas de Secuencias'));
children.push(para('Los diagramas de secuencias muestran la interacción temporal entre los objetos del sistema para los flujos más representativos del ciclo de operación del parqueadero.'));

children.push(figLabel('6.5.1', 'Secuencia: Inicio de Sesión'));
children.push(figTitle('Secuencia: Inicio de Sesión'));
children.push(imgPara('SEQ_01_login.png', 580, 440));
children.push(figNote('Diagrama de secuencia UML — Proceso de autenticación de usuario en el sistema. Elaboración propia mediante PlantUML (2026).'));
children.push(para('El usuario envía sus credenciales vía POST /login/. La vista login en usuarios/views.py consulta la base de datos por el correo, verifica la contraseña con check_password(), valida el estado de la cuenta y crea la sesión Django con las claves usuario_id, usuario_rol y usuario_nombre. La redirección final depende del rol: ADMIN hacia /admin-panel/, VIGILANTE hacia /guardia/, CLIENTE hacia /dashboard/.', { size: 22, spacing: { before: 60, after: 160 } }));

children.push(figLabel('6.5.2', 'Secuencia: Registro de Ingreso y Salida con Pago'));
children.push(figTitle('Secuencia: Registro de Ingreso y Salida con Pago'));
children.push(imgPara('SEQ_02_ingreso_salida.png', 560, 680));
children.push(figNote('Diagrama de secuencia UML — Proceso completo de ingreso y salida de vehículo con registro de pago. Elaboración propia mediante PlantUML (2026).'));
children.push(para('El diagrama muestra dos fases secuenciales. En la Fase 1 (Ingreso), la vista registrar_ingreso en parqueadero/views.py busca el vehículo por placa, verifica que no tenga un ingreso activo (parHoraSalida IS NULL), actualiza el estado del espacio a OCUPADO y crea el InventarioParqueo. En la Fase 2 (Salida), la vista registrar_salida localiza el registro activo, obtiene la tarifa vigente, calcula el monto, registra la hora de salida, libera el espacio y crea el Pago. Si la estadía supera 1 hora y el vehículo pertenece a un cliente registrado, crea además un Sticker.', { size: 22, spacing: { before: 60, after: 160 } }));

// ---- 6.6 MODELO DE DOMINIO ----
children.push(heading2('6.6 Modelo de Dominio (Diagrama de Clases)'));
children.push(para('El modelo de dominio representa las entidades principales del sistema MultiParking, sus atributos y las relaciones entre ellas. Corresponde directamente a los modelos Django definidos en cada aplicación del proyecto. El sistema cuenta con 14 modelos distribuidos en 9 aplicaciones Django.'));

children.push(figLabel('6.6.1', 'Diagrama de Clases — Modelo de Dominio MultiParking'));
children.push(figTitle('Diagrama de Clases — Modelo de Dominio MultiParking'));
children.push(imgPara('CLASE_dominio.png', 600, 720));
children.push(figNote('Diagrama UML de clases — Modelo de dominio completo del sistema MultiParking con los 14 modelos Django, sus atributos y relaciones. Elaboración propia mediante PlantUML (2026).'));

children.push(...tLabel(42, 'Relaciones Principales del Modelo de Dominio MultiParking'));
children.push(relTable([
  ['Usuario → Vehiculo', '1 a N (opcional)', 'Un usuario puede tener muchos vehículos. Los vehículos visitantes tienen fkIdUsuario = NULL (es_visitante = True).'],
  ['Vehiculo → InventarioParqueo', '1 a N', 'Cada vehículo puede tener múltiples registros históricos de parqueo. Solo uno puede estar activo (parHoraSalida IS NULL) simultáneamente.'],
  ['Espacio → InventarioParqueo', '1 a N', 'Un espacio puede tener múltiples registros históricos. Solo uno activo a la vez.'],
  ['Piso → Espacio', '1 a N', 'Cada piso contiene múltiples espacios físicos. No se puede eliminar un piso con espacios ocupados.'],
  ['TipoEspacio → Espacio', '1 a N', 'Cada espacio tiene un tipo (moto, carro, bicicleta, etc.) que determina la tarifa aplicable.'],
  ['TipoEspacio → Tarifa', '1 a N (una activa)', 'Cada tipo de espacio tiene su propia tarifa. Solo puede haber una tarifa activa por TipoEspacio en un momento dado.'],
  ['InventarioParqueo → Pago', '1 a 1 (opcional)', 'Cada registro de parqueo completado (con parHoraSalida) genera exactamente un pago.'],
  ['Pago → CuponAplicado', '1 a N', 'Un pago puede tener cupones de descuento aplicados (generalmente uno).'],
  ['Cupon → CuponAplicado', '1 a N', 'Un cupón puede ser usado en múltiples pagos a lo largo de su vigencia.'],
  ['Espacio → Reserva', '1 a N', 'Un espacio puede tener múltiples reservas en diferentes horarios sin conflicto.'],
  ['Vehiculo → Reserva', '1 a N', 'Un vehículo puede tener múltiples reservas. El sistema detecta conflictos de horario.'],
  ['InventarioParqueo → Sticker', '1 a 1', 'Por cada estadía mayor a 1 hora se genera exactamente un Sticker (OneToOneField). Solo para clientes registrados.'],
  ['Usuario → Sticker', '1 a N', 'Un usuario acumula múltiples stickers a lo largo del tiempo hasta alcanzar la metaStickers.'],
  ['Usuario → Novedad', '1 a N (x2)', 'El vigilante (fkIdReportador) reporta novedades; el administrador (fkIdResponsable) las gestiona y resuelve.']
]));
children.push(tNote());

children.push(...tLabel(43, 'Propiedades Derivadas del Modelo (No Almacenadas en Base de Datos)'));
children.push(simpleTable(
  ['Propiedad @property', 'Clase', 'Descripción'],
  [
    ['usuNombreCompleto', 'Usuario', 'Concatena usuNombre + " " + usuApellido. No almacenada en BD.'],
    ['es_visitante', 'Vehiculo', 'Retorna True cuando fkIdUsuario es NULL. Distingue vehículos de visitantes vs. clientes registrados.'],
    ['resConfirmada', 'Reserva', 'Retorna True cuando resEstado == "CONFIRMADA". Propiedad de conveniencia para plantillas.']
  ],
  [2000, 1500, 5326]
));
children.push(tNote());

// ================================================================
// PACK AND SAVE
// ================================================================
const doc = new Document({ sections: [{ properties: {}, children }] });
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT, buf);
  const kb = (buf.length / 1024).toFixed(1);
  const paragraphs = children.filter(c => c instanceof Paragraph).length;
  console.log(`OK: ${OUT}`);
  console.log(`Tamanio: ${kb} KB | Paragrafos/elementos: ${children.length}`);
}).catch(e => { console.error('ERROR:', e.message); process.exit(1); });
