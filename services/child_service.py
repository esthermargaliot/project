# services/child_service.py
from models.child import Child
from repository.child_repository import ChildRepository
from db_connection import get_session

class ChildService:
    def __init__(self):
        self.session = get_session()
        self.child_repo = ChildRepository(self.session)

    def create_child(self, data):
        """יוצר ילד חדש ושומר ב-DB"""
        child = Child(**data)
        self.child_repo.add(child)
        return child

    def delete_child(self, child_id):
        """מוחק ילד לפי מזהה"""
        child = self.child_repo.get_by_id(child_id)
        if not child:
            return False
        self.child_repo.delete(child)
        return True

    def get_all_children(self):
        """מחזיר רשימת כל הילדים"""
        return [c.to_dict() for c in self.child_repo.get_all()]
    def get_child_by_id(self, child_id):
        child = self.child_repo.get_by_id(child_id)
        return child.to_dict() if child else None

    def get_children_by_parent_id(self, parent_id):
        children = self.child_repo.get_by_parent_id(parent_id)
        return [c.to_dict() for c in children]

    def get_children_by_second_parent_id(self, second_parent_id):
        children = self.child_repo.get_by_second_parent_id(second_parent_id)
        return [c.to_dict() for c in children]

    def update_child(self, child_id, data):
        """מעדכן ילד קיים לפי מזהה"""
        child = self.child_repo.get_by_id(child_id)
        if not child:
            return False
        for key, value in data.items():
            setattr(child, key, value)
        self.child_repo.update(child)
        return True