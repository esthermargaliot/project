from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from models.spouses import SpouseAssociation

from models.base import Base




class Client(Base):
    __tablename__ = 'client'

    mispar_zehut = Column(String(9), primary_key=True)  # מספר זהות
    shem_mishpacha = Column(String(100))
    shem_prati = Column(String(100))
    shem_av = Column(String(100))
    taarich_leida = Column(Date)
    makom_leida = Column(String(100))
    aretz_leida = Column(String(100))
    min = Column(String(10))
    leom = Column(String(50))
    dat = Column(String(50))
    status_mishpachti = Column(String(50))
    taarich_aliya = Column(Date)
    taarich_tokef = Column(Date)

    # קשר  לילדים (One-to-Many)
    children = relationship(
        "Child",
        back_populates="parent",
        cascade="all, delete-orphan"
    )

    # קשר לבן זוג (Many-to-Many)
    # models/client.py
    spouses = relationship(
        "Client",
        secondary=SpouseAssociation,
        primaryjoin=mispar_zehut == SpouseAssociation.c.client_id,
        secondaryjoin=mispar_zehut == SpouseAssociation.c.spouse_id,
        backref="spouses_of"
    )

    def to_dict(self):
        return {
            "mispar_zehut": self.mispar_zehut,
            "shem_mishpacha": self.shem_mishpacha,
            "shem_prati": self.shem_prati,
            "shem_av": self.shem_av,
            "taarich_leida": str(self.taarich_leida) if self.taarich_leida else None,
            "makom_leida": self.makom_leida,
            "aretz_leida": self.aretz_leida,
            "min": self.min,
            "leom": self.leom,
            "dat": self.dat,
            "status_mishpachti": self.status_mishpachti,
            "taarich_aliya": str(self.taarich_aliya) if self.taarich_aliya else None,
            "taarich_tokef": str(self.taarich_tokef) if self.taarich_tokef else None
        }

