
from playwright.sync_api import Page, expect
import logging, time
import allure
# pyright: ignore[reportMissingImports]
from utils.base_page import BasePage


class GLP1MedicinePage(BasePage):
    """Handles GLP-1 medicine step interactions in the MEDVi Typeform flow."""

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
    @allure.step("Enter name dose frequency")
    def enter_name_dose_frequency(self):
        """Enter name dose frequency."""
        self._retry_action(self._enter_name_dose_frequency)
        self.log.info("✅ Name dose frequency entered successfully")

    @allure.step("Enter last dose days")
    def enter_last_dose_days(self, last_dose_days: str):
        """Selects the option for last dose days dynamically."""
        self._retry_action(lambda: self._enter_last_dose_days(last_dose_days))
        self.log.info(f"✅ Selected last dose days: '{last_dose_days}'")

    @allure.step("Enter starting weight")
    def enter_starting_weight(self):
        """Enter starting weight."""
        self._retry_action(self._enter_starting_weight)
        self.log.info("✅ Starting weight entered successfully")

    @allure.step("Upload GLP-1 medication photo")
    def upload_glp1_photo(self, file_path: str):
        """Uploads a GLP-1 medication photo file."""
        self._retry_action(lambda: self._upload_glp1_photo(file_path))
        self.log.info("✅ Photo uploaded successfully")

    @allure.step("Do you agree to move forward with his program")
    def agree_to_move_forward(self):
        """Agree to move forward with the program."""
        self._retry_action(self._agree_to_move_forward)
        self.log.info("✅ Agreed to move forward with the program.")

    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button safely."""
        self._retry_action(self._click_next)
        self.log.info("➡️ Clicked 'Next' button")

    # ----------------------- Internal Methods -----------------------

    def _enter_name_dose_frequency(self):
        self.log.info("💊 Entering name dose frequency:")
        verify_name_dose_heading = self.frame.locator("//span[text() ='Please list the name, dose, and frequency of your GLP-1 medication.']")
        expect(verify_name_dose_heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        name_dose_frequency = self.frame.locator("//*[@id='widget-qbjC']//textarea")
        name_dose_frequency.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        name_dose_frequency.fill("Panadol 100mg")

    def _enter_last_dose_days(self, last_dose_days: str):
        self.log.info(f"💉 Selecting last dose days: '{last_dose_days}'")
        verify_last_dose_heading = self.frame.locator("//span[text() ='When was your last dose of medication?']")
        expect(verify_last_dose_heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        option_locator = self.frame.locator(f"//div[text()='{last_dose_days}']")
        option_locator.wait_for(state="visible", timeout=10000)
        option_locator.scroll_into_view_if_needed()
        option_locator.click()

    def _enter_starting_weight(self):
        self.log.info("💊 Entering starting weight:")
        verify_starting_weight_heading = self.frame.locator("//span[text() ='What was your starting weight in pounds?']")
        expect(verify_starting_weight_heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        starting_weight = self.frame.locator("(//input[@data-cy='input-component'])[1]")
        starting_weight.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        starting_weight.fill("90")

    def _upload_glp1_photo(self, file_path: str):
        verify_upload_glp1_photo_heading = self.frame.locator("//h3[text() ='Please take or upload a photo of your GLP-1 medication']")
        verify_upload_glp1_photo_heading.scroll_into_view_if_needed()
        expect(verify_upload_glp1_photo_heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info(f"📸 Uploading medication photo: {file_path}")
        upload_input = self.frame.locator("(//input[@type='file'])[1]")
        upload_input.set_input_files(file_path)
        expect(upload_input).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

    def _agree_to_move_forward(self):
        self.log.info("💊 Agreeing to move forward with the program.")
        verify_agree_to_move_forward_heading = self.frame.locator("//span[text() ='Do you agree to only obtain weight loss medication through this program moving forward?']")
        verify_agree_to_move_forward_heading.scroll_into_view_if_needed()
        expect(verify_agree_to_move_forward_heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        agree_to_move_forward = self.frame.locator("//div[normalize-space(text())='Yes']")
        agree_to_move_forward.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        agree_to_move_forward.click()

    def _click_next(self):
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click(force=True)
        self.page.wait_for_timeout(1000)
