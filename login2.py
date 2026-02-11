# youtube_cdp.py
# Pré-requisito: Chrome já aberto com CDP em http://localhost:9222

from playwright.sync_api import sync_playwright, expect

VIDEO_URL = "https://www.youtube.com/watch?v=-vjW4dHEvCs&list=OLAK5uy_kCgEwOlrnK0sUf-U4jfnw9XAM3XKvyU_k"


def pegar_contexto_e_pagina(browser):
    contexto = browser.contexts[0] if browser.contexts else browser.new_context()
    pagina = contexto.pages[0] if contexto.pages else contexto.new_page()
    pagina.bring_to_front()
    return contexto, pagina


def esperar_Locator(pagina, candidatos_por_acao, intervalo_ms=500):
    """
    candidatos_por_acao: dict[str, list[Locator]]
    Retorna (acao, locator_que_apareceu)
    """
    while True:
        for acao, lista_locators in candidatos_por_acao.items():
            for loc in lista_locators:
                try:
                    if loc.is_visible():
                        return acao, loc
                except:
                    pass
        pagina.wait_for_timeout(intervalo_ms)


def clicar_no_botao_pular(pular_locator):
    expect(pular_locator).to_be_visible(timeout=30_000)
    pular_locator.click(timeout=30_000)


def clicar_cta_abrindo_e_fechando(contexto, pagina_principal, locator_cta, botao_pular_youtube):
    with contexto.expect_page() as pagina_info:
        locator_cta.click(timeout=30_000)
    nova = pagina_info.value

    try:
        nova.close()
    except:
        pass

    # try:
    #     pagina_principal.locator("#movie_player video").click(timeout=2_000)
    # except:
    #     pass

    clicar_no_botao_pular(botao_pular_youtube)


with sync_playwright() as pw:
    browser = pw.chromium.connect_over_cdp("http://localhost:9222")
    contexto, pagina = pegar_contexto_e_pagina(browser)

    print("URL inicial:", pagina.url)
    pagina.goto(VIDEO_URL, wait_until="commit", timeout=30_000)

    botao_pular_youtube = pagina.get_by_role("button", name="Pular", exact=True)

    # =========================
    # CTAs + variações (iguais ao padrão do "veja")
    # =========================

    # SAIBA MAIS
    saiba_1 = pagina.get_by_role("link", name="Saiba mais This link opens in")
    saiba_2 = pagina.get_by_label("Saiba mais", exact=True)
    saiba_3 = pagina.get_by_role("link", name="Saiba mais This link")

    # VEJA MAIS (referência)
    veja_1 = pagina.get_by_label("Veja mais", exact=True)
    veja_2 = pagina.get_by_role("link", name="Veja mais This link opens in")
    veja_3 = pagina.get_by_role("link", name="Veja mais This link")
    veja_4 = pagina.get_by_role("link", name="Veja mais")

    # ACESSAR O SITE
    site_1 = pagina.get_by_role("link", name="Acessar o site This link opens in")
    site_2 = pagina.get_by_label("Acessar o site", exact=True)
    site_3 = pagina.get_by_role("link", name="Acessar o site This link")
    site_4 = pagina.get_by_role("link", name="Acessar o site")

    # INSCR(E)V- SE AGORA
    inscrevase_agora_1 = pagina.get_by_label("Inscreva-se agora", exact=True)
    inscrevase_agora_2 = pagina.get_by_role("link", name="Inscreva-se agora This link opens in")
    inscrevase_agora_3 = pagina.get_by_role("link", name="Inscreva-se agora This link")
    inscrevase_agora_4 = pagina.get_by_role("link", name="Inscreva-se agora")

    # INSCREVA-SE
    inscrevase_1 = pagina.get_by_label("Inscreva-se", exact=True)
    inscrevase_2 = pagina.get_by_role("link", name="Inscreva-se This link opens in")
    inscrevase_3 = pagina.get_by_role("link", name="Inscreva-se This link")
    inscrevase_4 = pagina.get_by_role("link", name="Inscreva-se")

    # INSCREVER-SE
    inscrever_se_1 = pagina.get_by_label("Inscrever-se", exact=True)
    inscrever_se_2 = pagina.get_by_role("link", name="Inscrever-se This link opens in")
    inscrever_se_3 = pagina.get_by_role("link", name="Inscrever-se This link")
    inscrever_se_4 = pagina.get_by_role("link", name="Inscrever-se")

    # SOLICITAR COTAÇÃO
    cotacao_1 = pagina.get_by_label("Solicitar cotação", exact=True)
    cotacao_2 = pagina.get_by_role("link", name="Solicitar cotação This link opens in")
    cotacao_3 = pagina.get_by_role("link", name="Solicitar cotação This link")
    cotacao_4 = pagina.get_by_role("link", name="Solicitar cotação")

    # CONTATO
    contato_1 = pagina.get_by_label("Contato", exact=True)
    contato_2 = pagina.get_by_role("link", name="Contato This link opens in")
    contato_3 = pagina.get_by_role("link", name="Contato This link")
    contato_4 = pagina.get_by_role("link", name="Contato")

    # DOWNLOAD
    download_1 = pagina.get_by_label("Download", exact=True)
    download_2 = pagina.get_by_role("link", name="Download This link opens in")
    download_3 = pagina.get_by_role("link", name="Download This link")
    download_4 = pagina.get_by_role("link", name="Download")

    # RESERVAR AGORA
    reservar_1 = pagina.get_by_label("Reservar agora", exact=True)
    reservar_2 = pagina.get_by_role("link", name="Reservar agora This link opens in")
    reservar_3 = pagina.get_by_role("link", name="Reservar agora This link")
    reservar_4 = pagina.get_by_role("link", name="Reservar agora")

    # COMPRAR AGORA
    comprar_1 = pagina.get_by_label("Comprar agora", exact=True)
    comprar_2 = pagina.get_by_role("link", name="Comprar agora This link opens in")
    comprar_3 = pagina.get_by_role("link", name="Comprar agora This link")
    comprar_4 = pagina.get_by_role("link", name="Comprar agora")
    
    # COMECE AGORA (novo)
    comece_agora_1 = pagina.get_by_label("Comece agora", exact=True)
    comece_agora_2 = pagina.get_by_role("link", name="Comece agora This link opens in")
    comece_agora_3 = pagina.get_by_role("link", name="Comece agora This link")
    comece_agora_4 = pagina.get_by_role("link", name="Comece agora")
    
    visitar_site_1 = pagina.get_by_label("Visitar site", exact=True)
    visitar_site_2 = pagina.get_by_role("link", name="Visitar site This link opens in")
    visitar_site_3 = pagina.get_by_role("link", name="Visitar site This link")
    visitar_site_4 = pagina.get_by_role("link", name="Visitar site")

    candidatos_por_acao = {
        "saiba": [saiba_1, saiba_2, saiba_3],
        "veja": [veja_1, veja_2, veja_3, veja_4],
        "acessar_site": [site_1, site_2, site_3, site_4],
        "inscreva_agora": [inscrevase_agora_1, inscrevase_agora_2, inscrevase_agora_3, inscrevase_agora_4],
        "inscreva": [inscrevase_1, inscrevase_2, inscrevase_3, inscrevase_4],
        "inscrever_se": [inscrever_se_1, inscrever_se_2, inscrever_se_3, inscrever_se_4],
        "cotacao": [cotacao_1, cotacao_2, cotacao_3, cotacao_4],
        "contato": [contato_1, contato_2, contato_3, contato_4],
        "download": [download_1, download_2, download_3, download_4],
        "reservar": [reservar_1, reservar_2, reservar_3, reservar_4],
        "comprar": [comprar_1, comprar_2, comprar_3, comprar_4],
        "comece": [comece_agora_1, comece_agora_2, comece_agora_3, comece_agora_4],
        "visitar_site": [visitar_site_1, visitar_site_2, visitar_site_3, visitar_site_4],
    }

    qual, locator_ativo = esperar_Locator(pagina, candidatos_por_acao, intervalo_ms=500)
    print("CTA encontrado:", qual)

    clicar_cta_abrindo_e_fechando(contexto, pagina, locator_ativo, botao_pular_youtube)

    browser.close()
