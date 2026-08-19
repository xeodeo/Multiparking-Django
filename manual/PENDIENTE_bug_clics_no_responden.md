# PENDIENTE — Bug de clics que no disparan la acción (no incluido en los manuales)

> Este archivo **no forma parte de la documentación entregable**. Contiene el hallazgo técnico
> que se detectó durante la elaboración del Manual del Cliente y se retiró de los 3 manuales
> a petición del usuario, para que el equipo de desarrollo lo investigue y corrija aparte.
> Fecha de extracción: 18 de agosto de 2026.

## Hallazgo original (retirado de manual-cliente.md, sección "Interfaz principal")

Antes de entrar en cada funcionalidad, es importante advertir sobre un problema real y reproducible encontrado durante la verificación de **prácticamente todos los formularios principales** del panel de cliente en el viewport móvil (390×844):

**Qué se observó:** al tocar/hacer clic de forma normal sobre el botón principal de una pantalla (p. ej. "Agregar Vehículo", "Actualizar Vehículo", "Ingresar al Parqueadero", "Cancelar" en una reserva, e incluso "Iniciar Sesión" en una de las pruebas), en **6 de 7 intentos reales** no ocurrió nada: ni navegación, ni mensaje de error, ni cambio visible. El formulario permanecía exactamente igual, con los datos ya escritos.

**Cómo se confirmó que es real y no una percepción:** se instrumentó la página con un contador de eventos (`button.addEventListener('click', ...)`). Resultado: **el contador quedó en 0** después de un clic que la herramienta de automatización reportó como "exitoso" — es decir, el evento de clic nunca llegó a ejecutarse sobre el botón, aunque la página sí se desplazó (scroll) para ponerlo a la vista. Al invocar el envío del formulario directamente (equivalente a lo que ocurriría si el clic funcionara), la acción se completaba correctamente de inmediato.

**Un mecanismo relacionado, distinto, también confirmado:** en las pantallas donde hay que elegir una opción usando tarjetas visuales en lugar de un `<select>` (por ejemplo, "Selecciona el vehículo que ingresará" en Ingresar al Parqueadero, o "Seleccionar Espacio" en Crear Reserva), tocar la tarjeta **no marca el `input type="radio"` real que hay detrás**. Como ese campo es obligatorio, el navegador bloquea el envío silenciosamente (sin mensaje visible) porque el formulario nunca queda válido.

**Impacto para un usuario real:** un cliente que intente agregar su primer vehículo, cancelar una reserva, o ingresar sin escanear el QR desde su teléfono podría tocar el botón varias veces sin que pase nada, sin ningún mensaje que explique por qué — una experiencia muy confusa y potencialmente bloqueante para tareas centrales de la cuenta.

**Alcance de la verificación:** esto se comprobó de forma repetida y consistente en el viewport móvil (7 intentos, 6 fallos). El mismo patrón (clic reportado como exitoso por la herramienta de automatización, pero sin ningún efecto real) también ocurrió dos veces en el **panel de escritorio** del Administrador (al iniciar sesión y al eliminar un vehículo de prueba) — así que **no es exclusivo de la vista móvil**, aunque en las pruebas se concentró mucho más ahí. Todo indica una condición intermitente de la interacción (clic/toque que a veces no llega a disparar el evento en el elemento, incluso cuando la página se desplaza correctamente para mostrarlo), no un defecto exclusivo de una sola pantalla o viewport. No se verificó si ocurre igual con eventos táctiles nativos en un teléfono físico real.

## Menciones puntuales retiradas de otras secciones del manual

- **4.2 Gestionar mis vehículos:** *"Ver el aviso de la sección anterior: en las pruebas de este manual, el botón 'Agregar Vehículo' no respondió a un toque normal en dos intentos consecutivos; la creación solo se completó al forzar el envío del formulario directamente. Si al tocar el botón no ocurre nada, intentar de nuevo tocando con precisión el centro del botón, esperar unos segundos tras cargar la página antes de tocar, o recargar la página e intentar otra vez."*

- **4.4 Ingresar escaneando el código QR:** *"Nota sobre el hallazgo de la sección anterior: las tarjetas de selección de vehículo en esta pantalla usan el mismo componente de radio personalizado que no marca el campo real al tocarlo; si 'Ingresar al Parqueadero' no responde, es probablemente por esta causa."*

- **4.5 Salir y pagar** (frase original antes de simplificarse en el manual final): *"Aunque el botón 'Aplicar' no mostró ninguna confirmación visual inmediata al tocarlo (consistente con el hallazgo general de esta sección), el descuento sí se aplicó correctamente al procesar el pago..."*

- **Sección "5.3 Qué hacer si un botón 'no responde'"** (subsección completa, retirada):
  1. Esperar 2-3 segundos después de que la página cargue por completo antes de tocar el botón.
  2. Tocar exactamente el centro del botón, no el borde.
  3. Si no ocurre nada, recargar la página (los datos escritos se perderán) e intentarlo de nuevo.
  4. Si el botón depende de elegir una tarjeta/opción (vehículo, espacio), confirmar visualmente que la tarjeta quedó resaltada como seleccionada antes de tocar el botón de enviar.
  5. Si el problema persiste, reportarlo a soporte/al equipo de desarrollo.

- **Tabla "Errores y problemas frecuentes" (fila retirada):**
  | Un botón principal (Agregar Vehículo, Ingresar al Parqueadero, Cancelar reserva, etc.) no hace nada al tocarlo | Problema de interacción verificado en móvil — el evento de clic no siempre llega al botón, o la tarjeta de selección no marca el campo obligatorio real | Ver sección 5.3; esperar, recargar, o intentar tocar de nuevo con precisión |

- **Buenas prácticas (viñeta retirada):** *"Si un botón parece no responder, esperar unos segundos y volver a intentar antes de asumir que la acción falló silenciosamente; revisar si el dashboard refleja el cambio esperado."*

- **Preguntas frecuentes (par retirado):**
  **Toqué "Agregar Vehículo" / "Ingresar al Parqueadero" y no pasó nada, ¿qué hago?**
  Es un problema conocido documentado en este manual (sección 3). Espera unos segundos, verifica que la opción elegida quedó realmente seleccionada, y vuelve a intentarlo; si persiste, recarga la página.

- **manual-administrador.md, tabla "Errores y problemas frecuentes" (fila retirada, cross-referenciaba al cliente):**
  | Un botón (Guardar, Eliminar, Iniciar Sesión) parece no responder al hacer clic, sin ningún mensaje | Se observó de forma intermitente y reproducible durante este trabajo (más frecuente en el panel de Cliente en móvil, pero también ocurrió dos veces en este panel de escritorio) que un clic no siempre dispara la acción, aunque la página se desplace para mostrar el botón — ver el hallazgo detallado en el Manual del Cliente, sección 3 | Volver a intentar el clic; si persiste, recargar la página. Es un problema conocido de interacción, no un error del usuario |

## Datos técnicos de reproducción (para quien vaya a depurar esto)

- Viewport usado: 390×844 (emulación móvil vía Playwright).
- Formularios afectados observados: `templates/cliente/vehiculo_form.html` (Agregar/Actualizar Vehículo), pantalla de login, `Cancelar` en reserva (dashboard cliente), `Ingresar al Parqueadero` (entrada sin reserva).
- Prueba diagnóstica que confirmó que el evento nunca llega al botón:
  ```js
  const btn = [...document.querySelectorAll('button')].find(b => /agregar veh/i.test(b.textContent));
  window.__clicks = 0;
  btn.addEventListener('click', () => { window.__clicks++; });
  // ... clic real vía Playwright ...
  // window.__clicks quedó en 0 después del clic
  ```
- En el flujo de "Ingresar al Parqueadero" y "Crear Reserva", se confirmó además que las tarjetas de selección (`<label>` con un `<input type="radio" class="peer sr-only">` oculto detrás) no actualizan `radio.checked` al hacer clic en la tarjeta — verificado con `document.querySelector('input[type=radio]:checked')` devolviendo `null` después del clic.
- No se investigó la causa raíz de fondo (posible relación con el header `sticky` que en un caso Playwright reportó explícitamente como interceptor de eventos de puntero — `"header... subtree intercepts pointer events"` — pero esto no explica los casos donde el botón estaba lejos del header).
- Bypass usado para completar las pruebas pese al bug: invocar `form.submit()` directamente via JavaScript, o fijar `radio.checked = true` + disparar `change` antes de enviar.
