from pydantic import BaseModel
from typing import List, Optional


class HTMLTag(BaseModel):
    classes: Optional[List[str]]
    content: str
