# repository/client_repository.py
from sqlalchemy.orm import Session
from models.client import Client

class ClientRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, client: Client):
        self.session.add(client)
        self.session.commit()
        return client

    def get_all(self):
        return self.session.query(Client).all()

    def get_by_id(self, mispar_zehut: str):
        return self.session.query(Client).get(mispar_zehut)

    def update(self, mispar_zehut: str, new_data: Client):
        client = self.get_by_id(mispar_zehut)
        if client:
            for key, value in new_data.__dict__.items():
                if key != "_sa_instance_state":
                    setattr(client, key, value)
            self.session.commit()
        return client

    def delete(self, mispar_zehut: str):
        client = self.get_by_id(mispar_zehut)
        if client:
            self.session.delete(client)
            self.session.commit()
        return client