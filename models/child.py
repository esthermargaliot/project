from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from models.base import Base

class Child(Base):
    __tablename__ = 'child'

    id = Column(Integer, primary_key=True, autoincrement=True)
    mispar_zehut_parent = Column(String(9), ForeignKey('client.mispar_zehut'))
    shem_mishpacha = Column(String(100))
    shem_prati = Column(String(100))
    taarich_leida = Column(Date)

    # קשר חזרה להורה
    parent = relationship("Client", back_populates="children")