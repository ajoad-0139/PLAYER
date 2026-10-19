
import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage


@pytest.fixture
def home_page(page: Page) -> HomePage:
    home = HomePage(page)
    home.open_home()
    return home