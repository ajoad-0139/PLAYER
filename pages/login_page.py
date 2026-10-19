from playwright.sync_api import Page, Response

from config import settings
from pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.login_link = page.get_by_role("link", name="Login")
        self.logout_link = page.get_by_role("link", name="Logout")
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.submit_button = page.locator("input[type='submit']")

    def open_quotes_home(self):
        self.open(settings.QUOTES_BASE_URL)

    def click_login_link(self):
        self.login_link.click()
        self.page.wait_for_url(settings.QUOTES_LOGIN_URL)

    def login(self, username: str, password: str) -> Response:
        self.username_input.press_sequentially(username)
        self.password_input.press_sequentially(password)
        with self.page.expect_response(
            lambda response: (
                response.url == settings.QUOTES_LOGIN_URL
                and response.request.method == "POST"
            )
        ) as response_info:
            self.submit_button.click()

        return response_info.value