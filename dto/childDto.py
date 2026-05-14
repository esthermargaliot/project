# dto/child_dto.py
from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class ChildDTO:
    name: str
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    parent_id: Optional[str] = None