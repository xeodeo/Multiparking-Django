# SECCIÓN 1 — Planteamiento y Justificación del Problema
# Documento: MultiParking — SENA ADSO · Ficha 3119175
# Norma: APA 7ma edición

---

## INSTRUCCIONES DE FORMATO

- Esta sección inicia en página nueva (salto de página después de la Introducción)
- Título principal: "1. Planteamiento y Justificación del Problema" — negrita, centrado, 12pt Times New Roman
- Subtítulos de subsección (1.1, 1.2, etc.): negrita, alineado izquierda, 12pt
- Párrafos con sangría de primera línea 1.27 cm
- Doble espacio en todo el cuerpo
- El árbol del problema va como FIGURA con título APA 7:
  - Línea 1: **Figura 1** (negrita)
  - Línea 2: *Árbol del problema del sistema MultiParking* (cursiva)
  - Línea 3: Nota. Elaboración propia (2026).

---

## 1.1 — PLANTEAMIENTO DEL PROBLEMA

**Título:** 1.1. Planteamiento del problema

En la ciudad de Bogotá D.C., específicamente en la localidad de Suba, barrio Compartir, los parqueaderos privados de pequeña y mediana escala gestionan sus operaciones mediante procesos completamente manuales. El control del ingreso y salida de vehículos depende de planillas físicas, lo que impide contar con trazabilidad confiable y genera inconsistencias frecuentes en los tiempos registrados y los valores cobrados a los usuarios. La ausencia de un sistema tecnológico centralizado limita la visibilidad en tiempo real de los espacios disponibles, dificulta la conciliación de pagos y complica la detección oportuna de errores o irregularidades operativas.

	A esta problemática se suma la imposibilidad de realizar reservas anticipadas de espacios, lo que reduce la satisfacción del usuario y la competitividad del establecimiento frente a alternativas que sí ofrecen servicios digitales. Los propietarios y administradores tampoco cuentan con herramientas que les permitan generar reportes de ingresos, analizar la ocupación histórica o fidelizar a sus clientes habituales mediante incentivos digitales.

	De continuar esta situación, los establecimientos afectados seguirán incurriendo en pérdidas económicas por cobros imprecisos, pérdida de clientes por deficiencias en el servicio y exposición a fraudes internos por la falta de trazabilidad en los registros operativos.

---

## 1.2 — ÁRBOL DEL PROBLEMA

**Título:** 1.2. Árbol del problema

[INSERTAR FIGURA 1 AQUÍ — archivo: arbol_problema.png en esta misma carpeta]

**Figura 1**
*Árbol del problema del sistema MultiParking*
Nota. Elaboración propia (2026).

### Contenido del árbol (para construir el diagrama):

**EFECTOS (parte superior del árbol):**
1. Pérdida de información y trazabilidad en el registro de vehículos — causada por registros manuales dispersos y falta de integración del sistema.
2. Cobros imprecisos o injustos por uso del parqueadero — debido a la ausencia de tarifación confiable y auditoría en tiempo real.
3. Filas y demoras en el ingreso y salida de vehículos — por control manual y verificación lenta.
4. Inconformidad de los residentes y visitantes — generada por tiempos de espera, cobros erróneos y baja transparencia operativa.

**PROBLEMA PRINCIPAL (centro del árbol):**
Ineficiencia, falta de trazabilidad y pobre control en parqueaderos privados, ocasionado por procesos manuales, información no centralizada y carencia de herramientas digitales que soporten la operación, el cobro y la toma de decisiones (Bookings & Hernández, 2023).

**CAUSAS (parte inferior del árbol):**
1. Control manual del ingreso y salida de vehículos — provoca cuellos de botella y errores humanos.
2. Registro de información en papel o planillas físicas — genera pérdida de datos y dificultad para auditorías.
3. Falta de infraestructura tecnológica — limita la automatización y trazabilidad.
4. Ausencia de herramientas digitales para cobros y reservas — impide calcular tarifas correctas y agilizar pagos.

---

## 1.3 — JUSTIFICACIÓN

**Título:** 1.3. Justificación

Con el fin de fundamentar el desarrollo de este proyecto, se realizó un proceso de recolección de información directamente en parqueaderos privados de la localidad de Suba, barrio Compartir, en la ciudad de Bogotá D.C. Se aplicó una encuesta digital a 13 usuarios y administradores del sector, complementada con observación directa en días de alta y baja afluencia. Los resultados evidenciaron de manera contundente la necesidad de una solución tecnológica: el 84,6 % de los encuestados señaló que el efectivo es el único medio de pago aceptado en los parqueaderos que frecuentan; el 46,2 % manifestó inconformidad con los largos tiempos de espera y con la falta de claridad en las tarifas; y el 92,3 % consideró muy útil poder visualizar el tiempo de permanencia y el costo acumulado en tiempo real. Adicionalmente, el 61,5 % de los participantes indicó que usaría un sistema de reserva anticipada de espacios, y el 100 % se mostró abierto al uso de tecnología como códigos QR para el ingreso (Elaboración propia, 2026).

	Estos hallazgos se alinean con estudios académicos que confirman la efectividad de los sistemas digitales de gestión en este tipo de establecimientos. García y Martínez (2022) señalan que la adopción de plataformas digitales de gestión de aparcamientos mejora la eficiencia operativa, reduce errores humanos y ofrece trazabilidad de datos en tiempo real. Por su parte, Garavito Albao et al. (2021) demuestran que los sistemas de información en pequeñas empresas de servicios reducen el tiempo de atención hasta en un 40 % y disminuyen los errores de registro en más del 60 %.

	El desarrollo de MultiParking responde directamente a esta problemática al proporcionar una plataforma centralizada que digitaliza todos los procesos operativos del parqueadero. La solución beneficia a tres perfiles de usuarios: administradores, que obtienen visibilidad total del estado del parqueadero y acceso a reportes de inteligencia operativa; vigilantes, que agilizan los procesos de ingreso y salida mediante interfaces simplificadas; y clientes, que acceden a reservas anticipadas, historial de parqueos y beneficios de fidelización acumulables. Desde la perspectiva técnica, la implementación sobre Django (Python 3.12) con PostgreSQL garantiza mantenibilidad a largo plazo, escalabilidad y seguridad de datos, mientras que el despliegue en Render.com permite disponibilidad continua sin inversión en infraestructura propia.

---

## 1.4 — ALCANCE DEL PROYECTO

**Título:** 1.4. Alcance del proyecto

El proyecto consiste en desarrollar un sistema de información web denominado MultiParking, orientado a automatizar la gestión integral de parqueaderos privados de pequeña y mediana escala, tomando como contexto de referencia los establecimientos de la localidad de Suba, barrio Compartir, en la ciudad de Bogotá D.C. El sistema opera como plataforma web responsiva accesible desde dispositivos móviles o computadores de escritorio, sin requerir hardware especializado adicional.

	**El alcance incluye:**
- Levantamiento y documentación de requerimientos funcionales y no funcionales.
- Diseño de la arquitectura del sistema y la base de datos relacional (PostgreSQL).
- Desarrollo de nueve módulos funcionales: usuarios, vehículos, pisos y espacios, inventario de parqueos, tarifas, pagos, cupones de descuento, reservas, novedades operativas, fidelización y reportes.
- Notificaciones automáticas por correo electrónico mediante SendGrid.
- Exportación de reportes en formato PDF (reportlab) y Excel (openpyxl).
- Despliegue y puesta en producción en Render.com con integración continua (CI/CD).
- Documentación técnica completa del sistema.

	**Quedan fuera del alcance:**
- Integración con hardware automatizado (barreras vehiculares, sensores de presencia, cámaras de reconocimiento de placas).
- Desarrollo de aplicación móvil nativa (iOS/Android).
- Integración con pasarelas de pago en línea (contemplada para versiones futuras).
- Módulo de facturación electrónica DIAN.

---

## NOTA PARA CLAUDE DESKTOP

- La subsección 1.2 (Árbol del problema) debe tener un espacio reservado con el texto "[VER FIGURA 1]" centrado entre los párrafos, donde se insertará la imagen del árbol una vez creada.
- El árbol del problema se debe crear como diagrama visual en draw.io o Lucidchart con tres niveles: Efectos (arriba), Problema central (medio, en recuadro), Causas (abajo), conectados con líneas.
- Las listas con viñetas de "El alcance incluye" y "Quedan fuera del alcance" van con viñetas simples (•), no numeradas.
- Las referencias entre paréntesis siguen formato APA 7: (Autor, año) o (Autor et al., año).
