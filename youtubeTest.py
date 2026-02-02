from playwright.sync_api import sync_playwright

def tentar_click(locator, timeout_ms=300) -> bool:
    """
    Tenta esperar o locator ficar visível por um tempo curto e clicar.
    Retorna True se clicou, False se não apareceu nesse intervalo.
    """
    try:
        locator.wait_for(state="visible", timeout=timeout_ms)
        locator.click()
        return True
    except Exception:
        return False

with sync_playwright() as pw:
    navegador = pw.chromium.launch(headless=False)
    contexto = navegador.new_context()

    # Sem limite de tempo global (ações e navegação)
    contexto.set_default_timeout(0)
    contexto.set_default_navigation_timeout(0)

    pagina = contexto.new_page()

    pagina.goto("https://www.youtube.com/watch?v=-vjW4dHEvCs&list=OLAK5uy_kCgEwOlrnK0sUf-U4jfnw9XAM3XKvyU_k")

    # Observação importante:
    # get_by_label nem sempre é o melhor no YouTube.
    # Vou manter a ideia do texto, mas com role mais compatível:
    saiba_mais = pagina.get_by_role("link", name="Saiba mais").first
    veja_mais  = pagina.get_by_role("link", name="Veja mais").first

    clicou_anuncio = False

    # IF: se aparecer "Saiba mais" OU "Veja mais", clica no que aparecer primeiro
    while not clicou_anuncio:
        if tentar_click(saiba_mais, timeout_ms=300):
            clicou_anuncio = True
            break

        if tentar_click(veja_mais, timeout_ms=300):
            clicou_anuncio = True
            break

        pagina.wait_for_timeout(200)  # pequena pausa pra não consumir CPU

    # Só depois entra na lógica do botão "Pular"
    if clicou_anuncio:
        botao_pular = pagina.get_by_role("button", name="Pular").first

        # Espera "Pular" aparecer sem limite de tempo
        while True:
            if tentar_click(botao_pular, timeout_ms=300):
                break
            pagina.wait_for_timeout(200)

    pagina.wait_for_timeout(5000)
    # navegador.close()
