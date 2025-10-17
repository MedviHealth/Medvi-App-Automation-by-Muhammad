from playwright.sync_api import Page, expect
import logging, time
import allure
# pyright: ignore[reportMissingImports]
from utils.base_page import BasePage


class GoalWeightPage(BasePage):
    """Handles goal weight form interactions in the MEDVi Typeform flow."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.log = logging.getLogger(self.__class__.__name__)

    # ----------------------- Helpers -----------------------

    def _retry_action(self, func, retries=3, delay=2):
        """Retry a flaky action several times before giving up."""
        for attempt in range(1, retries + 1):
            try:
                return func()
            except Exception as e:
                if attempt < retries:
                    self.log.warning(
                        f"🔁 Attempt {attempt}/{retries} failed: {e}. Retrying in {delay}s…"
                    )
                    time.sleep(delay)
                else:
                    self.log.error(f"❌ All {retries} attempts failed: {e}")
                    raise

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    # ---------------------- Utilities ---------------------- #
    @staticmethod
    def escape_xpath_text(text: str) -> str:
        """Safely escape text for XPath — handles both single and double quotes."""
        if "'" not in text:
            return f"'{text}'"
        if '"' not in text:
            return f'"{text}"'
        parts = text.split("'")
        return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"

    # ---------------------- Actions ---------------------- #
    @allure.step("Verify goal weight page heading displayed")
    def verify_goal_weight_page_heading_displayed(self):
        """Verify the goal weight page heading displayed."""
        self.log.info("🔍 Verifying goal weight page heading displayed...")

        safe_text_1 = self.escape_xpath_text("We're in this together.")
        safe_text_2 = self.escape_xpath_text("What is your goal weight?")

        heading_1 = self.frame.locator(f"//*[normalize-space(text())={safe_text_1}]")
        heading_2 = self.frame.locator(f"//*[normalize-space(text())={safe_text_2}]")

        expect(heading_1).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        expect(heading_2).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

        self.log.info("✅ Goal weight page headings verified successfully")

    @allure.step("Enter goal weight")
    def add_goal_weight(self, goal_weight: str):
        """Enter goal weight (lbs) into the input field."""
        self._retry_action(lambda: self._fill_goal_weight(goal_weight))
        self.log.info(f"✅ Goal weight entered successfully: {goal_weight}")

    @allure.step("Verify motivational text is visible")
    def verify_together_text(self):
        """Ensure motivational text appears."""
        self.log.info("🔍 Verifying motivational text...")
        try:
            together_text = self.frame.locator(
                "text=We're in this together. Your goal is our goal."
            )
            together_text.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
            self.log.info("✅ Motivational text is visible")
        except Exception as e:
            self.log.warning(f"⚠️ Motivational text not found: {e}")

    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button safely."""
        self._retry_action(self._click_next)
        self.log.info("➡️ Clicked 'Next' button")

    # ----------------------- Internal Methods -----------------------

    def _fill_goal_weight(self, goal_weight: str):
        goal_input = self.frame.locator("(//input[@data-cy='input-component'])[1]")
        goal_input.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        goal_input.fill(goal_weight)
        expect(goal_input).to_have_value(goal_weight, timeout=self.DEFAULT_TIMEOUT)

    def _click_next(self):
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
