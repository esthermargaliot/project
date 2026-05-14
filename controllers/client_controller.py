from flask import Blueprint, request, jsonify
from dto.client_dto import ClientDTO
from services.client_service import ClientService
from repository.client_repository import ClientRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.client import Base

# הגדרת DB
engine = create_engine('sqlite:///clients.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# אינסטנציות Repository ו-Service
repo = ClientRepository(session)
service = ClientService(repo)

# Blueprint
client_blueprint = Blueprint('clients', __name__)

# Create Client
@client_blueprint.route('', methods=['POST'])
def add_client():
    dto = ClientDTO(**request.get_json())
    service.add_client(dto)
    return jsonify({'message': 'Client added'}), 201

# Get All Clients
@client_blueprint.route('', methods=['GET'])
def get_clients():
    clients = service.get_all_clients()
    return jsonify([{
        'mispar_zehut': c.mispar_zehut,
        'shem_mishpacha': c.shem_mishpacha,
        'shem_prati': c.shem_prati,
        'shem_av': c.shem_av,
        'taarich_leida': c.taarich_leida,
        'makom_leida': c.makom_leida,
        'aretz_leida': c.aretz_leida,
        'min': c.min,
        'leom': c.leom,
        'dat': c.dat,
        'status_mishpachti': c.status_mishpachti,
        'taarich_aliya': c.taarich_aliya,
        'taarich_tokef': c.taarich_tokef
    } for c in clients])

# Get Client By ID
@client_blueprint.route('/<string:mispar_zehut>', methods=['GET'])
def get_client(mispar_zehut):
    client = service.get_client_by_id(mispar_zehut)
    return jsonify({
        'mispar_zehut': client.mispar_zehut,
        'shem_mishpacha': client.shem_mishpacha,
        'shem_prati': client.shem_prati,
        'shem_av': client.shem_av,
        'taarich_leida': client.taarich_leida,
        'makom_leida': client.makom_leida,
        'aretz_leida': client.aretz_leida,
        'min': client.min,
        'leom': client.leom,
        'dat': client.dat,
        'status_mishpachti': client.status_mishpachti,
        'taarich_aliya': client.taarich_aliya,
        'taarich_tokef': client.taarich_tokef
    })

# Update Client
@client_blueprint.route('/<string:mispar_zehut>', methods=['PUT'])
def update_client(mispar_zehut):
    dto = ClientDTO(**request.get_json())
    service.update_client(mispar_zehut, dto)
    return jsonify({'message': 'Client updated'})

# Delete Client
@client_blueprint.route('/<string:mispar_zehut>', methods=['DELETE'])
def delete_client(mispar_zehut):
    service.delete_client(mispar_zehut)
    return jsonify({'message': 'Client deleted'})