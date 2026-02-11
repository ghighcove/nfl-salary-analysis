"""
Medium browser automation for article import and scheduling.
"""


def import_to_medium(github_pages_url, browser_tools):
    """
    Import article to Medium using browser automation.

    Args:
        github_pages_url: GitHub Pages URL for the HTML article
        browser_tools: Dict with browser automation tool functions

    Returns:
        (bool, str): (success, medium_draft_url or error_message)
    """
    try:
        # Get browser context
        tabs_context = browser_tools['tabs_context_mcp'](createIfEmpty=True)

        if not tabs_context.get('tabs'):
            return False, "No browser tabs available"

        tab_id = tabs_context['tabs'][0]['id']

        # Navigate to Medium new story page
        browser_tools['navigate'](
            url="https://medium.com/new-story",
            tabId=tab_id
        )
        browser_tools['wait'](duration=3)

        # Find and click "Import a story" link
        import_elements = browser_tools['find'](
            query="import story link",
            tabId=tab_id
        )

        if not import_elements:
            return False, "Could not find 'Import a story' link on Medium"

        # Click the import link
        browser_tools['computer'](
            action="left_click",
            ref=import_elements[0]['ref'],
            tabId=tab_id
        )
        browser_tools['wait'](duration=2)

        # Find URL input field
        url_input = browser_tools['find'](
            query="url input field for import",
            tabId=tab_id
        )

        if not url_input:
            return False, "Could not find URL input field for import"

        # Enter GitHub Pages URL
        browser_tools['form_input'](
            ref=url_input[0]['ref'],
            value=github_pages_url,
            tabId=tab_id
        )
        browser_tools['wait'](duration=1)

        # Find and click Import button
        import_button = browser_tools['find'](
            query="import button",
            tabId=tab_id
        )

        if not import_button:
            return False, "Could not find Import button"

        browser_tools['computer'](
            action="left_click",
            ref=import_button[0]['ref'],
            tabId=tab_id
        )

        # Wait for import to complete
        browser_tools['wait'](duration=5)

        # Get current URL to extract draft ID
        # We'll use javascript_tool to get window.location.href
        url_result = browser_tools['javascript_tool'](
            action="javascript_exec",
            text="window.location.href",
            tabId=tab_id
        )

        current_url = url_result.get('result', '')

        # Check if we're on a Medium draft editor page
        if '/p/' in current_url and '/edit' in current_url:
            return True, current_url
        else:
            return False, f"Import may have failed. Current URL: {current_url}"

    except Exception as e:
        return False, f"Browser automation error: {str(e)}"


def schedule_medium_article(draft_url, publish_datetime, browser_tools):
    """
    Schedule Medium article for publication.

    Args:
        draft_url: Medium draft editor URL
        publish_datetime: ISO format datetime string (e.g., "2026-02-15T10:00:00")
        browser_tools: Dict with browser automation tool functions

    Returns:
        (bool, str): (success, confirmation_message or error_message)
    """
    try:
        # Get tab context
        tabs_context = browser_tools['tabs_context_mcp']()
        if not tabs_context.get('tabs'):
            return False, "No browser tabs available"

        tab_id = tabs_context['tabs'][0]['id']

        # Navigate to draft URL
        browser_tools['navigate'](url=draft_url, tabId=tab_id)
        browser_tools['wait'](duration=3)

        # Find and click "..." menu button
        menu_button = browser_tools['find'](
            query="more options menu button",
            tabId=tab_id
        )

        if not menu_button:
            return False, "Could not find menu button in Medium editor"

        browser_tools['computer'](
            action="left_click",
            ref=menu_button[0]['ref'],
            tabId=tab_id
        )
        browser_tools['wait'](duration=1)

        # Find and click "Schedule for later" option
        schedule_option = browser_tools['find'](
            query="schedule for later option",
            tabId=tab_id
        )

        if not schedule_option:
            return False, "Could not find 'Schedule for later' option"

        browser_tools['computer'](
            action="left_click",
            ref=schedule_option[0]['ref'],
            tabId=tab_id
        )
        browser_tools['wait'](duration=2)

        # Note: The actual date/time selection would require more specific
        # implementation based on Medium's scheduling UI. This is a placeholder.

        return True, f"Navigation to scheduling interface successful. Manual date entry required for: {publish_datetime}"

    except Exception as e:
        return False, f"Scheduling error: {str(e)}"


if __name__ == "__main__":
    print("Medium automation module - use within skill workflow")
