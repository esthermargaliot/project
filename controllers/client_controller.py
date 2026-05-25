# controllers/client_controller.py
from flask import Blueprint, request, jsonify
from traits.trait_types import self

from models.client import Client
from services.client_service import ClientService

client_bp = Blueprint('client_bp', __name__)
client_service = ClientService()

@client_bp.route('/', methods=['GET'])
def get_clients():

    clients = client_service.get_all_clients()
    return jsonify(clients)

@client_bp.route('/', methods=['POST'])
def create_client():
    data = request.json
    client_service.create_client(data)
    return jsonify({'message': 'Client created'}), 201

@client_bp.route('/<int:mispar_zehut>', methods=['PUT'])
def update_client(mispar_zehut):
    data = request.json
    updated = client_service.update_client(mispar_zehut, data)
    if not updated:
        return jsonify({'message': 'Client not found'}), 404
    return jsonify({'message': 'Client updated'})

@client_bp.route('/<int:mispar_zehut>', methods=['DELETE'])
def delete_client(mispar_zehut):
    deleted = client_service.delete_client(mispar_zehut)
    if not deleted:
        return jsonify({'message': 'Client not found'}), 404
    return jsonify({'message': 'Client deleted'})

def to_dict(self):
    return {
        "mispar_zehut": self.mispar_zehut,
        "shem_mishpacha": self.shem_mishpacha,
        "shem_prati": self.shem_prati,
        "children": [
            {
                "id": c.id,
                "shem_prati": c.shem_prati,
                "shem_mishpacha": c.shem_mishpacha,
                "taarich_leida": str(c.taarich_leida) if c.taarich_leida else None
            }
            for c in self.children
        ]
    }