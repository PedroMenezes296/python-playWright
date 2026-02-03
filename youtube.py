from numpy import info
from playwright.sync_api import sync_playwright, expect

def esperar_saiba_ou_veja(pagina, saiba_locator, veja_locator, acesseSite_locator, intervalo_ms=200):
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
    pular_locator.click().timeout(0)


with sync_playwright() as pw:
    navegador = pw.chromium.launch(headless=False)
    contexto = navegador.new_context()
    
    contexto.set_default_timeout(0)
    contexto.set_default_navigation_timeout(0)
    
    import time
    # Abrir uma nova aba
    pagina = contexto.new_page()
    
    # Navegar até a página desejada
    pagina.goto("https://www.youtube.com/watch?v=-vjW4dHEvCs&list=OLAK5uy_kCgEwOlrnK0sUf-U4jfnw9XAM3XKvyU_k")
    
    
        # definindo os botoes
    botao_vejamais_anuncio = pagina.get_by_label("Veja mais", exact=True)
    botao_saibaMais_anuncio = pagina.get_by_label("Saiba mais", exact=True)
    botao_acessar_site_anuncio = pagina.get_by_role("link", name="Acessar o site This link")
    botao_pular_youtube = pagina.get_by_role("button", name="Pular", exact=True)
    
    
    qual = esperar_saiba_ou_veja(pagina, botao_saibaMais_anuncio, botao_vejamais_anuncio, botao_acessar_site_anuncio)

    if qual == "saiba":
    # clica no saiba mais
        with contexto.expect_page() as pagina2_info:
            botao_saibaMais_anuncio.click()
        pagina2 = pagina2_info.value
        pagina2.close()
        pagina.locator("#movie_player video").click()  # volta o foco para o video
        clicar_no_botao_pular(botao_pular_youtube)
    elif qual == "acessar_site":
        with contexto.expect_page() as pagina4_info:
            botao_acessar_site_anuncio.click()
        pagina4 = pagina4_info.value
        pagina4.close()
        pagina.locator("#movie_player video").click()  # volta o foco para o video
        clicar_no_botao_pular(botao_pular_youtube)
    else:
    # clica no veja mais
        with contexto.expect_page() as pagina3_info:
            botao_vejamais_anuncio.click()
        pagina3 = pagina3_info.value
        pagina3.close()
        pagina.locator("#movie_player video").click()  # volta o foco para o video
        clicar_no_botao_pular(botao_pular_youtube)
            
    
    # expect(botao_saibaMais_anuncio or botao_vejamais_anuncio).to_be_visible()
    # with contexto.expect_page() as pagina2_info:
    #     botao_saibaMais_anuncio.click()
    # pagina2 = pagina2_info.value
    

    # expect(botao_vejamais_anuncio).to_be_visible()
    # with contexto.expect_page() as pagina3_info:
    #     botao_vejamais_anuncio.click()
    # pagina3 = pagina3_info.value
    
    # botao_pular_youtube = pagina3.get_by_role("button", name="Pular", exact=True)
    # expect(botao_pular_youtube).to_be_visible()
    # botao_pular_youtube.click()
    
    
    #get_by_role("button", name="Pular", exact=True)
    #get_by_label("Saiba mais", exact=True)
    #get_by_role("link", name="Saiba mais This link opens in")
    
    time.sleep(5)

    navegador.close()