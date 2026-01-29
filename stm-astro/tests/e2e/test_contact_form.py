"""
End-to-end tests for the HubSpot contact form on stm.studio.

These tests:
1. Navigate to stm.studio/#contact
2. Fill out and submit the HubSpot form in the iframe
3. Verify the form submission notification email arrives via Gmail API

Requirements:
- Playwright installed: pip install playwright && playwright install chromium
- Gmail API credentials in tests/e2e/credentials.json
- Gmail API token (auto-generated on first run via OAuth flow)

Usage:
    pytest tests/e2e/test_contact_form.py -v

    # Run with visible browser
    pytest tests/e2e/test_contact_form.py -v --headed

    # Skip email verification
    VERIFY_EMAIL=false pytest tests/e2e/test_contact_form.py -v
"""

import os
import random
import time
import uuid
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

# Import shared Gmail client from savaslabs.com tests
import sys
SAVASLABS_TESTS = Path("/Users/chris/web/savas-things/savaslabs.com-website/tests/e2e")
sys.path.insert(0, str(SAVASLABS_TESTS))
from gmail_client import GmailClient


def human_delay(min_ms=300, max_ms=800):
    """Random delay to simulate human behavior."""
    time.sleep(random.randint(min_ms, max_ms) / 1000)


def human_type(locator, text):
    """Type text character by character with random delays like a human."""
    locator.click()
    human_delay(100, 300)
    locator.press_sequentially(text, delay=random.randint(50, 120))
    human_delay(200, 400)


# Configuration
BASE_URL = os.environ.get("TEST_BASE_URL", "https://stm.studio")

# Email to receive HubSpot notifications (987car@gmail.com gets them)
NOTIFICATION_EMAIL = "987car@gmail.com"

# Whether to verify email delivery (requires Gmail API credentials)
VERIFY_EMAIL = os.environ.get("VERIFY_EMAIL", "true").lower() == "true"

# HubSpot notification email subject (configure based on your HubSpot form settings)
HUBSPOT_NOTIFICATION_SUBJECT = "STM Contact Form"  # Adjust based on actual HubSpot config


@pytest.fixture(scope="session")
def gmail_client():
    """Gmail client for verifying email delivery."""
    if not VERIFY_EMAIL:
        return None

    client = GmailClient()
    try:
        client.authenticate()
        return client
    except FileNotFoundError as e:
        pytest.skip(f"Gmail credentials not configured: {e}")
    except Exception as e:
        pytest.skip(f"Gmail authentication failed: {e}")


@pytest.fixture
def test_identifier():
    """Unique identifier for this test run, used to verify correct email."""
    return f"stm-{uuid.uuid4().hex[:8]}"


def fill_contact_form(page: Page, test_id: str):
    """
    Fill out and submit the HubSpot contact form.
    Uses human-like behavior to avoid HubSpot's bot detection.

    Args:
        page: Playwright page object
        test_id: Unique test identifier to include in submission
    """
    # Navigate to the contact section
    page.goto(f"{BASE_URL}/#contact", wait_until='networkidle')
    human_delay(1000, 2000)

    # Scroll to the form area
    page.keyboard.press("End")
    human_delay(500, 1000)

    # Scroll up a bit to see the form
    page.mouse.wheel(0, -500)
    human_delay(500, 1000)

    # Wait for the HubSpot iframe to load
    iframe_locator = page.frame_locator('iframe[src*="hsforms.com"]')

    # Wait for email field to be ready
    email_field = iframe_locator.locator('input[name="email"]')
    expect(email_field).to_be_visible(timeout=15000)

    # Fill out form with human-like typing
    # Use unique email alias for tracking (Gmail ignores + aliases)
    unique_email = f"987car+{test_id}@gmail.com"
    human_type(email_field, unique_email)

    # Pause before submit like a human reviewing
    human_delay(800, 1500)

    # Submit the form
    submit_btn = iframe_locator.locator('button[type="submit"], input[type="submit"]')
    submit_btn.scroll_into_view_if_needed()
    human_delay(200, 400)
    submit_btn.click()

    # Wait for success message or form disappearance
    # HubSpot typically shows a thank you message
    human_delay(2000, 3000)

    return unique_email


def verify_email_received(
    gmail_client: GmailClient,
    test_id: str,
    timeout: int = 90,
) -> bool:
    """
    Verify that the form submission notification email was received.

    Args:
        gmail_client: Authenticated Gmail client
        test_id: Unique test identifier to look for in email body
        timeout: How long to wait for email

    Returns:
        True if email found with test_id, False otherwise
    """
    if gmail_client is None:
        return True  # Skip verification if no client

    email = gmail_client.wait_for_hubspot_email(
        subject_contains=HUBSPOT_NOTIFICATION_SUBJECT,
        timeout_seconds=timeout,
        poll_interval=10,
        since_minutes=15,
        body_contains=test_id,
    )

    return email is not None


class TestContactForm:
    """Test suite for the STM Studio contact form."""

    def test_contact_page_loads(self, page: Page):
        """Verify the contact section loads with the form."""
        page.goto(f"{BASE_URL}/#contact")

        # Check for "Get in touch" heading
        heading = page.locator('text=Get in touch')
        expect(heading).to_be_visible(timeout=10000)

        # Check HubSpot iframe is present
        iframe = page.locator('iframe[src*="hsforms.com"]')
        expect(iframe).to_be_visible(timeout=15000)

    def test_form_submission(self, page: Page, gmail_client, test_identifier):
        """
        Test that the HubSpot form can be submitted and email notification is received.

        This test:
        1. Navigates to stm.studio/#contact
        2. Fills out the embedded HubSpot form (with human-like behavior)
        3. Submits the form
        4. Verifies email notification arrives via Gmail API
        """
        # Submit the form
        submitted_email = fill_contact_form(page, test_identifier)
        print(f"\nSubmitted form with email: {submitted_email}")
        print(f"Test ID: {test_identifier}")

        # Verify email was received
        if VERIFY_EMAIL and gmail_client:
            assert verify_email_received(
                gmail_client, test_identifier, timeout=90
            ), f"Did not receive notification email (test_id: {test_identifier})"
            print("SUCCESS: Notification email received!")


def run_manual_test():
    """
    Manually test form submission with visible browser.

    Usage:
        python tests/e2e/test_contact_form.py
    """
    from playwright.sync_api import sync_playwright

    test_id = f"manual-{uuid.uuid4().hex[:8]}"

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        print(f"Testing stm.studio contact form...")
        print(f"Test ID: {test_id}")

        submitted_email = fill_contact_form(page, test_id)
        print(f"Submitted with email: {submitted_email}")

        if VERIFY_EMAIL:
            print("Checking for notification email...")
            gmail = GmailClient()
            gmail.authenticate()
            if verify_email_received(gmail, test_id):
                print("SUCCESS: Email received!")
            else:
                print("FAILED: Email not received within timeout")
        else:
            print("Email verification skipped (VERIFY_EMAIL=false)")

        input("Press Enter to close browser...")
        browser.close()


if __name__ == "__main__":
    run_manual_test()
