# services/child_service.py
from repository.child_repository import ChildRepository
from models.child import Child
from db_connection import get_session

class ChildService:
    def __init__(self):
        session = get_session()
        self.repo = ChildRepository(session)

    def get_all_children(self):
        return [c.to_dict() for c in self.repo.get_all()]

    def create_child(self, data):
        child = Child(**data)
        self.repo.add(child)

    def update_child(self, child_id, data):
        child = self.repo.get_by_id(child_id)
        if not child:
            return False
        for key, value in data.items():
            setattr(child, key, value)
        self.repo.update(child)
        return True

    def delete_child(self, child_id):
        child = self.repo.get_by_id(child_id)
        if not child:
            return False
        self.repo.delete(child)
        return True