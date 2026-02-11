# youtube_cdp.py
# Pré-requisito: Chrome já aberto com CDP em http://localhost:9222
# Ex.: chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\playwright-profile-youtube" --profile-directory="Default"

from playwright.sync_api import sync_playwright,expect


VIDEO_URL = "https://www.youtube.com/watch?v=-vjW4dHEvCs&list=OLAK5uy_kCgEwOlrnK0sUf-U4jfnw9XAM3XKvyU_k"

def pegar_contexto_e_pagina(browser):
    # Em CDP geralmente já existe 1 contexto e pelo menos 1 aba
    contexto = browser.contexts[0] if browser.contexts else browser.new_context()
    pagina = contexto.pages[0] if contexto.pages else contexto.new_page()
    pagina.bring_to_front()
    return contexto, pagina

def esperar_Locator(pagina, saiba_locator, veja_locator, acesseSite_locator):
    intervalo_ms = 500
    while True:
        if saiba_locator.is_visible():
            return "saiba"
        if veja_locator.is_visible():
            return "veja"
        if acesseSite_locator.is_visible():
            return "acessar_site"
        pagina.wait_for_timeout(intervalo_ms)

def clicar_no_botao_pular(pular_locator):
    expect(pular_locator).to_be_visible()
    pular_locator.click(timeout=30_000)

    
    
with sync_playwright() as pw:
    # Conecta no Chrome já aberto com CDP
    browser = pw.chromium.connect_over_cdp("http://localhost:9222")

    contexto, pagina = pegar_contexto_e_pagina(browser)

    print("URL inicial:", pagina.url)

    # Vai direto para o vídeo (commit evita travar esperando load completo)
    pagina.goto(VIDEO_URL, wait_until="commit", timeout=30_000)

    #get_by_role("link", name="Saiba mais This link opens in")
    botao_vejamais_anuncio = pagina.get_by_label("Veja mais", exact=True)
    botao_saibaMais_anuncio = pagina.get_by_label("Saiba mais", exact=True)
    botao_acessar_site_anuncio = pagina.get_by_role("link", name="Acessar o site This link")
    botao_pular_youtube = pagina.get_by_role("button", name="Pular", exact=True)
    botao_inscrever_se = pagina.get_by_role("link", name="Inscrever-se This link opens")
    botao_teste_ja = pagina.get_by_role("link", name="Teste já This link opens in")

    qual = esperar_Locator(pagina, botao_saibaMais_anuncio, botao_vejamais_anuncio, botao_acessar_site_anuncio)

    if qual == "saiba":
    # clica no saiba mais
        with contexto.expect_page() as pagina2_info:
            botao_saibaMais_anuncio.click()
        pagina2 = pagina2_info.value
        pagina2.close()
        pagina.locator("#movie_player video").click()  # volta o foco para o video
        clicar_no_botao_pular(botao_pular_youtube)
    elif qual == "acessar_site":
        with contexto.expect_page() as pagina2_info:
            botao_acessar_site_anuncio.click()
        pagina2 = pagina2_info.value
        pagina2.close()
        pagina.locator("#movie_player video").click()  # volta o foco para o video
        clicar_no_botao_pular(botao_pular_youtube)
    elif qual == "veja":
    # clica no veja mais
        with contexto.expect_page() as pagina2_info:
            botao_vejamais_anuncio.click()
        pagina2 = pagina2_info.value
        pagina2.close()
        pagina.locator("#movie_player video").click()  # volta o foco para o video
        clicar_no_botao_pular(botao_pular_youtube)
    elif qual == "inscrever_se":
        with contexto.expect_page() as pagina2_info:
            botao_inscrever_se.click()
        pagina2 = pagina2_info.value
        pagina2.close()
        pagina.locator("#movie_player video").click()  # volta o foco para o video
        clicar_no_botao_pular(botao_pular_youtube)
    elif qual == "teste_ja":
        with contexto.expect_page() as pagina2_info:
            botao_teste_ja.click()
        pagina2 = pagina2_info.value
        pagina2.close()
        pagina.locator("#movie_player video").click()  # volta o foco para o video
        clicar_no_botao_pular(botao_pular_youtube)
    else:
        print("Nenhum anúncio encontrado. Continuando o vídeo normalmente.")
        clicar_no_botao_pular(botao_pular_youtube)


    # Fecha a conexão CDP (pode fechar o Chrome dependendo do caso)
    browser.close()
