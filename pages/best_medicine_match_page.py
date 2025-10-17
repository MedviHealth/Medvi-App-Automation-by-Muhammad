from playwright.sync_api import Page, expect
import logging, time
import allure
# pyright: ignore[reportMissingImports]
from utils.base_page import BasePage


class BestMedicineMatchPage(BasePage):
    """Handles 'Best Medicine Match' step interactions in the MEDVi Typeform flow."""

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
    @allure.step("Verify best medicine match heading")
    def verify_best_medicine_match_heading(self):
        """Verify the best medicine match heading is visible."""
        self._retry_action(self._verify_best_medicine_match_heading)
        self.log.info("✅ Best medicine match heading verified successfully")

    @allure.step("Select best medicine match option")
    def select_best_medicine_match(self, best_medicine_match_value: str):
        """Select a best medicine match option dynamically based on provided value."""
        self._retry_action(lambda: self._select_best_medicine_match(best_medicine_match_value))
        self.log.info(f"✅ Successfully selected: '{best_medicine_match_value.strip()}'")

    @allure.step("Select GLP-1 tablet or injection")
    def select_glp1_tablet_or_injection(self, glp1_tablet_or_injection_value: str):
        """Select a GLP-1 tablet or injection option dynamically based on provided value."""
        self._retry_action(lambda: self._select_glp1_tablet_or_injection(glp1_tablet_or_injection_value))
        self.log.info(f"✅ Successfully selected: '{glp1_tablet_or_injection_value.strip()}'")

    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button safely."""
        self._retry_action(self._click_next)
        self.log.info("➡️ Clicked 'Next' button")

    # ----------------------- Internal Methods -----------------------

    def _verify_best_medicine_match_heading(self):
        self.log.info("🔍 Verifying best medicine match heading...")
        heading = self.frame.locator("//span[text()='Which of these is most important to you?']")
        expect(heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

    def _select_best_medicine_match(self, best_medicine_match_value: str):
        clean_value = best_medicine_match_value.strip()
        safe_value = self.escape_xpath_text(clean_value)
        self.log.info(f"🩺 Selecting best medicine match: '{clean_value}'")
        option_locator = self.frame.locator(f"//div[normalize-space(text())={safe_value}]")
        option_locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        option_locator.scroll_into_view_if_needed()
        expect(option_locator).to_be_visible(timeout=5000)
        option_locator.click()

    def _select_glp1_tablet_or_injection(self, glp1_tablet_or_injection_value: str):
        self.log.info("🔍 Verifying GLP-1 tablet or injection heading...")
        heading2 = self.frame.locator(
            "//span[text()='GLP-1 is available as an injection or a dissolvable tablet. Which sounds best?']"
        )
        expect(heading2).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info("✅ GLP-1 tablet or injection heading verified successfully")

        clean_value = glp1_tablet_or_injection_value.strip()
        safe_value = self.escape_xpath_text(clean_value)
        self.log.info(f"💉 Selecting GLP-1 tablet or injection: '{clean_value}'")
        option_locator = self.frame.locator(f"//div[normalize-space(text())={safe_value}]")
        option_locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        option_locator.scroll_into_view_if_needed()
        expect(option_locator).to_be_visible(timeout=5000)
        option_locator.click()

    def _click_next(self):
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
