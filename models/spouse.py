from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class Spouse(Base):
    __tablename__ = "spouse"

    id = Column(String(9), primary_key=True)  #

    client_id = Column(String(9), ForeignKey("client.id"))

    firstName = Column(String(100))
    lastName = Column(String(100))
    marital_status = Column(String(50))  # מצב אישי

    client = relationship(
        "Client",
        back_populates="spouse"
    )
    children = relationship("Child", back_populates="second_parent", cascade="all, delete-orphan")
    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "marital_status": self.marital_status,
        }
