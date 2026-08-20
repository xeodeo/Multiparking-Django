#!/usr/bin/env pwsh
# cdp_helper.ps1 — Chrome DevTools Protocol helper para capturas de pantalla
# Uso: .\cdp_helper.ps1 <subcomando> [opciones]
# Requiere: Chrome corriendo con --remote-debugging-port=9222

param(
    [Parameter(Position=0)]
    [string]$Command,
    [string]$Tab,          # Tab ID (obtenido de http://localhost:9222/json)
    [string]$Output,       # Ruta de salida para screenshots
    [string]$Selector,     # CSS selector
    [string]$Label,        # Texto del label para find-field
    [string]$Clip,         # "x,y,width,height" para recorte
    [double]$Scale = 1.5,  # Factor de zoom
    [int]$Padding = 15,    # Padding alrededor del elemento
    [int]$X = 0,
    [int]$Y = 0,
    [string]$Url,          # URL para navegar
    [string]$User = "admin",
    [string]$Pass = "admin",
    [int]$WaitMs = 2000,
    [int]$Index = -1,      # Indice del paragraph (0-based) para subcomandos de paragraphs
    [string]$ParagraphField = ""  # Nombre del campo paragraphs (ej: 'field-contenido')
)

# ============================================================
# Función base WebSocket CDP
# ============================================================
function Invoke-CDP {
    param([string]$TabId, [string]$Json, [int]$Wait = 1500)
    $wsUrl = "ws://localhost:9222/devtools/page/$TabId"
    $ws = New-Object System.Net.WebSockets.ClientWebSocket
    $ws.ConnectAsync([System.Uri]$wsUrl, [System.Threading.CancellationToken]::None).Wait()
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($Json)
    $ws.SendAsync([System.ArraySegment[byte]]$bytes, [System.Net.WebSockets.WebSocketMessageType]::Text, $true, [System.Threading.CancellationToken]::None).Wait()
    Start-Sleep -Milliseconds $Wait
    $ms = New-Object System.IO.MemoryStream
    $buf = New-Object byte[] 131072
    do {
        $seg = New-Object System.ArraySegment[byte]($buf, 0, $buf.Length)
        $res = $ws.ReceiveAsync($seg, [System.Threading.CancellationToken]::None).Result
        $ms.Write($buf, 0, $res.Count)
    } while (!$res.EndOfMessage)
    $ws.CloseAsync([System.Net.WebSockets.WebSocketCloseStatus]::NormalClosure, "done", [System.Threading.CancellationToken]::None).Wait()
    return [System.Text.Encoding]::UTF8.GetString($ms.ToArray())
}

function Invoke-JS {
    param([string]$TabId, [string]$Expr, [int]$Wait = 800)
    $payload = @{ id=99; method="Runtime.evaluate"; params=@{expression=$Expr; returnByValue=$true} } | ConvertTo-Json -Compress
    $r = Invoke-CDP -TabId $TabId -Json $payload -Wait $Wait
    return ($r | ConvertFrom-Json).result.result.value
}

function Save-Screenshot {
    param([string]$TabId, [string]$OutPath, [string]$ClipJson = $null, [double]$Sc = 1.5, [int]$Wait = 1500)
    if ($ClipJson) {
        $payload = '{"id":98,"method":"Page.captureScreenshot","params":{"format":"png","clip":' + $ClipJson + '}}'
    } else {
        $payload = '{"id":98,"method":"Page.captureScreenshot","params":{"format":"png"}}'
    }
    $r = Invoke-CDP -TabId $TabId -Json $payload -Wait $Wait
    $data = ($r | ConvertFrom-Json).result.data
    if (-not $data) { Write-Error "No se pudo obtener captura"; exit 1 }
    $bytes = [Convert]::FromBase64String($data)
    [IO.File]::WriteAllBytes($OutPath, $bytes)
    Write-Host "Captura guardada: $OutPath ($($bytes.Length) bytes)"
}

# ============================================================
# Verificar que Chrome está activo
# ============================================================
function Test-ChromeDebug {
    try {
        $info = Invoke-RestMethod -Uri "http://localhost:9222/json/version" -ErrorAction Stop
        Write-Host "Chrome conectado: $($info.Browser)"
        return $true
    } catch {
        Write-Error "Chrome no responde en puerto 9222. Lanza Chrome con --remote-debugging-port=9222"
        return $false
    }
}

# ============================================================
# SUBCOMANDOS
# ============================================================

switch ($Command) {

    # ----------------------------------------------------------
    # check — Verifica conexión y lista pestañas
    # ----------------------------------------------------------
    "check" {
        if (-not (Test-ChromeDebug)) { exit 1 }
        $tabs = Invoke-RestMethod -Uri "http://localhost:9222/json"
        $pages = $tabs | Where-Object { $_.type -eq "page" }
        Write-Host "`nPestanas activas:"
        $pages | ForEach-Object { Write-Host "  ID: $($_.id) | URL: $($_.url.Substring(0,[Math]::Min(80,$_.url.Length)))" }
    }

    # ----------------------------------------------------------
    # navigate — Navega a una URL
    # ----------------------------------------------------------
    "navigate" {
        if (-not $Tab) { Write-Error "--tab es requerido"; exit 1 }
        if (-not $Url)  { Write-Error "--url es requerido"; exit 1 }
        $payload = '{"id":1,"method":"Page.navigate","params":{"url":"' + $Url + '"}}'
        $r = Invoke-CDP -TabId $Tab -Json $payload -Wait $WaitMs
        $title = Invoke-JS -TabId $Tab -Expr "document.title"
        Write-Host "Navegado a: $Url | Titulo: $title"
    }

    # ----------------------------------------------------------
    # login — Login en Drupal via formulario
    # ----------------------------------------------------------
    "login" {
        if (-not $Tab) { Write-Error "--tab es requerido"; exit 1 }
        if (-not $Url)  { Write-Error "--url es requerido (URL del login)"; exit 1 }
        $nav = '{"id":1,"method":"Page.navigate","params":{"url":"' + $Url + '"}}'
        Invoke-CDP -TabId $Tab -Json $nav -Wait 3000 | Out-Null
        $expr = 'document.getElementById("edit-name").value="' + $User + '"; document.getElementById("edit-pass").value="' + $Pass + '"; document.getElementById("edit-submit").click(); "submitted"'
        $payload = @{id=2; method="Runtime.evaluate"; params=@{expression=$expr; returnByValue=$true}} | ConvertTo-Json -Compress
        Invoke-CDP -TabId $Tab -Json $payload -Wait 4000 | Out-Null
        $title = Invoke-JS -TabId $Tab -Expr "document.title + ' | ' + window.location.pathname"
        Write-Host "Login result: $title"
    }

    # ----------------------------------------------------------
    # screenshot — Captura de pantalla (full o clipped)
    # ----------------------------------------------------------
    "screenshot" {
        if (-not $Tab)    { Write-Error "--tab es requerido"; exit 1 }
        if (-not $Output) { Write-Error "--output es requerido"; exit 1 }
        $clipJson = $null
        if ($Clip) {
            $parts = $Clip -split ","
            if ($parts.Count -ne 4) { Write-Error "--clip debe ser x,y,width,height"; exit 1 }
            $clipJson = '{"x":' + $parts[0] + ',"y":' + $parts[1] + ',"width":' + $parts[2] + ',"height":' + $parts[3] + ',"scale":' + $Scale + '}'
        }
        Save-Screenshot -TabId $Tab -OutPath $Output -ClipJson $clipJson -Sc $Scale -Wait $WaitMs
    }

    # ----------------------------------------------------------
    # get-rect — Obtiene bounding box de un elemento
    # ----------------------------------------------------------
    "get-rect" {
        if (-not $Tab)      { Write-Error "--tab es requerido"; exit 1 }
        if (-not $Selector) { Write-Error "--selector es requerido"; exit 1 }
        $expr = "var el=document.querySelector('" + $Selector + "'); if(!el){'{}'} else { var r=el.getBoundingClientRect(); JSON.stringify({x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),cx:Math.round(r.left+r.width/2),cy:Math.round(r.top+r.height/2)}) }"
        $result = Invoke-JS -TabId $Tab -Expr $expr
        Write-Host $result
    }

    # ----------------------------------------------------------
    # find-field — Encuentra campo por texto de label y devuelve clip con padding
    # ----------------------------------------------------------
    "find-field" {
        if (-not $Tab)   { Write-Error "--tab es requerido"; exit 1 }
        if (-not $Label) { Write-Error "--label es requerido"; exit 1 }
        $expr = @"
(function() {
    var labels = document.querySelectorAll('label');
    for(var i=0; i<labels.length; i++) {
        var lbl = labels[i];
        if(lbl.textContent.trim().toLowerCase().indexOf('$($Label.ToLower())') >= 0) {
            var inputId = lbl.htmlFor;
            var input = inputId ? document.getElementById(inputId) : lbl.nextElementSibling;
            var lr = lbl.getBoundingClientRect();
            var ir = input ? input.getBoundingClientRect() : lr;
            var pad = $Padding;
            var x = Math.round(Math.min(lr.left, ir.left) - pad);
            var y = Math.round(lr.top - pad);
            var w = Math.round(Math.max(lr.right, ir.right) - x + pad);
            var h = Math.round(ir.bottom - y + pad);
            return JSON.stringify({x:x, y:y, w:w, h:h, clip: x+','+y+','+w+','+h, label: lbl.textContent.trim(), value: input ? input.value : ''});
        }
    }
    return '{"error":"Label not found"}';
})()
"@
        $result = Invoke-JS -TabId $Tab -Expr $expr
        Write-Host $result
        if ($Output -and $result -notlike '*error*') {
            $pos = $result | ConvertFrom-Json
            $clipJson = '{"x":' + $pos.x + ',"y":' + $pos.y + ',"width":' + $pos.w + ',"height":' + $pos.h + ',"scale":' + $Scale + '}'
            Save-Screenshot -TabId $Tab -OutPath $Output -ClipJson $clipJson -Sc $Scale
        }
    }

    # ----------------------------------------------------------
    # scroll-to — Hace scroll para llevar elemento al centro del viewport
    # ----------------------------------------------------------
    "scroll-to" {
        if (-not $Tab)      { Write-Error "--tab es requerido"; exit 1 }
        if (-not $Selector) { Write-Error "--selector es requerido"; exit 1 }
        $expr = "document.querySelector('" + $Selector + "').scrollIntoView({behavior:'instant',block:'center'})"
        $payload = @{id=50; method="Runtime.evaluate"; params=@{expression=$expr; returnByValue=$true}} | ConvertTo-Json -Compress
        Invoke-CDP -TabId $Tab -Json $payload -Wait 800 | Out-Null
        Write-Host "Scroll realizado a: $Selector"
    }

    # ----------------------------------------------------------
    # click — Hace clic en coordenadas x,y
    # ----------------------------------------------------------
    "click" {
        if (-not $Tab) { Write-Error "--tab es requerido"; exit 1 }
        $press   = '{"id":60,"method":"Input.dispatchMouseEvent","params":{"type":"mousePressed","x":' + $X + ',"y":' + $Y + ',"button":"left","clickCount":1,"buttons":1}}'
        $release = '{"id":61,"method":"Input.dispatchMouseEvent","params":{"type":"mouseReleased","x":' + $X + ',"y":' + $Y + ',"button":"left","clickCount":1,"buttons":0}}'
        Invoke-CDP -TabId $Tab -Json $press   -Wait 100  | Out-Null
        Invoke-CDP -TabId $Tab -Json $release -Wait $WaitMs | Out-Null
        Write-Host "Clic en ($X, $Y)"
    }

    # ----------------------------------------------------------
    # get-center — Devuelve cx,cy del centro de un elemento
    # ----------------------------------------------------------
    "get-center" {
        if (-not $Tab)      { Write-Error "--tab es requerido"; exit 1 }
        if (-not $Selector) { Write-Error "--selector es requerido"; exit 1 }
        $expr = "var r=document.querySelector('" + $Selector + "').getBoundingClientRect(); JSON.stringify({cx:Math.round(r.left+r.width/2),cy:Math.round(r.top+r.height/2)})"
        $result = Invoke-JS -TabId $Tab -Expr $expr
        Write-Host $result
    }

    # ----------------------------------------------------------
    # list-paragraphs — Lista todos los paragraphs en el formulario de edicion
    # ----------------------------------------------------------
    "list-paragraphs" {
        if (-not $Tab) { Write-Error "--tab es requerido"; exit 1 }
        $expr = @"
(function() {
    var wrappers = document.querySelectorAll('[class*="paragraph--type--"]');
    var result = [];
    wrappers.forEach(function(el, i) {
        var classes = el.className;
        var bundleMatch = classes.match(/paragraph--type--([\w-]+)/);
        var bundle = bundleMatch ? bundleMatch[1] : '?';
        var rect = el.getBoundingClientRect();
        var level = 0;
        var parent = el.parentElement;
        while(parent) {
            if(parent.className && parent.className.match && parent.className.match(/paragraph--type/)) level++;
            parent = parent.parentElement;
        }
        var collapsed = el.classList.contains('collapsed') || el.querySelector('.paragraph-summary') !== null;
        var summary = el.querySelector('.paragraph-summary, .field--name-field-titulo, .field--name-title, h2, h3');
        var summaryText = summary ? summary.textContent.trim().substring(0,60) : '';
        if (rect.width > 0) {
            result.push({
                index: i, bundle: bundle, level: level, collapsed: collapsed,
                summary: summaryText, top: Math.round(rect.top), h: Math.round(rect.height),
                cx: Math.round(rect.left + rect.width/2), cy: Math.round(rect.top + rect.height/2)
            });
        }
    });
    return JSON.stringify(result);
})()
"@
        $result = Invoke-JS -TabId $Tab -Expr $expr -Wait 1000
        Write-Host $result
    }

    # ----------------------------------------------------------
    # list-paragraph-types — Lista los bundles/variaciones disponibles
    # ----------------------------------------------------------
    "list-paragraph-types" {
        if (-not $Tab) { Write-Error "--tab es requerido"; exit 1 }
        $expr = @"
(function() {
    var addButtons = document.querySelectorAll('.field-add-more-submit, [id*="add-more"], button[name*="add_more"]');
    var typeSelect = document.querySelectorAll('select[name*="paragraph"][name*="type"], .paragraphs-dropdown select');
    var result = { buttons: [], selectOptions: [], addLinks: [] };
    addButtons.forEach(function(btn) { result.buttons.push(btn.value || btn.textContent.trim()); });
    typeSelect.forEach(function(sel) {
        [...sel.options].forEach(function(opt) {
            if(opt.value) result.selectOptions.push({value: opt.value, label: opt.text.trim()});
        });
    });
    var links = document.querySelectorAll('a[href*="paragraph"], .add-paragraph-type-list a, .paragraphs-add-dialog a');
    links.forEach(function(a) { result.addLinks.push(a.textContent.trim()); });
    return JSON.stringify(result);
})()
"@
        $result = Invoke-JS -TabId $Tab -Expr $expr -Wait 800
        Write-Host $result
        if ($Output) {
            $areaExpr = "var el = document.querySelector('.paragraphs-add-dialog, .field-add-more-submit, [class*=paragraphs][class*=add]'); if(el){var r=el.getBoundingClientRect(); JSON.stringify({x:Math.round(r.left-20),y:Math.round(r.top-20),w:Math.round(r.width+40),h:Math.round(r.height+40)})} else '{}'"
            $area = Invoke-JS -TabId $Tab -Expr $areaExpr -Wait 500
            if ($area -ne '{}') {
                $pos = $area | ConvertFrom-Json
                $clipJson = '{"x":' + $pos.x + ',"y":' + $pos.y + ',"width":' + $pos.w + ',"height":' + $pos.h + ',"scale":' + $Scale + '}'
                Save-Screenshot -TabId $Tab -OutPath $Output -ClipJson $clipJson -Sc $Scale
            }
        }
    }

    # ----------------------------------------------------------
    # expand-paragraph -- Expande un paragraph colapsado por indice
    # ----------------------------------------------------------
    "expand-paragraph" {
        if (-not $Tab) { Write-Error "--tab es requerido"; exit 1 }
        if ($Index -lt 0) { Write-Error "--index es requerido (0-based)"; exit 1 }
        $expr = @"
(function() {
    var wrappers = document.querySelectorAll('[class*="paragraph--type--"]');
    if ($Index >= wrappers.length) return JSON.stringify({error: 'index out of range', total: wrappers.length});
    var el = wrappers[$Index];
    var editBtn = el.querySelector('input[value="Editar"], input[value="Edit"], button.paragraphs-edit-mode-icon, .paragraph-edit-mode-icon, [id*="edit-mode"]');
    if (editBtn) {
        editBtn.click();
        return JSON.stringify({action:'clicked_edit', bundle: el.className.match(/paragraph--type--([\w-]+)/)?.[1]});
    }
    var details = el.querySelector('details');
    if (details) { details.open = true; return JSON.stringify({action:'opened_details'}); }
    return JSON.stringify({error: 'no_edit_button_found'});
})()
"@
        $result = Invoke-JS -TabId $Tab -Expr $expr -Wait $WaitMs
        Write-Host $result
    }

    # ----------------------------------------------------------
    # capture-paragraph -- Captura un paragraph especifico
    # ----------------------------------------------------------
    "capture-paragraph" {
        if (-not $Tab)    { Write-Error "--tab es requerido"; exit 1 }
        if (-not $Output) { Write-Error "--output es requerido"; exit 1 }
        if ($Index -lt 0) { Write-Error "--index es requerido (0-based)"; exit 1 }
        $scrollExpr = "var wrappers=document.querySelectorAll('[class*=paragraph--type--]'); if(wrappers[$Index]) wrappers[$Index].scrollIntoView({behavior:'instant',block:'start'}); 'ok'"
        Invoke-JS -TabId $Tab -Expr $scrollExpr -Wait 1000 | Out-Null
        $rectExpr = @"
(function() {
    var wrappers = document.querySelectorAll('[class*="paragraph--type--"]');
    var el = wrappers[$Index];
    if (!el) return '{}';
    var r = el.getBoundingClientRect();
    var bundle = (el.className.match(/paragraph--type--([\w-]+)/) || ['','?'])[1];
    var pad = 10;
    return JSON.stringify({
        bundle: bundle,
        x: Math.round(r.left - pad), y: Math.round(r.top - pad),
        w: Math.round(r.width + pad*2),
        h: Math.round(Math.min(r.height + pad*2, 700)),
        fullH: Math.round(r.height)
    });
})()
"@
        $rectResult = Invoke-JS -TabId $Tab -Expr $rectExpr -Wait 500
        Write-Host "Paragraph $Index: $rectResult"
        if ($rectResult -ne '{}' -and $rectResult) {
            $pos = $rectResult | ConvertFrom-Json
            $clipJson = '{"x":' + $pos.x + ',"y":' + $pos.y + ',"width":' + $pos.w + ',"height":' + $pos.h + ',"scale":' + $Scale + '}'
            Save-Screenshot -TabId $Tab -OutPath $Output -ClipJson $clipJson -Sc $Scale -Wait $WaitMs
        } else {
            Write-Error "No se encontro el paragraph con index $Index"
        }
    }

    # ----------------------------------------------------------
    # capture-paragraph-tree -- Captura el arbol completo de paragraphs
    # ----------------------------------------------------------
    "capture-paragraph-tree" {
        if (-not $Tab) { Write-Error "--tab es requerido"; exit 1 }
        $baseOut = if ($Output) { $Output } else { "paragraph" }
        $outDir = Split-Path $baseOut -Parent
        $baseName = Split-Path $baseOut -Leaf
        if (-not $outDir) { $outDir = "." }
        $treeExpr = @"
(function() {
    var all = document.querySelectorAll('[class*="paragraph--type--"]');
    var roots = [];
    all.forEach(function(el, i) {
        var level = 0;
        var p = el.parentElement;
        while(p) { if(p.className && p.className.match && p.className.match(/paragraph--type/)) level++; p=p.parentElement; }
        if (level === 0) {
            var r = el.getBoundingClientRect();
            var bundle = (el.className.match(/paragraph--type--([\w-]+)/) || ['','?'])[1];
            var children = el.querySelectorAll('[class*="paragraph--type--"]');
            roots.push({ index: i, bundle: bundle, childCount: children.length,
                top: Math.round(r.top), h: Math.round(r.height),
                cx: Math.round(r.left+r.width/2), cy: Math.round(r.top+r.height/2) });
        }
    });
    return JSON.stringify(roots);
})()
"@
        $roots = Invoke-JS -TabId $Tab -Expr $treeExpr -Wait 800
        Write-Host "Paragraphs raiz encontrados: $roots"
        $rootsList = $roots | ConvertFrom-Json
        if (-not $rootsList) { Write-Error "No se encontraron paragraphs"; exit 1 }
        foreach ($pg in $rootsList) {
            $outFile = "$outDir\${baseName}_$($pg.index)_$($pg.bundle).png"
            Write-Host "==> Capturando paragraph $($pg.index) [$($pg.bundle)] -> $outFile"
            $scrollExpr2 = "var wrappers=document.querySelectorAll('[class*=paragraph--type--]'); if(wrappers[$($pg.index)]) wrappers[$($pg.index)].scrollIntoView({behavior:'instant',block:'start'}); 'ok'"
            Invoke-JS -TabId $Tab -Expr $scrollExpr2 -Wait 800 | Out-Null
            $rectExpr2 = "var el=document.querySelectorAll('[class*=paragraph--type--]')[$($pg.index)]; var r=el.getBoundingClientRect(); JSON.stringify({x:Math.round(r.left-10),y:Math.round(r.top-10),w:Math.round(r.width+20),h:Math.round(Math.min(r.height+20,750))})"
            $rect2 = Invoke-JS -TabId $Tab -Expr $rectExpr2 -Wait 500
            $p2 = $rect2 | ConvertFrom-Json
            $clipJson2 = '{"x":' + $p2.x + ',"y":' + $p2.y + ',"width":' + $p2.w + ',"height":' + $p2.h + ',"scale":' + $Scale + '}'
            Save-Screenshot -TabId $Tab -OutPath $outFile -ClipJson $clipJson2 -Sc $Scale -Wait 1200
        }
        Write-Host "Arbol de paragraphs capturado: $($rootsList.Count) imagen(es) en $outDir"
    }

    # ----------------------------------------------------------
    # list-components — Lista componentes Canvas en la página
    # ----------------------------------------------------------
    "list-components" {
        if (-not $Tab) { Write-Error "--tab es requerido"; exit 1 }
        $expr = @"
var items = document.querySelectorAll('.canvas--sortable-item');
var result = [];
for(var i=0; i<items.length; i++) {
    var r = items[i].getBoundingClientRect();
    var lbl = items[i].querySelector('[class*="nameTag"]');
    result.push({
        index: i, label: lbl ? lbl.textContent.trim() : 'Componente '+(i+1),
        top: Math.round(r.top), height: Math.round(r.height),
        cx: Math.round(r.left + r.width/2), cy: Math.round(r.top + r.height/2)
    });
}
JSON.stringify(result)
"@
        $result = Invoke-JS -TabId $Tab -Expr $expr
        Write-Host $result
    }

    default {
        Write-Host @"
cdp_helper.ps1 — Chrome DevTools Protocol Helper

SUBCOMANDOS GENERALES:
  check                              Verifica conexion y lista pestanas
  navigate   --tab ID --url URL      Navega a una URL
  login      --tab ID --url URL --user admin --pass PASS  Login Drupal
  screenshot --tab ID --output PATH [--clip x,y,w,h] [--scale 2.0]  Captura
  find-field --tab ID --label TEXTO [--output PATH] [--scale 2.5]  Busca campo
  get-rect   --tab ID --selector CSS  Bounding box de un elemento
  scroll-to  --tab ID --selector CSS  Scroll al elemento
  click      --tab ID --x N --y N     Clic en coordenadas
  get-center --tab ID --selector CSS  Centro del elemento

SUBCOMANDOS PARAGRAPHS:
  list-paragraphs    --tab ID                        Lista todos los paragraphs
  list-paragraph-types --tab ID [--output PATH]      Lista bundles disponibles
  expand-paragraph   --tab ID --index N              Expande paragraph colapsado
  capture-paragraph  --tab ID --index N --output PATH [--scale 2.0]
  capture-paragraph-tree --tab ID --output BASE_PATH [--scale 1.5]

SUBCOMANDOS CANVAS:
  list-components    --tab ID                        Lista componentes Canvas
"@
    }
}
