# services/spouse_service.py
from models.spouse import Spouse
from repository.spouses_repository import SpouseRepository
from db_connection import get_session

class SpouseService:
    def __init__(self):
        self.session = get_session()
        self.spouse_repo = SpouseRepository(self.session)

    def create_spouse(self, data):
        spouse = Spouse(**data)
        self.spouse_repo.add(spouse)
        return spouse

    def delete_spouse(self, spouse_id):
        spouse = self.spouse_repo.get_by_id(spouse_id)
        if not spouse:
            return False
        self.spouse_repo.delete(spouse)
        return True

    def get_all_spouses(self):
        return [s.to_dict() for s in self.spouse_repo.get_all()]

    def get_spouse_by_id(self, spouse_id):
        spouse = self.spouse_repo.get_by_id(spouse_id)
        return spouse.to_dict() if spouse else None

    def get_spouse_by_client_id(self, client_id):
        spouse = self.spouse_repo.get_by_client_id(client_id)
        return spouse.to_dict() if spouse else None