"""Welcome page object — chainable Playwright tests for the main landing page."""
from playwright.sync_api import Page, expect
from tests.pages.base_page import BasePage


class WelcomePage(BasePage):
    URL = "/"

    def load(self):
        self.goto(self.URL)
        return self

    # ── Assertions ──────────────────────────────────────────────

    def assert_title_visible(self):
        """The app title is visible in the main content area."""
        self.assert_text_visible("股識", timeout=10000)
        return self

    def assert_lead1_visible(self):
        """The lead subtitle is visible."""
        self.assert_text_visible("認識一家公司，從這裡開始")
        return self

    def assert_search_bar_visible(self):
        """Search input box is present with correct placeholder."""
        search = self._page.query_selector("input[placeholder*='台積電']")
        assert search is not None, "Search input not found"
        assert search.is_visible(), "Search input not visible"
        return self

    def assert_search_above_welcome(self):
        """Search bar renders ABOVE the welcome subtitle."""
        search = self._page.query_selector("input[placeholder*='台積電']")
        subtitle = self._page.locator("text=認識一家公司，從這裡開始").first
        search_box = search.bounding_box()
        subtitle_box = subtitle.bounding_box()
        assert search_box["y"] < subtitle_box["y"], \
            f"Search (y={search_box['y']}) should be above subtitle (y={subtitle_box['y']})"
        return self

    def assert_sidebar_visible(self):
        """Sidebar is present and expanded."""
        sidebar = self._page.query_selector("[data-testid='stSidebar']")
        assert sidebar is not None, "Sidebar not found"
        assert sidebar.is_visible(), "Sidebar not visible"
        return self

    def assert_sidebar_has_item(self, label: str):
        """Check a sidebar navigation button exists."""
        btn = self._page.locator("button").filter(has_text=label).first
        assert btn.is_visible(), f"Sidebar item not visible: {label}"
        return self

    def assert_disclaimer_visible(self):
        """Disclaimer text is present in sidebar."""
        self.assert_text_visible("本工具僅供認識公司使用")
        return self

    def assert_hot_stocks_expander_visible(self):
        """Hot stocks expander is present."""
        self.assert_text_visible("熱門股票")
        return self

    def assert_hot_etfs_expander_visible(self):
        """Hot ETFs expander is present."""
        self.assert_text_visible("熱門 ETF")
        return self

    def assert_page_title_correct(self):
        """Browser tab title is '股識'."""
        expect(self._page).to_have_title("股識")
        return self

    # ── Navigation ──────────────────────────────────────────────

    def search(self, query: str):
        """Type a search query and press Enter, then return a StockPage."""
        search = self._page.query_selector("input[placeholder*='台積電']")
        assert search is not None, "Search input not found"
        search.fill(query)
        self._page.keyboard.press("Enter")
        self._page.wait_for_timeout(3000)
        from tests.pages.stock_page import StockPage
        return StockPage(self._page, self._base_url)

    def navigate_to_settings(self):
        """Click '設定' in sidebar."""
        self.click_sidebar_item("設定")
        from tests.pages.settings_page import SettingsPage
        return SettingsPage(self._page, self._base_url)
