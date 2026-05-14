# repository/child_repository.py
from sqlalchemy.orm import Session
from models.client import Child

class ChildRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, child: Child):
        self.session.add(child)
        self.session.commit()
        return child

    def get_all(self):
        return self.session.query(Child).all()

    def get_by_id(self, child_id: int):
        return self.session.query(Child).get(child_id)

    def update(self, child_id: int, new_data: Child):
        child = self.get_by_id(child_id)
        if child:
            for key, value in new_data.__dict__.items():
                if key != "_sa_instance_state":
                    setattr(child, key, value)
            self.session.commit()
        return child

    def delete(self, child_id: int):
        child = self.get_by_id(child_id)
        if child:
            self.session.delete(child)
            self.session.commit()
        return child