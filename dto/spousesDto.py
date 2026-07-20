# dto/spouse_dto.py
from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class SpouseDTO:
    first_name: str
    last_name: str
    marital_status: Optional[str]