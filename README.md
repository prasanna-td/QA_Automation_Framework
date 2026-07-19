# QA Automation Framework — E-commerce UI + API Testing

A Python test automation framework combining **UI automation (Playwright + Page Object Model)**
and **API automation (requests + Pytest)**, built to demonstrate end-to-end automation
engineering skills: framework design, data-driven testing, logging, reporting, and CI integration.

- **UI under test:** [saucedemo.com](https://www.saucedemo.com) — login, inventory, cart, checkout
- **API under test:** [fakestoreapi.com](https://fakestoreapi.com) — products, carts

## Architecture

```
qa-automation-framework/
├── pages/                  # Page Object Model classes (one per screen)
│   ├── base_page.py        # Shared Playwright actions (click, fill, screenshot...)
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── ui/                 # Playwright UI test suites
│   └── api/                # REST API test suites
├── utils/
│   ├── config_reader.py    # Loads config/config.yaml
│   └── logger.py           # Central logger -> console + reports/logs/
├── config/
│   └── config.yaml         # Base URLs, browser, timeouts, log level
├── test_data/
│   └── users.json          # Data-driven login test data
├── conftest.py             # Pytest fixtures: browser/page lifecycle, screenshot-on-fail
├── pytest.ini              # Markers, HTML report config
├── Jenkinsfile             # CI pipeline: install -> smoke -> full regression -> publish report
└── requirements.txt
```

## Why it's built this way

| Resume skill | Where it shows up |
|---|---|
| Automation Framework Development | Layered structure: pages / tests / utils / config |
| Page Object Model (POM) | `pages/` — each screen is a class, tests never touch raw selectors |
| Selenium/Playwright | Playwright drives the browser via fixtures in `conftest.py` |
| Pytest | All tests, markers (`smoke`, `regression`), fixtures, parametrized data |
| REST API Testing / API Validation | `tests/api/` — schema, status code, negative, and timing checks |
| Regression / Smoke / Functional Testing | Marked explicitly with `@pytest.mark.smoke` / `@pytest.mark.regression` |
| Log Parsing / Automated Reporting | `utils/logger.py` + `pytest-html` report in `reports/report.html` |
| Defect Evidence | Automatic screenshot-on-failure via `pytest_runtest_makereport` hook |
| Git / Jenkins | `.gitignore` + `Jenkinsfile` (checkout → install → smoke → regression → publish) |
| Requirement-Based / Test Case Design | Each test file maps to one feature/user flow, docstring states intent |

## Setup

```bash
git clone <your-repo-url>
cd qa-automation-framework
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
playwright install               # downloads browser binaries
```

## Running tests

```bash
# Everything
pytest

# Only smoke tests (fast sanity check)
pytest -m smoke

# Only UI or only API
pytest -m ui
pytest -m api

# Parallel execution
pytest -n auto
```

After a run, open `reports/report.html` in a browser for the full report
(pass/fail counts, durations, embedded failure screenshots).
Logs are in `reports/logs/run_<date>.log`.

## CI/CD

The included `Jenkinsfile` defines a pipeline that:
1. Checks out the repo
2. Creates a virtualenv and installs dependencies + Playwright browsers
3. Runs the smoke suite first (fail fast)
4. Runs the full UI + API regression suite in parallel
5. Publishes the HTML report and archives it as a build artifact

Point a Jenkins "Pipeline" job at this repo and it will pick up the `Jenkinsfile` automatically.

## Roadmap — building this out over 1–2 weeks

**Day 1–2: Get it running locally**
- Clone, install, run `pytest -m smoke` and confirm the login tests pass.
- Read through `pages/` and `tests/ui/test_login.py` until the POM pattern feels natural.

**Day 3–4: Extend UI coverage**
- Add a Page Object for the product **details** page and a test for "add to cart from details page."
- Add a test for **removing an item from the cart**.
- Add a negative test: try to checkout with empty first name / last name / zip and assert the error message.

**Day 5–6: Extend API coverage**
- Add tests for the `/users` endpoint (get all, get by id, create, login).
- Add a negative test for creating a product with missing required fields.
- Add JSON schema validation using the `jsonschema` library instead of manual field checks.

**Day 7–8: Reporting & CI**
- Set up a free Jenkins instance locally (or use GitHub Actions instead — I can help you convert
  the `Jenkinsfile` into a `.github/workflows/ci.yml` if you'd rather use GitHub Actions).
- Get the pipeline running on every push and confirm the HTML report gets archived.

**Day 9–10: Polish for the resume**
- Push to a public GitHub repo with a clean commit history (not one giant commit).
- Add badges to the README (build status, Python version).
- Record a 1–2 minute screen recording of a test run + HTML report for your LinkedIn/portfolio.

**Day 11–14 (stretch): Nice-to-haves**
- Swap `pytest-html` for **Allure** reporting (more resume-recognizable).
- Add a Dockerfile so the whole suite runs in a container.
- Add a GitHub Actions matrix to run against chromium, firefox, and webkit.

## Suggested resume bullets once this is live on GitHub

- Designed and built a Python test automation framework combining Playwright UI automation
  (Page Object Model) with REST API testing, covering smoke and regression suites.
- Implemented data-driven test execution, centralized logging, and automatic screenshot
  capture on failure to support defect evidence and root cause analysis.
- Integrated Jenkins CI pipeline to execute smoke and regression suites on every commit and
  publish HTML test reports as build artifacts.
- Structured API test suite validating schema, status codes, and negative scenarios (invalid
  IDs, missing fields) against a REST API using Python and Pytest.
