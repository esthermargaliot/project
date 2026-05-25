# # repository/spouse_repository.py
#
#
# class SpouseRepository:
#     def __init__(self, session):
#         self.session = session
#
#     def get_all_by_client(self, client_id):
#         return self.session.query(Spouse).filter_by(client_id=client_id).all()
#
#     def get_by_id(self, spouse_id):
#         return self.session.query(Spouse).filter_by(id=spouse_id).first()
#
#     def add(self, spouse):
#         self.session.add(spouse)
#         self.session.commit()
#
#     def update(self, spouse):
#         self.session.commit()
#
#     def delete(self, spouse):
#         self.session.delete(spouse)
#         self.session.commit()