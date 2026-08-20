---
name: drupal-screenshot-manual
description: >-
  Skill universal para capturar componentes de cualquier CMS/backend web
  (Drupal Gin, WordPress, paneles custom) e insertarlos en manuales de Google Docs.
  Incluye recorte inteligente por análisis de píxeles, upload a litterbox y
  inserción vía gws CLI. Modos: gin (bordes oscuros), auto (detecta automático),
  coords (coordenadas JS directas).
---

# Screenshot Manual — Skill universal para manuales con capturas de CMS

Captura componentes del backend de **cualquier CMS o panel de administración web**
e insértalos en un manual de Google Docs. Probado con Drupal 10 (tema Gin),
WordPress (WP-Admin) y paneles personalizados.

---

## Configuración por proyecto

Especificar en el prompt al invocar la skill:

| Parámetro     | Descripción                                    | Ejemplo                        |
|---------------|------------------------------------------------|--------------------------------|
| `BACKEND_URL` | URL del backend                                | `https://10.x.x.x:8443`       |
| `DOC_ID`      | ID del Google Doc del manual                   | `1uNmdg6z...`                  |
| `IMG_DIR`     | Carpeta local para guardar screenshots         | `C:\...\imagenes\`             |
| `CROP_MODE`   | Modo de recorte: `gin`, `auto`, `coords`       | `gin` para Drupal Gin          |
| Credenciales  | Usuario y contraseña del backend               | Solo en sesión, nunca al doc   |

---

## Herramientas requeridas

| Herramienta                  | Uso                                            | Instalación                  |
|------------------------------|------------------------------------------------|------------------------------|
| `mcp__playwright__*`         | Navegación, clics y screenshots                | MCP playwright               |
| Python 3 + Pillow + numpy    | Recorte inteligente por análisis de píxeles    | `pip install pillow numpy`   |
| PowerShell 7+                | Upload a litterbox, scripting                  | Incluido en Windows          |
| `gws` CLI                    | Inserción en Google Docs vía batchUpdate       | gws CLI del proyecto         |
| `scripts/cdp_helper.ps1`     | Alternativa CDP directa (sin playwright)       | Chrome con --remote-debugging-port=9222 |

---

## Modos de recorte (`CROP_MODE`)

| Modo     | Cuándo usarlo                                              | Cómo funciona                                  |
|----------|------------------------------------------------------------|------------------------------------------------|
| `gin`    | Drupal Gin y temas con bordes negros en cards              | Escanea píxeles oscuros para el borde real     |
| `auto`   | Cualquier backend — detecta tipo de borde automáticamente  | Prueba oscuro primero, luego claro             |
| `coords` | Backends con `position` confiable (sin headers fijos)      | Usa `getBoundingClientRect` directo            |

> **¿Por qué no siempre `coords`?** Los backends con toolbars fijos (`sticky/fixed`)
> desplazan el contenido visualmente pero `getBoundingClientRect` reporta las coords
> reales del DOM — que no coinciden con la posición en el screenshot. El análisis de
> píxeles resuelve ese desfase automáticamente.

---

## Workflow estándar

### 1. Preparar el navegador

```javascript
// Viewport grande para que bloques altos no queden cortados
mcp__playwright__browser_resize(width=1400, height=1100)
// Navegar al nodo/página en edición
mcp__playwright__browser_navigate(url="BACKEND_URL/path/to/edit")
```

### 2. Localizar el componente y obtener sus coordenadas

```javascript
// mcp__playwright__browser_evaluate:
// Adaptar el selector al CMS:
//   Drupal Gin  → 'tr.draggable.paragraph-type--TIPO'
//   WordPress   → '.wp-block[data-type="ns/block"], .acf-field[data-name="campo"]'
//   Custom CMS  → cualquier selector CSS del contenedor del componente
const el = document.querySelector('SELECTOR');
el.scrollIntoView({ block: 'start', behavior: 'instant' });
window.scrollBy(0, -10);
const r = el.getBoundingClientRect();
return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) };
```

**⚠️ Screenshot inmediatamente después** — evaluaciones adicionales pueden
re-scrollear y desincronizar las coordenadas.

### 3. Tomar el screenshot

```python
mcp__playwright__browser_take_screenshot(type="png", filename="raw.png")
```

### 4. Recortar el componente

```bash
# script incluido — elegir modo según el CMS:
python scripts/crop_component.py raw.png <js_x> <js_y> <js_w> <js_h> comp.png gin
python scripts/crop_component.py raw.png <js_x> <js_y> <js_w> <js_h> comp.png auto
python scripts/crop_component.py raw.png <js_x> <js_y> <js_w> <js_h> comp.png coords
```

La última línea de salida será `DIMENSIONS:WxH` — usarla para calcular los PT.

### 5. Verificar que el contenido inferior es visible

Si el bloque aparece cortado: aumentar el viewport o ajustar el scroll y repetir.

### 6. Subir a litterbox

```powershell
$url = .\scripts\upload_litterbox.ps1 -File "comp.png" -Time "1h"
# → https://litter.catbox.moe/XXXXX.png
```

**URLs expiran en 1h.** Subir justo antes de insertar en el doc.

### 7. Insertar en Google Docs

```bash
# Obtener índice de inserción:
node scripts/insert_image_docs.js get-end-index <DOC_ID>

# Insertar la imagen (W_PT=450 estándar, H_PT proporcional):
node scripts/insert_image_docs.js <DOC_ID> <INDEX> <URL> <W_PT> <H_PT>
```

O construir el batch manualmente:

```javascript
const W_PT = 450.0;
const H_PT = Math.round((imgH / imgW) * W_PT * 10) / 10;

const requests = [
    { insertText: { location: { index: IDX }, text: "\n" } },
    { insertInlineImage: {
        location: { index: IDX },
        uri: "https://litter.catbox.moe/XXXXX.png",
        objectSize: {
            height: { magnitude: H_PT, unit: "PT" },
            width:  { magnitude: W_PT, unit: "PT" }
        }
    }},
    { updateParagraphStyle: {
        range: { startIndex: IDX, endIndex: IDX + 2 },
        paragraphStyle: { namedStyleType: "NORMAL_TEXT", alignment: "CENTER" },
        fields: "namedStyleType,alignment"
    }},
];
```

---

## Layout estándar collapsed + expanded en el doc

```
HEADING_3   "Nombre del Componente"
[imagen collapsed — centrada]
Variación / descripción
Campo 1: descripción
...
[imagen expanded — centrada]
HEADING_3   "Siguiente Componente"
```

Expandir el componente antes del segundo screenshot:

```javascript
// Drupal Gin:
const btn = tr.querySelector('button[class*="edit"]') ||
            [...tr.querySelectorAll('button')].find(b => /editar|edit/i.test(b.textContent));
// WordPress ACF / Gutenberg:
const btn = el.querySelector('.edit-post-block-toolbar button, .acf-fc-layout-handle');
// Genérico:
const btn = [...el.querySelectorAll('button')].find(b => /editar|edit|expand/i.test(b.textContent));
if (btn) btn.click();
```

---

## Adaptación por CMS

### Drupal 10 — Tema Gin

```
CROP_MODE  : gin
Selector   : tr.draggable.paragraph-type--NOMBRE_BUNDLE
Viewport   : 1400x1100
```

### WordPress — WP-Admin / ACF

```
CROP_MODE  : auto  (WP-Admin tiene header fijo de ~32px)
Selector   : .wp-block[data-type="NAMESPACE/BLOCK"]  o  .acf-field[data-name="CAMPO"]
Viewport   : 1400x900
```

### Panel personalizado / SPA

```
CROP_MODE  : auto o coords
Selector   : identificar con DevTools el contenedor del componente
```

---

## Scripts incluidos

| Script                          | Descripción                                              |
|---------------------------------|----------------------------------------------------------|
| `scripts/crop_component.py`     | Recorte inteligente multi-modo (gin / auto / coords)     |
| `scripts/upload_litterbox.ps1`  | Sube imagen a litterbox.catbox.moe, devuelve URL         |
| `scripts/insert_image_docs.js`  | Inserta imagen en Google Doc via gws CLI                 |
| `scripts/cdp_helper.ps1`        | Helper CDP alternativo (Chrome DevTools Protocol directo)|

---

## Inserción limpia en el doc

- Hacer `get-end-index` justo antes de insertar para obtener índices actuales
- Procesar de mayor a menor índice cuando hay múltiples operaciones en un batch
- Si aparecen imágenes en posiciones incorrectas: `deleteContentRange` + re-insertar
- El punto de inserción puede heredar estilo `HEADING_3` — siempre aplicar
  `updateParagraphStyle NORMAL_TEXT` después de insertar

---

## Errores comunes

| Error                              | Causa                                       | Solución                                           |
|------------------------------------|---------------------------------------------|----------------------------------------------------|
| Screenshot incluye toolbar del CMS | Coords JS sin ajuste de header fijo         | Usar modo `gin` o `auto`                           |
| Parte inferior cortada             | Viewport pequeño o scroll insuficiente      | Usar 1400×1100, verificar strip inferior           |
| Imagen en HEADING_3 en el doc      | Insertion point hereda el heading           | Aplicar `updateParagraphStyle NORMAL_TEXT`         |
| URL de catbox expirada             | Pasó más de 1h desde la subida              | Re-subir justo antes de insertar                  |
| `DIMENSIONS` no aparece en crop    | Borde no detectado                          | Cambiar modo a `coords` o `auto`                  |
| Imagen en posición incorrecta      | Índices desincronizados por inserción previa| Hacer `get-end-index` después de cada insert      |
