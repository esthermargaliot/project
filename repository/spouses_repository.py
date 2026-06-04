from models.spouse import Spouse

class SpouseRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Spouse).all()

    def get_by_id(self, id):
        return self.session.query(Spouse).filter_by(id=id).first()

    def add(self, spouse):
        self.session.add(spouse)

    def delete(self, spouse):
        self.session.delete(spouse)

    def get_by_client_id(self, client_id):
            return self.session.query(Spouse).filter_by(client_id=client_id).first()