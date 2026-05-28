# repository/client_repository.py
from models.client import Client

class ClientRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Client).all()

    def get_by_id(self, mispar_zehut):
        return self.session.query(Client).filter_by(mispar_zehut=mispar_zehut).first()

    def add(self, client):
            try:
                self.session.add(client)
                self.session.commit()
                print("ID saved:", client.mispar_zehut)
            except Exception as e:
                self.session.rollback()
                raise e
    def update(self, client):
        self.session.commit()

    def delete(self, client):
        self.session.delete(client)
        self.session.commit()

    def save_all(self, client, spouse, child):
            self.session.add(client)
            self.session.add(spouse)
            self.session.add(child)
            self.session.commit()
            return client, spouse, child