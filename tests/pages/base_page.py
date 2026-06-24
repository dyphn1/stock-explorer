"""Base page object for chainable Playwright tests.

Usage:
    page = WelcomePage(browser_page, server_url)
    page.load()
    page.assert_title_visible()
    stock_page = page.search("2330")  # returns StockPage
    stock_page.assert_stock_id_visible()
"""

from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page, base_url: str):
        self._page = page
        self._base_url = base_url

    @property
    def page(self) -> Page:
        return self._page

    def goto(self, path: str = ""):
        self._page.goto(f"{self._base_url}{path}")
        self._page.wait_for_load_state("networkidle")
        self._page.wait_for_timeout(3000)
        return self

    def screenshot(self, path: str):
        self._page.screenshot(path=path, full_page=True)
        return self

    def wait(self, ms: int = 1000):
        self._page.wait_for_timeout(ms)
        return self

    def assert_no_raw_i18n_keys(self):
        i18n_key_prefixes = [
            'sidebar.', 'app.', 'page.', 'business_card.',
            'daily_market.', 'screener.', 'health.', 'moat.',
            'event_dashboard.', 'investment_memo.', 'notification_center.',
            'financial_wellness.', 'stock_screener.', 'case_study.',
            'comprehension_check.', 'academy.', 'debate_cards.',
            'compare_stories.', 'revenue_tree.', 'story_timeline.',
            'full_story_timeline.', 'daily_story.', 'first_visit_guide.',
            'case_study_library.', 'etf_section.', 'watchlist.',
            'group_structure.', 'peer_comparison.', 'financial_health.',
            'operation_checkup.', 'category_browser.', 'settings.',
            'sector_heatmap.', 'metric_education.', 'unit.',
            'status.', 'router_base.', 'helpers.',
            'study_log.', 'historical_pattern.', 'timeline_controls.',
            'key_takeaways.', 'error.',
        ]
        found = []
        for prefix in i18n_key_prefixes:
            elements = self._page.locator(f"text={prefix}").all()
            for el in elements:
                if el.is_visible():
                    text = (el.text_content() or "")[:100]
                    # Skip file paths (tracebacks contain "File \"..." patterns)
                    if 'File "' in text or '/src/' in text:
                        continue
                    found.append(f"'{prefix}' → '{text}'")
        assert not found, f"Raw i18n key prefixes found:\n" + "\n".join(found[:10])
        return self

    def assert_text_visible(self, text: str, timeout: int = 5000):
        self._page.locator(f"text={text}").first.wait_for(state="visible", timeout=timeout)
        return self

    def assert_element_exists(self, selector: str):
        assert self._page.query_selector(selector) is not None, f"Element not found: {selector}"
        return self

    def click_sidebar_item(self, label: str):
        btn = self._page.locator("button").filter(has_text=label).first
        btn.click()
        self._page.wait_for_timeout(2000)
        return self
