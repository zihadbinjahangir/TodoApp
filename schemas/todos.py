from pydantic import BaseModel, Field
from typing import Optional

class TodoSchema(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0,lt=6, description="Priority must be zero to five.")
    complete: bool