from playwright.sync_api import Page, expect
import logging, time
import allure
# pyright: ignore[reportMissingImports]
from utils.base_page import BasePage


class BodyChangingImgPage(BasePage):
    """Handles the 'Body Changing Image' step in the MEDVi Typeform flow."""

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

    @allure.step("Verify body changing img heading and image")
    def verify_body_changing_img_heading(self):
        """Verify body changing image heading and image."""
        self._retry_action(self._verify_body_changing_img_heading)
        self.log.info("✅ Body changing image verification completed")

    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button safely."""
        self._retry_action(self._click_next)
        self.log.info("➡️ Clicked 'Next' button")

    # ----------------------- Internal Methods -----------------------

    def _verify_body_changing_img_heading(self):
        self.log.info("💊 Verifying image displayed:")
        verify_image_displayed = self.frame.locator("img[src*='/tatman1.png']")
        expect(verify_image_displayed).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info("✅ Image displayed verified successfully")

        self.log.info("💊 Verifying weight change last year heading:")
        is_visible = self.frame.locator("h2").is_visible()
        if is_visible:
            self.log.info("✅ H2 element is visible on the page")
        else:
            self.log.warning("❌ H2 element is not visible")

    def _click_next(self):
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
