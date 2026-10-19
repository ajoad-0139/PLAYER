# Books to Scrape: UI Automation Framework

## 1. Project Overview

UI automation framework built with Playwright and Pytest. It validates the [Books to Scrape](https://books.toscrape.com/index.html) website (homepage, book navigation, data consistency, broken links, product images and pagination) and the login flow of [Quotes to Scrape](https://quotes.toscrape.com/).

It runs locally, in Docker and in GitHub Actions, and produces pytest-html and Allure reports.

## 2. Features

- Page Object Model with a shared `BasePage`
- Pytest fixtures for page objects and random test data
- No hardcoded waits: only Playwright auto-waiting, `expect()` assertions and `wait_for_url`
- Screenshots, videos and traces retained on failure
- pytest-html (single file) and Allure reports
- Dockerfile based on the official Playwright image
- GitHub Actions pipeline on push and pull request, with uploaded artifacts
- Mobile device emulation through the `--device` option

## 3. Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Language |
| Playwright 1.64.0 | Browser automation |
| Pytest | Test runner |
| pytest-playwright | Playwright fixtures and failure artifacts |
| pytest-html | Single-file HTML report |
| allure-pytest | Allure results |
| Docker | Containerised execution |
| GitHub Actions | CI/CD |

## 4. Installation Guide

```bash
git clone https://github.com/ajoad-0139/PLAYER.git
cd PLAYER
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium        # on a fresh Linux machine: playwright install --with-deps chromium
```

## 5. Environment Setup

- Python 3.9 or newer
- Optional, to view Allure reports locally: Java 8 or newer and the Allure CLI (`npm install -g allure-commandline`)
- Optional, to run in a container: Docker
- Optional environment variables for the login test:

| Variable | Default |
|---|---|
| `QUOTES_USERNAME` | `admin` |
| `QUOTES_PASSWORD` | `admin` |

Quotes to Scrape accepts any non-empty credentials. All URLs and constants live in `config/settings.py`.

## 6. Running Tests

```bash
pytest                                            # all tests
pytest tests/test_homepage.py                     # one file
pytest -k login                                   # by keyword
IGNORE_HTTPS_ERRORS=1 pytest  --headed                                  # watch the browser
pytest --browser chromium --device "iPhone 13"    # mobile emulation
```

Report and artifact options are set in `pytest.ini`, so the same command works locally, in Docker and in CI.

### Run in Docker

```bash
docker build -t books-automation .

docker run --rm --ipc=host \
  -v "$(pwd)/reports:/app/reports" \
  -v "$(pwd)/allure-results:/app/allure-results" \
  -v "$(pwd)/test-results:/app/test-results" \
  books-automation
```

The first build downloads a large base image (about 1 GB), so it can take several minutes. Later builds use the cache. If the generated report files end up owned by root, add `--user "$(id -u):$(id -g)" -e HOME=/tmp` to the `docker run` command.

The `playwright` version in `requirements.txt` must match the tag in the Dockerfile's `FROM` line.

## 7. Project Structure

```
.
├── .github/workflows/playwright.yml   # CI pipeline
├── config/
│   └── settings.py                    # URLs, credentials, constants
├── pages/
│   ├── base_page.py                   # shared actions (open, title, url, back)
│   ├── home_page.py                   # listing, headings, images, links, pagination
│   ├── book_details_page.py           # book details
│   └── login_page.py                  # Quotes to Scrape login flow
├── tests/
│   ├── conftest.py                    # page object and random index fixtures
│   ├── test_homepage.py               # TC1
│   ├── test_book_navigation.py        # TC2
│   ├── test_data_consistency.py       # TC3
│   ├── test_broken_links.py           # TC4
│   ├── test_product_image.py          # TC5
│   └── test_login.py                  # TC6
├── pytest.ini                         # report and artifact options
├── requirements.txt
├── Dockerfile
└── .dockerignore
```

Generated folders (`reports/`, `allure-results/`, `allure-report/`, `test-results/`) are git-ignored.

## 8. Test Case Coverage

| TC | File | What it checks |
|---|---|---|
| 1 | `test_homepage.py` | URL, title, visible non-empty headings (h1 to h6), books section visible, at least one book |
| 2 | `test_book_navigation.py` | 5 random books open a details page whose H1 matches the selected title, product info is visible, navigation back works |
| 3 | `test_data_consistency.py` | Title and price match between homepage and details page for 5 random books |
| 4 | `test_broken_links.py` | Every unique homepage link returns HTTP 200 |
| 5 | `test_product_image.py` | Visibility, `src`, `alt` and `thumbnail` class on images across up to 5 paginated pages |
| 6 | `test_login.py` | Login on Quotes to Scrape succeeds and the Logout link is visible and enabled |

Total: 8 tests (3 + 1 + 1 + 1 + 1 + 1).

## 9. Report Generation Guide

Every `pytest` run writes:

| Output | Location |
|---|---|
| HTML report | `reports/report.html` |
| Allure raw results | `allure-results/` |
| Screenshots, videos, traces (failed tests only) | `test-results/` |

`allure-results/` is cleaned at the start of each run, so old results never mix with new ones.

## 10. HTML Report Guide

Open `reports/report.html` in any browser. The file is self-contained, so a double-click works. It lists every test with its status, duration and failure details.

## 11. Allure Report Guide

The `allure-pytest` plugin only writes raw results. Turning them into a report needs Java 8+ and the Allure CLI.

```bash
allure serve allure-results                               # build and open a temporary report
allure generate allure-results -o allure-report --clean   # build a static report
allure open allure-report                                 # open the static report
```

**Do not double-click `allure-report/index.html`.** Browsers block the report's data loading on `file://` pages and show a `500` or `NetworkError when attempting to fetch resource`. Use `allure open`, or, if Allure is not installed, a plain static server:

```bash
python3 -m http.server 8080 --directory allure-report
```

Then open http://localhost:8080.

## 12. GitHub Actions Setup

The workflow `.github/workflows/playwright.yml` runs on every push to `main` and on every pull request. It has two jobs:

1. **test**: checkout, set up Python, install dependencies, install Chromium, run `pytest`, generate the Allure report, upload artifacts.
2. **docker**: builds the Dockerfile to prove the image is valid.

Artifacts uploaded on every run (even when tests fail):

| Artifact | Content |
|---|---|
| `html-report` | `reports/report.html` |
| `allure-results` | Raw Allure results |
| `allure-report` | Generated Allure report |
| `test-results` | Screenshots, videos and traces (only exists when a test failed) |

To view them: open the run in the **Actions** tab, download the artifact (GitHub login required) and unzip it. The `html-report` artifact opens directly. The `allure-report` artifact must be served over HTTP as described in the Allure section. Artifacts are kept for 90 days by default.

No secrets or repository settings are needed. The workflow works on a fresh fork.

## 13. Design Decisions

- **Page Object Model:** selectors and actions live in page classes, tests only assert. A site change means editing one class.
- **Inheritance:** every page object extends `BasePage`, which holds the common actions.
- **Fixtures, not custom setup:** `pytest-playwright` provides the browser and page. `conftest.py` only builds page objects and the random book indexes.
- **Random books:** a fixture returns 5 distinct random indexes and the test loops over them. The indexes are printed in the output so a failure can be reproduced by hand.
- **Titles from the `title` attribute:** the visible link text on the homepage is truncated, so the full title is read from the attribute.
- **Broken-link test:** uses `page.request` (no extra library), collects all failures and asserts once at the end so one bad link does not hide the others.
- **Reporting in `pytest.ini`:** one command behaves the same locally, in Docker and in CI.
- **No hardcoded waits:** `grep -rn "sleep\|wait_for_timeout" tests pages` returns nothing.
- **Constants in one place:** `config/settings.py`, so tests contain no magic strings.

