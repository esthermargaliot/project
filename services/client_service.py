# services/client_service.py
from repository.client_repository import ClientRepository
from models.client import Client
from db_connection import get_session

class ClientService:
    def __init__(self):
        session = get_session()
        self.repo = ClientRepository(session)

    def get_all_clients(self):
        return [c.to_dict() for c in self.repo.get_all()]

    def create_client(self, data):
        client = Client(**data)
        self.repo.add(client)

    def update_client(self, mispar_zehut, data):
        client = self.repo.get_by_id(mispar_zehut)
        if not client:
            return False
        for key, value in data.items():
            setattr(client, key, value)
        self.repo.update(client)
        return True

    def delete_client(self, mispar_zehut):
        client = self.repo.get_by_id(mispar_zehut)
        if not client:
            return False
        self.repo.delete(client)
        return True