from playwright.sync_api import Page, expect


class HeightWeightPage:
    """Handles height and weight form interactions in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        # Form elements
        self.feet_dropdown = self.frame.locator("(//div[@data-cy='dropdown-component'])[1]//input")
        self.inches_dropdown = self.frame.locator("(//div[@data-cy='dropdown-component'])[2]//input")
        self.weight_input = self.frame.locator("(//input[@data-cy='input-component'])[1]")
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")

    def wait_for_iframe_ready(self, max_retries: int = 5):
        """Wait for the Typeform iframe to load."""
        print("🔄 Waiting for iframe to load...")

        for attempt in range(1, max_retries + 1):
            try:
                # Wait for iframe to attach
                self.page.wait_for_selector(self.IFRAME_SELECTOR, state="attached", timeout=10000)
                self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

                # Wait for form elements to be visible
                self.feet_dropdown.wait_for(state="visible", timeout=10000)
                print("✅ Iframe loaded and form visible!")
                return

            except Exception as e:
                print(f"⚠️ Iframe not ready (Attempt {attempt}): {e}")
                if attempt < max_retries:
                    self.page.wait_for_timeout(2000)
                else:
                    raise TimeoutError("Iframe failed to load after multiple retries.") from e

    def select_feet(self, value: str):
        """Select feet from dropdown."""
        print(f"🦶 Selecting feet: {value}")
        self.feet_dropdown.wait_for(state="visible", timeout=10000)
        self.feet_dropdown.click()
        self.feet_dropdown.fill(value)
        self.page.keyboard.press("Enter")
        print(f"✅ Selected feet: {value}")

    def select_inches(self, value: str):
        """Select inches from dropdown."""
        print(f"📏 Selecting inches: {value}")
        self.inches_dropdown.wait_for(state="visible", timeout=10000)
        self.inches_dropdown.click()
        self.inches_dropdown.fill(value)
        self.page.keyboard.press("Enter")
        print(f"✅ Selected inches: {value}")

    def add_weight(self, weight: str):
        """Enter weight value."""
        print(f"⚖️ Entering weight: {weight}")
        self.weight_input.wait_for(state="visible", timeout=10000)
        self.weight_input.fill(weight)
        expect(self.weight_input).to_have_value(weight)
        print("✅ Weight entered successfully")

    def hit_next_button(self):
        """Click the 'Next' button."""
        self.next_button.wait_for(state="visible", timeout=10000)
        self.next_button.click()
        print("➡️ Clicked 'Next' button")
