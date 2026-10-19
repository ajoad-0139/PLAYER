from config import settings


def test_all_homepage_links_return_200(home_page):
    urls = home_page.get_all_links()  
    assert urls, "No links found on the homepage"

    failures = []
    for url in urls:
        response = home_page.page.request.get(url)
        if response.status != settings.HTTP_OK:
            failures.append(urls)
        assert not failures 