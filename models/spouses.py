from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

class Spouse(Base):
    __tablename__ = 'spouses'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    birth_date = Column(Date, nullable=True)

    partner_id = Column(Integer, ForeignKey('clients.id'))
    partner = relationship('Client', back_populates='spouse')