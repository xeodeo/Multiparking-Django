
$params = @'{"documentId": "1lGUt6SRZZK9R8ir3hj5Mjj37xEFj5LNvKDpPusvEb-4"}'@
$body = Get-Content -Raw -Path 'doc_batch_000.json' | ConvertFrom-Json | ConvertTo-Json -Depth 50 -Compress
gws docs documents batchUpdate --params $params --json $body
