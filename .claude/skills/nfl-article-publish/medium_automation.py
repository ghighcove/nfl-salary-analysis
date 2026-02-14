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

        # Navigate directly to Medium's import page (not new-story)
        browser_tools['navigate'](
            url="https://medium.com/p/import",
            tabId=tab_id
        )
        browser_tools['wait'](duration=3)

        # Find URL input field on import page
        url_input = browser_tools['find'](
            query="url input field",
            tabId=tab_id
        )

        if not url_input:
            return False, "Could not find URL input field on Medium import page"

        # Click input field and type URL (form_input doesn't work on Medium's custom fields)
        browser_tools['computer'](
            action="left_click",
            ref=url_input[0]['ref'],
            tabId=tab_id
        )
        browser_tools['computer'](
            action="type",
            text=github_pages_url,
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

        # Parse datetime from ISO format to Medium format
        from datetime import datetime
        try:
            dt = datetime.fromisoformat(publish_datetime)
            date_str = dt.strftime("%m/%d/%Y")  # MM/DD/YYYY
            time_str = dt.strftime("%I:%M %p")  # HH:MM AM/PM
        except ValueError as e:
            return False, f"Invalid datetime format: {publish_datetime}. Use ISO format (YYYY-MM-DDTHH:MM:SS)"

        # Take screenshot to debug UI structure
        screenshot = browser_tools['computer'](
            action="screenshot",
            tabId=tab_id
        )

        # Try to find date and time input fields
        date_inputs = browser_tools['find'](
            query="date input field",
            tabId=tab_id
        )
        time_inputs = browser_tools['find'](
            query="time input field",
            tabId=tab_id
        )

        if not date_inputs or not time_inputs:
            return False, f"Could not find date/time input fields. Screenshot saved. Manual entry required for: {date_str} at {time_str}"

        # Try form_input first (cleaner approach)
        try:
            browser_tools['form_input'](
                ref=date_inputs[0]['ref'],
                value=date_str,
                tabId=tab_id
            )
            browser_tools['form_input'](
                ref=time_inputs[0]['ref'],
                value=time_str,
                tabId=tab_id
            )
        except Exception:
            # Fallback to click + type approach
            try:
                browser_tools['computer'](
                    action="left_click",
                    ref=date_inputs[0]['ref'],
                    tabId=tab_id
                )
                browser_tools['computer'](
                    action="key",
                    text="cmd+a" if browser_tools.get('platform') == 'darwin' else "ctrl+a",
                    tabId=tab_id
                )
                browser_tools['computer'](
                    action="type",
                    text=date_str,
                    tabId=tab_id
                )
                browser_tools['wait'](duration=0.5)

                browser_tools['computer'](
                    action="left_click",
                    ref=time_inputs[0]['ref'],
                    tabId=tab_id
                )
                browser_tools['computer'](
                    action="key",
                    text="cmd+a" if browser_tools.get('platform') == 'darwin' else "ctrl+a",
                    tabId=tab_id
                )
                browser_tools['computer'](
                    action="type",
                    text=time_str,
                    tabId=tab_id
                )
            except Exception as e:
                return False, f"Failed to enter date/time: {str(e)}. Manual entry required for: {date_str} at {time_str}"

        browser_tools['wait'](duration=1)

        # Find and click Schedule/Confirm button
        schedule_button = browser_tools['find'](
            query="schedule button",
            tabId=tab_id
        )

        if not schedule_button:
            # Try alternative names
            schedule_button = browser_tools['find'](
                query="confirm button",
                tabId=tab_id
            )

        if not schedule_button:
            return False, f"Could not find Schedule button. Date/time entered: {date_str} at {time_str}. Click Schedule manually."

        browser_tools['computer'](
            action="left_click",
            ref=schedule_button[0]['ref'],
            tabId=tab_id
        )
        browser_tools['wait'](duration=2)

        # Verify scheduling succeeded by checking page text
        page_text = browser_tools['get_page_text'](tabId=tab_id)
        success_indicators = [
            "scheduled",
            "will be published",
            "publish on",
            f"{date_str}"
        ]

        if any(indicator.lower() in page_text.lower() for indicator in success_indicators):
            return True, f"Successfully scheduled for {date_str} at {time_str}"
        else:
            return False, f"Scheduling may have failed. Please verify manually. Attempted: {date_str} at {time_str}"

    except Exception as e:
        return False, f"Scheduling error: {str(e)}"


if __name__ == "__main__":
    print("Medium automation module - use within skill workflow")
