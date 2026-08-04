# Graph Report - Multiparking-Django  (2026-08-04)

## Corpus Check
- 234 files · ~1,020,605 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1321 nodes · 2167 edges · 113 communities (84 shown, 29 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 306 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `63f1537b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- multiparking/urls.py
- Cupon
- Guía de Datos de Demostración
- gen_fusionado.js
- Verification Checklist
- Usuario
- gen_seccion_04.js
- DOCUMENTOS FALTANTES
- tarifas/views.py
- MultiParking
- 6.3 Diagrama UML de Casos de Uso
- CLAUDE.md
- gen_sec06.js
- email_utils.py
- Database Schema Designer
- AdminRequiredMixin
- MÓDULOS
- 2026-05-29 — SESIÓN 1: Exploración e Inventario Inicial
- Norma: APA 7ma edición
- novedades/views.py
- build_docx.py
- ROADMAP DE DOCUMENTACIÓN — Multiparking
- Adición RF63 (escaneo QR) identificada en verificación cruzada — presente en CLAUDE.md y /parqueadero/escanear/
- 📋 Guión Completo
- Database Schema Design Checklist
- gen_seccion_03.js
- Estructura de Base de Datos
- vehiculos/cliente_views.py
- gen_seccion_01.js
- DatabaseErrorMiddleware
- Presentación MultiParking — Lunes 11 de Mayo
- ESTADO GENERAL DE LA DOCUMENTACIÓN — Multiparking
- CATÁLOGO DE ARCHIVOS GOOGLE DRIVE — Multiparking
- gen_seccion_00.js
- gen_seccion_02.js
- Norma de citación: APA 7ma edición
- AGENTES ACTIVOS — Sistema Multiagente Multiparking
- Norma: APA 7ma edición
- PLANTILLA PRINCIPAL — Multiparking
- Fecha: 2026-06-09
- Norma: APA 7ma edición
- build_doc.py
- Norma: APA 7ma edición
- add_toc.py
- ClienteSalidaView
- buildTablaRiesgos
- CuponesConfig
- gen_charts_04.py
- buildStatsTable
- FidelidadConfig
- main
- NovedadesConfig
- PagosConfig
- ParqueaderoConfig
- ReservasConfig
- TarifasConfig
- UsuariosConfig
- VehiculosConfig
- build.sh
- cupones/migrations/0001_initial.py
- fidelidad/migrations/0001_initial.py
- 0002_alter_configuracionfidelidad_id.py
- 0003_add_porcentaje_bono.py
- asgi.py
- settings.py
- settings copy.py
- wsgi.py
- novedades/migrations/0001_initial.py
- pagos/migrations/0001_initial.py
- parqueadero/migrations/0001_initial.py
- 0002_alter_espacio_espestado.py
- reservas/migrations/0001_initial.py
- tarifas/migrations/0001_initial.py
- usuarios/migrations/0001_initial.py
- 0002_alter_usuario_usucorreo.py
- vehiculos/migrations/0001_initial.py

## God Nodes (most connected - your core abstractions)
1. `AdminRequiredMixin` - 78 edges
2. `Espacio` - 61 edges
3. `InventarioParqueo` - 54 edges
4. `Piso` - 52 edges
5. `CuponAplicado` - 47 edges
6. `TipoEspacio` - 41 edges
7. `Usuario` - 34 edges
8. `Verification Checklist` - 32 edges
9. `Cupon` - 28 edges
10. `Reserva` - 28 edges

## Surprising Connections (you probably didn't know these)
- `ClienteSalidaView` --uses--> `Cupon`  [INFERRED]
  parqueadero/cliente_views.py → cupones/models.py
- `ClienteSalidaView` --uses--> `CuponAplicado`  [INFERRED]
  parqueadero/cliente_views.py → cupones/models.py
- `Command` --uses--> `CuponAplicado`  [INFERRED]
  parqueadero/management/commands/seed_data.py → cupones/models.py
- `CuponListView` --uses--> `AdminRequiredMixin`  [INFERRED]
  cupones/views.py → usuarios/mixins.py
- `CuponCreateView` --uses--> `AdminRequiredMixin`  [INFERRED]
  cupones/views.py → usuarios/mixins.py

## Import Cycles
- None detected.

## Communities (113 total, 29 thin omitted)

### Community 0 - "multiparking/urls.py"
Cohesion: 0.05
Nodes (65): CuponAplicado, EspacioAdmin, InventarioParqueoAdmin, PisoAdmin, register, TipoEspacioAdmin, Espacio, EstadoChoices (+57 more)

### Community 1 - "Cupon"
Cohesion: 0.06
Nodes (43): CuponAdmin, CuponAplicadoAdmin, register, Cupon, Meta, Calcula el monto a descontar según el tipo del cupón. Centraliza la lógica…, TipoChoices, ConfiguracionFidelidad (+35 more)

### Community 2 - "Guía de Datos de Demostración"
Cohesion: 0.04
Nodes (46): 1. `cargar_datos_iniciales.py`, 2. `mantener_datos_demo.py`, 3. `generar_datos_prueba.py` (Modificado), Archivos Relacionados, Configuración Recomendada, Credenciales de Prueba, Cupones de Descuento, Error: "Faltan datos básicos" (+38 more)

### Community 3 - "gen_fusionado.js"
Cohesion: 0.04
Nodes (21): CHARTS_04, doc, {
  Document, Packer, Paragraph, TextRun, ImageRun,
  AlignmentType, PageNumber, Footer, LevelFormat,
  HeadingLevel, SectionType, PageBreak,
  PositionalTab, PositionalTabAlignment,
  PositionalTabRelativeTo, PositionalTabLeader,
  Table, TableRow, TableCell, WidthType, BorderStyle,
  ShadingType, VerticalAlign
}, fs, pageFooter, path, RIESGOS, T10 (+13 more)

### Community 4 - "Verification Checklist"
Cohesion: 0.05
Nodes (42): 1st Normal Form (1NF), 2nd Normal Form (2NF), 3rd Normal Form (3NF), Adding a Column (Zero-Downtime), Anti-Patterns, Boolean, Commands, Composite Index Order (+34 more)

### Community 5 - "Usuario"
Cohesion: 0.06
Nodes (31): cuponera_context(), Indica si el cliente tiene un cupón bono activo para mostrar la cuponera., never_cache, Cancela las reservas PENDIENTES cuya hora de inicio ya pasó o está en ≤15 min,…, register, UsuarioAdmin, _is_ajax(), Meta (+23 more)

### Community 6 - "gen_seccion_04.js"
Cohesion: 0.06
Nodes (23): BD, buildStatsTable(), CHARTS, doc, {
  Document, Packer, Paragraph, TextRun, ImageRun,
  AlignmentType, PageNumber, Footer, LevelFormat,
  Table, TableRow, TableCell, WidthType, BorderStyle,
  ShadingType, VerticalAlign
}, fs, pageFooter, path (+15 more)

### Community 7 - "DOCUMENTOS FALTANTES"
Cohesion: 0.06
Nodes (35): ARCHIVOS OBSOLETOS EN DRIVE, DOCS ADICIONALES DESCUBIERTOS EN EL REPOSITORIO (no en Drive), DOCUMENTOS FALTANTES, F-001 — Historias de Usuario, F-002 — Diagrama de Casos de Uso UML Visual, F-003 — Diagramas de Actividades, F-004 — Diagramas de Secuencias, F-005 — Diagrama de Clases / Modelo de Dominio (+27 more)

### Community 8 - "tarifas/views.py"
Cohesion: 0.09
Nodes (15): CuponCreateView, CuponDeleteView, CuponListView, CuponUpdateView, View, Validators compartidos entre apps. Centraliza funciones de validación para…, Parsea y valida un valor decimal positivo. Retorna (Decimal, None) si es…, validar_decimal_positivo() (+7 more)

### Community 9 - "MultiParking"
Cohesion: 0.06
Nodes (32): Arquitectura de Apps, Características, Casos de Uso, ✅ Completado, Convenciones del Código, Credenciales de Prueba, Cupones Activos, Código QR (+24 more)

### Community 10 - "6.3 Diagrama UML de Casos de Uso"
Cohesion: 0.06
Nodes (31): 6.1 Mockups / Interfaces del Sistema, 6.2 Historias de Usuario, 6.3 Diagrama UML de Casos de Uso, 6.4 Diagramas de Actividades, 6.5 Diagramas de Secuencias, 6.6 Modelo de Dominio (Diagrama de Clases), Figura 6.1.1 — Página de Inicio, Figura 6.1.2 — Panel Administrador — Dashboard Principal (+23 more)

### Community 11 - "CLAUDE.md"
Cohesion: 0.06
Nodes (29): 1. Model validators (`django.core.validators`), 2. Server-side view validation (`re.match()` + `messages.error()`), 3. Frontend HTML5 + JavaScript, Apps, Architecture, Authentication & Authorization, Business Rules, cupones / cupones_aplicados (+21 more)

### Community 12 - "gen_sec06.js"
Cohesion: 0.08
Nodes (19): ACT_images, BORDER, CB, children, CU_images, dCell(), doc, {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, WidthType, BorderStyle, ShadingType, ImageRun, PageBreak
} (+11 more)

### Community 14 - "email_utils.py"
Cohesion: 0.11
Nodes (26): _build_msg(), enviar_bienvenida(), enviar_bono_stickers(), enviar_confirmacion_entrada(), enviar_confirmacion_reserva(), enviar_novedad(), enviar_recibo_pago(), enviar_recordatorio_reserva() (+18 more)

### Community 15 - "Database Schema Designer"
Cohesion: 0.07
Nodes (26): Available Commands, Avoid, Basic Schema Design, Best Practices, Database Schema Designer, Do, How It Works, Key Features (+18 more)

### Community 17 - "AdminRequiredMixin"
Cohesion: 0.05
Nodes (38): PagosListView, View, Vista para listar pagos con estadísticas, búsqueda y filtros., ReciboView, ExportarExcelReportesView, ExportarPDFReportesView, View, Vistas para el módulo de Reportes y Estadísticas (+30 more)

### Community 18 - "MÓDULOS"
Cohesion: 0.09
Nodes (22): ARQUITECTURA, Backend, CONTEXTO DEL PROYECTO, Cupones, Descripción General, Espacios, Exportaciones, Fidelidad (+14 more)

### Community 19 - "2026-05-29 — SESIÓN 1: Exploración e Inventario Inicial"
Cohesion: 0.09
Nodes (21): 09:00 — Inicio del sistema multiagente, 09:05 — Exploración de estructura local, 09:10 — Carga de skill gws-drive, 09:15 — Búsqueda en Google Drive (cuenta xeodeo53@gmail.com), 09:20 — Catalogación de estructura Drive, 09:30 — Descarga masiva de documentos (paralela), 09:45 — Análisis de documentos críticos, 10:30 — Identificación de Plantilla Principal (+13 more)

### Community 21 - "Norma: APA 7ma edición"
Cohesion: 0.10
Nodes (19): 4.1 — IDENTIFICACIÓN DE PROCESOS, 4.2 — RECOLECCIÓN DE LA INFORMACIÓN DEL SOFTWARE A CONSTRUIR, 4.3 — ELECCIÓN DE LA TÉCNICA DE RECOLECCIÓN DE LA INFORMACIÓN, 4.4 — APLICACIÓN DE LA TÉCNICA DE RECOLECCIÓN DE INFORMACIÓN, 4.5.1 Encuesta, 4.5.2 Observación directa, 4.5 — ORGANIZACIÓN DE LA INFORMACIÓN RECOLECTADA, 4.6 — INFORME DE LA RECOLECCIÓN DE DATOS (+11 more)

### Community 22 - "novedades/views.py"
Cohesion: 0.18
Nodes (10): EstadoChoices, Meta, Novedad, NovedadCreateView, NovedadDeleteView, NovedadListView, NovedadUpdateView, View (+2 more)

### Community 23 - "build_docx.py"
Cohesion: 0.10
Nodes (16): p(), pb(), tabla_generica(), h3(), p(), pb(), Tabla de 5 filas × 2 cols — formato V4, Tabla genérica con encabezados en negrita (+8 more)

### Community 24 - "ROADMAP DE DOCUMENTACIÓN — Multiparking"
Cohesion: 0.11
Nodes (18): CHECKLIST DE ENTREGA FINAL, CRONOGRAMA SUGERIDO, ESTADO ACTUAL vs OBJETIVO, FASE 1: CRÍTICO — Diagramas UML Faltantes (Prioridad MÁXIMA), FASE 2: ALTO — Pruebas y API (Prioridad ALTA), FASE 3: MEDIO — Diseño y BD Completos, FASE 4: IMPLANTACIÓN — Documentación de Entrega, Limpieza y Consistencia (+10 more)

### Community 25 - "Adición RF63 (escaneo QR) identificada en verificación cruzada — presente en CLAUDE.md y /parqueadero/escanear/"
Cohesion: 0.11
Nodes (18): 5.1 — REQUERIMIENTOS FUNCIONALES, 5.2 — REQUERIMIENTOS NO FUNCIONALES, 5.3 — REQUERIMIENTOS NORMATIVOS, 5.4 — REGLAS DEL NEGOCIO, 5.5.1 Cronograma, 5.5.2 Costos estimados, 5.5.3 Requisitos de hardware, 5.5.4 Requisitos de software (+10 more)

### Community 26 - "📋 Guión Completo"
Cohesion: 0.11
Nodes (18): ⏱ Distribución de Tiempo, 👥 División por Integrante, 📋 Guión Completo, Guión de Presentación — MultiParking, 🟢 KEVIN OVALLE — Diapositiva 12 · Cierre (0:15), 🟢 KEVIN OVALLE — Diapositiva 1 (0:15), 🟢 KEVIN OVALLE — Diapositiva 2 · La necesidad (1:00), 🟢 KEVIN OVALLE — Diapositivas 3 y 4 · Resumen del proyecto (2:00) (+10 more)

### Community 27 - "Database Schema Design Checklist"
Cohesion: 0.11
Nodes (17): Constraints, Data Types, Database Schema Design Checklist, Documentation, Foreign Keys, Index Limits, Index Strategy, Indexing (+9 more)

### Community 29 - "gen_seccion_03.js"
Cohesion: 0.11
Nodes (9): dataRows, doc, {
  Document, Packer, Paragraph, TextRun,
  AlignmentType, PageNumber, Footer,
  Table, TableRow, TableCell, WidthType, BorderStyle,
  ShadingType, VerticalAlign
}, fs, headerRow, pageFooter, ROWS, table (+1 more)

### Community 30 - "Estructura de Base de Datos"
Cohesion: 0.12
Nodes (16): 10. Cupones Aplicados, 11. Reservas, 12. Novedades, 13. Fidelidad — Configuración, 14. Fidelidad — Stickers, 1. Usuarios, 2. Vehículos, 3. Pisos (+8 more)

### Community 31 - "vehiculos/cliente_views.py"
Cohesion: 0.10
Nodes (21): ClienteCancelarReservaView, ClienteConfirmarReservaView, ClienteCrearReservaView, ClienteEditarReservaView, ClienteRequiredMixin, View, Vista para que un cliente edite su reserva, Vista para que un cliente cree una reserva (+13 more)

### Community 32 - "gen_seccion_01.js"
Cohesion: 0.13
Nodes (4): doc, {
  Document, Packer, Paragraph, TextRun, ImageRun,
  AlignmentType, PageNumber, Footer, LevelFormat
}, fs, pageFooter

### Community 33 - "DatabaseErrorMiddleware"
Cohesion: 0.15
Nodes (7): DatabaseErrorMiddleware, NoCacheAfterLogoutMiddleware, Captura errores de base de datos (OperationalError, ProgrammingError) en…, Agrega headers de seguridad HTTP a todas las respuestas: - Content-Security-…, Agrega headers Cache-Control a las respuestas de usuarios autenticados para que…, _render_500(), SecurityHeadersMiddleware

### Community 35 - "Presentación MultiParking — Lunes 11 de Mayo"
Cohesion: 0.14
Nodes (13): DIAPOSITIVA 10 — El Código: Intérprete, DIAPOSITIVA 11 — El Código: estructura, DIAPOSITIVA 12 — Cierre, DIAPOSITIVA 1 — Portada, DIAPOSITIVA 2 — La Necesidad, DIAPOSITIVA 3 — ¿Qué es MultiParking?, DIAPOSITIVA 4 — Los 3 Paneles, DIAPOSITIVA 5 — Patrón de Diseño (+5 more)

### Community 36 - "ESTADO GENERAL DE LA DOCUMENTACIÓN — Multiparking"
Cohesion: 0.15
Nodes (12): AGENTE-API-MODELOS — Hallazgos clave, AGENTE-LOCAL-ESTRUCTURA — Hallazgos clave, ANÁLISIS DEL DOCUMENTO PRINCIPAL v2, CHECKLIST DE CUMPLIMIENTO SENA, CONFIRMACIONES DE AGENTES ESPECIALIZADOS (v1.1), Documentos Obsoletos, Documentos Válidos y Actuales, ESTADO DEL CÓDIGO (Proyecto Django) (+4 more)

### Community 38 - "CATÁLOGO DE ARCHIVOS GOOGLE DRIVE — Multiparking"
Cohesion: 0.17
Nodes (11): CARPETA RAÍZ (My Drive), CATÁLOGO DE ARCHIVOS GOOGLE DRIVE — Multiparking, HALLAZGO CLAVE DEL DRAWIO, RESUMEN DE DESCARGA, SUBCARPETA: BD/, SUBCARPETA: Casos de Uso/, SUBCARPETA: Clase Miercoles/, SUBCARPETA: Cronograma/ (+3 more)

### Community 39 - "gen_seccion_00.js"
Cohesion: 0.17
Nodes (4): doc, {
  Document, Packer, Paragraph, TextRun,
  AlignmentType, PageNumber, Footer, SectionType, PageBreak
}, fs, pageFooter

### Community 40 - "gen_seccion_02.js"
Cohesion: 0.17
Nodes (4): doc, {
  Document, Packer, Paragraph, TextRun,
  AlignmentType, PageNumber, Footer, LevelFormat
}, fs, pageFooter

### Community 41 - "Norma de citación: APA 7ma edición"
Cohesion: 0.17
Nodes (11): 0.05 — ÍNDICE / TABLA DE CONTENIDO, 0.0 — PORTADA, 0.1 — RESUMEN, 0.2 — ABSTRACT, 0.3 — INTRODUCCIÓN, Documento: Sistema de Información Web para la Gestión Integral de Parqueaderos Privados — MultiParking, INSTRUCCIONES DE FORMATO (para Claude Desktop al crear el Word), Norma de citación: APA 7ma edición (+3 more)

### Community 42 - "AGENTES ACTIVOS — Sistema Multiagente Multiparking"
Cohesion: 0.18
Nodes (10): AGENTE API-MODELOS, AGENTE-BD, AGENTE COORDINADOR (Principal), AGENTE-DIAGRAMAS, AGENTE DRIVE-DESCARGA (COMPLETADO), AGENTE LOCAL-ESTRUCTURA, AGENTE-QA, AGENTE-SEGURIDAD (+2 more)

### Community 43 - "Norma: APA 7ma edición"
Cohesion: 0.18
Nodes (10): 1.1 — PLANTEAMIENTO DEL PROBLEMA, 1.2 — ÁRBOL DEL PROBLEMA, 1.3 — JUSTIFICACIÓN, 1.4 — ALCANCE DEL PROYECTO, Contenido del árbol (para construir el diagrama):, Documento: MultiParking — SENA ADSO · Ficha 3119175, INSTRUCCIONES DE FORMATO, Norma: APA 7ma edición (+2 more)

### Community 44 - "PLANTILLA PRINCIPAL — Multiparking"
Cohesion: 0.20
Nodes (9): 1. Archivo Maestro Identificado, 2. Motivo por el cual se considera la Plantilla Principal, 3. Resumen del Contenido de la Plantilla, 4. Secciones Obligatorias Según Plantilla, 5. Documento Principal Actual del Proyecto, 6. Nivel de Cumplimiento Actual, 7. Riesgos de Incumplimiento, 8. Plantillas Adicionales Detectadas (+1 more)

### Community 46 - "Fecha: 2026-06-09"
Cohesion: 0.22
Nodes (8): DATOS DE REFERENCIA — Encuesta Suba (n=13, 2026), Fecha: 2026-06-09, FIX-001 — "Suba" ausente en Introducción (Sección 0), FIX-002 — "Suba" ausente en Alcance (Sección 1.4), FIX-003 — Justificación basada en estudios genéricos, no en datos propios (Sección 1.3), FIX-004 — Objetivo general sin mencionar Suba (Sección 2.1), FIX.MD — Correcciones aplicadas a las secciones, PENDIENTES POR REVISAR EN SECCIONES FUTURAS

### Community 47 - "Norma: APA 7ma edición"
Cohesion: 0.22
Nodes (8): 2.1 — OBJETIVO GENERAL, 2.2 — OBJETIVOS ESPECÍFICOS, 2.3 — ALCANCE DEL PROYECTO, Documento: MultiParking — SENA ADSO · Ficha 3119175, INSTRUCCIONES DE FORMATO, Norma: APA 7ma edición, NOTA PARA CLAUDE DESKTOP, SECCIÓN 2 — Objetivos del Trabajo Final de Proyecto Formativo (TFPF)

### Community 48 - "build_doc.py"
Cohesion: 0.42
Nodes (8): add(), h1(), h2(), h3(), h4(), p(), subtitulo(), titulo()

### Community 49 - "Norma: APA 7ma edición"
Cohesion: 0.25
Nodes (7): 3.1 — TEXTO INTRODUCTORIO, 3.2 — TABLA DE RIESGOS, Documento: MultiParking — SENA ADSO · Ficha 3119175, INSTRUCCIONES DE FORMATO, Norma: APA 7ma edición, NOTA PARA CLAUDE DESKTOP, SECCIÓN 3 — Matriz de Riesgo

### Community 50 - "add_toc.py"
Cohesion: 0.33
Nodes (6): make_toc_field_para(), para_text(), qtag(), Post-procesa MultiParking_Documentacion.docx sin python-docx: - Abre el .docx…, Devuelve el texto concatenado de un párrafo., Construye el elemento <w:p> con el campo TOC complejo de Word.

### Community 51 - "ClienteSalidaView"
Cohesion: 0.40
Nodes (4): ClienteSalidaView, ClienteRequiredMixin, View, Vista para procesar la salida del vehículo del parqueadero

### Community 53 - "buildTablaRiesgos"
Cohesion: 0.50
Nodes (4): buildTablaRiesgos(), nivelCell(), tdCell(), thCell()

### Community 57 - "buildStatsTable"
Cohesion: 0.67
Nodes (3): buildStatsTable(), tdStat(), thStat()

## Knowledge Gaps
- **512 isolated node(s):** `{
  Document, Packer, Paragraph, TextRun, ImageRun,
  AlignmentType, PageNumber, Footer, LevelFormat,
  HeadingLevel, SectionType, PageBreak,
  PositionalTab, PositionalTabAlignment,
  PositionalTabRelativeTo, PositionalTabLeader,
  Table, TableRow, TableCell, WidthType, BorderStyle,
  ShadingType, VerticalAlign
}`, `fs`, `path`, `CHARTS_04`, `W3` (+507 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AdminRequiredMixin` connect `AdminRequiredMixin` to `multiparking/urls.py`, `Cupon`, `Usuario`, `tarifas/views.py`, `novedades/views.py`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Why does `Espacio` connect `multiparking/urls.py` to `Cupon`, `novedades/views.py`, `AdminRequiredMixin`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Why does `ClienteSalidaView` connect `ClienteSalidaView` to `multiparking/urls.py`, `Cupon`?**
  _High betweenness centrality (0.008) - this node is a cross-community bridge._
- **Are the 65 inferred relationships involving `AdminRequiredMixin` (e.g. with `CuponCreateView` and `CuponDeleteView`) actually correct?**
  _`AdminRequiredMixin` has 65 INFERRED edges - model-reasoned connections that need verification._
- **Are the 35 inferred relationships involving `Espacio` (e.g. with `EspacioAdmin` and `InventarioParqueoAdmin`) actually correct?**
  _`Espacio` has 35 INFERRED edges - model-reasoned connections that need verification._
- **Are the 35 inferred relationships involving `InventarioParqueo` (e.g. with `EspacioAdmin` and `InventarioParqueoAdmin`) actually correct?**
  _`InventarioParqueo` has 35 INFERRED edges - model-reasoned connections that need verification._
- **Are the 35 inferred relationships involving `Piso` (e.g. with `EspacioAdmin` and `InventarioParqueoAdmin`) actually correct?**
  _`Piso` has 35 INFERRED edges - model-reasoned connections that need verification._