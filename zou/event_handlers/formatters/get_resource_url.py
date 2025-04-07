from zou.app.utils.slack import send_slack_notification
import json
from flask import current_app
from zou.event_handlers.formatters.slack_formatters import get_formatter

def get_resource_url(model_type, resource_id, project_id=None):
    """
    Create a full URL to a resource based on its type and ID.
    
    Args:
        model_type (str): The type of resource (asset, task, comment, etc.)
        resource_id (str): The ID of the resource
        project_id (str): The ID of the project (optional)
        
    Returns:
        str: A URL to the resource in the web interface
    """
    base_url = f"{current_app.config.get('DOMAIN_PROTOCOL', 'http')}://{current_app.config.get('DOMAIN_NAME', '127.0.0.1:8080')}"
    
    if model_type == "asset":
        if project_id:
            return f"{base_url}/productions/{project_id}/assets/{resource_id}"
        else:
            return f"{base_url}/assets/{resource_id}"
    elif model_type == "task":
        if project_id:
            return f"{base_url}/productions/{project_id}/tasks/{resource_id}"
        else:
            return f"{base_url}/tasks/{resource_id}"
    elif model_type == "comment":
        # Comments are usually viewed in the context of their task
        from zou.app.services import comments_service
        try:
            comment = comments_service.get_comment(resource_id)
            task_id = comment.get("task_id")
            if task_id and project_id:
                return f"{base_url}/productions/{project_id}/tasks/{task_id}?comment={resource_id}"
            elif task_id:
                return f"{base_url}/tasks/{task_id}?comment={resource_id}"
        except Exception as e:
            current_app.logger.error(f"Error getting comment info: {e}")
            
    # Default case
    return f"{base_url}/{model_type}s/{resource_id}"