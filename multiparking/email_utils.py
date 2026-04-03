"""
Utilidades centralizadas para envío de correos electrónicos via SendGrid SMTP.
Todos los envíos se realizan en un hilo separado para no bloquear la request HTTP.
"""
import threading
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def _send_async(msg):
    """Envía un EmailMultiAlternatives en un hilo separado para no bloquear el request."""
    def _send():
        try:
            msg.send(fail_silently=False)
        except Exception as e:
            # En producción esto iría a un logger; por ahora solo imprime
            print(f"[EMAIL ERROR] {e}")
    threading.Thread(target=_send, daemon=True).start()


def _build_msg(subject, template_html, context, to_email):
    """Construye un EmailMultiAlternatives con versión HTML y texto plano."""
    html_body = render_to_string(template_html, context)
    # Versión texto plano mínima para clientes que no soporten HTML
    text_body = f"Multiparking — {subject}\n\nAbre este correo en un cliente con soporte HTML para verlo correctamente."
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )
    msg.attach_alternative(html_body, "text/html")
    return msg


# ── Correos públicos ───────────────────────────────────────────────────────────

def enviar_bienvenida(usuario):
    """Envía el correo de bienvenida tras el registro exitoso de un nuevo cliente."""
    msg = _build_msg(
        subject="¡Bienvenido a Multiparking!",
        template_html="emails/bienvenida.html",
        context={"usuario": usuario},
        to_email=usuario.usuCorreo,
    )
    _send_async(msg)


def enviar_confirmacion_reserva(reserva):
    """
    Envía confirmación de reserva al cliente dueño del vehículo.
    reserva.fkIdVehiculo.fkIdUsuario debe ser un Usuario (no visitante).
    """
    usuario = reserva.fkIdVehiculo.fkIdUsuario
    if not usuario:
        return  # Vehículo visitante, sin correo
    msg = _build_msg(
        subject="Reserva confirmada — Multiparking",
        template_html="emails/confirmacion_reserva.html",
        context={"reserva": reserva, "usuario": usuario},
        to_email=usuario.usuCorreo,
    )
    _send_async(msg)


def enviar_recordatorio_reserva(reserva):
    """
    Envía recordatorio 24h antes de la reserva.
    Llamado por el management command enviar_recordatorios.
    """
    usuario = reserva.fkIdVehiculo.fkIdUsuario
    if not usuario:
        return
    msg = _build_msg(
        subject="Recordatorio: tienes una reserva mañana — Multiparking",
        template_html="emails/recordatorio_reserva.html",
        context={"reserva": reserva, "usuario": usuario},
        to_email=usuario.usuCorreo,
    )
    _send_async(msg)


def enviar_recibo_pago(pago, registro):
    """
    Envía recibo de pago al salir del parqueadero.
    Solo se llama cuando el vehículo pertenece a un usuario registrado.
    registro es el objeto InventarioParqueo.
    """
    usuario = registro.fkIdVehiculo.fkIdUsuario
    if not usuario:
        return
    msg = _build_msg(
        subject="Recibo de pago — Multiparking",
        template_html="emails/recibo_pago.html",
        context={"pago": pago, "registro": registro, "usuario": usuario},
        to_email=usuario.usuCorreo,
    )
    _send_async(msg)


def enviar_registro_vehiculo(vehiculo, usuario):
    """
    Envía confirmación al registrar un vehículo nuevo en la cuenta del cliente.
    """
    msg = _build_msg(
        subject="Vehículo registrado — Multiparking",
        template_html="emails/registro_vehiculo.html",
        context={"vehiculo": vehiculo, "usuario": usuario},
        to_email=usuario.usuCorreo,
    )
    _send_async(msg)


def enviar_confirmacion_entrada(registro):
    """
    Envía confirmación de entrada al parqueadero.
    Solo se llama cuando el vehículo pertenece a un usuario registrado (no visitante).
    registro es el objeto InventarioParqueo recién creado.
    """
    usuario = registro.fkIdVehiculo.fkIdUsuario
    if not usuario:
        return
    msg = _build_msg(
        subject="Entrada registrada — Multiparking",
        template_html="emails/confirmacion_entrada.html",
        context={"registro": registro, "usuario": usuario},
        to_email=usuario.usuCorreo,
    )
    _send_async(msg)


def enviar_novedad(novedad):
    """
    Notifica al usuario afectado cuando se crea o actualiza una novedad.
    Busca el usuario en el vehículo asociado o en la reserva del espacio.
    """
    usuario = None
    if novedad.fkIdVehiculo and novedad.fkIdVehiculo.fkIdUsuario:
        usuario = novedad.fkIdVehiculo.fkIdUsuario
    if not usuario:
        return
    msg = _build_msg(
        subject=f"Novedad en tu vehículo — Multiparking",
        template_html="emails/novedad.html",
        context={"novedad": novedad, "usuario": usuario},
        to_email=usuario.usuCorreo,
    )
    _send_async(msg)


def enviar_bono_stickers(usuario, cupon):
    """
    Notifica al usuario que ha acumulado suficientes stickers y tiene un bono disponible.
    """
    msg = _build_msg(
        subject="¡Tienes un bono del 100%! — Multiparking",
        template_html="emails/bono_stickers.html",
        context={"usuario": usuario, "cupon": cupon},
        to_email=usuario.usuCorreo,
    )
    _send_async(msg)


def enviar_reset_clave(usuario, token, request):
    """
    Envía el correo de restablecimiento de contraseña con el enlace firmado.
    token: string generado con django.core.signing.
    request: usado para construir la URL absoluta.
    """
    reset_url = request.build_absolute_uri(f"/password-reset/{token}/")
    msg = _build_msg(
        subject="Restablecer contraseña — Multiparking",
        template_html="emails/restablecer_clave.html",
        context={"usuario": usuario, "reset_url": reset_url},
        to_email=usuario.usuCorreo,
    )
    _send_async(msg)
