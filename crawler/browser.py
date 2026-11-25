from playwright.sync_api import sync_playwright


class Browser:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self, headless=False):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        print("[BROWSER] Navegador iniciado.")
        return self.page

    def close(self):
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
