from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# טבלת קשר Many-to-Many עבור בני זוג
spouse_association = Table(
    'spouses',
    Base.metadata,
    Column('client_id', String(9), ForeignKey('clients.mispar_zehut'), primary_key=True),
    Column('spouse_id', String(9), ForeignKey('clients.mispar_zehut'), primary_key=True)
)


class Client(Base):
    __tablenaדZme__ = 'clients'

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
    spouses = relationship(
        "Client",
        secondary=spouse_association,
        primaryjoin=mispar_zehut == spouse_association.c.person_id,
        secondaryjoin=mispar_zehut == spouse_association.c.spouse_id,
        backref="partners"
    )


class Child(Base):
    __tablename__ = 'children'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    last_name = Column(String(100))
    date_of_birth = Column(Date)
    parent_id = Column(String(9), ForeignKey('clients.mispar_zehut'))

    # חזרה ללקוח
    parent = relationship("Client", back_populates="children")