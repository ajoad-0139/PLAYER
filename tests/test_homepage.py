from playwright.sync_api import expect

from config import settings


def test_homepage_url_and_title(home_page):
    expect(home_page.page).to_have_url(settings.HOME_URL)
    expect(home_page.page).to_have_title(settings.HOME_TITLE)


def test_homepage_headings_are_visible_and_not_empty(home_page):
    headings = home_page.get_visible_headings()
    assert headings, "No visible headings found on the homepage"
    for heading in headings:
        expect(heading).to_be_visible()
        expect(heading).not_to_be_empty()
        assert heading.inner_text().strip(), "A visible heading has empty text"


def test_homepage_books_section_has_books(home_page):
    expect(home_page.books_section).to_be_visible()
    expect(home_page.books).not_to_have_count(0)