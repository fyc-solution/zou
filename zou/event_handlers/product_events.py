from zou.app.utils.slack import send_slack_notification
import json
from flask import current_app
from zou.event_handlers.formatters.slack_formatters import get_formatter
from zou.event_handlers.formatters.get_resource_url import get_resource_url

def handle_event(data):
    """
    Handle events and send notifications to Slack.
    This function is called by Zou's event system.
    """
    event_name = data.get("event", "")
    current_app.logger.info(f"Received event: {event_name}")
    
    try:
        # Parse event name to determine model and event type
        # Event format is "model:event_type", e.g. "asset:new"
        model_type, event_type = event_name.split(":")
        current_app.logger.info(f"Parsed event: model={model_type}, type={event_type}")
        
        # Get the appropriate formatter function
        formatter = get_formatter(model_type)
        
        # Format the message
        message = formatter(event_type, data)
        current_app.logger.info(f"Formatted message: {message}")
        
        # Get resource ID and generate URL
        resource_id = data.get(f"{model_type}_id")
        project_id = data.get("project_id")
        resource_url = ""
        
        if resource_id:
            resource_url = get_resource_url(model_type, resource_id, project_id)
            current_app.logger.info(f"Generated resource URL: {resource_url}")
        
        # Create attachment with additional details
        attachment = {
            "fallback": message,
            "color": "#3AA3E3",
            "fields": [
                {
                    "title": "Event",
                    "value": event_name,
                    "short": True
                },
                {
                    "title": "Project",
                    "value": data.get("project_id", "Unknown"),
                    "short": True
                },
                {
                    "title": "Details",
                    "value": f"```{json.dumps(data, indent=2)}```",
                    "short": False
                }
            ],
            "footer": "Zou Production Management",
            "ts": int(data.get("created_at", 0)) if "created_at" in data else 0
        }
                
        # Add URL if available
        if resource_url:
            attachment["title"] = f"{model_type.capitalize()} Details"
            attachment["title_link"] = resource_url

        # Send to Slack
        current_app.logger.info(f"Sending notification to Slack for event: {event_name}")
        result = send_slack_notification(
            message=message,
            attachments=[attachment]
        )
        
        if result:
            current_app.logger.info(f"Successfully sent Slack notification for {event_name}")
        else:
            current_app.logger.warning(f"Failed to send Slack notification for {event_name}")
            
    except ValueError:
        current_app.logger.error(f"Invalid event format: {event_name}. Expected format: 'model:event_type'")
    except Exception as e:
        current_app.logger.error(f"Error handling event {event_name}: {str(e)}", exc_info=True)