from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from django.shortcuts import redirect, render

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
            usuNombreCompleto=nombre,
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
