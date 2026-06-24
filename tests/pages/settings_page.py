"""Settings page object — stub for future use."""
from tests.pages.base_page import BasePage


class SettingsPage(BasePage):
    def assert_loaded(self):
        self.assert_element_exists("[data-testid='stAppViewContainer']")
        return self
