from playwright.sync_api import Page, expect
import logging, time
import allure
# pyright: ignore[reportMissingImports]
from utils.base_page import BasePage


class TakenMedicationPage(BasePage):
    """Handles 'Taken Medication' step interactions in the MEDVi Typeform flow."""

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

    @allure.step("Select taken medication option")
    def select_taken_medication(self, taken_medication_value: str):
        """Select a 'taken medication' option dynamically and verify its border color."""
        self._retry_action(lambda: self._select_taken_medication(taken_medication_value))
        self.log.info(f"✅ Successfully selected and verified: '{taken_medication_value.strip()}'")

    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button safely."""
        self._retry_action(self._click_next)
        self.log.info("➡️ Clicked 'Next' button")

    # ----------------------- Internal Methods -----------------------

    def _select_taken_medication(self, taken_medication_value: str):
        clean_value = taken_medication_value.strip()
        self.log.info(f"💊 Selecting taken medication: '{clean_value}'")

        # Build safe XPath for text with quotes
        safe_value = self.escape_xpath_text(clean_value)
        option_locator = self.frame.locator(f"xpath=//div[normalize-space(text())={safe_value}]")

        # Wait for and click the main option
        option_locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        option_locator.scroll_into_view_if_needed()
        expect(option_locator).to_be_visible(timeout=5000)
        option_locator.click()
        self.log.info(f"✅ Option clicked: '{clean_value}'")

        # Locate the radio or highlight span and get computed border color
        radio = self.frame.locator(
            f"xpath=//div[normalize-space(text())={safe_value}]/../../preceding-sibling::span"
        )
        border_color = radio.evaluate("el => getComputedStyle(el).borderColor")
        self.log.info(f"🎨 Detected border color: {border_color}")

        # ✅ Corrected: compare as string, not with expect()
        assert border_color == "rgb(198, 166, 115)", (
            f"❌ Border color mismatch for '{clean_value}': {border_color}"
        )

    def _click_next(self):
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
