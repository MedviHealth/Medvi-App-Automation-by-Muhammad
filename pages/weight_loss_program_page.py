from playwright.sync_api import Page, expect
import logging, time
import allure
# pyright: ignore[reportMissingImports]
from utils.base_page import BasePage


class WeightLossProgramPage(BasePage):
    """Handles the 'Weight Loss Program' step in the MEDVi Typeform flow."""

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

    @allure.step("Verify weight loss program heading")
    def verify_weight_loss_program_heading(self):
        """Verify weight loss program heading."""
        self._retry_action(self._verify_weight_loss_program_heading)
        self.log.info("✅ Weight loss program heading verified successfully")

    @allure.step("Select weight loss program option (Yes/No)")
    def select_weight_loss_program_option(self, option: str, weight_loss_program_name: str = None):
        """Select Yes/No and handle conditional medication name input if Yes is chosen."""
        self._retry_action(lambda: self._select_weight_loss_program_option(option, weight_loss_program_name))
        self.log.info(f"✅ Selected option: {option.strip().capitalize()}")

    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button safely."""
        self._retry_action(self._click_next)
        self.log.info("➡️ Clicked 'Next' button")

    # ----------------------- Internal Methods -----------------------

    def _verify_weight_loss_program_heading(self):
        self.log.info("💊 Verifying weight loss program heading:")
        verify_weight_loss_program_heading = self.frame.locator("//h1[text()='How about weight loss programs?']")
        expect(verify_weight_loss_program_heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

    def _select_weight_loss_program_option(self, option: str, weight_loss_program_name: str = None):
        clean_option = option.strip().capitalize()
        self.log.info(f"💊 Selecting weight loss program option: {clean_option}")

        # Click Yes or No
        option_locator = self.frame.locator(f"//div[normalize-space(text())='{clean_option}']")
        option_locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        option_locator.scroll_into_view_if_needed()
        option_locator.click()

        # Conditional field: only appears if 'Yes' is selected
        if clean_option == "Yes":
            self.log.info("🩺 User selected 'Yes' — waiting for weight loss program input field...")
            label_text_locator = self.frame.locator("//span[text()='Please provide brief details.']")
            expect(label_text_locator).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
            weight_loss_program_input = self.frame.locator("//*[@data-cy='long-answer-component']//textarea")

            try:
                weight_loss_program_input.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
                if weight_loss_program_name:
                    weight_loss_program_input.fill(weight_loss_program_name)
                    self.log.info(f"✅ Entered weight loss program name: {weight_loss_program_name}")
                else:
                    self.log.info("✅ No weight loss program name provided, field left blank.")

            except Exception as e:
                self.log.error(f"❌ Weight loss program input field not visible after selecting 'Yes': {e}")
                raise

    def _click_next(self):
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
