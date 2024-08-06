import uuid
from datetime import datetime
from pydantic import BaseModel


class UserResponse(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    phone: str = None
    is_email_verified: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime
