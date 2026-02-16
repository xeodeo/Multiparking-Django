import os
import django
from django.test import Client, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multiparking.settings')
django.setup()

from parqueadero.views import AdminDashboardView
from usuarios.models import Usuario

def debug_view():
    print("--- INICIANDO DEBUG DE VISTA ---")
    
    # Crear usuario admin si no existe
    admin_user, _ = Usuario.objects.get_or_create(
        usuCorreo='admin_debug@test.com',
        defaults={
            'usuNombreCompleto': 'Admin Debug',
            'usuDocumento': '999999',
            'rolTipoRol': 'ADMIN',
            'usuEstado': True
        }
    )
    admin_user.rolTipoRol = 'ADMIN'
    admin_user.save()

    factory = RequestFactory()
    request = factory.get('/admin-panel/')
    
    # Simular middleware de sesión
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session['usuario_id'] = admin_user.pk
    request.session['usuario_rol'] = 'ADMIN'
    request.session['usuario_nombre'] = 'Admin Debug'
    request.session.save()
    
    # Ejecutar vista
    view = AdminDashboardView.as_view()
    response = view(request)
    
    print(f"Status Code: {response.status_code}")
    # Renderizado (si es TemplateResponse)
    if hasattr(response, 'render'):
        response.render()
        content = response.content.decode('utf-8')
        if "No hay pisos configurados en el sistema" in content:
            print("❌ El HTML contiene el mensaje 'No hay pisos configurados'")
        else:
            print("✅ El HTML NO contiene el mensaje de error (Pisos encontrados)")
            if "piso-button" in content or "tab-btn" in content:
                print("✅ Se encontraron botones de pestañas en el HTML")

if __name__ == '__main__':
    debug_view()
