import os
import django
from django.conf import settings
from django.urls import reverse
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multiparking.settings')
django.setup()

from parqueadero.views import AdminDashboardView
from reservas.views import ReservaListView

def verify():
    print("--- VERIFICANDO CARACTERÍSTICAS DEL DASHBOARD ---")
    
    # 1. Verificar URL de Reservas
    try:
        url = reverse('admin_reservas')
        print(f"[OK] URL 'admin_reservas' resuelve a: {url}")
    except Exception as e:
        print(f"[ERROR] No se pudo resolver 'admin_reservas': {e}")

    # 2. Verificar Renderizado del Dashboard (Contexto de Gráficos)
    factory = RequestFactory()
    request = factory.get(reverse('admin_dashboard'))
    
    # Simular sesión de admin
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session['usuario_id'] = 1 # Asumimos ID 1 es admin
    request.session['usuario_rol'] = 'ADMIN'
    request.session.save()

    view = AdminDashboardView()
    try:
        response = view.get(request)
        print(f"[OK] AdminDashboardView responde con status: {response.status_code}")
        
        # Verificar contenido del contexto (si es posible acceder, o buscar en contenido renderizado)
        content = response.content.decode('utf-8')
        if 'id="occupancyChart"' in content:
            print("[OK] Gráfico de Ocupación encontrado en HTML.")
        else:
            print("[ERROR] Gráfico de Ocupación NO encontrado.")

        if 'id="incomeChart"' in content:
            print("[OK] Gráfico de Ingresos encontrado en HTML.")
        else:
            print("[ERROR] Gráfico de Ingresos NO encontrado.")

        if 'Vista General de Reservas' in content:
            print("[OK] Tabla de Reservas encontrada en HTML.")
        else:
            print("[ERROR] Tabla de Reservas NO encontrada.")
            
    except Exception as e:
        print(f"[ERROR] Falló AdminDashboardView: {e}")

if __name__ == '__main__':
    verify()
