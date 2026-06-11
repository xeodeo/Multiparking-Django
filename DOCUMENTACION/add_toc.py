"""
Post-procesa MultiParking_Documentacion.docx sin python-docx:
  - Abre el .docx como ZIP, lee word/document.xml
  - Elimina las entradas estáticas del índice (tocEntry dot-leaders)
  - Inserta campo TOC de Word (se actualiza con Ctrl+A → F9 en Word)
"""
import os
import sys
import re
import shutil
import zipfile
import xml.etree.ElementTree as ET

DOC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "MultiParking_Documentacion.docx")
BACKUP = DOC + ".bak"

if not os.path.exists(DOC):
    print(f"ERROR: no se encontró {DOC}")
    sys.exit(1)

# Namespace map
NS = {
    'w':   'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
    'r':   'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

def qtag(local):
    return f'{{{W}}}{local}'


def para_text(p_elem):
    """Devuelve el texto concatenado de un párrafo."""
    return ''.join(t.text or '' for t in p_elem.iter(qtag('t')))


def make_toc_field_para():
    """Construye el elemento <w:p> con el campo TOC complejo de Word."""
    raw = (
        '<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:pPr><w:ind w:firstLine="0"/></w:pPr>'
        '<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
        '<w:r>'
          '<w:instrText xml:space="preserve"> TOC \\o "1-3" \\h \\z \\u </w:instrText>'
        '</w:r>'
        '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
        '<w:r>'
          '<w:t>[Actualizar tabla: seleccionar todo (Ctrl+A) y presionar F9 en Word]</w:t>'
        '</w:r>'
        '<w:r><w:fldChar w:fldCharType="end"/></w:r>'
        '</w:p>'
    )
    return ET.fromstring(raw)


# ── 1. Hacer backup ────────────────────────────────────────────────────────────
shutil.copy2(DOC, BACKUP)
print(f"Backup: {BACKUP}")

# ── 2. Extraer document.xml ────────────────────────────────────────────────────
with zipfile.ZipFile(DOC, 'r') as z:
    xml_bytes = z.read('word/document.xml')
    all_names = z.namelist()

# ── 3. Parsear ─────────────────────────────────────────────────────────────────
ET.register_namespace('w', W)
# Registrar todos los prefijos relevantes para no perderlos
for prefix, uri in [
    ('wpc', 'http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas'),
    ('cx',  'http://schemas.microsoft.com/office/drawing/2014/chartex'),
    ('r',   'http://schemas.openxmlformats.org/officeDocument/2006/relationships'),
    ('m',   'http://schemas.openxmlformats.org/officeDocument/2006/math'),
    ('o',   'urn:schemas-microsoft-com:office:office'),
    ('v',   'urn:schemas-microsoft-com:vml'),
    ('wp14','http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing'),
    ('wp',  'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'),
    ('w10', 'urn:schemas-microsoft-com:office:word'),
    ('w14', 'http://schemas.microsoft.com/office/word/2010/wordml'),
    ('w15', 'http://schemas.microsoft.com/office/word/2012/wordml'),
    ('w16se','http://schemas.microsoft.com/office/word/2015/wordml/symex'),
    ('wpg', 'http://schemas.microsoft.com/office/word/2010/wordprocessingGroup'),
    ('wpi', 'http://schemas.microsoft.com/office/word/2010/wordprocessingInk'),
    ('wne', 'http://schemas.microsoft.com/office/word/2006/wordml'),
    ('wps', 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape'),
]:
    ET.register_namespace(prefix, uri)

root = ET.fromstring(xml_bytes)

# Encontrar el body
body = root.find(f'.//{qtag("body")}')
if body is None:
    body = root  # fallback

children = list(body)

# ── 4. Localizar "Tabla de Contenido" y el salto de página posterior ──────────
toc_title_idx = None
pb_idx = None

for i, child in enumerate(children):
    if child.tag != qtag('p'):
        continue
    text = para_text(child)
    if toc_title_idx is None and 'Tabla de Contenido' in text:
        toc_title_idx = i
        print(f"  Título TOC encontrado en párrafo [{i}]: '{text[:60]}'")
        continue
    if toc_title_idx is not None:
        for br in child.iter(qtag('br')):
            btype = br.get(qtag('type'))
            if btype == 'page':
                pb_idx = i
                break
        if pb_idx is not None:
            print(f"  Salto de página en párrafo [{i}]")
            break

if toc_title_idx is None or pb_idx is None:
    print(f"ERROR: título={toc_title_idx}, pb={pb_idx}")
    print("No se encontró la sección TOC. Revisa que el docx tenga 'Tabla de Contenido'.")
    sys.exit(1)

# ── 5. Eliminar entradas estáticas (entre título+1 y pb, sin incluir pb) ──────
to_remove = children[toc_title_idx + 1 : pb_idx]
print(f"  Eliminando {len(to_remove)} párrafos estáticos...")
for elem in to_remove:
    body.remove(elem)

# Después de la eliminación, pb_idx cambió — recalcular
children2 = list(body)
new_pb_idx = None
for i, child in enumerate(children2):
    if child.tag != qtag('p'):
        continue
    for br in child.iter(qtag('br')):
        if br.get(qtag('type')) == 'page':
            new_pb_idx = i
            break
    if new_pb_idx is not None and i > toc_title_idx:
        break

insert_at = toc_title_idx + 1  # justo después del título

# ── 6. Insertar el campo TOC ───────────────────────────────────────────────────
toc_para = make_toc_field_para()
body.insert(insert_at, toc_para)
print(f"  Campo TOC insertado en posición [{insert_at}]")

# ── 7. Serializar ──────────────────────────────────────────────────────────────
# ET preserva los namespaces registrados
new_xml = ET.tostring(root, encoding='unicode', xml_declaration=False)
new_xml_bytes = ('<?xml version=\'1.0\' encoding=\'UTF-8\' standalone=\'yes\'?>\n' +
                 new_xml).encode('utf-8')

# ── 8. Reescribir el ZIP ───────────────────────────────────────────────────────
tmp = DOC + ".tmp"
with zipfile.ZipFile(DOC, 'r') as zin:
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename == 'word/document.xml':
                zout.writestr(item, new_xml_bytes)
            else:
                zout.writestr(item, zin.read(item.filename))

os.replace(tmp, DOC)
print(f"\nOK — {DOC}")
print("Abre en Word y presiona Ctrl+A + F9 para actualizar el indice.")
