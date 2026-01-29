from playwright.sync_api import sync_playwright, expect

with sync_playwright() as pw:
    navegador = pw.chromium.launch(headless=False)
    contexto = navegador.new_context()
    import time
    # Abrir uma nova aba
    pagina = contexto.new_page()
    
    # Navegar até a página desejada
    pagina.goto("https://www.hashtagtreinamentos.com/")
    
    # pegar info da página
    print(pagina.title())
    
    # Selecionar um elemento na tela 
    # Isso pode funcionar por 2 formatos 
    # 1. Por ID
    # 2. Por XPath
    
    #pagina.locator("//input[@name='q']").fill("Teste de automação com Playwright")
    
    #pagina.locator('xpath = /html/body/main/section[1]/div[2]/a')
    
    # Utilizar a estrutura do get_by

    botao = pagina.get_by_role("link", name="Quero aprender").first
    
    # significa "eu espero que esse clique me gere uma nova pagina"
    with contexto.expect_page() as pagina2_info:
        botao.click()
    # pagina2 recebe a nova pagina aberta
    pagina2 = pagina2_info.value
        
    # Selecionar varios elementos
    links = pagina.get_by_role("link").all()
    for link in links:
        print(link.inner_text())
    
    # nova pagina em branco
    # pagina2 = contexto.new_page()
    
    # preencher dados em um campo
    pagina2.goto("https://www.hashtagtreinamentos.com/curso-python")
    pagina2.get_by_role("textbox", name="Seu primeiro nome").fill("Pedro")
    pagina2.get_by_role("textbox", name="Seu melhor e-mail").fill("menezes@gmail.com")
    pagina2.get_by_role("textbox", name="Seu WhatsApp com DDD").fill("5399072390")
    pagina2.get_by_role("button", name="Quero acessar as informações").click()
    
    # esperar um elemento aparecer na tela
    novo_botao = pagina2.get_by_role("link", name="quero aproveitar")
    expect(novo_botao).to_be_visible()
    novo_botao.click()
    
    time.sleep(5)
    
    navegador.close()