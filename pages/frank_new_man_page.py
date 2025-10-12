from playwright.sync_api import Page, expect
import logging


class FrankNewManPage:
    """Handles testimonial verification in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("FrankNewManPage")
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")

    def verify_recommendation_visible(self):
        """Verify that the testimonial text is visible."""
        self.log.info("🔍 Verifying recommendation visible...")
        recommendation_locator = self.frame.locator(
            "//*[contains(text(), '\"From the first day, MEDVi has been so attentive and informative\")]"
        )
        expect(recommendation_locator).to_be_visible(timeout=10000)
        self.log.info("✅ Recommendation visible")

    def hit_next_button(self):
        """Click the 'Next' button."""
        self.next_button.wait_for(state="visible", timeout=10000)
        self.next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
