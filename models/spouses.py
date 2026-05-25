from sqlalchemy import Table, Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from models.base import Base


SpouseAssociation = Table(
    'spouse_association',
    Base.metadata,
    Column('client_id', String(9), ForeignKey('client.mispar_zehut'), primary_key=True),
    Column('spouse_id', String(9), ForeignKey('client.mispar_zehut'), primary_key=True)
)