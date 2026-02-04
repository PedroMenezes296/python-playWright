# youtube_cdp.py
# Pré-requisito: Chrome já aberto com CDP em http://localhost:9222
# Ex.: chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\playwright-profile-youtube" --profile-directory="Default"

from playwright.sync_api import sync_playwright

VIDEO_URL = "https://www.youtube.com/watch?v=-vjW4dHEvCs&list=OLAK5uy_kCgEwOlrnK0sUf-U4jfnw9XAM3XKvyU_k"

def pegar_contexto_e_pagina(browser):
    # Em CDP geralmente já existe 1 contexto e pelo menos 1 aba
    contexto = browser.contexts[0] if browser.contexts else browser.new_context()
    pagina = contexto.pages[0] if contexto.pages else contexto.new_page()
    pagina.bring_to_front()
    return contexto, pagina

with sync_playwright() as pw:
    # Conecta no Chrome já aberto com CDP
    browser = pw.chromium.connect_over_cdp("http://localhost:9222")

    contexto, pagina = pegar_contexto_e_pagina(browser)

    print("URL inicial:", pagina.url)

    # Vai direto para o vídeo (commit evita travar esperando load completo)
    pagina.goto(VIDEO_URL, wait_until="commit", timeout=30_000)
    print("URL após goto:", pagina.url)

    input("Vídeo aberto. Pressione ENTER para encerrar a conexão...")

    # Fecha a conexão CDP (pode fechar o Chrome dependendo do caso)
    browser.close()
