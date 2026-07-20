# controllers/spouse_controller.py
from flask import Blueprint, request, jsonify

from db_connection import get_session
from repository.spouses_repository import SpouseRepository
from services.spouse_service import SpouseService

spouse_bp = Blueprint('spouse_bp', __name__)
service = SpouseService()
@spouse_bp.route('/', methods=['GET'])
def get_spouses():
    spouses = service.get_all_spouses()
    return jsonify(spouses), 200
@spouse_bp.route('/client/<client_id>', methods=['GET'])
def get_spouse_by_client_id(client_id):
    result = service.get_spouse_by_client_id(client_id)
    if not result:
        return jsonify({"error": "Spouse not found for this client"}), 404
    return jsonify(result), 200
@spouse_bp.route('/<spouse_id>', methods=['GET'])
def get_spouse_by_id(spouse_id):
    result = service.get_spouse_by_id(spouse_id)
    if not result:
        return jsonify({"error": "Spouse not found"}), 404
    return jsonify(result), 200

# הוספת בן/בת זוג ללקוח
@spouse_bp.route('/<client_id>/<spouse_id>', methods=['POST'])
def add_spouse(client_id, spouse_id):
    success = service.add_spouse(client_id, spouse_id)
    if not success:
        return jsonify({'message': 'Client or spouse not found'}), 404
    return jsonify({'message': 'Spouse added'}), 201

# הסרת בן/בת זוג מלקוח
@spouse_bp.route('/<client_id>/<spouse_id>', methods=['DELETE'])
def remove_spouse(client_id, spouse_id):
    success = service.remove_spouse(client_id, spouse_id)
    if not success:
        return jsonify({'message': 'Client or spouse not found'}), 404
    return jsonify({'message': 'Spouse removed'}), 200