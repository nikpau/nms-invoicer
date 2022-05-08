from dataclasses import dataclass
from datetime import datetime
from dataclasses_json import dataclass_json

# Unique name for an event
EventSlug = str

@dataclass
class Event:
  id: int
  slug: EventSlug
  date: datetime
  location: str
  
  
@dataclass_json
@dataclass
class Invoice:
    event_slug: EventSlug
    date: datetime
    purpose: str
    cost: float
    user: str