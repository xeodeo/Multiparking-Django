#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

# Limpiar y cargar datos de prueba
python scripts/render_limpiar_bd.py
python scripts/render_datos_prueba.py