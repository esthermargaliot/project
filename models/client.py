from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base import Base
from models.child import Child


class Client(Base):
    __tablename__ = "client"

    id = Column(String(9), primary_key=True)

    lastName = Column(String(100))
    firstName = Column(String(100))

    street = Column(String(100))
    city = Column(String(100))
    HouseNumber = Column(String(100))
    ApartmentNumber = Column(String(100))

    # קשר אחד-לאחד לבן זוג
    spouse = relationship(
        "Spouse",
        back_populates="client",
        uselist=False,
        cascade="all, delete-orphan"
    )
    children = relationship(
        "Child",
        back_populates="parent",
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}