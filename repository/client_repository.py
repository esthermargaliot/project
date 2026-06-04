from models.client import Client


class ClientRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Client).all()

    def get_by_id(self, mispar_zehut):
        return self.session.query(Client).filter_by(mispar_zehut=mispar_zehut).first()

    def add(self, client):
        self.session.add(client)

    def delete(self, client):
        self.session.delete(client)