from playwright.sync_api import Locator, Page

from config import settings
from pages.base import BasePage



class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.books_section = page.locator("ol.row")
        self.books = page.locator("article.product_pod")
        self.headings = page.locator("h1, h2, h3, h4, h5, h6")

    def open_home(self) -> None:
        self.open(settings.HOME_URL)

    def get_visible_headings(self) -> list[Locator]:
        visible_headings = []
        for heading in self.headings.all():
            if heading.is_visible():
                visible_headings.append(heading)

        return visible_headings