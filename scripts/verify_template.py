
import os
import django
from django.conf import settings
from django.template import engines

# Configure Django settings manually if not already configured
if not settings.configured:
    settings.configure(
        DEBUG=True,
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'multiparking',
            'usuarios',
            'vehiculos',
            'parqueadero',
            'reservas',
            'tarifas',
            'pagos',
            'cupones',
        ],
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(os.getcwd(), 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        }],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(os.getcwd(), 'db.sqlite3'),
            }
        },
        ROOT_URLCONF='multiparking.urls',
    )
    django.setup()

def verify_template():
    template_name = 'admin_panel/dashboard.html'
    print(f"Testing render of: {template_name}")
    
    try:
        django_engine = engines['django']
        template = django_engine.get_template(template_name)
        print("Template syntax is VALID.")
        
        # Try to render with dummy context
        context = {
            'total_espacios': 10,
            'disponibles': 5,
            'ocupados': 5,
            'reservas_activas': 2,
            'reservas_recientes': [],
            'ocupacion_labels': [],
            'ocupacion_data': [],
            'ingresos_data': [],
            # Add session mock if needed
        }
        rendered = template.render(context)
        print("Template rendering SUCCESSFUL.")
        
        if "{{ res.fkIdEspacio.espNumero }}" in rendered:
            print("CRITICAL: Raw tags found in rendered output!")
        else:
            print("No raw tags found in rendered output.")
            
    except Exception as e:
        print(f"Template Rendering FAILED: {e}")

if __name__ == '__main__':
    verify_template()
