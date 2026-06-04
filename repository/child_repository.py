from models.child import Child

class ChildRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Child).all()

    def get_by_id(self, id):
        return self.session.query(Child).filter_by(id=id).first()

    def add(self, child):
        self.session.add(child)

    def delete(self, child):
        self.session.delete(child)


    def get_by_parent_id(self, parent_id):
        return self.session.query(Child).filter_by(parent_id=parent_id).all()

    def get_by_second_parent_id(self, second_parent_id):
        return self.session.query(Child).filter_by(second_parent_id=second_parent_id).all()