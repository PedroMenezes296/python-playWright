# youtube_cdp.py
# Pré-requisito: Chrome já aberto com CDP em http://localhost:9222

import time
from playwright.sync_api import sync_playwright, expect

VIDEO_URL = "https://www.youtube.com/watch?v=J0J5CeJFGE0&list=RDJ0J5CeJFGE0&start_radio=1"

# URLs extras (abas à direita). Pode colocar outros vídeos do YouTube aqui também.
URLS_EXTRAS = [
    "https://www.youtube.com/watch?v=p4WMcOSrxPU&list=OLAK5uy_l4y3stt6SZ-NVWOVSwQ7aarB1wVkjM3r8",
    "https://www.youtube.com/watch?v=Il6yt7NMHtI&list=OLAK5uy_m9a_txVco3lLPXY6V9oOuede2fLtsndbg",
    "https://www.youtube.com/watch?v=sCIOUJvntDU&list=OLAK5uy_k4zaVLCeB0rxfL9iB-B7MNdCfjvTwksOA",
    "https://www.youtube.com/watch?v=fr3dM97MG9Q&list=OLAK5uy_k9o5mGL9zlv1IDxwXJZF9k1B80kLcDAS4",
    "https://www.youtube.com/watch?v=fhGGgriDXl4&list=OLAK5uy_kBNy6zs2ix_4tuZfTxhtKB-MToTfXtrd0"
]


def pegar_contexto_e_pagina(browser):
    contexto = browser.contexts[0] if browser.contexts else browser.new_context()
    pagina = contexto.pages[0] if contexto.pages else contexto.new_page()
    pagina.bring_to_front()
    return contexto, pagina


def pegar_video_id(pagina):
    try:
        return pagina.evaluate("() => new URL(location.href).searchParams.get('v') || ''")
    except:
        return ""


def esperar_trocar_video(pagina, video_id_atual, timeout_ms=500):
    try:
        pagina.wait_for_function(
            "(prev) => (new URL(location.href).searchParams.get('v') || '') !== prev",
            arg=video_id_atual,
            timeout=timeout_ms
        )
        return True
    except:
        return False


def esperar_Locator(pagina, candidatos_por_acao, intervalo_ms=500):
    while True:
        for acao, lista_locators in candidatos_por_acao.items():
            for loc in lista_locators:
                try:
                    if loc.is_visible():
                        return acao, loc
                except:
                    pass
        pagina.wait_for_timeout(intervalo_ms)


def garantir_video_tocando(pagina):
    video = pagina.locator("#movie_player video")
    tocando = False
    try:
        video.wait_for(state="attached", timeout=5000)
        tocando = video.evaluate("v => !v.paused && !v.ended && v.readyState > 2")
        if not tocando:
            video.click(timeout=5_000)
            tocando = video.evaluate("v => !v.paused && !v.ended && v.readyState > 2")
    except:
        pass
    return tocando


def clicar_no_botao_pular(pular_locator):
    try:
        expect(pular_locator).to_be_visible(timeout=5000)
        pular_locator.click(timeout=5000)
    except:
        pass


def clicar_cta_abrindo_e_fechando(contexto, pagina_principal, locator_cta, botao_pular_youtube):
    nova = None

    # tenta capturar nova aba (se abrir)
    try:
        with contexto.expect_page(timeout=5000) as pagina_info:
            locator_cta.click(timeout=5000)
        nova = pagina_info.value
    except:
        # pode abrir na mesma aba ou não abrir
        try:
            locator_cta.click(timeout=5000)
        except:
            pass

    # fecha a aba nova se existir
    if nova is not None:
        try:
            nova.wait_for_timeout(2000)
            nova.close()
        except:
            pass

    # garante o vídeo tocando
    garantir_video_tocando(pagina_principal)

    # tenta pular
    clicar_no_botao_pular(botao_pular_youtube)


with sync_playwright() as pw:
    browser = pw.chromium.connect_over_cdp("http://localhost:9222")
    contexto, pagina = pegar_contexto_e_pagina(browser)

    # 1) Primeira aba: YouTube no link do vídeo
    print("URL inicial:", pagina.url)
    pagina.goto(VIDEO_URL, wait_until="commit", timeout=30_000)

    # 2) Abre abas extras à direita (opcional)
    abas = [pagina]
    for url in URLS_EXTRAS:
        p = contexto.new_page()
        p.goto(url, wait_until="commit", timeout=30_000)
        abas.append(p)

    # garante que começamos na aba do vídeo
    indice_aba = 0
    pagina = abas[indice_aba]
    pagina.bring_to_front()

    while True:
        try:
            # só faz a lógica se estiver em página do YouTube (opcional, evita ruído em abas tipo Google)
            if "youtube.com" not in pagina.url:
                print("Aba atual não é YouTube. Pulando ciclo. URL:", pagina.url)
            else:

                try:
                    modal = pagina.get_by_text("Vídeo pausado. Quer continuar assistindo?")
                    expect(modal).to_be_visible(timeout=500)
                    pagina.get_by_role("button", name="Sim").click(timeout=500)
                except: 
                    pass
            
                video_id_antes = pegar_video_id(pagina)
                print("Aba:", indice_aba, "| VideoID:", video_id_antes, "| URL:", pagina.url)

                botao_pular_youtube = pagina.get_by_role("button", name="Pular", exact=True)

                # SAIBA MAIS
                saiba_1 = pagina.get_by_role("link", name="Saiba mais This link opens in")
                saiba_2 = pagina.get_by_label("Saiba mais", exact=True)
                saiba_3 = pagina.get_by_role("link", name="Saiba mais This link")

                # VEJA MAIS
                veja_1 = pagina.get_by_label("Veja mais", exact=True)
                veja_2 = pagina.get_by_role("link", name="Veja mais This link opens in")
                veja_3 = pagina.get_by_role("link", name="Veja mais This link")
                veja_4 = pagina.get_by_role("link", name="Veja mais")

                # ACESSAR O SITE
                site_1 = pagina.get_by_role("link", name="Acessar o site This link opens in")
                site_2 = pagina.get_by_label("Acessar o site", exact=True)
                site_3 = pagina.get_by_role("link", name="Acessar o site This link")
                site_4 = pagina.get_by_role("link", name="Acessar o site")

                site_var_1 = pagina.get_by_role("link", name="Acessar site This link opens in")
                site_var_2 = pagina.get_by_label("Acessar site", exact=True)
                site_var_3 = pagina.get_by_role("link", name="Acessar site This link")
                site_var_4 = pagina.get_by_role("link", name="Acessar site")

                site_visite_1 = pagina.get_by_role("link", name="Visite site This link opens in")
                site_visite_2 = pagina.get_by_label("Visite site", exact=True)
                site_visite_3 = pagina.get_by_role("link", name="Visite site This link")
                site_visite_4 = pagina.get_by_role("link", name="Visite site")

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

                # COMECE AGORA
                comece_agora_1 = pagina.get_by_label("Comece agora", exact=True)
                comece_agora_2 = pagina.get_by_role("link", name="Comece agora This link opens in")
                comece_agora_3 = pagina.get_by_role("link", name="Comece agora This link")
                comece_agora_4 = pagina.get_by_role("link", name="Comece agora")

                # VISITAR SITE
                visitar_site_1 = pagina.get_by_label("Visitar site", exact=True)
                visitar_site_2 = pagina.get_by_role("link", name="Visitar site This link opens in")
                visitar_site_3 = pagina.get_by_role("link", name="Visitar site This link")
                visitar_site_4 = pagina.get_by_role("link", name="Visitar site")

                candidatos_por_acao = {
                    "saiba": [saiba_1, saiba_2, saiba_3],
                    "veja": [veja_1, veja_2, veja_3, veja_4],
                    "acessar_o_site": [site_1, site_2, site_3, site_4],
                    "visite_o_site": [site_visite_1, site_visite_2, site_visite_3, site_visite_4],
                    "acessar_site": [site_var_1, site_var_2, site_var_3, site_var_4],
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
                if (qual is not None):
                    clicar_cta_abrindo_e_fechando(contexto, pagina, locator_ativo, botao_pular_youtube)
                else: 
                    pass
                trocou = esperar_trocar_video(pagina, video_id_antes, timeout_ms=500)
                if trocou:
                    print("Autoplay trocou para:", pagina.url)
                else:
                    print("Não trocou de vídeo (ou autoplay desligado).")

        except Exception as e:
            print("Erro no ciclo:", e)

        # Vai para a aba da direita (UI)
        pagina.keyboard.press("Control+Tab")

        # # Atualiza a referência do Playwright para a próxima aba
        indice_aba = (indice_aba + 1) % len(abas)
        pagina = abas[indice_aba]
        pagina.bring_to_front()

        time.sleep(2)