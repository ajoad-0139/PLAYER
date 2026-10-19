from playwright.sync_api import expect

from config import settings


def test_login_displays_logout_link(login_page):
    login_page.open_quotes_home()
    expect(login_page.page).to_have_title(settings.QUOTES_HOME_TITLE)
    expect(login_page.login_link).to_be_visible()

    login_page.click_login_link()
    expect(login_page.username_input).to_be_visible()
    expect(login_page.password_input).to_be_visible()

    response = login_page.login(settings.QUOTES_USERNAME, settings.QUOTES_PASSWORD)
    assert response.status < 400, f"Login request failed with status {response.status}"

    expect(login_page.logout_link).to_be_visible()
    expect(login_page.logout_link).to_be_enabled()