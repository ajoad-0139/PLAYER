from playwright.sync_api import Page

from pages.base_page import BasePage


class BookDetailsPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.locator(".product_main h1")
        self.price = page.locator(".product_main .price_color")
        self.product_info = page.locator("table.table-striped")

    def get_book_title(self) -> str:
        return self.heading.inner_text()

    def get_price(self) -> str:
        return self.price.inner_text()

    def is_product_info_visible(self) -> bool:
        return self.product_info.is_visible()