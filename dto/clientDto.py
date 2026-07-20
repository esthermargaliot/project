# dto/client_dto.py
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date
from dto.childDto import ChildDTO
from dto.spousesDto import SpouseDTO


@dataclass
class ClientDTO:
    id: str
    first_name: str
    last_name: str

    street: Optional[str]
    city: Optional[str]
    house_number: Optional[str]
    apartment_number: Optional[str]

    spouse: Optional[SpouseDTO]
    children: List[ChildDTO] = field(default_factory=list)