from playwright.sync_api import Page


def access_page(page: Page, url: str):
    page.goto(url, wait_until="domcontentloaded")
    print(f"[NAVIGATION] Página acessada: {url}")
    print(f"[NAVIGATION] Título: {page.title()}")
