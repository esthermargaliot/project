# repository/child_repository.py
from models.child import Child

class ChildRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Child).all()

    def get_by_id(self, child_id):
        return self.session.query(Child).filter_by(id=child_id).first()

    def add(self, child):
        self.session.add(child)
        self.session.commit()

    def update(self, child):
        self.session.commit()

    def delete(self, child):
        self.session.delete(child)
        self.session.commit()