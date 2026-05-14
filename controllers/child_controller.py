from flask import Blueprint, request, jsonify
from dto.child_dto import ChildDTO
from services.child_service import ChildService
from repository.child_repository import ChildRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.client import Base

engine = create_engine('sqlite:///clients.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

repo = ChildRepository(session)
service = ChildService(repo)

child_blueprint = Blueprint('children', __name__)

@child_blueprint.route('', methods=['POST'])
def add_child():
    dto = ChildDTO(**request.get_json())
    service.add_child(dto)
    return jsonify({'message': 'Child added'}), 201

@child_blueprint.route('/<string:client_id>', methods=['GET'])
def get_children(client_id):
    children = service.get_children_for_client(client_id)
    return jsonify([c.to_dict() for c in children])