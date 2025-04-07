import requests
import os
import json
from flask import current_app


def send_slack_notification(message, channel="UN07YTUEB", attachments=None):
    """
    Send a message to a Slack channel using Slack's webhook API.
    
    Args:
        message (str): The message to send
        channel (str): The channel to send the message to
        attachments (list): Optional attachments for rich formatting
    
    Returns:
        bool: True if successful, False otherwise
    """
    webhook_url = current_app.config.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        current_app.logger.warning("SLACK_WEBHOOK_URL not configured, skipping notification")
        return False
        
        # Format channel properly - if it's a user ID, don't add the # prefix
    if channel.startswith("U") and not channel.startswith("#"):
        slack_channel = f"@{channel}"
    elif not channel.startswith("#"):
        slack_channel = f"#{channel}"
    else:
        slack_channel = channel

    payload = {
        "text": message,
        "channel": slack_channel,
        "username": "Zou Bot",
        "icon_emoji": ":factory:",
    }
    
    if attachments:
        payload["attachments"] = attachments
        
    try:
        current_app.logger.info(f"Sending Slack notification to {slack_channel}")
        response = requests.post(
            webhook_url,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send Slack notification: {e}")
        return False