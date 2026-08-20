#!/usr/bin/env pwsh
# upload_litterbox.ps1 — Sube un archivo a litterbox.catbox.moe y devuelve la URL
#
# Uso:
#   .\upload_litterbox.ps1 -File "C:\path\to\image.png" [-Time "1h"]
#
# Tiempos disponibles: 1h, 12h, 24h, 72h
# La URL devuelta es del tipo: https://litter.catbox.moe/XXXXX.png

param(
    [Parameter(Mandatory=$true)]
    [string]$File,

    [Parameter(Mandatory=$false)]
    [ValidateSet("1h","12h","24h","72h")]
    [string]$Time = "1h"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $File)) {
    Write-Error "Archivo no encontrado: $File"
    exit 1
}

$uri = "https://litterbox.catbox.moe/resources/internals/api.php"

try {
    # Construir multipart form
    $boundary = [System.Guid]::NewGuid().ToString("N")
    $fileBytes = [System.IO.File]::ReadAllBytes($File)
    $fileName  = [System.IO.Path]::GetFileName($File)
    $mimeType  = switch ([System.IO.Path]::GetExtension($File).ToLower()) {
        ".png"  { "image/png" }
        ".jpg"  { "image/jpeg" }
        ".jpeg" { "image/jpeg" }
        ".gif"  { "image/gif" }
        ".pdf"  { "application/pdf" }
        default { "application/octet-stream" }
    }

    $body = [System.Text.StringBuilder]::new()
    $LF = "`r`n"

    # reqtype field
    [void]$body.Append("--$boundary$LF")
    [void]$body.Append("Content-Disposition: form-data; name=`"reqtype`"$LF$LF")
    [void]$body.Append("fileupload$LF")

    # time field
    [void]$body.Append("--$boundary$LF")
    [void]$body.Append("Content-Disposition: form-data; name=`"time`"$LF$LF")
    [void]$body.Append("$Time$LF")

    # file field header
    $fileHeader = "--$boundary$LF" +
                  "Content-Disposition: form-data; name=`"fileToUpload`"; filename=`"$fileName`"$LF" +
                  "Content-Type: $mimeType$LF$LF"

    $fileFooter = "$LF--$boundary--$LF"

    $headerBytes  = [System.Text.Encoding]::UTF8.GetBytes($body.ToString() + $fileHeader)
    $footerBytes  = [System.Text.Encoding]::UTF8.GetBytes($fileFooter)

    $allBytes = $headerBytes + $fileBytes + $footerBytes

    $response = Invoke-RestMethod `
        -Uri $uri `
        -Method Post `
        -ContentType "multipart/form-data; boundary=$boundary" `
        -Body $allBytes

    $url = $response.Trim()

    if ($url -match "^https://litter\.catbox\.moe/") {
        Write-Host $url
        exit 0
    } else {
        Write-Error "Respuesta inesperada de litterbox: $url"
        exit 1
    }
} catch {
    Write-Error "Error al subir a litterbox: $_"
    exit 1
}
