# SECCIÓN 5 — Requerimientos del Sistema
# Documento: MultiParking — SENA ADSO · Ficha 3119175
# Norma: APA 7ma edición
# Fuente base: Documentacion_Multiparking_COMPLETA_v2.txt (documento más reciente)
# Verificado contra: Documentacion_V3.docx, Documentacion_V4.docx, Requerimientos_MultiParking.docx
# Correcciones aplicadas vs código real: espEstado usa INACTIVO (no MANTENIMIENTO); 9 apps Django (no 11)
# Adición RF63 (escaneo QR) identificada en verificación cruzada — presente en CLAUDE.md y /parqueadero/escanear/

---

## INSTRUCCIONES DE FORMATO

- Sección inicia en página nueva
- Título "5. Requerimientos del Sistema" — negrita, centrado, 12pt
- Subtítulos 5.1 / 5.2 / 5.3 / 5.4 — negrita, alineado izquierda, 12pt
- Cada módulo dentro de 5.1 tiene su propia tabla APA 7:
  - **Tabla N** — negrita, flush left, sin sangría
  - *Título en cursiva* — flush left, sin sangría
  - Tabla de datos (10pt)
  - *Nota.* Elaboración propia (2026). — flush left, sin sangría, 10pt
- Columnas de tablas RF: Código | Nombre | Descripción | Entradas | Prioridad
- Columnas de tablas RNF: Código | Nombre | Descripción | Criterio de aceptación | Prioridad
- La columna Descripción puede tener texto en varias líneas — está bien
- Párrafos introductorios de sección con sangría de primera línea 1.27 cm

---

## 5.1 — REQUERIMIENTOS FUNCIONALES

**Título:** 5.1. Requerimientos funcionales

	Los requerimientos funcionales describen las capacidades y comportamientos que el sistema MultiParking debe proveer a sus usuarios. Se organizan por módulo de aplicación y se identifican con el prefijo RF seguido de un número secuencial.

---

**Tabla 14**
*Requerimientos funcionales — Módulo Usuarios*

| Código | Nombre | Descripción | Entradas | Prioridad |
|---|---|---|---|---|
| RF01 | Registrar usuario | El sistema permitirá registrar un nuevo usuario capturando nombre, apellido, documento de identidad, correo electrónico, teléfono y contraseña. La contraseña se almacenará cifrada con PBKDF2-SHA256. | usuNombre, usuApellido, usuDocumento, usuCorreo, usuTelefono, usuClaveHash | Alta |
| RF02 | Iniciar sesión | El sistema permitirá autenticarse mediante correo y contraseña. Se verificará el hash y se creará sesión con datos del usuario y su rol. | usuCorreo, contraseña | Alta |
| RF03 | Cerrar sesión | El sistema permitirá finalizar la sesión activa, eliminando los datos de sesión del servidor. | Sesión activa | Alta |
| RF04 | Recuperar contraseña | El sistema enviará al correo registrado un enlace de recuperación con token de un solo uso. Al usarlo, el token queda invalidado automáticamente. | usuCorreo | Alta |
| RF05 | Gestionar usuarios (Admin) | El administrador podrá crear, editar, activar/desactivar y eliminar usuarios del sistema. | usuNombre, usuApellido, usuDocumento, usuCorreo, usuTelefono, rolTipoRol | Alta |
| RF06 | Asignar rol | El sistema soportará tres roles: ADMIN, VIGILANTE y CLIENTE, con acceso diferenciado por panel y vistas. | rolTipoRol (ENUM) | Alta |
| RF07 | Ver perfil propio | El usuario podrá consultar sus datos personales, historial de parqueos, stickers acumulados y reservas activas. | Sesión activa | Media |
| RF08 | Actualizar datos personales | El usuario podrá modificar su nombre, apellido, teléfono y contraseña desde su perfil. | usuNombre, usuApellido, usuTelefono, nueva contraseña | Media |

*Nota.* Elaboración propia (2026).

---

**Tabla 15**
*Requerimientos funcionales — Módulo Vehículos*

| Código | Nombre | Descripción | Entradas | Prioridad |
|---|---|---|---|---|
| RF09 | Registrar vehículo propio | El cliente podrá registrar vehículos asociados a su cuenta indicando placa, tipo, color, marca y modelo. | vehPlaca, vehTipo, vehColor, vehMarca, vehModelo, fkIdUsuario | Alta |
| RF10 | Registrar vehículo visitante | El vigilante podrá registrar vehículos de visitantes sin cuenta, capturando placa, tipo, nombre y teléfono de contacto. | vehPlaca, vehTipo, nombre_contacto, telefono_contacto | Alta |
| RF11 | Listar vehículos por usuario | El sistema mostrará la lista de vehículos registrados por el usuario autenticado. | fkIdUsuario (sesión) | Media |
| RF12 | Editar vehículo | El usuario podrá modificar los datos de un vehículo propio (color, marca, modelo). | vehPlaca, vehTipo, vehColor, vehMarca, vehModelo | Media |
| RF13 | Eliminar vehículo | El administrador podrá eliminar un vehículo si no tiene registros activos ni reservas vigentes. | idVehiculo | Baja |

*Nota.* Elaboración propia (2026).

---

**Tabla 16**
*Requerimientos funcionales — Módulo Espacios*

| Código | Nombre | Descripción | Entradas | Prioridad |
|---|---|---|---|---|
| RF14 | Gestionar pisos | El administrador podrá crear, editar y desactivar pisos del parqueadero. No se elimina un piso con espacios ocupados. | pisNombre, pisEstado | Alta |
| RF15 | Gestionar tipos de espacio | El administrador podrá crear y editar tipos de espacio (p. ej., CARRO, MOTO, BICICLETA). | nombre (TipoEspacio) | Alta |
| RF16 | Gestionar espacios | El administrador podrá crear, editar y eliminar espacios individuales por piso y tipo. | espNumero, fkIdPiso, fkIdTipoEspacio, espEstado | Alta |
| RF17 | Ver disponibilidad en tiempo real | El sistema mostrará la vista general de pisos coloreada por estado (DISPONIBLE / OCUPADO / RESERVADO / INACTIVO), actualizada vía AJAX. | Dashboard | Alta |
| RF18 | Cambiar estado de espacio | El administrador podrá cambiar manualmente el estado de un espacio a INACTIVO y viceversa. | idEspacio, espEstado | Media |
| RF19 | Mostrar placa en espacio ocupado | La vista general mostrará la placa del vehículo actualmente parqueado en espacios OCUPADOS. | InventarioParqueo activo (fkIdEspacio) | Media |

*Nota.* Elaboración propia (2026).

---

**Tabla 17**
*Requerimientos funcionales — Módulo Inventario Parqueos*

| Código | Nombre | Descripción | Entradas | Prioridad |
|---|---|---|---|---|
| RF20 | Registrar ingreso de vehículo | El vigilante registrará el ingreso seleccionando placa y espacio. El sistema registra la hora de entrada y cambia el espacio a OCUPADO. | fkIdVehiculo, fkIdEspacio, parHoraEntrada | Alta |
| RF21 | Registrar salida de vehículo | El vigilante registrará la salida. El sistema calcula el costo, genera el pago y libera el espacio a DISPONIBLE. | idParqueo, parHoraSalida | Alta |
| RF22 | Calcular costo de parqueo | Fórmula: ceil((minutos / 60) × precioHora / 100) × 100. Visitantes usan precioHoraVisitante. Mínimo 100 COP. | parHoraEntrada, parHoraSalida, precioHora | Alta |
| RF23 | Control de estado del espacio | Al ingresar: espacio → OCUPADO. Al salir: espacio → DISPONIBLE. También aplica al confirmar o cancelar reservas. | espEstado (ENUM) | Alta |
| RF24 | Ver historial de parqueos | El admin ve historial completo con filtros. El cliente ve solo sus propios registros. | Fecha, fkIdVehiculo, fkIdEspacio | Media |
| RF25 | Ver parqueos activos en tiempo real | El dashboard del vigilante muestra vehículos parqueados con espacio, hora y tiempo acumulado, actualizado vía AJAX. | parHoraSalida IS NULL | Alta |
| RF26 | Evitar doble ingreso activo | El sistema valida que un vehículo no pueda tener más de un registro activo simultáneo. | fkIdVehiculo, parHoraSalida__isnull | Alta |
| RF63 | Iniciar ingreso mediante escaneo QR | El sistema dispondrá de una URL de entrada accesible vía código QR físico en el parqueadero. Al escanearla, el usuario es dirigido al flujo de verificación, selección de vehículo y asignación de espacio sin pasar por el panel de vigilante. | Token del QR, usuDocumento, idVehiculo o datos de nuevo vehículo | Alta |

*Nota.* Elaboración propia (2026).

---

**Tabla 18**
*Requerimientos funcionales — Módulo Tarifas*

| Código | Nombre | Descripción | Entradas | Prioridad |
|---|---|---|---|---|
| RF27 | Crear tarifa | El administrador creará tarifas con nombre, tipo de espacio, precio por hora (usuario/visitante), precio por día, precio mensual y fechas de vigencia. | nombre, fkIdTipoEspacio, precioHora, precioHoraVisitante, precioDia, precioMensual, fechaInicio, fechaFin | Alta |
| RF28 | Tarifa activa única por tipo | Solo una tarifa activa por tipo de espacio. Al activar una nueva, se desactiva automáticamente la anterior del mismo tipo. | activa (BooleanField), fkIdTipoEspacio | Alta |
| RF29 | Editar y desactivar tarifa | El administrador podrá editar o desactivar tarifas. No se eliminan tarifas con parqueos asociados. | idTarifa, activa | Media |
| RF30 | Consultar tarifa vigente | El sistema mostrará la tarifa activa del tipo de espacio al registrar un ingreso o calcular un costo. | fkIdTipoEspacio, activa=True | Alta |

*Nota.* Elaboración propia (2026).

---

**Tabla 19**
*Requerimientos funcionales — Módulo Pagos*

| Código | Nombre | Descripción | Entradas | Prioridad |
|---|---|---|---|---|
| RF31 | Generar pago al registrar salida | Al registrar la salida se generará automáticamente un registro de pago con monto calculado, método y estado PAGADO. | pagMonto, pagMetodo, pagEstado, fkIdParqueo | Alta |
| RF32 | Aplicar cupón en pago | El vigilante podrá ingresar un código de cupón antes de finalizar el cobro. Si es válido, el descuento se aplica al monto total. | cupCodigo, pagMonto | Alta |
| RF33 | Ver historial de pagos | El admin ve todos los pagos con filtros por fecha, monto, método y estado. El cliente ve solo los suyos. | pagFechaPago, pagEstado | Media |
| RF34 | Reportes de ingresos | El sistema generará reportes de ingresos agrupados por período, mostrando total recaudado y número de transacciones. | pagFechaPago, pagMonto | Media |
| RF35 | Exportar reportes | El admin podrá descargar reportes de ingresos, ocupación, reservas y cupones en PDF (reportlab) o Excel (openpyxl). | Filtros de reporte seleccionados | Media |

*Nota.* Elaboración propia (2026).

---

**Tabla 20**
*Requerimientos funcionales — Módulo Cupones*

| Código | Nombre | Descripción | Entradas | Prioridad |
|---|---|---|---|---|
| RF36 | Crear cupón | El administrador creará cupones con nombre, código único alfanumérico en mayúsculas, tipo (PORCENTAJE / VALOR_FIJO), valor, fechas de vigencia y estado activo. | cupNombre, cupCodigo, cupTipo, cupValor, cupFechaInicio, cupFechaFin, cupActivo | Alta |
| RF37 | Validar cupón | Al aplicar un cupón se verificará: código existente, activo=True y dentro de fechas de vigencia. | cupCodigo, cupActivo, cupFechaFin | Alta |
| RF38 | Aplicar descuento | PORCENTAJE: descuento = cupValor% del total. VALOR_FIJO: descuento fijo en COP. El monto final no puede ser negativo. | cupTipo, cupValor, pagMonto | Alta |
| RF39 | Registrar uso de cupón | Cada uso de cupón se registra en CuponAplicado con pago, cupón y monto descontado. | fkIdPago, fkIdCupon, montoDescontado | Alta |
| RF40 | Desactivar cupón vencido | El sistema detecta cupones con cupFechaFin pasada y los marca inactivos en el momento de la validación. | cupFechaFin, fecha actual | Media |
| RF41 | Listar cupones activos | El administrador consultará la lista de cupones con estado, vigencia y número de usos. | cupActivo, cupFechaFin | Media |

*Nota.* Elaboración propia (2026).

---

**Tabla 21**
*Requerimientos funcionales — Módulo Reservas*

| Código | Nombre | Descripción | Entradas | Prioridad |
|---|---|---|---|---|
| RF42 | Registrar reserva | El cliente o administrador podrá reservar un espacio para una fecha y hora específicas, verificando que no exista traslape con otra reserva activa. | resFechaReserva, resHoraInicio, resHoraFin, fkIdEspacio, fkIdVehiculo | Alta |
| RF43 | Consultar disponibilidad para reserva | El sistema mostrará espacios disponibles para una fecha y rango horario, excluyendo los que tengan reservas solapadas o estén OCUPADOS o INACTIVOS. | resFechaReserva, resHoraInicio, resHoraFin | Alta |
| RF44 | Cancelar reserva | El cliente podrá cancelar una reserva propia siempre que no haya comenzado. Al cancelar, el espacio regresa a DISPONIBLE. | idReserva, resEstado | Alta |
| RF45 | Modificar reserva | El administrador o cliente podrán editar fecha u hora de una reserva, siempre que el nuevo horario esté disponible. | idReserva, resFechaReserva, resHoraInicio, resHoraFin | Media |
| RF46 | Bloquear espacio al confirmar reserva | Al confirmar: espacio → RESERVADO. Al cancelar: espacio → DISPONIBLE. Al convertir a parqueo: espacio → OCUPADO. | espEstado, resEstado | Alta |

*Nota.* Elaboración propia (2026).

---

**Tabla 22**
*Requerimientos funcionales — Módulo Novedades*

| Código | Nombre | Descripción | Entradas | Prioridad |
|---|---|---|---|---|
| RF47 | Registrar novedad | El vigilante o administrador registrará una novedad asociándola a un vehículo y/o espacio, con descripción, foto (máx. 5 MB, JPG/PNG/GIF/WEBP) y estado PENDIENTE por defecto. | novDescripcion, novFoto, fkIdVehiculo, fkIdEspacio, fkIdReportador | Alta |
| RF48 | Actualizar estado de novedad | El administrador cambiará el estado entre PENDIENTE, EN_PROCESO y RESUELTO, agregando comentario de seguimiento. | novEstado, novComentario | Alta |
| RF49 | Asignar responsable | Al crear o editar una novedad se podrá asignar un responsable con rol ADMIN o VIGILANTE. | fkIdResponsable | Media |
| RF50 | Filtrar novedades | El listado se filtrará por estado y por texto en la descripción. | novEstado, novDescripcion__icontains | Media |
| RF51 | Notificar usuario por correo | Al crear o actualizar una novedad, el sistema enviará correo al dueño del vehículo afectado mediante SendGrid. | fkIdVehiculo → fkIdUsuario → usuCorreo | Alta |
| RF52 | Eliminar novedad | El administrador podrá eliminar una novedad del sistema (acción irreversible). | idNovedad | Baja |

*Nota.* Elaboración propia (2026).

---

**Tabla 23**
*Requerimientos funcionales — Módulo Fidelización*

| Código | Nombre | Descripción | Entradas | Prioridad |
|---|---|---|---|---|
| RF53 | Acumular sticker al completar parqueo | Al registrar la salida de un vehículo con propietario registrado y permanencia > 60 minutos, se asigna automáticamente un sticker al usuario. | parHoraEntrada, parHoraSalida, fkIdUsuario, permanencia > 60 min | Alta |
| RF54 | Ver stickers en perfil | El cliente verá en su perfil los stickers acumulados, la meta configurada y una barra de progreso. Cuando alcance la meta, aparece el botón de canje. | fkIdUsuario, metaStickers (ConfiguracionFidelidad) | Alta |
| RF55 | Reclamar bono por meta alcanzada | Al alcanzar la meta, el usuario reclama un cupón del 100% generado automáticamente, con vigencia configurada y uso único. | stkFecha, metaStickers, cupValor=100, cupTipo=PORCENTAJE | Alta |
| RF56 | Configurar meta de stickers | El administrador modificará el número de stickers necesarios para el bono y los días de vigencia del cupón generado. | metaStickers, diasVencimientoBono (ConfiguracionFidelidad) | Media |

*Nota.* Elaboración propia (2026).

---

**Tabla 24**
*Requerimientos funcionales — Módulo Reportes*

| Código | Nombre | Descripción | Entradas | Prioridad |
|---|---|---|---|---|
| RF57 | Reporte de ingresos por período | El administrador generará reportes de ingresos filtrando por rango de fechas, con total recaudado, número de transacciones y promedio por operación. | pagFechaPago (rango), pagMonto | Alta |
| RF58 | Reporte de ocupación por espacio | El sistema generará un reporte de porcentaje de ocupación por espacio para identificar los de mayor y menor rotación. | fkIdEspacio, parHoraEntrada (rango) | Media |
| RF59 | Reporte de reservas | El admin verá el volumen de reservas por período con desglose por estado y tipo de espacio. | resFechaReserva (rango), resEstado | Media |
| RF60 | Reporte de cupones aplicados | Reporte de cupones utilizados con código, número de usos, monto total descontado y período de aplicación. | fkIdCupon, montoDescontado, pagFechaPago | Media |
| RF61 | Visualización con gráficas | El dashboard mostrará gráficas interactivas con Chart.js: barras de ingresos por día, líneas de ocupación y dona por tipo de espacio. | Datos de pagos e inventario agrupados | Media |
| RF62 | Exportar a PDF y Excel | Todos los reportes podrán descargarse en PDF (reportlab) o Excel (openpyxl) con encabezado, logo y fecha de generación. | Filtros de reporte seleccionados | Media |

*Nota.* Elaboración propia (2026).

---

## 5.2 — REQUERIMIENTOS NO FUNCIONALES

**Título:** 5.2. Requerimientos no funcionales

	Los requerimientos no funcionales establecen los atributos de calidad del sistema, siguiendo el modelo ISO/IEC 25010 (ISO, 2011).

**Tabla 25**
*Requerimientos no funcionales del sistema MultiParking*

| Código | Nombre | Descripción | Criterio de aceptación | Prioridad |
|---|---|---|---|---|
| RNF01 | Rendimiento | El tiempo de respuesta para operaciones estándar no superará 3 segundos bajo condiciones normales de uso. | Tiempo de respuesta HTTP < 3 s en el 95% de las peticiones | Alta |
| RNF02 | Seguridad | HTTPS obligatorio, Content-Security-Policy y X-XSS-Protection mediante middleware, X-Frame-Options: DENY, HSTS y protección contra fijación de sesión. | SecurityHeadersMiddleware activo; sin vulnerabilidades OWASP Top 10 | Alta |
| RNF03 | Usabilidad | Interfaz responsiva con Tailwind CSS. Tres paneles diferenciados por rol (morado para Admin, azul para Vigilante, verde para Cliente). Validación en tiempo real en formularios. | Pruebas de usabilidad exitosas en móvil y escritorio | Alta |
| RNF04 | Disponibilidad | 99% de uptime en horario operativo, garantizado por Render.com con reinicio automático ante fallos del proceso. | Uptime ≥ 99% medido mensualmente | Alta |
| RNF05 | Mantenibilidad | Código organizado en 9 apps Django con arquitectura MVT. Convenciones de nomenclatura consistentes (camelCase prefijado por tabla). | Todas las apps con models.py, views.py y urls.py propios | Alta |
| RNF06 | Portabilidad | Desplegable en cualquier PaaS que soporte Python 3.12 y PostgreSQL sin depender de hardware específico. | requirements.txt y .env.example incluidos en el repositorio | Media |
| RNF07 | Escalabilidad | Paginación en vistas con más de 20 registros para evitar degradación de rendimiento. | Django Paginator implementado en listados de inventario y pagos | Media |
| RNF08 | Compatibilidad | Compatible con las dos últimas versiones de Chrome, Firefox y Microsoft Edge. | Sin errores de renderizado en los tres navegadores | Media |
| RNF09 | Internacionalización | Interfaz completamente en español, zona horaria America/Bogotá, valores monetarios en pesos colombianos (COP). | LANGUAGE_CODE = 'es-co', TIME_ZONE = 'America/Bogota' | Alta |
| RNF10 | Trazabilidad | Los registros críticos almacenarán marcas de tiempo de creación y actualización mediante campos auto_now_add y auto_now. | Campos de timestamp presentes en InventarioParqueo, Pago, Novedad y Sticker | Media |

*Nota.* Elaboración propia (2026).

---

## 5.3 — REQUERIMIENTOS NORMATIVOS

**Título:** 5.3. Requerimientos normativos

	El sistema MultiParking deberá cumplir las siguientes disposiciones legales y normativas aplicables al tratamiento de datos personales y a los lineamientos del programa formativo:

**Tabla 26**
*Requerimientos normativos del sistema MultiParking*

| Código | Normativa | Descripción |
|---|---|---|
| RNO01 | Ley 1581 de 2012 (Habeas Data) | Manejo de datos personales con consentimiento del titular. El sistema almacena datos de usuarios únicamente con fines operativos del parqueadero (Congreso de la República de Colombia, 2012). |
| RNO02 | Decreto 1377 de 2013 | Autorización expresa del titular antes de recopilar datos personales. El formulario de registro incluirá aviso de privacidad (Presidencia de la República de Colombia, 2013). |
| RNO03 | Normas SENA ADSO | Estructura y artefactos requeridos por el programa Análisis y Desarrollo de Software para el Trabajo Final del Proyecto Formativo (SENA, 2023). |
| RNO04 | APA 7ª edición | Referencias bibliográficas y citas siguen el Manual APA 7.ª edición (American Psychological Association, 2020). |

*Nota.* Elaboración propia (2026).

---

## 5.4 — REGLAS DEL NEGOCIO

**Título:** 5.4. Reglas del negocio

	Las reglas del negocio definen las restricciones y políticas operativas que el sistema debe respetar en todo momento, independientemente del canal de acceso o el rol del usuario:

**Tabla 27**
*Reglas del negocio del sistema MultiParking*

| Código | Nombre | Descripción |
|---|---|---|
| RN01 | Ingreso único activo por vehículo | Un vehículo no puede tener más de un registro con parHoraSalida IS NULL simultáneamente. |
| RN02 | Solo espacios DISPONIBLE aceptan ingresos | Espacios OCUPADOS, RESERVADOS o INACTIVOS no pueden recibir nuevos ingresos. |
| RN03 | Cálculo de costo minuto-base | costo = ceil((minutos / 60) × precioHora / 100) × 100. Los visitantes pagan con precioHoraVisitante. Mínimo cobrable: $100 COP. |
| RN04 | Tarifa activa única por tipo de espacio | Al activar una nueva tarifa del mismo tipo, la anterior se desactiva automáticamente. |
| RN05 | Validación de cupón antes de aplicar | El cupón debe existir, tener activo=True y encontrarse dentro de su fecha de vigencia. |
| RN06 | Pisos con espacios ocupados no se eliminan | No se puede eliminar un piso con espacios OCUPADOS, ni un espacio con parqueo activo. |
| RN07 | Gestión de estado al reservar/cancelar | Confirmar reserva → RESERVADO. Cancelar reserva → DISPONIBLE. Convertir a parqueo → OCUPADO. |
| RN08 | Token de recuperación de un solo uso | El token incorpora la huella del hash de la contraseña actual. Al cambiar la contraseña, el token queda invalidado automáticamente. |
| RN09 | Criterio de acumulación de sticker | Sticker solo si: el vehículo tiene propietario registrado Y la permanencia fue superior a 60 minutos. |
| RN10 | Generación automática de bono al canjear | Al reclamar el bono se crea un cupón tipo PORCENTAJE con valor 100%, uso único, con vigencia igual a diasVencimientoBono definido en ConfiguracionFidelidad. |

*Nota.* Elaboración propia (2026).

---

---

## 5.5 — PROPUESTA TÉCNICA

**Título:** 5.5. Propuesta técnica

	La propuesta técnica establece la planificación temporal del proyecto, los costos estimados de desarrollo y los requisitos de hardware y software necesarios para implementar y operar el sistema MultiParking.

---

### 5.5.1 Cronograma

	El proyecto se organizó en cuatro fases de desarrollo bajo metodología ágil, con un período de ejecución comprendido entre enero de 2025 y julio de 2026. Cada fase agrupa las actividades, los responsables y los entregables correspondientes.

**Tabla 28**
*Cronograma del proyecto MultiParking — Fase 1: Análisis (enero – abril 2025)*

| Actividad | Descripción | Encargados | Entregable |
|---|---|---|---|
| Identificación del problema y justificación | Establecer el alcance del proyecto y los objetivos general y específicos | Kevin Grisales, Kevin Pinto | Documento de justificación y objetivos |
| Recolección de información | Aplicación de observación directa y encuesta digital a 13 usuarios de parqueaderos de la localidad de Suba | Kevin Grisales, Kevin Pinto | Formatos de encuesta y observación; informe de recolección |
| Análisis y especificación de requerimientos | Análisis de la información recolectada y definición de RF, RNF, normativos y reglas de negocio | Kevin Grisales, Kevin Pinto | Documento de especificación de requerimientos (Sección 5) |
| Modelado de requisitos y riesgos | Elaboración de la Matriz de Riesgo y definición de la Propuesta Técnica | Kevin Grisales, Kevin Pinto | Matriz de riesgo; cronograma; estimación de costos |
| Modelado de casos de uso | Construcción del diagrama de casos de uso y documentación (CU001–CUnn) | Kevin Grisales, Kevin Pinto | Diagrama de casos de uso y documentación |

*Nota.* Elaboración propia (2026).

---

**Tabla 29**
*Cronograma del proyecto MultiParking — Fase 2: Planeación y Diseño (mayo – agosto 2025)*

| Actividad | Descripción | Encargados | Entregable |
|---|---|---|---|
| Diseño conceptual (mockups) | Elaboración de prototipos visuales de la interfaz web por rol (Admin, Vigilante, Cliente) | Kevin Grisales, Kevin Pinto | Mockups del sistema |
| Modelado de flujos y dominio | Creación de diagramas de actividades, secuencias y modelo de dominio (diagrama de clases) | Kevin Grisales, Kevin Pinto | Diagramas UML de análisis y diseño |
| Arquitectura y metodología | Definición de arquitectura MVT con Django, diagrama de componentes y aplicación de metodología ágil (Scrum) | Kevin Grisales, Kevin Pinto | Diagrama de componentes; tablero Scrum |
| Diseño lógico de datos | Elaboración del Modelo Entidad-Relación, modelo relacional y diccionario de datos con PostgreSQL | Kevin Grisales, Kevin Pinto | MER, modelo relacional y diccionario de datos |

*Nota.* Elaboración propia (2026).

---

**Tabla 30**
*Cronograma del proyecto MultiParking — Fase 3: Desarrollo (septiembre 2025 – abril 2026)*

| Actividad | Descripción | Encargados | Entregable |
|---|---|---|---|
| Construcción e implementación de la BD | Generación del script DDL/DML, creación de modelos Django, migraciones y objetos de base de datos (triggers, vistas) | Kevin Grisales, Kevin Pinto | Script SQL; migraciones Django |
| Desarrollo backend (9 apps Django) | Codificación de la lógica de negocio en Python/Django: vistas de clase, validaciones, cálculo de tarifas, fidelización y reportes | Kevin Grisales, Kevin Pinto | Módulos funcionales completados |
| Desarrollo frontend responsivo | Codificación de templates Django con Tailwind CSS; tres paneles diferenciados por rol; validación JS en tiempo real | Kevin Grisales, Kevin Pinto | Interfaces web responsivas por rol |
| Estándares y control de versiones | Aplicación de convenciones camelCase prefijado, documentación del código y gestión del repositorio Git/GitHub | Kevin Grisales, Kevin Pinto | Repositorio con historial de commits; README |

*Nota.* Elaboración propia (2026).

---

**Tabla 31**
*Cronograma del proyecto MultiParking — Fase 4: Documentación y Entrega (mayo – julio 2026)*

| Actividad | Descripción | Encargados | Entregable |
|---|---|---|---|
| Planeación y ejecución de pruebas | Diseño y ejecución de pruebas unitarias y de sistema sobre los módulos funcionales, con registro de hallazgos | Kevin Grisales, Kevin Pinto | Informe de hallazgos de pruebas |
| Corrección de errores e integración | Corrección de errores identificados en pruebas; documentación de manejo de excepciones | Kevin Grisales, Kevin Pinto | Código corregido; documentación de correcciones |
| Plan de despliegue e implantación | Configuración del entorno de producción en Render.com (PostgreSQL, variables de entorno, CI/CD); plan de capacitación | Kevin Grisales, Kevin Pinto | Sistema desplegado; plan de implantación |
| Documentación final y entrega | Elaboración del manual de usuario, documentación técnica SENA ADSO y sustentación formal del proyecto | Kevin Grisales, Kevin Pinto | Documento técnico completo; manual de usuario |

*Nota.* Elaboración propia (2026).

---

### 5.5.2 Costos estimados

	La siguiente tabla presenta la estimación de los costos asociados al desarrollo, despliegue y operación del sistema MultiParking, considerando recursos humanos, infraestructura en la nube y licencias de herramientas.

**Tabla 32**
*Costos estimados del proyecto MultiParking*

| Ítem | Descripción | Cantidad | Costo unitario (COP) | Total estimado (COP) |
|---|---|---|---|---|
| Desarrollo de software | Horas de análisis, diseño, codificación y pruebas por dos desarrolladores aprendices SENA | 480 h | $0 (formación) | $0 |
| Hosting Render.com | Plan Free (instancia web + PostgreSQL 1 GB) — suficiente para la fase piloto | 12 meses | $0 | $0 |
| Dominio web personalizado | Dominio .com.co o .co para producción (opcional, fase post-piloto) | 1 año | $45.000 | $45.000 |
| SendGrid (correo electrónico) | Plan Free: 100 correos/día para notificaciones de novedades y recuperación de contraseña | 12 meses | $0 | $0 |
| Herramientas de desarrollo | VS Code, Git, GitHub (gratuitos); Draw.io para diagramas (gratuito) | — | $0 | $0 |
| Licencias de software | Python 3.12, Django, PostgreSQL, Tailwind CSS — todos de código abierto (MIT/BSD) | — | $0 | $0 |
| Contingencia técnica (10%) | Reserva para imprevistos: migración de tier en Render.com o contratación de dominio antes del piloto | — | $4.500 | $4.500 |
| **Total** | | | | **$49.500** |

*Nota.* Costos proyectados para la fase piloto (2025-2026). Los recursos de desarrollo no generan costo monetario al ser ejecutados por aprendices en el marco del programa ADSO-SENA. Elaboración propia (2026).

---

### 5.5.3 Requisitos de hardware

	Los requisitos de hardware se dividen en dos categorías: el servidor de producción (infraestructura en la nube) y el equipo cliente utilizado por los usuarios del sistema.

**Tabla 33**
*Requisitos de hardware del sistema MultiParking*

| Componente | Especificación mínima | Especificación recomendada | Observación |
|---|---|---|---|
| **Servidor (producción)** | | | Gestionado por Render.com |
| CPU | 0.1 vCPU (shared) — Plan Free Render.com | 0.5 vCPU dedicado | El sistema Django no requiere alto cómputo; las operaciones son mayoritariamente de E/S |
| RAM | 512 MB — Plan Free Render.com | 1 GB | Suficiente para Django + Gunicorn con 2 workers |
| Almacenamiento BD | PostgreSQL 1 GB — Plan Free Render.com | 5 GB | La base de datos es relacional y de tamaño moderado; crece principalmente por imágenes de novedades |
| Ancho de banda | 100 GB/mes — Plan Free Render.com | Ilimitado | Suficiente para la fase piloto con uso simultáneo de hasta 20 usuarios |
| **Cliente (usuario final)** | | | Sin instalación requerida |
| Dispositivo | Computador de escritorio, portátil o smartphone | — | El sistema es web responsivo; funciona en cualquier dispositivo con navegador moderno |
| Pantalla | 360 px de ancho mínimo (smartphone) | 1024 px o superior | Tailwind CSS garantiza adaptabilidad desde 360 px |
| Conexión a internet | 1 Mbps mínimo | 5 Mbps o superior | Conexión estable requerida para actualizaciones AJAX en tiempo real |
| Navegador | Chrome 90+, Firefox 90+, Edge 90+ | Última versión disponible | Sin soporte para Internet Explorer |

*Nota.* Elaboración propia (2026).

---

### 5.5.4 Requisitos de software

	Los requisitos de software describen las tecnologías, plataformas y componentes de terceros que deben estar presentes para el correcto funcionamiento del sistema MultiParking en los entornos de desarrollo y producción.

**Tabla 34**
*Requisitos de software del sistema MultiParking*

| Componente | Versión | Licencia | Rol en el sistema |
|---|---|---|---|
| Python | 3.12 | PSF (código abierto) | Lenguaje base del backend y procesamiento de datos |
| Django | 4.2 LTS | BSD (código abierto) | Framework principal; MVT, ORM, sesiones, middleware |
| PostgreSQL | 15 (producción) / MySQL 8.0 (desarrollo local) | PostgreSQL License / GPL | Motor de base de datos relacional |
| Gunicorn | 21+ | MIT | Servidor WSGI para producción en Render.com |
| Whitenoise | 6+ | MIT | Servicio de archivos estáticos en producción sin servidor adicional |
| dj-database-url | 2+ | BSD | Configuración de base de datos via DATABASE_URL en Render.com |
| python-dotenv | 1+ | BSD | Carga de variables de entorno desde .env en desarrollo |
| reportlab | 4+ | BSD | Generación de reportes en formato PDF |
| openpyxl | 3+ | MIT | Generación de reportes en formato Excel (.xlsx) |
| Pillow | 10+ | HPND | Procesamiento de imágenes adjuntas en novedades |
| django-sendgrid-v5 | — | MIT | Envío de correos para recuperación de contraseña y novedades |
| Tailwind CSS | v3 (CDN) | MIT | Framework CSS; no requiere instalación local |
| Chart.js | v4 (CDN) | MIT | Gráficas interactivas en el dashboard del administrador |
| Git / GitHub | — | GPL / Propietario (gratuito) | Control de versiones y repositorio remoto |
| Visual Studio Code | — | MIT | Editor de código recomendado para el equipo de desarrollo |
| Sistema Operativo (servidor) | Linux (Ubuntu 22.04 LTS gestionado por Render.com) | — | Sistema operativo del servidor de producción |
| Sistema Operativo (cliente) | Windows 10+, macOS 12+, Android 10+, iOS 15+ | — | Compatibilidad de cliente web; no requiere instalación |

*Nota.* Todas las dependencias de Python están declaradas en `requirements.txt` del repositorio. Elaboración propia (2026).

---

## NOTA PARA CLAUDE DESKTOP

- Esta sección tiene tablas grandes — usar 9pt o 10pt para el contenido de las tablas y que quepan en el ancho de página
- Las tablas de RF tienen 5 columnas: Código (10%) | Nombre (20%) | Descripción (40%) | Entradas (20%) | Prioridad (10%)
- Las tablas de RNF tienen 5 columnas: Código (10%) | Nombre (15%) | Descripción (40%) | Criterio de aceptación (25%) | Prioridad (10%)
- Las tablas de RNO y RN tienen 3 columnas: Código (10%) | Nombre (20%) | Descripción (70%)
- Los encabezados de tabla en negrita
- La columna Prioridad puede tener color de fondo:
  - Alta → fondo rojo claro (#FFCCCC)
  - Media → fondo amarillo claro (#FFF2CC)
  - Baja → fondo verde claro (#D9EAD3)
- Numeración de tablas: continúa desde sección 4 (Tablas 2–13 = encuesta). Esta sección: Tablas 14–27
- RF63 (Escaneo QR) se ubica al final de la Tabla 17 (Módulo Inventario Parqueos) como fila adicional
- Títulos de tabla (**Tabla N** + *cursiva*): flush left, sin sangría, 12pt
- Notas de tabla (*Nota.*...): flush left, sin sangría, 10pt
- La sección 6 inicia en página nueva
