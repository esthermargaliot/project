# dto/child_dto.py
from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class ChildDTO:
    first_name: str
    last_name: str
    date_of_birth: Optional[str]
    gender: Optional[str]