import re
from config import settings
from playwright.sync_api import Locator, expect

def is_valid_image(image: Locator) :
    expect(image).to_be_visible()
    expect(image).to_have_attribute("src", re.compile(r".+"))
    expect(image).to_have_attribute("alt", re.compile(r".+"))
    expect(image).to_have_class(re.compile(r"\bthumbnail\b"))


def test_product_images_on_up_to_five_pages(home_page):
    pages_checked = 0

    for page_number in range(1, settings.MAX_PAGES + 1):
        images = home_page.get_images()
        assert images, f"No product images found on page {page_number}"
        for image in images:
            is_valid_image(image)
        pages_checked += 1

        if page_number == settings.MAX_PAGES or not home_page.has_next_page():
            break
        home_page.go_to_next_page()
        expect(home_page.page).to_have_url(re.compile(rf"page-{page_number + 1}\.html"))

    assert pages_checked == settings.MAX_PAGES, "Pagination ended earlier than expected"