from playwright.sync_api import sync_playwright


def capture_screenshot(html_content):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(html_content)
        page.wait_for_timeout(1000)

        content_box = page.query_selector("body > div").bounding_box()
        page.set_viewport_size(
            {
                "width": int(content_box["width"]) + 120,
                "height": int(content_box["height"]) + 120,
            }
        )

        screenshot = page.screenshot(full_page=True)
        browser.close()
    return screenshot
