
import os
import pytest
import random
from config import settings
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.book_details_page import BookDetailsPage
from pages.login_page import LoginPage


@pytest.fixture
def home_page(page: Page) -> HomePage:
    home = HomePage(page)
    home.open_home()
    return home

@pytest.fixture
def book_details_page(page: Page) -> BookDetailsPage:
    return BookDetailsPage(page)


@pytest.fixture
def random_book_indexes() -> list[int]:
    indexes = random.sample(range(settings.BOOKS_PER_PAGE), settings.BOOKS_TO_SAMPLE)
    return indexes

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "ignore_https_errors": os.getenv("IGNORE_HTTPS_ERRORS") == "1",
    }