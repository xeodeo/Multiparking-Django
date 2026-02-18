from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .mixins import AdminRequiredMixin
from .models import Usuario


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

        # Si viene apellido separado (modal home), concatenar. Sino usar nombre directamente
        nombre_completo = f"{nombre} {apellido}".strip() if apellido else nombre

        def _err(msg):
            if _is_ajax(request):
                return JsonResponse({'ok': False, 'error': msg})
            messages.error(request, msg)
            return render(request, 'auth/register.html', {
                'form_data': {
                    'documento': documento,
                    'nombre': nombre,
                    'correo': correo,
                    'telefono': telefono
                }
            })

        if not all([documento, nombre, correo, clave]):
            return _err('Todos los campos obligatorios deben estar llenos.')

        if len(documento) < 6:
            return _err('El documento debe tener al menos 6 caracteres.')

        if clave != clave_confirm:
            return _err('Las contraseñas no coinciden.')

        if len(clave) < 6:
            return _err('La contraseña debe tener al menos 6 caracteres.')

        # Validar documento duplicado
        if Usuario.objects.filter(usuDocumento=documento).exists():
            return _err('Ya existe un usuario registrado con ese número de documento.')

        # Validar correo duplicado
        if Usuario.objects.filter(usuCorreo=correo).exists():
            return _err('Ya existe un usuario registrado con ese correo electrónico.')

        Usuario.objects.create(
            usuDocumento=documento,
            usuNombreCompleto=nombre_completo,
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
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('home')


def dashboard_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, 'Debes iniciar sesión para acceder.')
        return redirect('login')

    return render(request, 'auth/dashboard.html', {
        'usuario_nombre': request.session.get('usuario_nombre'),
        'usuario_rol': request.session.get('usuario_rol'),
    })


# ── ADMIN PANEL — Gestión de Usuarios ───────────────────────────────

class UsuarioListView(AdminRequiredMixin, View):
    def get(self, request):
        q = request.GET.get('q', '').strip()
        usuarios = Usuario.objects.order_by('-usuEstado', 'usuNombreCompleto')

        if q:
            usuarios = usuarios.filter(
                Q(usuNombreCompleto__icontains=q)
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
        nombre = request.POST.get('usuNombreCompleto', '').strip()
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
                'usuNombreCompleto': nombre,
                'usuCorreo': correo,
                'usuTelefono': telefono,
                'rolTipoRol': rol,
                'usuEstado': activo,
            },
        }

        if not all([documento, nombre, correo, clave]):
            messages.error(request, 'Documento, nombre, correo y contraseña son obligatorios.')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        if len(documento) < 6:
            messages.error(request, 'El documento debe tener al menos 6 caracteres.')
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
            usuNombreCompleto=nombre,
            usuCorreo=correo,
            usuTelefono=telefono,
            rolTipoRol=rol,
            usuClaveHash=make_password(clave),
            usuEstado=activo,
        )
        messages.success(request, f'Usuario {nombre} creado exitosamente.')
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
        nombre = request.POST.get('usuNombreCompleto', '').strip()
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

        if not all([documento, nombre, correo]):
            messages.error(request, 'Documento, nombre y correo son obligatorios.')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        if len(documento) < 6:
            messages.error(request, 'El documento debe tener al menos 6 caracteres.')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        # Validar duplicados excluyendo el usuario actual
        if Usuario.objects.filter(usuDocumento=documento).exclude(pk=pk).exists():
            messages.error(request, 'Ya existe otro usuario con ese documento.')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        if Usuario.objects.filter(usuCorreo=correo).exclude(pk=pk).exists():
            messages.error(request, 'Ya existe otro usuario con ese correo.')
            return render(request, 'admin_panel/usuarios/form.html', ctx)

        usuario.usuDocumento = documento
        usuario.usuNombreCompleto = nombre
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
        messages.success(request, f'Usuario {nombre} actualizado.')
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
