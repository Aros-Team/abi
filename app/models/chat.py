import uuid
from pydantic import BaseModel, field_validator
from typing import Optional


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

    @field_validator("session_id", mode="before")
    @classmethod
    def resolve_session_id(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v == "undefined":
            return str(uuid.uuid4())
        return v


class ChatResponse(BaseModel):
    session_id: str
