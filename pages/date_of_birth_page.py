import logging, time
import allure
from playwright.sync_api import Page, expect
# pyright: ignore[reportMissingImports]
from utils.base_page import BasePage


class DateOfBirthPage(BasePage):
    """Handles the 'Date of Birth' step in the MEDVi Typeform flow."""

    def __init__(self, page: Page):
        super().__init__(page)

    # ----------------------- Helpers -----------------------

    def _retry_action(self, func, retries=3, delay=2):
        """Retry a flaky action several times before giving up."""
        for attempt in range(1, retries + 1):
            try:
                return func()
            except Exception as e:
                if attempt < retries:
                    self.log.warning(f"🔁 Attempt {attempt}/{retries} failed: {e}. Retrying in {delay}s…")
                    time.sleep(delay)
                else:
                    self.log.error(f"❌ All {retries} attempts failed: {e}")
                    raise

    # ---------------------- Actions ---------------------- #

    @allure.step("Verify date of birth heading displayed")
    def verify_date_of_birth_heading_displayed(self):
        """Verify the date of birth heading displayed."""
        self._retry_action(self._verify_date_of_birth_heading_displayed)
        self.log.info("✅ Date of birth heading displayed verified successfully")

    @allure.step("Select day")
    def select_day(self, value: str):
        """Select day value."""
        self._retry_action(lambda: self._select_dropdown(2, value))
        self.log.info(f"✅ Selected day: {value}")

    @allure.step("Select month")
    def select_month(self, value: str):
        """Select month value."""
        self._retry_action(lambda: self._select_dropdown(1, value))
        self.log.info(f"✅ Selected month: {value}")

    @allure.step("Fill year")
    def add_year(self, value: str):
        """Fill year value."""
        self._retry_action(lambda: self._fill_year(value))
        self.log.info(f"✅ Filled year: {value}")

    @allure.step("Click 'Next' button on date of birth page")
    def hit_next_button(self):
        """Click the 'Next' button safely."""
        self._retry_action(self._click_next)
        self.log.info("➡️ Clicked 'Next' button")

    # ----------------------- Internal Methods -----------------------

    def _verify_date_of_birth_heading_displayed(self):
        self.log.info("🔍 Verifying date of birth heading displayed...")
        heading = self.frame.locator("//span[text() ='What is your date of birth?']")
        label_month = self.frame.locator("//h3[text() ='Month']")
        label_day = self.frame.locator("//h3[text() ='Day']")
        label_year = self.frame.locator("//h3[text() ='Year']")
        expect(label_month).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        expect(label_day).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        expect(label_year).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        expect(heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

    def _select_dropdown(self, position: int, value: str):
        dropdown = self.frame.locator(f"(//div[@data-cy='dropdown-component'])[{position}]//input")
        dropdown.wait_for(state="visible", timeout=10000)
        dropdown.click()
        dropdown.fill(value)
        self.page.keyboard.press("Enter")

    def _fill_year(self, value: str):
        year_input = self.frame.locator("(//input[@data-cy='input-component'])[1]")
        year_input.wait_for(state="visible", timeout=10000)
        year_input.fill(value)
        expect(year_input).to_have_value(value)

    def _click_next(self):
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
