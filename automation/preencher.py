from playwright.sync_api import Page


def preencher_campo(page: Page, nome: str, valor: str):
    campo = page.locator(f'[name="{nome}"]')
    if campo.count() != 1:
        print(f"[AVISO] Campo não encontrado: {nome}")
        return False

    elemento = campo.first
    if not elemento.is_visible() or not elemento.is_enabled():
        print(f"[AVISO] Campo indisponível: {nome}")
        return False

    tag = elemento.evaluate("(el) => el.tagName.toLowerCase()")
    try:
        if tag == "select":
            elemento.select_option(label=str(valor))
        elif tag in ("input", "textarea"):
            elemento.fill(str(valor))
        else:
            print(f"[AVISO] Tipo não suportado: {nome}")
            return False
        print(f"[OK] Preenchido: {nome}")
        return True
    except Exception as error:
        print(f"[ERRO] Falha ao preencher {nome}: {error}")
        return False


def preencher_laudo(page: Page, dados: dict):
    resultados = {}
    for grupo in (dados.get("imovel", {}), dados.get("avaliacao", {})):
        for nome, valor in grupo.items():
            resultados[nome] = preencher_campo(page, nome, valor)
    return resultados
