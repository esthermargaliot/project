# services/spouse_service.py
from db_connection import get_session
from repository.client_repository import ClientRepository

class SpouseService:
    def __init__(self):
        session = get_session()
        self.client_repo = ClientRepository(session)

    def get_spouses(self, client_id):
        client = self.client_repo.get_by_id(client_id)
        if not client:
            return None
        return [s.to_dict() for s in client.spouses]

    def add_spouse(self, client_id, spouse_id):
        client = self.client_repo.get_by_id(client_id)
        spouse = self.client_repo.get_by_id(spouse_id)
        if not client or not spouse:
            return False
        if spouse not in client.spouses:
            client.spouses.append(spouse)
            self.client_repo.update(client)
        return True

    def remove_spouse(self, client_id, spouse_id):
        client = self.client_repo.get_by_id(client_id)
        spouse = self.client_repo.get_by_id(spouse_id)
        if not client or not spouse:
            return False
        if spouse in client.spouses:
            client.spouses.remove(spouse)
            self.client_repo.update(client)
        return True