from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = None

class RoleOut(RoleBase):
    id: str
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True
