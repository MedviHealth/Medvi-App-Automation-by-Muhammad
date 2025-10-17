from playwright.sync_api import Page, expect
import logging, time
import allure
# pyright: ignore[reportMissingImports]
from utils.base_page import BasePage


class AverageRestingHeartRatePage(BasePage):
    """Handles the 'Average Resting Heart Rate' step in the MEDVi Typeform flow."""

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

    @allure.step("Verify average resting heart rate heading and image")
    def verify_average_resting_heart_rate_heading(self):
        """Verify average resting heart rate heading and image."""
        self._retry_action(self._verify_average_resting_heart_rate_heading)
        self.log.info("✅ Average resting heart rate verification completed")

    @allure.step("Select average resting heart rate option")
    def select_average_resting_heart_rate_option(self):
        """Select average resting heart rate option."""
        self._retry_action(self._select_average_resting_heart_rate_option)
        self.log.info("✅ Selected option: 60-100 beats per minute (Normal)")

    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button safely."""
        self._retry_action(self._click_next)
        self.log.info("➡️ Clicked 'Next' button")

    # ----------------------- Internal Methods -----------------------

    def _verify_average_resting_heart_rate_heading(self):
        self.log.info("💊 Verifying image displayed:")
        verify_image_displayed = self.frame.locator("img[src*='9c488a250fc7_0.png']")
        expect(verify_image_displayed).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info("✅ Image displayed verified successfully")

        self.log.info("💊 Verifying average resting heart rate heading:")
        is_visible = self.frame.locator("//span[text() ='How about your average resting heart rate?']").is_visible()
        if is_visible:
            self.log.info("✅ Average resting heart rate heading is visible on the page")
        else:
            self.log.warning("❌ Average resting heart rate heading is not visible")

    def _select_average_resting_heart_rate_option(self):
        self.log.info("💊 Selecting average resting heart rate option:")
        # Click Yes or No
        option_locator = self.frame.locator("//div[normalize-space(text())='60-100 beats per minute (Normal)']")
        option_locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        option_locator.scroll_into_view_if_needed()
        option_locator.click()

    def _click_next(self):
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
