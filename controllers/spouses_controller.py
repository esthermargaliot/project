# controllers/spouse_controller.py
from flask import Blueprint, request, jsonify
from services.spouse_service import SpouseService

spouse_bp = Blueprint('spouse_bp', __name__)
service = SpouseService()

# קבלת כל בני הזוג של לקוח
@spouse_bp.route('/<client_id>', methods=['GET'])
def get_spouses(client_id):
    spouses = service.get_spouses(client_id)
    if spouses is None:
        return jsonify({'message': 'Client not found'}), 404
    return jsonify(spouses), 200

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