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
@child_bp.route('/<child_id>', methods=['GET'])
def get_child_by_id(child_id):
    result = child_service.get_child_by_id(child_id)
    if not result:
        return jsonify({"error": "Child not found"}), 404
    return jsonify(result), 200
@child_bp.route('/parent/<parent_id>', methods=['GET'])
def get_children_by_parent(parent_id):
    result = child_service.get_children_by_parent_id(parent_id)
    return jsonify(result), 200
@child_bp.route('/spouse/<second_parent_id>', methods=['GET'])
def get_children_by_second_parent(second_parent_id):
    result = child_service.get_children_by_second_parent_id(second_parent_id)
    return jsonify(result), 200


@child_bp.route('/<int:child_id>', methods=['DELETE'])
def delete_child(child_id):
    deleted = child_service.delete_child(child_id)
    if not deleted:
        return jsonify({'message': 'Child not found'}), 404
    return jsonify({'message': 'Child deleted'})