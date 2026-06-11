# FIX.MD — Correcciones aplicadas a las secciones
# Fecha: 2026-06-09

---

## FIX-001 — "Suba" ausente en Introducción (Sección 0)
**Sección afectada:** `Seccion_00_Portada_Resumen/contenido.md`
**Problema:** La introducción hablaba de parqueaderos en general sin ubicar el proyecto.
**Corrección:** Primer párrafo actualizado para abrir con:
> "En la ciudad de Bogotá D.C., específicamente en la localidad de Suba, barrio Compartir..."
**Estado:** ✅ APLICADO

---

## FIX-002 — "Suba" ausente en Alcance (Sección 1.4)
**Sección afectada:** `Seccion_01_Planteamiento_Problema/contenido.md`
**Problema:** El alcance describía el proyecto de forma genérica sin mencionar la ubicación real.
**Corrección:** Primer párrafo del alcance actualizado para incluir:
> "...tomando como contexto de referencia los establecimientos de la localidad de Suba, barrio Compartir, en la ciudad de Bogotá D.C."
**Estado:** ✅ APLICADO

---

## FIX-003 — Justificación basada en estudios genéricos, no en datos propios (Sección 1.3)
**Sección afectada:** `Seccion_01_Planteamiento_Problema/contenido.md`
**Problema:** La justificación original citaba solo estudios académicos genéricos (García & Martínez, 2022; Garavito Albao et al., 2021) sin mencionar los datos reales del trabajo de campo realizado en Suba.
**Corrección:** Justificación reescrita para abrir con los datos reales de la encuesta (n=13) aplicada en el parqueadero de Suba:
- 84,6% usa solo efectivo
- 46,2% inconforme con tiempos de espera y tarifas poco claras
- 92,3% quiere ver costo en tiempo real
- 61,5% usaría reserva anticipada
- 100% abierto a tecnología QR
Los estudios académicos se mantienen como respaldo teórico en el segundo párrafo.
**Estado:** ✅ APLICADO

---

## FIX-004 — Objetivo general sin mencionar Suba (Sección 2.1)
**Sección afectada:** `Seccion_02_Objetivos/contenido.md`
**Problema:** El objetivo general de la sección 2 ya incluye Suba desde la creación inicial.
**Estado:** ✅ YA CORRECTO (creado con Suba desde el inicio)

---

## PENDIENTES POR REVISAR EN SECCIONES FUTURAS

| Sección | Item | Descripción |
|---|---|---|
| Sec 04 | Elicitación | Confirmar que los resultados de la encuesta (13 preguntas completas) están todos documentados |
| Sec 05 | RF | Verificar que los RF reflejan los hallazgos de la encuesta (ej. pago en efectivo, QR, reservas) |
| Sec 12 | Implantación | El plan de capacitación debe mencionar al personal del parqueadero de Suba como beneficiario directo |
| Todas | Referencias | Unificar que "Suba, barrio Compartir" aparece en todas las secciones de contexto |

---

## DATOS DE REFERENCIA — Encuesta Suba (n=13, 2026)

Extraídos de `Documentacion_Multiparking_COMPLETA_v2.txt` líneas 158–376.

| Pregunta | Resultado clave |
|---|---|
| Frecuencia de uso | 30,8% todos los días; 23,1% varias veces/semana |
| Medio de pago | 84,6% efectivo; 7,7% tarjeta; 7,7% app |
| Aspectos molestos | 53,8% pago solo efectivo; 46,2% tiempos de espera; 46,2% tarifas poco claras |
| Código QR para ingreso | 38,5% sí; 61,5% tal vez; 0% no |
| Ver costo en tiempo real | 92,3% sí muy útil |
| Reserva anticipada | 61,5% sí; 30,8% tal vez; 7,7% no |
