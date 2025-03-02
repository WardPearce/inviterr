from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SessionModel(BaseModel):
    expires: datetime
    created: datetime

    device: Optional[str] = None

    user_id: str

    id: str
