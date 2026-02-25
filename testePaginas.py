from playwright.sync_api import sync_playwright

urls = [
    "https://www.youtube.com/",
    "https://www.google.com/",
    "https://www.wikipedia.org/",
]

with sync_playwright() as pw:
    browser = pw.chromium.connect_over_cdp("http://localhost:9222")
    contexto = browser.contexts[0]  # contexto já existente do CDP

    # abre várias abas
    abas = []
    for url in urls:
        p = contexto.new_page()
        p.goto(url, wait_until="commit", timeout=30_000)
        abas.append(p)

    # traz a última para frente só pra você ver
    abas[-1].bring_to_front()

    input("Abas abertas. ENTER para fechar conexão...")
    browser.close()