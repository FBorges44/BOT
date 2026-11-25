import json
import os
from pathlib import Path

from dotenv import load_dotenv
from playwright.sync_api import Page

from automation.preencher import preencher_laudo
from crawler.browser import Browser
from crawler.extractor import extract_elements, save_elements
from crawler.navigation import access_page


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


def carregar_dados():
    with open(PROJECT_ROOT / "data" / "dados_laudo.json", "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def validar_preenchimento(page: Page, dados: dict):
    resultados = {}
    for grupo in (dados.get("imovel", {}), dados.get("avaliacao", {})):
        for nome, valor in grupo.items():
            campo = page.locator(f'[name="{nome}"]')
            resultados[nome] = (
                campo.count() == 1
                and campo.first.input_value() == str(valor)
            )
    return resultados


def salvar_resultados(resultados):
    caminho = PROJECT_ROOT / "data" / "resultado_automacao.json"
    caminho.parent.mkdir(exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(resultados, arquivo, ensure_ascii=False, indent=2)


def main():
    dados = carregar_dados()
    url = os.getenv(
        "TARGET_URL",
        (PROJECT_ROOT / "formulario-teste.html").as_uri(),
    )
    headless = os.getenv("BROWSER_HEADLESS", "false").lower() == "true"
    navegador = Browser()

    try:
        page = navegador.start(headless=headless)
        access_page(page, url)

        elementos = extract_elements(page)
        save_elements(elementos)
        print(f"[EXTRACTOR] {len(elementos)} elementos identificados.")

        print("[CRAWLER] Iniciando preenchimento...")
        preenchimento = preencher_laudo(page, dados)
        validacao = validar_preenchimento(page, dados)

        logs_path = PROJECT_ROOT / "logs"
        logs_path.mkdir(exist_ok=True)
        page.screenshot(
            path=str(logs_path / "laudo_preenchido.png"),
            full_page=True,
        )
        sucesso = all(preenchimento.values()) and all(validacao.values())

        salvar_resultados({
            "preenchimento": preenchimento,
            "validacao": validacao,
            "sucesso": sucesso,
        })

        print("[CRAWLER] Processo concluído.")
        print(f"[CRAWLER] Sucesso: {sucesso}")
        if not headless:
            try:
                input("[CRAWLER] Revise o formulário no navegador e pressione Enter para fechar.")
            except EOFError:
                pass
        return sucesso
    finally:
        navegador.close()


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
