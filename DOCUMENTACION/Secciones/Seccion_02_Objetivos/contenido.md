# SECCIÓN 2 — Objetivos del Trabajo Final de Proyecto Formativo (TFPF)
# Documento: MultiParking — SENA ADSO · Ficha 3119175
# Norma: APA 7ma edición

---

## INSTRUCCIONES DE FORMATO

- Esta sección inicia en página nueva (salto de página después de la sección 1)
- Título principal: "2. Objetivos del Trabajo Final de Proyecto Formativo (TFPF)" — negrita, centrado, 12pt Times New Roman
- Subtítulos (2.1, 2.2, 2.3): negrita, alineado izquierda, 12pt
- Los objetivos específicos van en lista con viñetas simples (•), con sangría
- Las fases van como sub-etiquetas en negrita antes de cada grupo de objetivos
- Párrafos del cuerpo con sangría de primera línea 1.27 cm
- Doble espacio en todo

---

## 2.1 — OBJETIVO GENERAL

**Título:** 2.1. Objetivo general

Desarrollar un sistema de información web que permita la gestión integral de parqueaderos privados en la localidad de Suba, barrio Compartir, de la ciudad de Bogotá D.C., optimizando el control de ingreso y salida de vehículos, la asignación de espacios en tiempo real, el cálculo automático de tarifas, la gestión de reservas anticipadas, el seguimiento de novedades operativas y la fidelización de usuarios mediante una plataforma accesible, segura y escalable.

---

## 2.2 — OBJETIVOS ESPECÍFICOS

**Título:** 2.2. Objetivos específicos

**Fase de inicio:**

• Analizar los procesos actuales de operación y control en parqueaderos privados de la localidad de Suba para identificar los requerimientos funcionales y no funcionales del sistema.

• Identificar las necesidades de los usuarios (administradores, vigilantes y clientes) mediante la aplicación de encuestas digitales y observación directa en el entorno real.

**Fase de planificación:**

• Diseñar la arquitectura del sistema web bajo el patrón MVT (Modelo-Vista-Template), definiendo la estructura de la base de datos relacional, los módulos funcionales y las interfaces de usuario por rol.

• Elaborar los diagramas de análisis y diseño requeridos: casos de uso, actividades, secuencias, clases y modelo entidad-relación.

**Fase de ejecución:**

• Desarrollar los nueve módulos principales del sistema: usuarios, vehículos, pisos y espacios, inventario de parqueos, tarifas, pagos, cupones de descuento, reservas, novedades operativas, programa de fidelización y reportes.

• Implementar el cálculo automático de tarifas por minuto, las notificaciones automáticas por correo electrónico mediante SendGrid y la exportación de reportes en formatos PDF y Excel.

• Garantizar la seguridad del sistema mediante autenticación por sesión propia, control de acceso basado en roles (ADMIN, VIGILANTE, CLIENTE), política de cabeceras CSP y protección CSRF.

**Fase de implementación:**

• Desplegar el sistema en la plataforma Render.com, configurando el entorno de producción con PostgreSQL, variables de entorno seguras e integración continua (CI/CD).

• Capacitar al personal operativo del parqueadero y realizar pruebas piloto con datos reales antes de la puesta en marcha definitiva.

• Documentar el sistema conforme a la estructura del programa ADSO-SENA y las normas de presentación APA séptima edición.

---

## 2.3 — ALCANCE DEL PROYECTO

**Título:** 2.3. Alcance del proyecto

El sistema MultiParking está diseñado para dar solución a las necesidades operativas de parqueaderos privados de pequeña y mediana escala, con especial referencia a los establecimientos ubicados en la localidad de Suba, barrio Compartir, Bogotá D.C. No obstante, la solución es generalizable a cualquier parqueadero privado con características similares en el territorio nacional.

	**El proyecto abarca las siguientes fases y entregables:**

• Levantamiento y documentación de requerimientos funcionales (RF), no funcionales (RNF), normativos y reglas de negocio.

• Diseño de la arquitectura del sistema y la base de datos relacional (PostgreSQL) con su respectivo diccionario de datos, triggers y scripts SQL.

• Desarrollo e integración de nueve módulos funcionales con sus respectivas interfaces web responsivas.

• Notificaciones automáticas por correo electrónico (SendGrid) para novedades operativas y recuperación de contraseña.

• Exportación de reportes en formato PDF (reportlab) y Excel (openpyxl).

• Despliegue y puesta en producción en Render.com con configuración de CI/CD.

• Documentación técnica completa del sistema según estructura SENA ADSO.

	**Limitaciones y exclusiones del proyecto:**

• No incluye integración con hardware automatizado (barreras vehiculares, sensores de presencia, cámaras de reconocimiento de placas).

• No contempla el desarrollo de aplicación móvil nativa (iOS/Android); el sistema es web responsivo.

• No incluye integración con pasarelas de pago en línea (PSE, PayU, Wompi); los pagos se registran manualmente en el sistema.

• No incluye módulo de facturación electrónica DIAN.

• Las funcionalidades descritas como "versiones futuras" en el documento quedan fuera del alcance del presente trabajo formativo.

---

## NOTA PARA CLAUDE DESKTOP

- Las fases (**Fase de inicio:**, **Fase de planificación:**, etc.) van en negrita como sub-etiqueta antes de los puntos de lista, sin numeración propia.
- Cada viñeta (•) de objetivos específicos va en párrafo separado con sangría de lista 1.27 cm.
- El párrafo introductorio de 2.3 lleva sangría de primera línea.
- Las dos listas de 2.3 ("El proyecto abarca..." y "Limitaciones...") van precedidas por su etiqueta en negrita y luego viñetas con sangría.
