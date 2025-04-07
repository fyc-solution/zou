from zou.app.services import assets_service, persons_service
from flask import current_app

def format_asset_message(event_type, data):
    """Format the Slack message for asset events"""
    
    # Get asset ID from the event data
    asset_id = data.get("asset_id")
    
    if not asset_id:
        return f"Unknown asset {event_type} event occurred"
    
    # Get asset details
    try:
        asset = assets_service.get_asset(asset_id)
        asset_name = asset.get("name", "Unknown")
        project_name = "Unknown"
        if asset.get("project_id"):
            try:
                from zou.app.services import projects_service
                project = projects_service.get_project(asset["project_id"])
                project_name = project.get("name", "Unknown")
            except Exception as e:
                current_app.logger.error(f"Error getting project: {e}")
        
        # Get user info if available
        user_info = ""
        if "user_id" in data:
            try:
                user = persons_service.get_person(data["user_id"])
                user_info = f" by {user['full_name']}"
            except Exception as e:
                current_app.logger.error(f"Error getting user: {e}")
        
        if event_type == "new":
            return f":new: Asset *{asset_name}* was created in project *{project_name}*{user_info}"
        elif event_type == "update":
            return f":pencil2: Asset *{asset_name}* was updated in project *{project_name}*{user_info}"
        elif event_type == "delete":
            return f":x: Asset *{asset_name}* was deleted from project *{project_name}*{user_info}"
        else:
            return f":bell: Asset *{asset_name}* event: *{event_type}* in project *{project_name}*{user_info}"
            
    except Exception as e:
        current_app.logger.error(f"Error formatting asset message: {e}")
        return f"Asset {event_type} event occurred (Error: {str(e)})"

def format_task_message(event_type, data):
    """Format the Slack message for task events"""
    
    task_id = data.get("task_id")
    
    if not task_id:
        return f"Unknown task {event_type} event occurred"
    
    try:
        from zou.app.services import tasks_service
        task = tasks_service.get_task(task_id)
        task_name = task.get("name", "Unknown")
        project_name = "Unknown"
        
        if task.get("project_id"):
            try:
                from zou.app.services import projects_service
                project = projects_service.get_project(task["project_id"])
                project_name = project.get("name", "Unknown")
            except Exception as e:
                current_app.logger.error(f"Error getting project: {e}")
        
        # Get user info if available
        user_info = ""
        if "user_id" in data:
            try:
                from zou.app.services import persons_service
                user = persons_service.get_person(data["user_id"])
                user_info = f" by {user['full_name']}"
            except Exception as e:
                current_app.logger.error(f"Error getting user: {e}")
        
        if event_type == "new":
            return f":new: Task *{task_name}* was created in project *{project_name}*{user_info}"
        elif event_type == "update":
            return f":pencil2: Task *{task_name}* was updated in project *{project_name}*{user_info}"
        elif event_type == "delete":
            return f":x: Task *{task_name}* was deleted from project *{project_name}*{user_info}"
        else:
            return f":bell: Task *{task_name}* event: *{event_type}* in project *{project_name}*{user_info}"
            
    except Exception as e:
        current_app.logger.error(f"Error formatting task message: {e}")
        return f"Task {event_type} event occurred (Error: {str(e)})"

def format_comment_message(event_type, data):
    """Format the Slack message for comment events"""
    
    comment_id = data.get("comment_id")
    
    if not comment_id:
        return f"Unknown comment {event_type} event occurred"
    
    try:
        from zou.app.services import comments_service
        comment = comments_service.get_comment(comment_id)
        
        # Get task info
        task_name = "Unknown"
        project_name = "Unknown"
        if comment.get("task_id"):
            try:
                from zou.app.services import tasks_service
                task = tasks_service.get_task(comment["task_id"])
                task_name = task.get("name", "Unknown")
                
                if task.get("project_id"):
                    try:
                        from zou.app.services import projects_service
                        project = projects_service.get_project(task["project_id"])
                        project_name = project.get("name", "Unknown")
                    except Exception as e:
                        current_app.logger.error(f"Error getting project: {e}")
            except Exception as e:
                current_app.logger.error(f"Error getting task: {e}")
        
        # Get user info if available
        user_info = ""
        if "user_id" in data:
            try:
                from zou.app.services import persons_service
                user = persons_service.get_person(data["user_id"])
                user_info = f" by {user['full_name']}"
            except Exception as e:
                current_app.logger.error(f"Error getting user: {e}")
        
        # Truncate comment text if too long
        comment_text = comment.get("text", "")
        if len(comment_text) > 50:
            comment_text = comment_text[:47] + "..."
        
        if event_type == "new":
            return f":speech_balloon: New comment on task *{task_name}* in project *{project_name}*{user_info}: \"{comment_text}\""
        elif event_type == "update":
            return f":pencil2: Comment updated on task *{task_name}* in project *{project_name}*{user_info}"
        elif event_type == "delete":
            return f":x: Comment deleted from task *{task_name}* in project *{project_name}*{user_info}"
        else:
            return f":bell: Comment event: *{event_type}* on task *{task_name}* in project *{project_name}*{user_info}"
            
    except Exception as e:
        current_app.logger.error(f"Error formatting comment message: {e}")
        return f"Comment {event_type} event occurred (Error: {str(e)})"

def get_formatter(model_type):
    """Return the appropriate formatter function based on model type"""
    formatters = {
        "asset": format_asset_message,
        "task": format_task_message,
        "comment": format_comment_message
    }
    return formatters.get(model_type, lambda e, d: f"Unhandled model type: {model_type}")