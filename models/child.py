from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from models.base import Base


class Child(Base):
    __tablename__ = "child"

    id = Column(Integer, primary_key=True, autoincrement=True)

    first_name = Column(String(100))
    last_name = Column(String(100))
    date_of_birth = Column(Date)
    date_of_birth_heb = Column(String(100))
    gender = Column(String(100))
    status=Column(String(100))
    # הורה ראשון
    parent_id = Column(String(9), ForeignKey("client.id"))
    parent = relationship("Client", back_populates="children")

    # הורה שני – Spouse
    second_parent_id = Column(String(9), ForeignKey("spouse.id"))
    second_parent = relationship("Spouse", back_populates="children")