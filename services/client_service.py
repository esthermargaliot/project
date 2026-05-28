# services/client_service.py
from models.child import Child
from models.spouse import Spouse
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

    def create_client_with_spouse_and_child(self, client_data, spouse_data=None, children_data=None):
        try:
            # בדיקה אם הלקוח כבר קיים
            existing_client = self.session.query(Client).filter_by(id=client_data['id']).first()
            if existing_client:
                return {"error": "Client already exists"}

            client = Client(**client_data)

            # אם יש בן זוג
            if spouse_data:
                existing_spouse = self.session.query(Spouse).filter_by(id=spouse_data['id']).first()
                if existing_spouse:
                    client.spouse = existing_spouse
                else:
                    spouse = Spouse(**spouse_data)
                    client.spouse = spouse

            # ילדים
            if children_data:
                for c_data in children_data:
                    child = Child(**c_data)
                    client.children.append(child)

            self.session.add(client)
            self.session.commit()
            return client

        except Exception as e:
            self.session.rollback()
            raise e