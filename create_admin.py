import os
import django
from django.contrib.auth.hashers import make_password

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multiparking.settings')
django.setup()

from usuarios.models import Usuario

def create_admin():
    email = 'admin@multiparking.com'
    password = 'admin123'
    
    if Usuario.objects.filter(usuCorreo=email).exists():
        print(f"Usuario {email} ya existe.")
        u = Usuario.objects.get(usuCorreo=email)
        u.rolTipoRol = 'ADMIN'
        u.usuClaveHash = make_password(password)
        u.save()
        print("Rol actualizado a ADMIN y contraseña restablecida.")
    else:
        Usuario.objects.create(
            usuDocumento='ADMIN001',
            usuNombreCompleto='Administrador Principal',
            usuCorreo=email,
            usuTelefono='0000000000',
            usuClaveHash=make_password(password),
            rolTipoRol='ADMIN',
            usuEstado=True
        )
        print(f"Usuario {email} creado exitosamente como ADMIN.")

if __name__ == '__main__':
    create_admin()
