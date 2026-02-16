import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multiparking.settings')
django.setup()

from parqueadero.models import Piso

def check_pisos():
    pisos = Piso.objects.all()
    print(f"Total Pisos: {pisos.count()}")
    for p in pisos:
        print(f"- {p.pisNombre} (ID: {p.pk})")

if __name__ == '__main__':
    check_pisos()
