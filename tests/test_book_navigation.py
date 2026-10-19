from playwright.sync_api import expect

from config import settings


def test_random_books_open_matching_details_page(home_page, book_details_page, random_book_indexes):
    for index in random_book_indexes:
        expected_title = home_page.get_book_title(index)

        home_page.open_book(index)

        expect(book_details_page.heading).to_have_text(expected_title)
        expect(book_details_page.product_info).to_be_visible()

        home_page.go_back()
        expect(home_page.books).to_have_count(settings.BOOKS_PER_PAGE)