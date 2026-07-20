# services/client_service.py
from mappers.form_mapper import map_form_to_db
from models import client
from models.client import Client
from models.child import Child
from models.spouse import Spouse
from repository.client_repository import ClientRepository
from repository.spouses_repository import SpouseRepository
from repository.child_repository import ChildRepository
from db_connection import get_session
from dto import childDto, spousesDto, clientDto
class ClientService:
    def __init__(self):
        self.session = get_session()
        self.client_repo = ClientRepository(self.session)
        self.spouse_repo = SpouseRepository(self.session)
        self.child_repo = ChildRepository(self.session)

    def get_all_clients(self):
        return [c.to_dict() for c in self.client_repo.get_all()]

    def create_client(self, client_data):
        client = Client(**client_data)
        try:
            self.client_repo.add(client)
            self.session.commit()  # 👈 כאן commit
            return client
        except Exception:
            self.session.rollback()
            raise

    def update_client(self, id, data):
        client = self.client_repo.get_by_id(id)
        if not client:
            return False
        for key, value in data.items():
            setattr(client, key, value)
        try:
            self.session.commit()  # 👈 commit אחרי עדכון
            return True
        except Exception:
            self.session.rollback()
            raise

    def delete_client(self, id):
        client = self.client_repo.get_by_id(id)
        if not client:
            return False
        try:
            self.client_repo.delete(client)
            self.session.commit()  # 👈 commit אחרי מחיקה
            return True
        except Exception:
            self.session.rollback()
            raise

    def create_client_with_spouse_and_children(self, client_data, spouse_data=None, children_data=None):
        try:
            client = Client(**client_data)

            # בן זוג
            if spouse_data:
                spouse = Spouse(**spouse_data)
                client.spouse = spouse

            # ילדים
            if children_data:
                client.children = [Child(**c) for c in children_data]

            # שמירה
            self.session.add(client)
            self.session.commit()  # 👈 commit אחד לכל האובייקטים
            return client

        except Exception:
            self.session.rollback()
            raise
    def build_flat_dict(self,client):
      data = {
        "first_name": client.firstName,
        "last_name": client.lastName,
        "city": client.city,
        "street": client.street,
        "house_number": client.HouseNumber,
        "apartment_number": client.ApartmentNumber,
    }

    # 👨‍👩‍👧 בן/בת זוג
      if client.spouse:
          data.update({
            "spouse_first_name": client.spouse.firstName,
            "spouse_last_name": client.spouse.lastName,
            "spouse_marital_status": client.spouse.marital_status
        })

    # 👶 ילדים (רשימה)
      children = []
      for i, child in enumerate(client.children):
        children.append({
            "index": i,
            "first_name": child.first_name,
            "last_name": child.last_name,
            "gender": child.gender,
            "date_of_birth": str(child.date_of_birth) if child.date_of_birth else None
        })

      data["children"] = [
          {
              "first_name": c.first_name,
              "last_name": c.last_name,
              "gender": c.gender,
              "date_of_birth": str(c.date_of_birth) if c.date_of_birth else None
          }
          for c in client.children
      ]

      return data

    @staticmethod
    def flatten_client(client):
        flat = {}

        # =====================
        # CLIENT LEVEL
        # =====================
        for key, value in client.__dict__.items():
            if value is None:
                continue

            # אובייקטים מורכבים נטפל בנפרד
            if key in ["spouse", "children"]:
                continue

            flat[f"client.{key}"] = value

        # =====================
        # SPOUSE
        # =====================
        spouse = getattr(client, "spouse", None)
        if spouse:
            for key, value in spouse.__dict__.items():
                if value is not None:
                    flat[f"spouse.{key}"] = value

        # =====================
        # CHILDREN (list)
        # =====================
        children = getattr(client, "children", [])
        if children:
            for i, child in enumerate(children):
                for key, value in child.__dict__.items():
                    if value is not None:
                        flat[f"children.{i}.{key}"] = value

        return flat

def get_all_clients(self):
    session = get_session()
    return session.query(Client).all()


