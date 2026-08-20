#!/usr/bin/env node
/**
 * insert_image_docs.js — Inserta una imagen en un Google Doc via gws CLI
 *
 * Uso:
 *   node insert_image_docs.js <docId> <insertIndex> <imageUrl> <widthPt> <heightPt>
 *
 * Ejemplo:
 *   node insert_image_docs.js 1uNmdg6z... 450 https://litter.catbox.moe/abc.png 450 280
 *
 * Requiere: gws CLI configurado con autenticación OAuth2
 *
 * El script:
 * 1. Inserta un párrafo vacío en insertIndex
 * 2. Inserta la imagen inline
 * 3. Aplica estilo NORMAL_TEXT + centrado al párrafo
 */

const { execSync } = require('child_process');

function gwsBatchUpdate(docId, requests) {
    const params = JSON.stringify({ documentId: docId });
    const jsonBody = JSON.stringify({ requests });
    const result = execSync(
        'gws docs documents batchUpdate --params ' + JSON.stringify(params) + ' --json ' + JSON.stringify(jsonBody),
        { encoding: 'utf8', maxBuffer: 10 * 1024 * 1024 }
    );
    return JSON.parse(result.replace(/^Using keyring backend: keyring\n/, ''));
}

function insertImage(docId, insertIndex, imageUrl, widthPt, heightPt) {
    const idx = parseInt(insertIndex);
    const wPt = parseFloat(widthPt);
    const hPt = parseFloat(heightPt);

    const requests = [
        // 1. Crear párrafo vacío en la posición de inserción
        {
            insertText: {
                location: { index: idx },
                text: '\n'
            }
        },
        // 2. Insertar imagen inline
        {
            insertInlineImage: {
                location: { index: idx },
                uri: imageUrl,
                objectSize: {
                    height: { magnitude: hPt, unit: 'PT' },
                    width:  { magnitude: wPt, unit: 'PT' }
                }
            }
        },
        // 3. Aplicar NORMAL_TEXT + centrado (para limpiar herencia de HEADING_*)
        {
            updateParagraphStyle: {
                range: { startIndex: idx, endIndex: idx + 2 },
                paragraphStyle: {
                    namedStyleType: 'NORMAL_TEXT',
                    alignment: 'CENTER'
                },
                fields: 'namedStyleType,alignment'
            }
        }
    ];

    const res = gwsBatchUpdate(docId, requests);
    console.log('Imagen insertada correctamente');
    console.log('Respuestas:', JSON.stringify(res.replies, null, 2));
}

function getDocumentEndIndex(docId) {
    const params = JSON.stringify({ documentId: docId });
    const result = execSync(
        'gws docs documents get --params ' + JSON.stringify(params),
        { encoding: 'utf8', maxBuffer: 20 * 1024 * 1024 }
    );
    const doc = JSON.parse(result.replace(/^Using keyring backend: keyring\n/, ''));
    const content = doc.body?.content || [];
    if (content.length === 0) return 1;
    return content[content.length - 1].endIndex - 1;
}

// --- CLI ---
const args = process.argv.slice(2);

if (args[0] === 'get-end-index') {
    const docId = args[1];
    if (!docId) { console.error('Uso: node insert_image_docs.js get-end-index <docId>'); process.exit(1); }
    const endIdx = getDocumentEndIndex(docId);
    console.log(endIdx);
    process.exit(0);
}

if (args.length < 5) {
    console.error(`
Uso:
  node insert_image_docs.js <docId> <insertIndex> <imageUrl> <widthPt> <heightPt>
  node insert_image_docs.js get-end-index <docId>

Ejemplo:
  node insert_image_docs.js 1uNmdg6z... 450 https://litter.catbox.moe/abc.png 450 280.5
`);
    process.exit(1);
}

const [docId, insertIndex, imageUrl, widthPt, heightPt] = args;
insertImage(docId, insertIndex, imageUrl, widthPt, heightPt);
