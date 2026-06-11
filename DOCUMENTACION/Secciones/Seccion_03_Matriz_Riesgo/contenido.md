# SECCIÓN 3 — Matriz de Riesgo
# Documento: MultiParking — SENA ADSO · Ficha 3119175
# Norma: APA 7ma edición

---

## INSTRUCCIONES DE FORMATO

- Esta sección inicia en página nueva
- Título: "3. Matriz de Riesgo" — negrita, centrado, 12pt Times New Roman
- La tabla lleva título APA 7 ANTES de la tabla:
  - Línea 1: **Tabla 1** (negrita, alineada a la izquierda)
  - Línea 2: *Matriz de Riesgos del Proyecto MultiParking* (cursiva, alineada a la izquierda)
- Después de la tabla va la nota:
  - *Nota.* Elaboración propia (2026).
- La tabla puede ser en tamaño 10pt para que quepa en una página
- Encabezados de tabla en negrita
- Columnas: Nº | Riesgo | Causa | Impacto | Probabilidad | Nivel | Estrategia de mitigación

---

## 3.1 — TEXTO INTRODUCTORIO

**Título:** 3. Matriz de Riesgo

Durante la fase de planificación del proyecto se identificaron los principales riesgos que podrían afectar el desarrollo, la implementación y la operación del sistema MultiParking. La Tabla 1 presenta cada riesgo con su causa, impacto potencial, probabilidad de ocurrencia, nivel de riesgo resultante y la estrategia de mitigación definida por el equipo de desarrollo.

---

## 3.2 — TABLA DE RIESGOS

**Tabla 1**
*Matriz de Riesgos del Proyecto MultiParking*

| Nº | Riesgo | Causa | Impacto | Probabilidad | Nivel | Estrategia de mitigación |
|---|---|---|---|---|---|---|
| 1 | Retrasos en el desarrollo del sistema | Subestimación de tiempos o problemas técnicos imprevistos | Aplazamiento en la entrega final del TFPF | Media | **Medio** | Cronograma ágil con revisión semanal de avances y redistribución de tareas. |
| 2 | Insatisfacción de usuarios por ausencia de pago digital automatizado | La integración con pasarelas de pago en línea (PSE, PayU, Wompi) quedó fuera del alcance del TFPF por complejidad técnica y requerimientos de certificación | Usuarios podrían percibir el sistema como incompleto al no poder pagar directamente en línea desde la plataforma | Media | **Medio** | El módulo de pagos registra manualmente efectivo, transferencia bancaria y tarjeta como categorías. El diseño del módulo está preparado para integración con pasarelas en versiones futuras. |
| 3 | Falta de conectividad en el entorno piloto (Suba) | Infraestructura deficiente de red en el parqueadero | Fallos en el acceso o carga del sistema durante la operación | Alta | **Alto** | Verificar requisitos técnicos de conectividad del sitio previamente al despliegue. |
| 4 | Baja adopción por parte de los usuarios | Resistencia al cambio por parte del personal operativo | Uso limitado del sistema y regreso a procesos manuales | Media | **Medio** | Capacitaciones prácticas y pruebas piloto con retroalimentación continua. |
| 5 | Pérdida de datos durante el uso | Fallos en el servidor o en la base de datos | Pérdida de historial de parqueos y registros operativos | Baja | **Bajo** | Backups automáticos diarios en Render.com (pg_dump + snapshots). |
| 6 | Cambios en los requerimientos del cliente | Nuevas necesidades descubiertas durante el desarrollo | Re-trabajo o rediseño de módulos ya implementados | Media | **Medio** | Reuniones frecuentes con stakeholders y control de cambios documentado. |
| 7 | Salida de un integrante clave del equipo | Problemas personales o deserción académica | Retrasos significativos o redistribución forzada de tareas | Baja | **Bajo** | Documentación compartida, repositorio Git con historial completo y roles cruzados. |

*Nota.* Elaboración propia (2026).

---

## NOTA PARA CLAUDE DESKTOP

- La tabla debe ocupar todo el ancho de la página.
- La columna "Estrategia de mitigación" puede tener texto en varias líneas — está bien.
- El nivel de riesgo (Alto/Medio/Bajo) puede tener color de fondo en la celda:
  - Alto → fondo rojo claro (#FFCCCC)
  - Medio → fondo amarillo claro (#FFF2CC)
  - Bajo → fondo verde claro (#D9EAD3)
- La nota va en tamaño 10pt debajo de la tabla, sin sangría, con *Nota.* en cursiva.
- No hay texto después de la tabla en esta sección — la sección 4 empieza en página nueva.
