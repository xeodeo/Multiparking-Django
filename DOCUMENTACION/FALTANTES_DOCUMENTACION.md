# FALTANTES DE DOCUMENTACIÓN — Multiparking

**Fecha:** 2026-05-29 | **Versión:** 1.1 | **Agente:** COORDINADOR + AGENTE-API-MODELOS + AGENTE-LOCAL-ESTRUCTURA
**Referencia plantilla:** GUIA PARA APRENDIZ - TRABAJO FINAL DEL PROYECTO FORMATIVO (SENA ADSO)
**Documento principal:** Documentacion Multiparking COMPLETA v2

---

## RESUMEN EJECUTIVO

| Categoría | Total | Críticos | Altos | Medios | Bajos |
|---|---|---|---|---|---|
| Documentos faltantes | 8 | 3 | 3 | 2 | 0 |
| Secciones faltantes | 7 | 4 | 2 | 1 | 0 |
| Diagramas faltantes | 5 | 3 | 2 | 0 | 0 |
| Evidencias faltantes | 4 | 2 | 1 | 1 | 0 |
| Inconsistencias | 9 | 2 | 5 | 2 | 0 |
| Archivos obsoletos | 6 | 0 | 1 | 3 | 2 |
| **TOTAL** | **39** | **14** | **14** | **9** | **2** |

> **v1.1 — Hallazgos adicionales de AGENTE-API-MODELOS y AGENTE-LOCAL-ESTRUCTURA:** +2 inconsistencias (F-019, F-020), confirmación de I-003 (espEstado=INACTIVO en código), y actualización de I-006 (DRF sin serializers — estado es inexistente, no parcial).

---

## DOCUMENTOS FALTANTES

### F-001 — Historias de Usuario
| Campo | Valor |
|---|---|
| **ID** | F-001 |
| **Nombre** | Historias de Usuario del sistema MultiParking |
| **Tipo** | Documento faltante |
| **Descripción** | No existe ningún documento con historias de usuario en formato estándar (Como [rol], quiero [acción], para [beneficio]). Ausente en Drive y en el doc principal. |
| **Documento relacionado** | Documentacion Multiparking COMPLETA v2 |
| **Ubicación esperada** | Sección 6.2 del documento principal |
| **Prioridad** | ALTA |
| **Criticidad** | CRÍTICA |
| **Estado** | PENDIENTE |
| **Responsable sugerido** | Kevin Grisales / Kevin Pinto |
| **Recomendación** | Crear documento con HU para los 3 roles (Admin, Vigilante, Cliente). Mínimo 15-20 historias cubriendo los módulos críticos. |
| **Dependencias** | RF01–RF62 (base para HU) |
| **Relación con plantilla** | Sección 6.2 — OBLIGATORIA |
| **Impacto del incumplimiento** | Incumplimiento directo del entregable SENA. Evaluación incompleta. |
| **Fecha de detección** | 2026-05-29 |

---

### F-002 — Diagrama de Casos de Uso UML Visual
| Campo | Valor |
|---|---|
| **ID** | F-002 |
| **Nombre** | Diagrama UML de Casos de Uso (imagen formal) |
| **Tipo** | Diagrama faltante |
| **Descripción** | El doc v2 describe casos de uso en texto. Existe un "casos de uso V1.pdf" en Drive pero no está integrado en el documento y no se confirmó su contenido. Se requiere diagrama UML formal con actores, casos y relaciones include/extend. |
| **Documento relacionado** | Documentacion Multiparking COMPLETA v2; casos de uso V1.pdf (Drive) |
| **Ubicación esperada** | Sección 6.3 del documento principal |
| **Prioridad** | ALTA |
| **Criticidad** | CRÍTICA |
| **Estado** | PARCIAL |
| **Responsable sugerido** | Kevin Grisales / Kevin Pinto |
| **Recomendación** | Integrar el PDF existente al documento principal. Si no es UML formal, crear diagrama con draw.io o Lucidchart con los 3 actores y mínimo 15 casos. |
| **Dependencias** | F-001 (Historias de Usuario) |
| **Relación con plantilla** | Sección 6.3 — OBLIGATORIA |
| **Impacto del incumplimiento** | Evaluación incompleta en análisis del sistema. |
| **Fecha de detección** | 2026-05-29 |

---

### F-003 — Diagramas de Actividades
| Campo | Valor |
|---|---|
| **ID** | F-003 |
| **Nombre** | Diagramas de Actividades UML |
| **Tipo** | Diagrama faltante |
| **Descripción** | No existe ningún diagrama de actividades para los flujos críticos del sistema (ingreso vehículo, salida+pago, reserva, fidelización). |
| **Documento relacionado** | Documentacion Multiparking COMPLETA v2 |
| **Ubicación esperada** | Sección 6.4 del documento principal |
| **Prioridad** | ALTA |
| **Criticidad** | CRÍTICA |
| **Estado** | PENDIENTE |
| **Responsable sugerido** | Kevin Grisales / Kevin Pinto |
| **Recomendación** | Crear mínimo 3 diagramas: (1) Flujo ingreso-salida-pago, (2) Flujo de reservas, (3) Flujo de fidelización. Usar draw.io. |
| **Dependencias** | F-002 |
| **Relación con plantilla** | Sección 6.4 — OBLIGATORIA |
| **Impacto del incumplimiento** | Incumplimiento de entregable SENA. |
| **Fecha de detección** | 2026-05-29 |

---

### F-004 — Diagramas de Secuencias
| Campo | Valor |
|---|---|
| **ID** | F-004 |
| **Nombre** | Diagramas de Secuencias UML |
| **Tipo** | Diagrama faltante |
| **Descripción** | No existe ningún diagrama de secuencias UML para las interacciones entre capas del sistema. Requerido para los flujos principales. |
| **Documento relacionado** | Documentacion Multiparking COMPLETA v2 |
| **Ubicación esperada** | Sección 6.5 del documento principal |
| **Prioridad** | ALTA |
| **Criticidad** | CRÍTICA |
| **Estado** | PENDIENTE |
| **Responsable sugerido** | Kevin Grisales / Kevin Pinto |
| **Recomendación** | Crear mínimo 2 diagramas: (1) Secuencia login/autenticación, (2) Secuencia registro ingreso-salida-pago. |
| **Dependencias** | F-002, F-003 |
| **Relación con plantilla** | Sección 6.5 — OBLIGATORIA |
| **Impacto del incumplimiento** | Incumplimiento de entregable SENA. |
| **Fecha de detección** | 2026-05-29 |

---

### F-005 — Diagrama de Clases / Modelo de Dominio
| Campo | Valor |
|---|---|
| **ID** | F-005 |
| **Nombre** | Diagrama UML de Clases (Modelo de Dominio) |
| **Tipo** | Diagrama faltante |
| **Descripción** | No existe diagrama de clases UML formal. El diccionario de datos tiene la información, pero no hay representación visual con atributos, métodos y relaciones. |
| **Documento relacionado** | Documentacion Multiparking COMPLETA v2 |
| **Ubicación esperada** | Sección 6.6 del documento principal |
| **Prioridad** | ALTA |
| **Criticidad** | ALTA |
| **Estado** | PENDIENTE |
| **Responsable sugerido** | Kevin Grisales / Kevin Pinto |
| **Recomendación** | Crear diagrama UML con las 13 clases/modelos del sistema mostrando atributos, tipos y relaciones (herencia, asociación, FK). |
| **Dependencias** | Diccionario de datos (disponible en doc v2) |
| **Relación con plantilla** | Sección 6.6 — OBLIGATORIA |
| **Impacto del incumplimiento** | Evaluación de diseño incompleta. |
| **Fecha de detección** | 2026-05-29 |

---

### F-006 — Diagrama de Componentes (Arquitectura Software)
| Campo | Valor |
|---|---|
| **ID** | F-006 |
| **Nombre** | Diagrama UML de Componentes |
| **Tipo** | Diagrama faltante |
| **Descripción** | La arquitectura del software se describe en texto pero no existe un diagrama UML de componentes que muestre las apps Django, sus dependencias y las interfaces entre capas. |
| **Documento relacionado** | Documentacion Multiparking COMPLETA v2, Sección "Arquitectura del Software" |
| **Ubicación esperada** | Sección 7.2 del documento principal |
| **Prioridad** | ALTA |
| **Criticidad** | ALTA |
| **Estado** | PENDIENTE |
| **Responsable sugerido** | Kevin Grisales / Kevin Pinto |
| **Recomendación** | Crear diagrama de componentes mostrando las 11 apps Django, PostgreSQL, Render.com, SendGrid, Gunicorn, Whitenoise. |
| **Dependencias** | — |
| **Relación con plantilla** | Sección 7.2 — OBLIGATORIA |
| **Impacto del incumplimiento** | Diseño de arquitectura incompleto. |
| **Fecha de detección** | 2026-05-29 |

---

### F-007 — Mapa de Navegación de la Aplicación
| Campo | Valor |
|---|---|
| **ID** | F-007 |
| **Nombre** | Mapa de Navegación |
| **Tipo** | Diagrama faltante |
| **Descripción** | No existe ningún diagrama o documento que muestre la navegación entre pantallas por rol de usuario. Requerido por la sección 7.6 de la plantilla. |
| **Documento relacionado** | Documentacion Multiparking COMPLETA v2 |
| **Ubicación esperada** | Sección 7.6 del documento principal |
| **Prioridad** | MEDIA |
| **Criticidad** | ALTA |
| **Estado** | PENDIENTE |
| **Responsable sugerido** | Kevin Grisales / Kevin Pinto |
| **Recomendación** | Crear diagrama de navegación por rol: (1) Admin: /admin-panel/* (2) Vigilante: /guardia/* (3) Cliente: /cliente/* y /dashboard/. |
| **Dependencias** | Mockups (disponibles) |
| **Relación con plantilla** | Sección 7.6 — OBLIGATORIA |
| **Impacto del incumplimiento** | Diseño front-end incompleto según plantilla. |
| **Fecha de detección** | 2026-05-29 |

---

### F-008 — Plan de Capacitación de Usuarios
| Campo | Valor |
|---|---|
| **ID** | F-008 |
| **Nombre** | Plan de Capacitación de Usuarios del Sistema |
| **Tipo** | Documento faltante |
| **Descripción** | No existe ningún documento de plan de capacitación que defina cómo se entrenará al personal (admins, vigilantes, clientes) para usar el sistema. |
| **Documento relacionado** | Documentacion Multiparking COMPLETA v2 |
| **Ubicación esperada** | Sección 12.2 del documento principal |
| **Prioridad** | MEDIA |
| **Criticidad** | MEDIA |
| **Estado** | PENDIENTE |
| **Responsable sugerido** | Kevin Grisales / Kevin Pinto |
| **Recomendación** | Crear plan de capacitación con: objetivos, duración por rol, material didáctico, cronograma de sesiones. |
| **Dependencias** | F-009 (Manual de usuario) |
| **Relación con plantilla** | Sección 12.2 — OBLIGATORIA |
| **Impacto del incumplimiento** | Implantación incompleta según plantilla SENA. |
| **Fecha de detección** | 2026-05-29 |

---

### F-009 — Manual de Usuario en PDF Formal
| Campo | Valor |
|---|---|
| **ID** | F-009 |
| **Nombre** | Manual de Usuario (PDF standalone) |
| **Tipo** | Documento faltante |
| **Descripción** | Existe una descripción básica del manual en el doc v2 pero no hay un PDF formal e independiente con capturas de pantalla, pasos numerados y guía completa por rol. |
| **Documento relacionado** | Documentacion Multiparking COMPLETA v2, Sección "Manual del Usuario" |
| **Ubicación esperada** | Sección 12.3 del documento principal |
| **Prioridad** | ALTA |
| **Criticidad** | ALTA |
| **Estado** | PARCIAL |
| **Responsable sugerido** | Kevin Grisales / Kevin Pinto |
| **Recomendación** | Crear PDF con: portada, índice, guías paso a paso por rol con screenshots reales del sistema. |
| **Dependencias** | Mockups (disponibles) |
| **Relación con plantilla** | Sección 12.3 — OBLIGATORIA |
| **Impacto del incumplimiento** | Implantación y entrega final incompleta. |
| **Fecha de detección** | 2026-05-29 |

---

### F-010 — Garantía / Acuerdos de Nivel de Servicio (SLA)
| Campo | Valor |
|---|---|
| **ID** | F-010 |
| **Nombre** | Contrato de Garantía / SLA |
| **Tipo** | Documento faltante |
| **Descripción** | No existe documento de garantía, acuerdo de nivel de servicio o contrato de soporte post-implantación. |
| **Documento relacionado** | Documentacion Multiparking COMPLETA v2 |
| **Ubicación esperada** | Sección 12.5 del documento principal |
| **Prioridad** | BAJA |
| **Criticidad** | MEDIA |
| **Estado** | PENDIENTE |
| **Responsable sugerido** | Kevin Grisales / Kevin Pinto |
| **Recomendación** | Incluir al menos un párrafo con compromisos de soporte (tiempo respuesta, versiones, periodo de garantía). |
| **Dependencias** | — |
| **Relación con plantilla** | Sección 12.5 |
| **Impacto del incumplimiento** | Entrega final incompleta. |
| **Fecha de detección** | 2026-05-29 |

---

### F-011 — Sección Buenas Prácticas en el Proceso de Desarrollo
| Campo | Valor |
|---|---|
| **ID** | F-011 |
| **Nombre** | Adopción de Buenas Prácticas (Sección 13) |
| **Tipo** | Sección faltante |
| **Descripción** | La sección 13 requerida por la plantilla "ADOPCIÓN DE BUENAS PRÁCTICAS EN EL PROCESO DE DESARROLLO DE SOFTWARE" no existe en el documento principal. |
| **Documento relacionado** | Documentacion Multiparking COMPLETA v2 |
| **Ubicación esperada** | Sección 13 del documento principal |
| **Prioridad** | MEDIA |
| **Criticidad** | MEDIA |
| **Estado** | PENDIENTE |
| **Responsable sugerido** | Kevin Grisales / Kevin Pinto |
| **Recomendación** | Agregar sección describiendo metodología ágil usada, principios SOLID aplicados, code review, pair programming, etc. |
| **Dependencias** | — |
| **Relación con plantilla** | Sección 13 — OBLIGATORIA |
| **Impacto del incumplimiento** | Documento incompleto según estructura SENA. |
| **Fecha de detección** | 2026-05-29 |

---

### F-012 — Tests Automatizados (Django test suite)
| Campo | Valor |
|---|---|
| **ID** | F-012 |
| **Nombre** | Pruebas automatizadas con Django TestCase |
| **Tipo** | Evidencia faltante / Código faltante |
| **Descripción** | Todos los archivos `tests.py` de cada app Django están vacíos. Las pruebas PU01-PU20 y PS01-PS08 se ejecutaron manualmente. No existe ninguna prueba automatizable. |
| **Documento relacionado** | Documentacion Multiparking COMPLETA v2, Sección "Pruebas" |
| **Ubicación** | usuarios/tests.py, vehiculos/tests.py, parqueadero/tests.py, reservas/tests.py, etc. |
| **Prioridad** | ALTA |
| **Criticidad** | ALTA |
| **Estado** | PENDIENTE |
| **Responsable sugerido** | Kevin Grisales / Kevin Pinto |
| **Recomendación** | Implementar mínimo 5 tests Django automatizados cubriendo: login, cálculo de costo, validación cupón, registro ingreso, sticker. |
| **Dependencias** | — |
| **Relación con plantilla** | Sección 10 — Pruebas del Software |
| **Impacto del incumplimiento** | Sin tests automatizados ejecutables, las pruebas no son verificables por terceros. |
| **Fecha de detección** | 2026-05-29 |

---

### F-013 — Documentación formal de API REST (OpenAPI/Swagger)
| Campo | Valor |
|---|---|
| **ID** | F-013 |
| **Nombre** | Documentación de Servicios Web / API REST |
| **Tipo** | Documento faltante |
| **Descripción** | El doc v2 menciona DRF instalado con endpoints bajo `/api/<app>/` para espacios, reservas y parqueos activos. Sin embargo, no existe documentación formal de los endpoints (métodos, parámetros, respuestas, autenticación). |
| **Documento relacionado** | Documentacion Multiparking COMPLETA v2, Sección "Servicios Web" |
| **Ubicación esperada** | Sección 9.4 del documento principal |
| **Prioridad** | ALTA |
| **Criticidad** | ALTA |
| **Estado** | PARCIAL |
| **Responsable sugerido** | Kevin Grisales / Kevin Pinto |
| **Recomendación** | Implementar drf-spectacular o drf-yasg para generar Swagger automático, o documentar manualmente los endpoints en tabla con: URL, método, descripción, parámetros, respuesta ejemplo. |
| **Dependencias** | — |
| **Relación con plantilla** | Sección 9.4 — Servicios Web |
| **Impacto del incumplimiento** | Servicios web sin documentar, evaluación técnica incompleta. |
| **Fecha de detección** | 2026-05-29 |

---

### F-014 — Evidencias de Ejecución de Pruebas
| Campo | Valor |
|---|---|
| **ID** | F-014 |
| **Nombre** | Evidencias/Screenshots de pruebas ejecutadas |
| **Tipo** | Evidencia faltante |
| **Descripción** | Las pruebas PU01-PU20 y PS01-PS08 reportan estado "PASÓ" pero no existen evidencias (screenshots, videos, logs) que demuestren la ejecución real de cada caso. |
| **Documento relacionado** | Documentacion Multiparking COMPLETA v2, Tablas PT-01 y PT-02 |
| **Ubicación esperada** | Sección 10.2 y 10.6 del documento principal |
| **Prioridad** | ALTA |
| **Criticidad** | ALTA |
| **Estado** | PENDIENTE |
| **Responsable sugerido** | Kevin Grisales / Kevin Pinto |
| **Recomendación** | Usar Playwright/Selenium para capturar screenshots de cada caso de prueba, o documentar manualmente con imágenes del sistema ejecutando cada test. |
| **Dependencias** | F-012 |
| **Relación con plantilla** | Sección 10.2 — Ejecución de Pruebas, Informe de Hallazgos |
| **Impacto del incumplimiento** | Pruebas no verificables. Hallazgos sin soporte. |
| **Fecha de detección** | 2026-05-29 |

---

### F-015 — Propuesta Técnica Completa (Costos, Hardware, Software)
| Campo | Valor |
|---|---|
| **ID** | F-015 |
| **Nombre** | Propuesta Técnica — Costos estimados, Requisitos Hardware y Software |
| **Tipo** | Sección incompleta |
| **Descripción** | La sección 5.5 de la plantilla requiere: Cronograma, Costos Estimados, Requisitos de Hardware y Requisitos de Software. El documento v2 no incluye tabla de costos ni requisitos de hardware del servidor/cliente. |
| **Documento relacionado** | Documentacion Multiparking COMPLETA v2 |
| **Ubicación esperada** | Sección 5.5 del documento principal |
| **Prioridad** | MEDIA |
| **Criticidad** | MEDIA |
| **Estado** | PARCIAL |
| **Responsable sugerido** | Kevin Grisales / Kevin Pinto |
| **Recomendación** | Agregar: tabla de costos del proyecto (tiempo, herramientas, hosting); tabla de requisitos hardware (servidor y cliente mínimo); tabla de software requerido (Python 3.12, PostgreSQL, etc.). |
| **Dependencias** | — |
| **Relación con plantilla** | Sección 5.5.2, 5.5.3, 5.5.4 |
| **Impacto del incumplimiento** | Propuesta técnica incompleta. |
| **Fecha de detección** | 2026-05-29 |

---

### F-016 — Diagrama MER/ER Integrado en Documento Principal
| Campo | Valor |
|---|---|
| **ID** | F-016 |
| **Nombre** | Modelo Entidad-Relación visual integrado |
| **Tipo** | Evidencia faltante |
| **Descripción** | Existen imágenes MER.jpeg, MR.png, MultiParking_MR_Def.png, Multiparking_MR_V2.png en Drive, pero ninguna está integrada al documento principal v2. El doc solo tiene descripción textual de relaciones. |
| **Documento relacionado** | Documentacion Multiparking COMPLETA v2; imágenes en Drive/BD/ |
| **Ubicación esperada** | Sección 8.1.1 y 8.1.2 del documento principal |
| **Prioridad** | ALTA |
| **Criticidad** | ALTA |
| **Estado** | PARCIAL |
| **Responsable sugerido** | Kevin Grisales / Kevin Pinto |
| **Recomendación** | Integrar la imagen más actualizada (MultiParking_MR_Def.png o Multiparking_MR_V2.png) al documento con referencia formal y verificar que refleje el modelo actual de Django. |
| **Dependencias** | — |
| **Relación con plantilla** | Sección 8.1.1 MER, 8.1.2 Diagrama ER, 8.1.3 Modelo Relacional |
| **Impacto del incumplimiento** | Documentación de BD visualmente incompleta. |
| **Fecha de detección** | 2026-05-29 |

---

### F-017 — Procedimientos Almacenados y Vistas de BD
| Campo | Valor |
|---|---|
| **ID** | F-017 |
| **Nombre** | Procedimientos Almacenados y Vistas de Base de Datos |
| **Tipo** | Sección incompleta |
| **Descripción** | La sección 8.1.4 requiere documentar Procedimientos Almacenados, Vistas y Disparadores. Solo los 3 triggers están documentados. No hay Stored Procedures ni Vistas de BD formales. |
| **Documento relacionado** | Documentacion Multiparking COMPLETA v2, Sección "Objetos de la Base de Datos" |
| **Ubicación esperada** | Sección 8.1.4 del documento principal |
| **Prioridad** | MEDIA |
| **Criticidad** | MEDIA |
| **Estado** | PARCIAL |
| **Responsable sugerido** | Kevin Grisales / Kevin Pinto |
| **Recomendación** | Crear al menos 1 vista SQL (ej. vista de parqueos activos con datos del vehículo y usuario) y documentarla. Los SP pueden justificarse como no aplicables dado el uso de ORM. |
| **Dependencias** | SQL scripts disponibles en Drive |
| **Relación con plantilla** | Sección 8.1.4 — PROCEDIMIENTOS ALMACENADOS, VISTAS, DISPARADORES |
| **Impacto del incumplimiento** | Construcción de BD incompleta según plantilla. |
| **Fecha de detección** | 2026-05-29 |

---

### F-018 — Índices de Diagramas y Tablas
| Campo | Valor |
|---|---|
| **ID** | F-018 |
| **Nombre** | Índice de diagramas e Índice de tablas |
| **Tipo** | Sección faltante |
| **Descripción** | El documento v2 referencia "Índice de diagramas" e "Índice de tablas" pero están vacíos. Una vez se completen los diagramas faltantes, estos índices deben actualizarse. |
| **Documento relacionado** | Documentacion Multiparking COMPLETA v2 |
| **Ubicación esperada** | Al final del documento principal |
| **Prioridad** | BAJA |
| **Criticidad** | BAJA |
| **Estado** | PENDIENTE |
| **Responsable sugerido** | Kevin Grisales / Kevin Pinto |
| **Recomendación** | Completar una vez se agreguen los diagramas faltantes (F-002 a F-007). |
| **Dependencias** | F-002, F-003, F-004, F-005, F-006, F-007 |
| **Relación con plantilla** | Índice de diagramas, Índice de tablas |
| **Impacto del incumplimiento** | Documento sin índice formal. |
| **Fecha de detección** | 2026-05-29 |

---

## INCONSISTENCIAS DETECTADAS

### I-001 — Integrante Faltante (ACTA vs Documento Principal)
| Campo | Valor |
|---|---|
| **ID** | I-001 |
| **Tipo** | Inconsistencia |
| **Descripción** | El ACTA DE REVISION (Julio 2025) menciona 3 integrantes: Kevin Santiago Pinto López, **Jhorman Steven Cortes Lasso**, Kevin Arley Grisales Ovalle. El documento principal v2 solo menciona 2: Kevin Arley Grisales Ovalle, Kevin Santiago Pinto López. Jhorman Steven fue omitido. |
| **Documentos** | ACTA_REVISION_PROYECTOS_2025.docx vs Documentacion_Multiparking_COMPLETA_v2.txt |
| **Prioridad** | ALTA |
| **Recomendación** | Aclarar si Jhorman sigue siendo integrante y actualizar portada del documento principal si corresponde. |
| **Fecha de detección** | 2026-05-29 |

---

### I-002 — Tecnología Obsoleta en Documentacion_V4.docx
| Campo | Valor |
|---|---|
| **ID** | I-002 |
| **Tipo** | Inconsistencia / Archivo obsoleto |
| **Descripción** | Documentacion_V4.docx describe el sistema usando **React.js, Node.js/Express y MySQL** con Prisma ORM — tecnologías que NO corresponden al sistema actual (Django/PostgreSQL). Esta versión es un plan de proyecto anterior que fue descartado pero sigue en Drive sin marcar como obsoleto. |
| **Documentos** | Documentacion_V4.docx (obsoleto) vs Sistema real Django/PostgreSQL |
| **Prioridad** | ALTA |
| **Recomendación** | Marcar Documentacion_V4.docx como OBSOLETO y moverlo a carpeta Old-BD o eliminar de la carpeta principal. |
| **Fecha de detección** | 2026-05-29 |

---

### I-003 — espEstado: MANTENIMIENTO vs INACTIVO ✅ CONFIRMADO
| Campo | Valor |
|---|---|
| **ID** | I-003 |
| **Tipo** | Inconsistencia código vs documentación |
| **Descripción** | El documento v2 (RF17, DD-05) dice el estado del espacio puede ser DISPONIBLE/OCUPADO/RESERVADO/**MANTENIMIENTO**. El código real (parqueadero/migrations/0002_*.py confirmado por AGENTE-LOCAL-ESTRUCTURA) usa DISPONIBLE/OCUPADO/RESERVADO/**INACTIVO**. MANTENIMIENTO nunca existió en el ENUM real del modelo. |
| **Documentos** | Documentacion_Multiparking_COMPLETA_v2 vs parqueadero/migrations/0002_*.py |
| **Prioridad** | ALTA |
| **Estado** | **CONFIRMADO — El código usa INACTIVO. El documento debe corregirse.** |
| **Recomendación** | Reemplazar todas las ocurrencias de "MANTENIMIENTO" en el documento v2 (RF17, DD-05) por "INACTIVO". No modificar el código — el código es correcto. |
| **Fecha de detección** | 2026-05-29 |
| **Fecha de confirmación** | 2026-05-29 (AGENTE-LOCAL-ESTRUCTURA, migration 0002) |

---

### I-004 — Tabla DD-13 faltante (fidelidad_configuracion)
| Campo | Valor |
|---|---|
| **ID** | I-004 |
| **Tipo** | Omisión en diccionario de datos |
| **Descripción** | El diccionario de datos incluye DD-01 a DD-12 (12 tablas). Sin embargo, el modelo `ConfiguracionFidelidad` (tabla `fidelidad_configuracion`) no tiene entrada en el diccionario. Solo se documentó `fidelidad_stickers` (DD-12). |
| **Documentos** | Documentacion_Multiparking_COMPLETA_v2, Sección Diccionario de Datos |
| **Prioridad** | MEDIA |
| **Recomendación** | Agregar DD-13 para tabla `fidelidad_configuracion` con campos: id (PK, singleton pk=1), metaStickers (INT), diasVencimientoBono (INT). |
| **Fecha de detección** | 2026-05-29 |

---

### I-005 — cupones_aplicados no tiene entrada en Diccionario de Datos
| Campo | Valor |
|---|---|
| **ID** | I-005 |
| **Tipo** | Omisión en diccionario de datos |
| **Descripción** | La tabla `cupones_aplicados` (modelo `CuponAplicado`) con campos `fkIdPago`, `fkIdCupon`, `montoDescontado` no tiene entrada en el diccionario de datos del documento v2. |
| **Documentos** | Documentacion_Multiparking_COMPLETA_v2, Sección Diccionario de Datos |
| **Prioridad** | MEDIA |
| **Recomendación** | Agregar DD-14 para tabla `cupones_aplicados`. |
| **Fecha de detección** | 2026-05-29 |

---

### I-006 — API REST: DRF instalado pero NO implementado (serializers inexistentes) ✅ CONFIRMADO
| Campo | Valor |
|---|---|
| **ID** | I-006 |
| **Tipo** | Documentación incorrecta / Inconsistencia crítica |
| **Descripción** | El doc v2 dice "se exponen endpoints de consulta para espacios, reservas y parqueos activos bajo /api/<app>/". CONFIRMADO por AGENTE-API-MODELOS: NO existe ningún archivo serializers.py en ninguna app. DRF está instalado en requirements.txt pero NO está siendo utilizado. Los ~80 endpoints del sistema son vistas CBV Django que retornan HTML o JsonResponse directo, NO recursos DRF/REST. Las 7 respuestas JSON son AJAX helpers, no API REST. |
| **Documentos** | Documentacion_Multiparking_COMPLETA_v2; inspeccion directa del código fuente |
| **Prioridad** | ALTA |
| **Estado** | **CONFIRMADO — No existe ningún serializer. La mención de API REST en el doc v2 es incorrecta.** |
| **Recomendación** | Opción A: Implementar serializers DRF reales + ViewSets para al menos 3 recursos (Espacio, Reserva, InventarioParqueo). Opción B: Corregir el documento para declarar que el sistema usa JsonResponse directo para integración AJAX, no REST formal. |
| **Fecha de detección** | 2026-05-29 |
| **Fecha de confirmación** | 2026-05-29 (AGENTE-API-MODELOS, búsqueda exhaustiva en 9 apps) |

---

### I-007 — Dos copias vacías de "Documentacion Multiparking COMPLETA" en Drive
| Campo | Valor |
|---|---|
| **ID** | I-007 |
| **Tipo** | Duplicados / Archivos obsoletos |
| **Descripción** | En la carpeta MULTIPARKING existen 2 archivos Google Doc llamados "Documentacion Multiparking COMPLETA" (sin versión) con solo 1KB de tamaño — vacíos o con contenido mínimo. Generan confusión sobre cuál es el documento oficial. |
| **Documentos** | IDs: 1DmTvP_ADxAn6vkoWhkXopKpcXquOxojd_5677sUMFss y 1shENlXVXpAIu0-5e8g0t3-QMORVN-imbn9WdaV60gJA |
| **Prioridad** | MEDIA |
| **Recomendación** | Eliminar o mover a papelera los 2 documentos vacíos. Mantener solo el v2 como documento oficial. |
| **Fecha de detección** | 2026-05-29 |

---

## ARCHIVOS OBSOLETOS EN DRIVE

| ID | Archivo | Razón | Acción Recomendada |
|---|---|---|---|
| O-001 | Documentacion_V4.docx | Tecnología incorrecta (React/Node) | Mover a carpeta Obsoletos |
| O-002 | Documentacion_V3.docx | Versión anterior superada | Mover a carpeta Obsoletos |
| O-003 | Documentacion_V2.docx | Versión anterior superada | Mover a carpeta Obsoletos |
| O-004 | Documentacion_Final_V1.docx | Versión anterior superada | Mover a carpeta Obsoletos |
| O-005 | "Documentacion Multiparking COMPLETA" (x2, 1KB) | Archivos vacíos duplicados | Eliminar |
| O-006 | Bd provisional_ (sin extensión) | Archivo temporal sin identificar | Revisar y eliminar si no aplica |

---

## PENDIENTES DE DESCARGA/ANÁLISIS

| ID | Archivo | ID Drive | Estado | Prioridad |
|---|---|---|---|---|
| PD-001 | casos de uso V1.pdf | 11Xikmmmw0eYlOCc9W0tyq58GqsckA5NL | ✅ Descargado — pendiente análisis de contenido | ALTA |
| PD-002 | MultiParking.drawio | 1vsuiwrra_2Taz-buO5HO9f8CDrEcVHgc | ✅ Descargado — contiene Modelo Relacional (2 páginas) | ALTA |
| PD-003 | BD_multiparking_V3.sql | 1uycNMfZ66PT0Vwl7ijWpgM8Y5jv3T5cu | ⏳ Pendiente | MEDIA |
| PD-004 | Requerimientos y Modelos MultiParking.docx | 1u5ApWY3HXm976oKU5qkxq2zmqC4o8IY0 | ⏳ Pendiente | MEDIA |
| PD-005 | Copia de Requerimientos y Modelos MultiParking.docx | 1ofQD3vBom2Abi2WBI3gDgssF-u-c2ExP | ⏳ Pendiente | BAJA |
| PD-006 | Mockup images (6 imágenes) | Varios | ⏳ Pendiente | BAJA |

---

## HALLAZGOS ADICIONALES — AGENTES ESPECIALIZADOS (v1.1)

### F-019 — pagMetodo: valor PSE no documentado
| Campo | Valor |
|---|---|
| **ID** | F-019 |
| **Nombre** | Enum pagMetodo incluye PSE (sin documentar) |
| **Tipo** | Inconsistencia código vs documentación |
| **Descripción** | El modelo `Pago` en pagos/models.py tiene `pagMetodo` ENUM con valores: EFECTIVO / TARJETA / TRANSFERENCIA / **PSE**. El documento v2 (DD-09) solo documenta EFECTIVO, TARJETA, TRANSFERENCIA — omite PSE (Pagos Seguros en Línea). |
| **Fuente** | AGENTE-API-MODELOS — inspección directa de pagos/models.py |
| **Prioridad** | MEDIA |
| **Criticidad** | MEDIA |
| **Estado** | PENDIENTE |
| **Recomendación** | Actualizar DD-09 en el diccionario de datos para incluir PSE como valor válido de pagMetodo. Si PSE no está implementado funcionalmente, documentarlo como "reservado para uso futuro". |
| **Relación con plantilla** | Sección 8.2 — Diccionario de Datos |
| **Fecha de detección** | 2026-05-29 (AGENTE-API-MODELOS) |

---

### F-020 — ConfiguracionFidelidad.porcentajeBono no documentado
| Campo | Valor |
|---|---|
| **ID** | F-020 |
| **Nombre** | Campo porcentajeBono en ConfiguracionFidelidad omitido en DD-13 |
| **Tipo** | Omisión en diccionario de datos |
| **Descripción** | El modelo `ConfiguracionFidelidad` (tabla `fidelidad_configuracion`) tiene un campo adicional `porcentajeBono` que no está documentado en DD-13 del diccionario de datos ni en la sección de reglas de negocio. Este campo configura el porcentaje de descuento que otorga el bono de fidelidad (actualmente 100% según CLAUDE.md, pero configurable). |
| **Fuente** | AGENTE-LOCAL-ESTRUCTURA — inspección directa de fidelidad/models.py |
| **Prioridad** | MEDIA |
| **Criticidad** | MEDIA |
| **Estado** | PENDIENTE |
| **Recomendación** | Agregar campo `porcentajeBono` a DD-13 con tipo INT, valor por defecto 100, descripción "Porcentaje de descuento que otorga el bono al alcanzar metaStickers". |
| **Relación con plantilla** | Sección 8.2 — Diccionario de Datos |
| **Fecha de detección** | 2026-05-29 (AGENTE-LOCAL-ESTRUCTURA) |

---

## DOCS ADICIONALES DESCUBIERTOS EN EL REPOSITORIO (no en Drive)

Los agentes encontraron documentación adicional existente en el repo local que no estaba registrada:

| Archivo | Ubicación | Contenido | Estado |
|---|---|---|---|
| README.md | Raíz del proyecto | ~362 líneas — documentación técnica del proyecto | ✅ Existe — integrar referencias al doc principal |
| .claude/database.md | .claude/ | ~318 líneas — documentación de modelos de BD | ✅ Existe — verificar si está sincronizado con doc v2 |
| presentacion/GUION.md | presentacion/ | Guión de presentación del proyecto | ✅ Existe — útil para sección de implantación |
| presentacion/PRESENTACION.md | presentacion/ | Material de presentación | ✅ Existe — útil para anexos |

> **Recomendación:** Revisar estos archivos y referirlos o integrarlos al documento principal v2 donde corresponda. El README.md en particular puede usarse para la sección de instalación/despliegue.
