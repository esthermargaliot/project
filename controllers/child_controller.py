# controllers/child_controller.py
from flask import Blueprint, request, jsonify
from services.child_service import ChildService

child_bp = Blueprint('child_bp', __name__)
child_service = ChildService()

@child_bp.route('/', methods=['GET'])
def get_children():
    children = child_service.get_all_children()
    return jsonify(children)

@child_bp.route('/', methods=['POST'])
def create_child():
    data = request.json
    child_service.create_child(data)
    return jsonify({'message': 'Child created'}), 201

@child_bp.route('/<int:child_id>', methods=['PUT'])
def update_child(child_id):
    data = request.json
    updated = child_service.update_child(child_id, data)
    if not updated:
        return jsonify({'message': 'Child not found'}), 404
    return jsonify({'message': 'Child updated'})

@child_bp.route('/<int:child_id>', methods=['DELETE'])
def delete_child(child_id):
    deleted = child_service.delete_child(child_id)
    if not deleted:
        return jsonify({'message': 'Child not found'}), 404
    return jsonify({'message': 'Child deleted'})