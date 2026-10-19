from playwright.sync_api import expect

from config import settings


def test_homepage_data_matches_details_page(home_page, book_details_page, random_book_indexes):
    for index in random_book_indexes:
        home_title = home_page.get_book_title(index)
        home_price = home_page.get_book_price(index)

        home_page.open_book(index)
        expect(book_details_page.heading).to_be_visible()

        assert book_details_page.get_book_title() == home_title, f"Title missmatch for book {index}"
        assert book_details_page.get_price() == home_price, f"Price missmatch for book {index}"

        home_page.go_back()
        expect(home_page.books).to_have_count(settings.BOOKS_PER_PAGE)