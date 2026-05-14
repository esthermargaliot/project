# dto/client_dto.py
from dataclasses import dataclass
from typing import List, Optional
from datetime import date
from dto.childDto import ChildDTO
from dto.spousesDto import SpouseDTO

@dataclass
class ClientDTO:
    mispar_zehut: str
    shem_mishpacha: Optional[str] = None
    shem_prati: Optional[str] = None
    shem_av: Optional[str] = None
    taarich_leida: Optional[date] = None
    makom_leida: Optional[str] = None
    aretz_leida: Optional[str] = None
    min: Optional[str] = None
    leom: Optional[str] = None
    dat: Optional[str] = None
    status_mishpachti: Optional[str] = None
    taarich_aliya: Optional[date] = None
    taarich_tokef: Optional[date] = None
    children: Optional[List[ChildDTO]] = None
    spouses: Optional[List[SpouseDTO]] = None