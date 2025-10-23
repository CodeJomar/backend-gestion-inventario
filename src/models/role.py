from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Role:
    id: str
    name: str
    description: Optional[str] = None
    created_at: datetime = None
    modified_at: datetime = None