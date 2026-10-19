from playwright.sync_api import Page


class BasePage:

    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded")

    def get_title(self) -> str:
        return self.page.title()

    def get_url(self) -> str:
        return self.page.url

    def go_back(self) -> None:
        self.page.go_back(wait_until="domcontentloaded")