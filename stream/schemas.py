from pydantic import BaseModel
from datetime import datetime

class WatchEvent(BaseModel):
    user_id: str
    item_id: str
    timestamp: datetime

class RateEvent(BaseModel):
    user_id: str
    item_id: str
    rating: float
    timestamp: datetime
