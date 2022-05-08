import json
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime
from enum import Enum
from typing import Dict, List, Union

import requests

from models import Event, EventSlug


class HomepageEventStatus(Enum):
  Published = "published"
  
@dataclass_json
@dataclass
class HomepageEvent:
  id: int
  slug: EventSlug
  status: HomepageEventStatus
  date_created: str
  date_updated: str
  date: str
  time: Union[str, None]
  location: str
  type: str  # TODO: Use enum if event of different type should get special treatment
  translations: List[int]


@dataclass_json
@dataclass
class ListEventResponse:
  data: List[HomepageEvent]
  

def get_events() -> Dict[EventSlug, Event]:
    """ Get the events from the API """
    raw = requests.get("https://api.nms-ev.org/items/events").content
    response: ListEventResponse = ListEventResponse.schema().loads(raw)
    return {event.slug: convert_event(event) for event in response.data} 


def convert_event(event: HomepageEvent) -> Event:
    return Event(
        id=event.id, 
        slug=event.slug,
        date=datetime.strptime(f"{event.date} {event.time}", "%Y-%m-%d %H:%M:%S"),
        location=event.location
   ) 
