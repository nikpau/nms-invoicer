from dataclasses import dataclass
from datetime import datetime

# Unique name for an event
EventSlug = str

@dataclass
class Event:
  id: int
  slug: EventSlug
  date: datetime
  location: str