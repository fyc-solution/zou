from zou.app.utils import events
from . import product_events
from enum import Enum

# Define available events as an Enum
class EventType(Enum):
    NEW = "new"
    UPDATE = "update"
    DELETE = "delete"

# List of models
models = ["comment", "task", "asset"]

# Generate event_map dynamically
event_map = {}
for model in models:
    for event in EventType:
        event_key = f"{model}:{event.value}"
        event_map[event_key] = product_events