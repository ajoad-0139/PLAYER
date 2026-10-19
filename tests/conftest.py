
import pytest
import random
from config import settings
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.book_details_page import BookDetailsPage


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