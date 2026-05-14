# dto/spouse_dto.py
from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class SpouseDTO:
    first_name: str
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    partner_id: Optional[str] = None