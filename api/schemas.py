"""fastapi docs schema"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum


class sys_node_type(Enum):
    folder = "folder"
    file = "file"


class sys_node(BaseModel):
    name: str
    type: sys_node_type
    mtime: datetime
    ctime: datetime


class sys_folder(sys_node):
    type: sys_node_type = sys_node_type.folder


class sys_file(sys_node):
    type: sys_node_type = sys_node_type.file
    size: str
    mime: Optional[str]
