import re

from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .mixins import AdminRequiredMixin
from .models import Usuario

RE_SOLO_NUMEROS = re.compile(r'^[0-9]+$')
RE_SOLO_LETRAS = re.compile(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$')
RE_CORREO = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]{2,}$')


def _is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


def home_view(request):
    if request.session.get('usuario_id'):
        return redirect('admin_dashboard' if request.session.get('usuario_rol') == 'ADMIN' else 'dashboard')
    return render(request, 'home.html')


def login_view(request):
    if request.session.get('usuario_id'):
        target = 'admin_dashboard' if request.session.get('usuario_rol') == 'ADMIN' else 'dashboard'
        if _is_ajax(request):
            return JsonResponse({'ok': True, 'redirect': target}) # JsonResponse needs URL path, not name, but let's assume client handles it or returned path in line 59 logic
            # Correction: line 59 returns '/admin-panel/' string.
            # Ideally we return the string path here too to be consistent.
            # But line 59 logic is: return JsonResponse({'ok': True, 'redirect': '/admin-panel/' if usuario.rolTipoRol == 'ADMIN' else '/dashboard/'})
            # Let's match that.
            return JsonResponse({'ok': True, 'redirect': '/admin-panel/' if request.session.get('usuario_rol') == 'ADMIN' else '/dashboard/'})
        return redirect(target)

    if request.method == 'POST':
        correo = request.POST.get('correo', '').strip()
        clave = request.POST.get('clave', '')

        try:
            usuario = Usuario.objects.get(usuCorreo=correo)
        except Usuario.DoesNotExist:
            if _is_ajax(request):
                return JsonResponse({'ok': False, 'error': 'Correo o contraseña incorrectos.'})
            messages.error(request, 'Correo o contraseña incorrectos.')
            return render(request, 'auth/login.html', {'correo': correo})

        if not usuario.usuEstado:
            msg = 'Tu cuenta está desactivada. Contacta al administrador.'
            if _is_ajax(request):
                return JsonResponse({'ok': False, 'error': msg})
            messages.error(request, msg)
            return render(request, 'auth/login.html', {'correo': correo})

        if not check_password(clave, usuario.usuClaveHash):
            if _is_ajax(request):
                return JsonResponse({'ok': False, 'error': 'Correo o contraseña incorrectos.'})
            messages.error(request, 'Correo o contraseña incorrectos.')
            return render(request, 'auth/login.html', {'correo': correo})

        # Crear sesión
        request.session['usuario_id'] = usuario.pk
        request.session['usuario_nombre'] = usuario.usuNombreCompleto
        request.session['usuario_rol'] = usuario.rolTipoRol
        request.session['usuario_correo'] = usuario.usuCorreo

        if _is_ajax(request):
            return JsonResponse({'ok': True, 'redirect': '/admin-panel/' if usuario.rolTipoRol == 'ADMIN' else '/dashboard/'})
        messages.success(request, f'Bienvenido, {usuario.usuNombreCompleto}.')
        return redirect('admin_dashboard' if usuario.rolTipoRol == 'ADMIN' else 'dashboard')

    return render(request, 'auth/login.html')


def register_view(request):
    if request.session.get('usuario_id'):
        target_redirect = '/admin-panel/' if request.session.get('usuario_rol') == 'ADMIN' else '/dashboard/'
        if _is_ajax(request):
            return JsonResponse({'ok': True, 'redirect': target_redirect})
        return redirect('admin_dashboard' if request.session.get('usuario_rol') == 'ADMIN' else 'dashboard')

    if request.method == 'POST':
        documento = request.POST.get('documento', '').strip()
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        correo = request.POST.get('correo', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        clave = request.POST.get('clave', '')
        clave_confirm = request.POST.get('clave_confirm', '')

        def _err(msg):
            if _is_ajax(request):
                return JsonResponse({'ok': False, 'error': msg})
            messages.error(request, msg)
            return render(request, 'auth/register.html', {
                'form_data': {
                    'documento': documento,
                    'nombre': nombre,
                    'apellido': apellido,
                    'correo': correo,
                    'telefono': telefono
                }
            })

        if not all([documento, nombre, apellido, correo, clave]):
            return _err('Todos los campos obligatorios deben estar llenos.')

        if len(documento) < 6:
            return _err('El documento debe tener al menos 6 caracteres.')

        if clave != clave_confirm:
            return _err('Las contraseñas no coinciden.')

        if len(clave) < 6:
            return _err('La contraseña debe tener al menos 6 caracteres.')

        # Validar formato de campos
        if not RE_SOLO_NUMEROS.match(documento):
            return _err('El documento solo debe contener números.')
        if not RE_SOLO_LETRAS.match(nombre):
            return _err('El nombre solo debe contener letras.')
        if not RE_SOLO_LETRAS.match(apellido):
            return _err('El apellido solo debe contener letras.')
        if telefono and not RE_SOLO_NUMEROS.match(telefono):
            return _err('El teléfono solo debe contener números.')
        if not RE_CORREO.match(correo):
            return _err('Ingresa un correo válido (ej: usuario@dominio.com).')

        # Validar documento duplicado
        if Usuario.objects.filter(usuDocumento=documento).exists():
            return _err('Ya existe un usuario registrado con ese número de documento.')

        # Validar correo duplicado
        if Usuario.objects.filter(usuCorreo=correo).exists():
            return _err('Ya existe un usuario registrado con ese correo electrónico.')

        Usuario.objects.create(
            usuDocumento=documento,
            usuNombre=nombre,
            usuApellido=apellido,
            usuCorreo=correo,
            usuTelefono=telefono,
            usuClaveHash=make_password(clave),
            rolTipoRol='CLIENTE',
            usuEstado=True,
        )

        if _is_ajax(request):
            return JsonResponse({'ok': True, 'message': 'Cuenta creada exitosamente.'})
        messages.success(request, 'Cuenta creada exitosamente. Ahora puedes iniciar sesión.')
        return redirect('home')

    return render(request, 'auth/register.html')


def logout_view(request):
    request.session.flush()
    return redirect('home')


def dashboard_view(request):
    """Dashboard para clientes/usuarios registrados"""
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, 'Debes iniciar sesión para acceder.')
        return redirect('home')

    from vehiculos.models import Vehiculo
    from reservas.models import Reserva
    from pagos.models import Pago
    from parqueadero.models import InventarioParqueo
    from django.utils import timezone

    # Obtener usuario actual
    usuario = Usuario.objects.get(pk=usuario_id)

    # Vehículos del usuario (registrados)
    vehiculos = Vehiculo.objects.filter(
        fkIdUsuario=usuario
    ).order_by('-pk')

    # Reservas del usuario (activas y futuras)
    from datetime import datetime, timedelta

    now = timezone.now()

    # Auto-cancelar reservas PENDIENTES no confirmadas que faltan 15 min o menos
    reservas_pendientes = Reserva.objects.filter(
        resEstado='PENDIENTE'
    )
    for res in reservas_pendientes:
        fecha_hora_res = datetime.combine(res.resFechaReserva, res.resHoraInicio)
        fecha_hora_res = timezone.make_aware(fecha_hora_res)
        tiempo_restante = fecha_hora_res - now
        if tiempo_restante <= timedelta(minutes=15):
            res.resEstado = 'CANCELADA'
            res.save()

    reservas_raw = Reserva.objects.filter(
        fkIdVehiculo__fkIdUsuario=usuario,
        resEstado__in=['PENDIENTE', 'CONFIRMADA']
    ).select_related(
        'fkIdVehiculo',
        'fkIdEspacio',
        'fkIdEspacio__fkIdPiso'
    ).order_by('-resFechaReserva', '-resHoraInicio')[:5]

    # Calcular si falta menos de 1h para cada reserva
    reservas = []
    for reserva in reservas_raw:
        fecha_hora_reserva = datetime.combine(reserva.resFechaReserva, reserva.resHoraInicio)
        fecha_hora_reserva = timezone.make_aware(fecha_hora_reserva)

        tiempo_restante = fecha_hora_reserva - now
        necesita_confirmacion = timedelta(0) <= tiempo_restante <= timedelta(hours=1)
        puede_editar = tiempo_restante > timedelta(hours=1)

        # Calcular minutos restantes para mostrar cuenta regresiva
        minutos_restantes = int(tiempo_restante.total_seconds() / 60) if tiempo_restante.total_seconds() > 0 else 0

        reservas.append({
            'reserva': reserva,
            'necesita_confirmacion': necesita_confirmacion and not reserva.resConfirmada,
            'puede_editar': puede_editar,
            'confirmada': reserva.resConfirmada,
            'minutos_restantes': minutos_restantes,
        })

    # Estado de parqueo actual (vehículo estacionado)
    import math
    from tarifas.models import Tarifa
    registro_activo = InventarioParqueo.objects.filter(
        fkIdVehiculo__fkIdUsuario=usuario,
        parHoraSalida__isnull=True
    ).select_related(
        'fkIdVehiculo',
        'fkIdEspacio',
        'fkIdEspacio__fkIdPiso',
        'fkIdEspacio__fkIdTipoEspacio'
    ).first()

    parqueo_activo = None
    if registro_activo:
        entrada = registro_activo.parHoraEntrada
        duracion = now - entrada
        total_seconds = int(duracion.total_seconds())
        total_minutos = max((total_seconds + 59) // 60, 1)
        d = total_minutos // 1440
        h = (total_minutos % 1440) // 60
        m = total_minutos % 60
        dur_str = ""
        if d > 0:
            dur_str += f"{d}d "
        if h > 0:
            dur_str += f"{h}h "
        dur_str += f"{m}m"

        tarifa_activa = Tarifa.objects.filter(
            fkIdTipoEspacio=registro_activo.fkIdEspacio.fkIdTipoEspacio,
            activa=True
        ).first()

        precio_hora = 0
        valor_acumulado = 0
        if tarifa_activa:
            es_vis = registro_activo.fkIdVehiculo.es_visitante
            precio_hora = float(tarifa_activa.precioHoraVisitante) if es_vis and tarifa_activa.precioHoraVisitante > 0 else float(tarifa_activa.precioHora)
            valor_acumulado = math.ceil((precio_hora / 60) * total_minutos)

        parqueo_activo = {
            'vehiculo': registro_activo.fkIdVehiculo,
            'espacio': registro_activo.fkIdEspacio,
            'entrada': timezone.localtime(entrada),
            'entrada_iso': timezone.localtime(entrada).isoformat(),
            'duracion': dur_str,
            'precio_hora': precio_hora,
            'valor_acumulado': valor_acumulado,
        }

    # Historial de pagos del usuario
    pagos_historial = Pago.objects.filter(
        fkIdParqueo__fkIdVehiculo__fkIdUsuario=usuario
    ).select_related(
        'fkIdParqueo',
        'fkIdParqueo__fkIdVehiculo'
    ).order_by('-pagFechaPago')[:10]

    # Calcular duración para cada pago
    pagos_con_duracion = []
    for pago in pagos_historial:
        parqueo = pago.fkIdParqueo
        if parqueo.parHoraSalida:
            duracion = parqueo.parHoraSalida - parqueo.parHoraEntrada
            horas = duracion.total_seconds() / 3600
            duracion_str = f"{horas:.1f} horas"
        else:
            duracion_str = "En curso"

        pagos_con_duracion.append({
            'pago': pago,
            'duracion': duracion_str,
            'placa': parqueo.fkIdVehiculo.vehPlaca
        })

    return render(request, 'cliente/dashboard.html', {
        'usuario': usuario,
        'vehiculos': vehiculos,
        'reservas': reservas,
        'pagos': pagos_con_duracion,
        'parqueo_activo': parqueo_activo,
    })


# ── ADMIN PANEL — Gestión de Usuarios ───────────────────────────────

class UsuarioListView(AdminRequiredMixin, View):
    def get(self, request):
        q = request.GET.get('q', '').strip()
        usuarios = Usuario.objects.order_by('-usuEstado', 'usuNombre', 'usuApellido')

        if q:
            usuarios = usuarios.filter(
                Q(usuNombre__icontains=q)
                | Q(usuApellido__icontains=q)
                | Q(usuDocumento__icontains=q)
                | Q(usuCorreo__icontains=q)
            )

        total = usuarios.count()
        activos = usuarios.filter(usuEstado=True).count()
        admins = usuarios.filter(rolTipoRol='ADMIN').count()
        clientes = usuarios.filter(rolTipoRol='CLIENTE').count()
        vigilantes = usuarios.filter(rolTipoRol='VIGILANTE').count()

        return render(request, 'admin_panel/usuarios/list.html', {
            'active_page': 'usuarios',
            'usuarios': usuarios,
            'total': total,
            'activos': activos,
            'inactivos': total - activos,
            'admins': admins,
            'clientes': clientes,
            'vigilantes': vigilantes,
            'q': q,
        })


class UsuarioCreateView(AdminRequiredMixin, View):
    def get(self, request):
        return render(request, 'admin_panel/usuarios/form.html', {
            'active_page': 'usuarios',
            'title': 'Nuevo Usuario',
            'roles': Usuario.RolChoices.choices,
        })

    def post(self, request):
        documento = request.POST.get('usuDocumento', '').strip()
        nombre = request.POST.get('usuNombre', '').strip()
        apellido = request.POST.get('usuApellido', '').strip()
        correo = request.POST.get('usuCorreo', '').strip()
        telefono = request.POST.get('usuTelefono', '').strip()
        rol = request.POST.get('rolTipoRol', 'CLIENTE')
        clave = request.POST.get('clave', '')
        activo = 'usuEstado' in request.POST

        ctx = {
            'active_page': 'usuarios',
            'title': 'Nuevo Usuario',
            'roles': Usuario.RolChoices.choices,
            'usuario': {
                'usuDocumento': documento,
                'usuNombre': nombre,
                'usuApellido': apellido,
                'usuCorreo': correo,
                'usuTelefono': telefono,
                'rolTipoRol': rol,
                'usuEstado': activo,
            },
        }

        if not all([documento, nombre, apellido, correo, clave]):
            messages.error(request, 'Documento, nombre, apellido, correo y contraseña son obligatorios.')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        if len(documento) < 6:
            messages.error(request, 'El documento debe tener al menos 6 caracteres.')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        if not RE_SOLO_NUMEROS.match(documento):
            messages.error(request, 'El documento solo debe contener números.')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        if not RE_SOLO_LETRAS.match(nombre):
            messages.error(request, 'El nombre solo debe contener letras.')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        if not RE_SOLO_LETRAS.match(apellido):
            messages.error(request, 'El apellido solo debe contener letras.')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        if telefono and not RE_SOLO_NUMEROS.match(telefono):
            messages.error(request, 'El teléfono solo debe contener números.')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        if not RE_CORREO.match(correo):
            messages.error(request, 'Ingresa un correo válido (ej: usuario@dominio.com).')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        if len(clave) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        if Usuario.objects.filter(usuDocumento=documento).exists():
            messages.error(request, 'Ya existe un usuario con ese documento.')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        if Usuario.objects.filter(usuCorreo=correo).exists():
            messages.error(request, 'Ya existe un usuario con ese correo.')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        Usuario.objects.create(
            usuDocumento=documento,
            usuNombre=nombre,
            usuApellido=apellido,
            usuCorreo=correo,
            usuTelefono=telefono,
            rolTipoRol=rol,
            usuClaveHash=make_password(clave),
            usuEstado=activo,
        )
        messages.success(request, f'Usuario {nombre} {apellido} creado exitosamente.')
        return redirect('admin_usuarios')


class UsuarioUpdateView(AdminRequiredMixin, View):
    def get(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)
        return render(request, 'admin_panel/usuarios/form.html', {
            'active_page': 'usuarios',
            'title': 'Editar Usuario',
            'roles': Usuario.RolChoices.choices,
            'usuario': usuario,
            'editing': True,
        })

    def post(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)
        documento = request.POST.get('usuDocumento', '').strip()
        nombre = request.POST.get('usuNombre', '').strip()
        apellido = request.POST.get('usuApellido', '').strip()
        correo = request.POST.get('usuCorreo', '').strip()
        telefono = request.POST.get('usuTelefono', '').strip()
        rol = request.POST.get('rolTipoRol', 'CLIENTE')
        clave = request.POST.get('clave', '')
        activo = 'usuEstado' in request.POST

        ctx = {
            'active_page': 'usuarios',
            'title': 'Editar Usuario',
            'roles': Usuario.RolChoices.choices,
            'usuario': usuario,
            'editing': True,
        }

        if not all([documento, nombre, apellido, correo]):
            messages.error(request, 'Documento, nombre, apellido y correo son obligatorios.')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        if len(documento) < 6:
            messages.error(request, 'El documento debe tener al menos 6 caracteres.')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        if not RE_SOLO_NUMEROS.match(documento):
            messages.error(request, 'El documento solo debe contener números.')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        if not RE_SOLO_LETRAS.match(nombre):
            messages.error(request, 'El nombre solo debe contener letras.')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        if not RE_SOLO_LETRAS.match(apellido):
            messages.error(request, 'El apellido solo debe contener letras.')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        if telefono and not RE_SOLO_NUMEROS.match(telefono):
            messages.error(request, 'El teléfono solo debe contener números.')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        if not RE_CORREO.match(correo):
            messages.error(request, 'Ingresa un correo válido (ej: usuario@dominio.com).')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        # Validar duplicados excluyendo el usuario actual
        if Usuario.objects.filter(usuDocumento=documento).exclude(pk=pk).exists():
            messages.error(request, 'Ya existe otro usuario con ese documento.')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        if Usuario.objects.filter(usuCorreo=correo).exclude(pk=pk).exists():
            messages.error(request, 'Ya existe otro usuario con ese correo.')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        usuario.usuDocumento = documento
        usuario.usuNombre = nombre
        usuario.usuApellido = apellido
        usuario.usuCorreo = correo
        usuario.usuTelefono = telefono
        usuario.rolTipoRol = rol
        usuario.usuEstado = activo

        # Solo actualizar contraseña si se proporcionó una nueva
        if clave:
            if len(clave) < 6:
                messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
                return render(request, 'admin_panel/usuarios/form.html', ctx)
            usuario.usuClaveHash = make_password(clave)

        usuario.save()
        messages.success(request, f'Usuario {nombre} {apellido} actualizado.')
        return redirect('admin_usuarios')


class UsuarioDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)

        # No permitir eliminarse a sí mismo
        if usuario.pk == request.session.get('usuario_id'):
            messages.error(request, 'No puedes eliminar tu propia cuenta.')
            return redirect('admin_usuarios')

        nombre = usuario.usuNombreCompleto
        usuario.delete()
        messages.success(request, f'Usuario {nombre} eliminado.')
        return redirect('admin_usuarios')


class UsuarioToggleView(AdminRequiredMixin, View):
    def post(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)

        # No permitir desactivarse a sí mismo
        if usuario.pk == request.session.get('usuario_id'):
            messages.error(request, 'No puedes desactivar tu propia cuenta.')
            return redirect('admin_usuarios')

        usuario.usuEstado = not usuario.usuEstado
        usuario.save()
        estado = 'activado' if usuario.usuEstado else 'desactivado'
        messages.success(request, f'Usuario {usuario.usuNombreCompleto} {estado}.')
        return redirect('admin_usuarios')
