from flask import Blueprint, request, jsonify
from dto.spouse_dto import SpouseDTO
from services.spouse_service import SpouseService
from repository.spouse_repository import SpouseRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.client import Base

engine = create_engine('sqlite:///clients.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

repo = SpouseRepository(session)
service = SpouseService(repo)

spouse_blueprint = Blueprint('spouses', __name__)

@spouse_blueprint.route('', methods=['POST'])
def add_spouse():
    dto = SpouseDTO(**request.get_json())
    service.add_spouse(dto)
    return jsonify({'message': 'Spouse added'}), 201

@spouse_blueprint.route('/<string:client_id>', methods=['GET'])
def get_spouses(client_id):
    spouses = service.get_spouses_for_client(client_id)
    return jsonify([s.to_dict() for s in spouses])