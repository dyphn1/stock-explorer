"""Stock detail page object — chainable Playwright tests."""
from tests.pages.base_page import BasePage


class StockPage(BasePage):
    def assert_stock_id_visible(self, stock_id: str):
        self._page.locator(f"code").filter(has_text=stock_id).first.wait_for(state="visible", timeout=10000)
        return self

    def assert_stock_name_visible(self, name: str):
        self._page.locator(f"text={name}").first.wait_for(state="visible", timeout=10000)
        return self

    def assert_stock_header_visible(self):
        self.assert_element_exists("[data-testid='stHorizontalBlock']")
        return self

    def assert_metric_icons_visible(self):
        for icon in ["📊", "💰", "📈"]:
            assert self._page.locator(f"text={icon}").first.is_visible(), \
                f"Metric icon not visible: {icon}"
        return self
