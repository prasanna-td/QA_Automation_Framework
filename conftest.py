"""
conftest.py
Shared pytest fixtures for the whole framework:
 - browser/page lifecycle (Playwright)
 - automatic screenshot-on-failure for UI tests
 - config access
"""

import os
import json
import pytest
from playwright.sync_api import sync_playwright

from utils.config_reader import get_ui_config
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="session")
def ui_config():
    return get_ui_config()


@pytest.fixture(scope="function")
def page(ui_config):
    """
    Provides a fresh Playwright page per test function.
    Browser/context are function-scoped for full test isolation,
    matching how independent regression cases should not leak state.
    """
    with sync_playwright() as p:
        browser_type = getattr(p, ui_config.get("browser", "chromium"))
        browser = browser_type.launch(headless=ui_config.get("headless", False))
        context = browser.new_context()
        pg = context.new_page()
        pg.set_default_timeout(ui_config.get("timeout", 10000))

        yield pg

        context.close()
        browser.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Captures a screenshot automatically when a UI test fails,
    and attaches the path to the pytest-html report.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page_fixture = item.funcargs.get("page")
        if page_fixture is not None:
            os.makedirs("reports/screenshots", exist_ok=True)
            screenshot_path = f"reports/screenshots/{item.name}.png"
            try:
                page_fixture.screenshot(path=screenshot_path)
                logger.error(f"Test failed: {item.name}. Screenshot: {screenshot_path}")
            except Exception as e:
                logger.error(f"Could not capture failure screenshot: {e}")


@pytest.fixture(scope="session")
def user_data():
    with open("test_data/users.json") as f:
        return json.load(f)
