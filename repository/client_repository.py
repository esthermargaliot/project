from models.client import Client


class ClientRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Client).all()

    def get_by_id(self, id):
        return self.session.query(Client).filter_by(id=id).first()

    def add(self, client):
        self.session.add(client)

    def delete(self, client):
        self.session.delete(client)