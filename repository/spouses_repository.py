# repository/spouse_repository.py
from sqlalchemy.orm import Session
from models.client import Spouse

class SpouseRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, spouse: Spouse):
        self.session.add(spouse)
        self.session.commit()
        return spouse

    def get_all(self):
        return self.session.query(Spouse).all()

    def get_by_id(self, spouse_id: int):
        return self.session.query(Spouse).get(spouse_id)

    def update(self, spouse_id: int, new_data: Spouse):
        spouse = self.get_by_id(spouse_id)
        if spouse:
            for key, value in new_data.__dict__.items():
                if key != "_sa_instance_state":
                    setattr(spouse, key, value)
            self.session.commit()
        return spouse

    def delete(self, spouse_id: int):
        spouse = self.get_by_id(spouse_id)
        if spouse:
            self.session.delete(spouse)
            self.session.commit()
        return spouse