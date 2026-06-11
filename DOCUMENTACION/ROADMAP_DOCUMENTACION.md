# ROADMAP DE DOCUMENTACIÓN — Multiparking

**Fecha:** 2026-05-29 | **Versión:** 1.0
**Objetivo:** Llevar la documentación del 68% actual al 100% de cumplimiento SENA ADSO

---

## ESTADO ACTUAL vs OBJETIVO

| Área | Actual | Objetivo | Gap |
|---|---|---|---|
| Análisis de Requisitos | 95% | 100% | 5% |
| Diagramas UML | 20% | 100% | **80%** |
| Pruebas | 60% | 100% | 40% |
| API / Servicios Web | 25% | 100% | **75%** |
| Diseño del Sistema | 55% | 100% | 45% |
| Construcción BD | 70% | 100% | 30% |
| Implantación | 40% | 100% | **60%** |
| Buenas Prácticas | 0% | 100% | **100%** |
| **GLOBAL** | **68%** | **100%** | **32%** |

---

## FASE 1: CRÍTICO — Diagramas UML Faltantes (Prioridad MÁXIMA)

**Duración estimada:** 1 semana
**Impacto en cumplimiento:** +15%

| Tarea | ID Faltante | Herramienta sugerida | Entregable |
|---|---|---|---|
| Crear Historias de Usuario | F-001 | Documento Word/Google Doc | 15+ HU en formato estándar |
| Crear Diagrama de Casos de Uso UML | F-002 | draw.io / Lucidchart | Imagen PNG + integración en doc |
| Crear Diagramas de Actividades (3) | F-003 | draw.io | 3 diagramas: ingreso-salida, reserva, fidelización |
| Crear Diagramas de Secuencias (2) | F-004 | draw.io | 2 diagramas: login, ingreso-pago |
| Crear Modelo de Dominio (Clases) | F-005 | draw.io | 1 diagrama UML clases con 13 entidades |
| Crear Diagrama de Componentes | F-006 | draw.io | 1 diagrama arquitectura |
| Crear Mapa de Navegación | F-007 | draw.io / Figma | 1 diagrama por rol (3 diagramas) |

**Criterio de éxito:** Todos los diagramas integrados en el documento principal v2 como figuras con caption y referencia en índice de diagramas.

---

## FASE 2: ALTO — Pruebas y API (Prioridad ALTA)

**Duración estimada:** 1 semana
**Impacto en cumplimiento:** +10%

| Tarea | ID Faltante | Responsable | Entregable |
|---|---|---|---|
| Implementar tests.py Django (mínimo 5) | F-012 | Desarrollador | tests.py funcionales en usuarios/ y parqueadero/ |
| Capturar evidencias de pruebas | F-014 | Tester | Screenshots/videos de cada caso PU01-PU20 |
| Documentar endpoints API REST | F-013 | Desarrollador | Tabla de endpoints o Swagger |
| Corregir inconsistencia espEstado | I-003 | Desarrollador | Código y doc sincronizados |
| Agregar DD-13 (fidelidad_configuracion) | I-004 | Documentador | Entrada en diccionario de datos |
| Agregar DD-14 (cupones_aplicados) | I-005 | Documentador | Entrada en diccionario de datos |

**Criterio de éxito:** `python manage.py test` ejecuta sin errores; API documentada con al menos 5 endpoints.

---

## FASE 3: MEDIO — Diseño y BD Completos

**Duración estimada:** 3-4 días
**Impacto en cumplimiento:** +8%

| Tarea | ID Faltante | Entregable |
|---|---|---|
| Integrar imágenes MER/MR al documento | F-016 | Secciones 8.1.1-8.1.3 con figuras |
| Crear/documentar vista SQL de parqueos activos | F-017 | SQL de vista + documentación |
| Completar propuesta técnica (costos/hardware) | F-015 | Tablas en sección 5.5 |
| Verificar y analizar casos de uso V1.pdf | I-003 | Integración o reemplazo |
| Analizar MultiParking.drawio | VP-003 | Integración si aplica |

---

## FASE 4: IMPLANTACIÓN — Documentación de Entrega

**Duración estimada:** 3-4 días
**Impacto en cumplimiento:** +7%

| Tarea | ID Faltante | Entregable |
|---|---|---|
| Crear Manual de Usuario PDF formal | F-009 | PDF con screenshots por rol |
| Crear Plan de Capacitación | F-008 | Documento con sesiones y material |
| Agregar sección Garantía/SLA | F-010 | Párrafo en sección 12.5 |
| Agregar sección Buenas Prácticas | F-011 | Sección 13 en doc principal |
| Completar Anexos | F-018 | Evidencias, actas, cronograma |
| Actualizar Índice de diagramas | F-018 | Índice actualizado |
| Aclarar integrante Jhorman | I-001 | Actualizar portada si aplica |
| Archivar documentos obsoletos | O-001..O-006 | Mover a carpeta Obsoletos |

---

## CRONOGRAMA SUGERIDO

```
Semana 1 (Fase 1): Diagramas UML
├── Lun-Mar: HU + Casos de Uso
├── Mié-Jue: Actividades + Secuencias
└── Vie: Clases + Componentes + Navegación

Semana 2 (Fase 2): Pruebas + API
├── Lun-Mar: Tests automatizados Django
├── Mié-Jue: Evidencias de pruebas
└── Vie: Documentación API REST

Semana 3 (Fases 3 y 4): Completar
├── Lun-Mar: MER, vistas BD, propuesta técnica
├── Mié-Jue: Manual PDF, capacitación
└── Vie: Revisión final, índices, cierre
```

---

## CHECKLIST DE ENTREGA FINAL

### Sección 6 — Análisis (Actualmente 35%)
- [ ] F-001: Historias de Usuario (15+ HU)
- [ ] F-002: Diagrama de Casos de Uso UML visual
- [ ] F-003: Diagramas de Actividades (3 flujos)
- [ ] F-004: Diagramas de Secuencias (2 flujos)
- [ ] F-005: Modelo de Dominio (Diagrama de Clases)

### Sección 7 — Diseño (Actualmente 55%)
- [ ] F-006: Diagrama de Componentes UML
- [ ] VP-003: Verificar drawio y diagrama despliegue
- [ ] F-007: Mapa de Navegación (3 roles)

### Sección 8 — Construcción BD (Actualmente 70%)
- [ ] F-016: Integrar MER/MR visual al documento
- [ ] F-017: Vista SQL documentada
- [ ] I-004: DD-13 (fidelidad_configuracion)
- [ ] I-005: DD-14 (cupones_aplicados)

### Sección 9 — Codificación (Actualmente 65%)
- [ ] F-013: Documentación API REST (endpoints)
- [ ] I-003: Resolver MANTENIMIENTO vs INACTIVO

### Sección 10 — Pruebas (Actualmente 60%)
- [ ] F-012: Implementar tests.py automatizados
- [ ] F-014: Evidencias/screenshots de pruebas
- [ ] VP-002: Analizar y usar casos de uso V1.pdf

### Sección 12 — Implantación (Actualmente 40%)
- [ ] F-008: Plan de Capacitación
- [ ] F-009: Manual de Usuario PDF
- [ ] F-010: Garantía / SLA

### Sección 13 — Buenas Prácticas (Actualmente 0%)
- [ ] F-011: Sección de Buenas Prácticas

### Limpieza y Consistencia
- [ ] I-001: Aclarar integrante Jhorman
- [ ] I-002: Archivar Documentacion_V4.docx (obsoleto)
- [ ] O-001 a O-006: Limpiar archivos obsoletos en Drive
- [ ] F-018: Completar índices de diagramas y tablas

---

## RIESGOS DEL ROADMAP

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Falta de tiempo para todos los diagramas UML | MEDIA | ALTO | Priorizar Casos de Uso y Clases |
| Diagramas sin integrar al doc principal | ALTA | ALTO | Agregar como imágenes con referencias formales |
| Tests Django requieren conocimiento avanzado | MEDIA | MEDIO | Implementar mínimo viable (5 tests básicos) |
| API REST parcialmente implementada | ALTA | MEDIO | Documentar estado actual y dejar nota de trabajo futuro |
| Disponibilidad del equipo | BAJA | ALTO | Documentación compartida y roles cruzados (per RN07) |

---

## MÉTRICAS DE SEGUIMIENTO

| Semana | Meta cumplimiento | Faltantes resueltos |
|---|---|---|
| Actual | 68% | 0/37 |
| Semana 1 | 83% | ~14/37 (Fase 1) |
| Semana 2 | 90% | ~22/37 (Fases 1+2) |
| Semana 3 | 100% | 37/37 (Completo) |
