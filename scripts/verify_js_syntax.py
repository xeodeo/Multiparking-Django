def verify_braces(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract script block (roughly)
    start = content.find('{% block extra_js %}')
    end = content.find('{% endblock %}', start)
    
    if start == -1 or end == -1:
        print("[FAIL] Could not find extra_js block.")
        return

    script_content = content[start:end]
    
    # Count braces
    open_braces = script_content.count('{')
    close_braces = script_content.count('}')
    
    # We expect some diff due to {{ }} django tags having 2 braces.
    # But let's look at net balance of script logic.
    # It's hard to parse perfectly without a lexer, but let's check basic nesting.
    # Actually, JS structure check:
    
    print(f"Block Content (last 200 chars):\n{script_content[-200:]}")
    
    if "data: {{ ingresos_data|safe }}" in script_content:
        print("[OK] Found correct django tag format.")
    else:
        print("[FAIL] Did not find correct django tag format.")

    # Check for the bad pattern
    if "data: {{ ingresos_data| safe }\n" in script_content:
         print("[FAIL] Found broken pattern from before.")
    else:
         print("[OK] Broken pattern not found.")

verify_braces('c:/Users/xeodeo/Desktop/Gemini - copia/templates/admin_panel/dashboard.html')
