from playwright.sync_api import sync_playwright, expect

with sync_playwright() as pw:
    navegador = pw.chromium.launch(headless=False)
    contexto = navegador.new_context()
    
    import time
    # Abrir uma nova aba
    pagina = contexto.new_page()
    
    # Navegar até a página desejada
    pagina.goto("https://www.youtube.com/watch?v=-vjW4dHEvCs&list=OLAK5uy_kCgEwOlrnK0sUf-U4jfnw9XAM3XKvyU_k")
    
    
        # esperar um elemento aparecer na tela
    novo_botao = pagina.get_by_label("Saiba mais", exact=True)
    expect(novo_botao).to_be_visible(timeout=300_000)
    with contexto.expect_page() as pagina2_info:
        novo_botao.click()
    pagina2 = pagina2_info.value
    
    novo_botao2 = pagina.get_by_label("Veja mais", exact=True)
    expect(novo_botao2).to_be_visible(timeout=300_000)
    with contexto.expect_page() as pagina3_info:
        novo_botao2.click()
    pagina3 = pagina3_info.value
    
    
    #get_by_role("button", name="Pular", exact=True)
    #get_by_label("Saiba mais", exact=True)
    #get_by_role("link", name="Saiba mais This link opens in")
    
    time.sleep(5)

    #navegador.close()