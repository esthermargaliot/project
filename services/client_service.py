# services/client_service.py
from models.client import Client
from models.child import Child
from models.spouse import Spouse
from repository.client_repository import ClientRepository
from repository.spouses_repository import SpouseRepository
from repository.child_repository import ChildRepository
from db_connection import get_session

class ClientService:
    def __init__(self):
        self.session = get_session()
        self.client_repo = ClientRepository(self.session)
        self.spouse_repo = SpouseRepository(self.session)
        self.child_repo = ChildRepository(self.session)

    def get_all_clients(self):
        return [c.to_dict() for c in self.client_repo.get_all()]

    def create_client(self, client_data):
        client = Client(**client_data)
        try:
            self.client_repo.add(client)
            self.session.commit()  # 👈 כאן commit
            return client
        except Exception:
            self.session.rollback()
            raise

    def update_client(self, mispar_zehut, data):
        client = self.client_repo.get_by_id(mispar_zehut)
        if not client:
            return False
        for key, value in data.items():
            setattr(client, key, value)
        try:
            self.session.commit()  # 👈 commit אחרי עדכון
            return True
        except Exception:
            self.session.rollback()
            raise

    def delete_client(self, mispar_zehut):
        client = self.client_repo.get_by_id(mispar_zehut)
        if not client:
            return False
        try:
            self.client_repo.delete(client)
            self.session.commit()  # 👈 commit אחרי מחיקה
            return True
        except Exception:
            self.session.rollback()
            raise

    def create_client_with_spouse_and_children(self, client_data, spouse_data=None, children_data=None):
        try:
            client = Client(**client_data)

            # בן זוג
            if spouse_data:
                spouse = Spouse(**spouse_data)
                client.spouse = spouse

            # ילדים
            if children_data:
                client.children = [Child(**c) for c in children_data]

            # שמירה
            self.session.add(client)
            self.session.commit()  # 👈 commit אחד לכל האובייקטים
            return client

        except Exception:
            self.session.rollback()
            raise