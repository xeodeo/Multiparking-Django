#!/usr/bin/env python3
"""
crop_component.py — Recorta un componente de un screenshot de cualquier CMS/backend web.

Uso:
    python crop_component.py <screenshot.png> <js_x> <js_y> <js_w> <js_h> <output.png> [modo]

Modos:
    gin      Busca borde oscuro (Drupal Gin, temas oscuros con bordes ~#000)  [default]
    coords   Usa coordenadas JS directamente sin análisis de píxeles
    auto     Intenta detectar el borde automáticamente (oscuro o claro)

Ejemplos:
    python crop_component.py raw.png 0 120 1380 450 componente.png gin
    python crop_component.py raw.png 0 80  1380 300 componente.png coords
    python crop_component.py raw.png 0 90  1380 500 componente.png auto
"""

import sys
import numpy as np
from PIL import Image


# ─────────────────────────────────────────────
# Detección de bordes
# ─────────────────────────────────────────────

def find_dark_border(arr, js_x, js_y, js_w, search_range=400, threshold=60, ratio=0.7):
    """Busca una fila de píxeles oscuros (#000-ish) que cubra >ratio del ancho."""
    height = arr.shape[0]
    for y in range(js_y, min(js_y + search_range, height)):
        row = arr[y, js_x: js_x + js_w]
        if len(row) == 0:
            continue
        dark = np.sum((row[:, 0] < threshold) & (row[:, 1] < threshold) & (row[:, 2] < threshold))
        if dark > len(row) * ratio:
            return y
    return None


def find_light_border(arr, js_x, js_y, js_w, search_range=400, bg_threshold=240, ratio=0.7):
    """Busca una fila muy clara (blanco/gris claro) que indique borde de card en temas claros."""
    height = arr.shape[0]
    for y in range(js_y, min(js_y + search_range, height)):
        row = arr[y, js_x: js_x + js_w]
        if len(row) == 0:
            continue
        light = np.sum((row[:, 0] > bg_threshold) & (row[:, 1] > bg_threshold) & (row[:, 2] > bg_threshold))
        if light > len(row) * ratio:
            return y
    return None


def get_card_x_bounds(arr, border_y, dark_threshold=60, light_threshold=240):
    """Determina left/right del card desde la fila del borde."""
    border_row = arr[border_y, :]
    # Intentar con oscuro primero
    dark_mask = (border_row[:, 0] < dark_threshold) & \
                (border_row[:, 1] < dark_threshold) & \
                (border_row[:, 2] < dark_threshold)
    dark_x = np.where(dark_mask)[0]
    if len(dark_x) > 10:
        return int(dark_x.min()) - 2, int(dark_x.max()) + 2
    # Fallback: zona no-fondo (diferencia del fondo blanco)
    non_bg = np.where(~((border_row[:, 0] > light_threshold) &
                        (border_row[:, 1] > light_threshold) &
                        (border_row[:, 2] > light_threshold)))[0]
    if len(non_bg) > 10:
        return int(non_bg.min()) - 2, int(non_bg.max()) + 2
    return None, None


# ─────────────────────────────────────────────
# Función principal
# ─────────────────────────────────────────────

def crop_component(screenshot_path, js_x, js_y, js_w, js_h, output_path, mode="gin", padding=8):
    img = Image.open(screenshot_path).convert("RGB")
    arr = np.array(img)

    print(f"Screenshot : {img.width}x{img.height}px")
    print(f"Coords JS  : x={js_x} y={js_y} w={js_w} h={js_h}  modo={mode}")

    card_top  = None
    card_left = js_x
    card_right = js_x + js_w

    if mode == "coords":
        # Usar coordenadas JS sin análisis
        card_top = js_y
        print(f"Modo coords: usando coordenadas JS directamente")

    elif mode == "gin":
        # Drupal Gin y temas con borde oscuro
        card_top = find_dark_border(arr, js_x, js_y, js_w)
        if card_top is None:
            print("Advertencia: borde oscuro no encontrado, usando js_y como fallback")
            card_top = js_y
        else:
            left, right = get_card_x_bounds(arr, card_top)
            if left is not None:
                card_left, card_right = left, right

    elif mode == "auto":
        # Intentar oscuro primero, luego claro
        card_top = find_dark_border(arr, js_x, js_y, js_w)
        if card_top:
            print(f"Auto: borde oscuro encontrado en y={card_top}")
        else:
            card_top = find_light_border(arr, js_x, js_y, js_w)
            if card_top:
                print(f"Auto: borde claro encontrado en y={card_top}")
            else:
                print("Auto: sin borde detectado, usando js_y")
                card_top = js_y

        left, right = get_card_x_bounds(arr, card_top)
        if left is not None:
            card_left, card_right = left, right

    offset     = card_top - js_y
    card_bottom = min(js_y + js_h + offset + padding, img.height)

    print(f"Offset visual vs JS: {offset}px")
    print(f"Recorte: left={card_left} top={card_top} right={card_right} bottom={card_bottom}")

    crop = img.crop((card_left, max(0, card_top - 2), card_right, card_bottom))
    crop.save(output_path)
    print(f"Guardado : {output_path} ({crop.width}x{crop.height}px)")

    # Imprimir para que el caller calcule PT
    print(f"DIMENSIONS:{crop.width}x{crop.height}")
    return crop.width, crop.height


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print(__doc__)
        sys.exit(1)

    _screenshot = sys.argv[1]
    _js_x  = int(sys.argv[2])
    _js_y  = int(sys.argv[3])
    _js_w  = int(sys.argv[4])
    _js_h  = int(sys.argv[5])
    _out   = sys.argv[6]
    _mode  = sys.argv[7] if len(sys.argv) > 7 else "gin"

    crop_component(_screenshot, _js_x, _js_y, _js_w, _js_h, _out, mode=_mode)
