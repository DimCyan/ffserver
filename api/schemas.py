"""fastapi docs schema"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class folder(BaseModel):
    name: str
    type: str = "📁"
    mtime: datetime
    size: Optional[str]


class file(folder):
    type: str = "❓"
    size: str
