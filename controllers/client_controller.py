from flask import Blueprint, request, jsonify, session

from repository import client_repository, child_repository, spouses_repository
from repository.child_repository import ChildRepository
from services.client_service import ClientService
from services.tz import TeudatZehutData

client_bp = Blueprint('client_bp', __name__)

client_service = ClientService()
tz_service = TeudatZehutData()


# 🔹 GET - כל הלקוחות
@client_bp.route('/', methods=['GET'])
def get_clients():
    clients = client_service.get_all_clients()
    return jsonify(clients)


# 🔥 POST - העלאת ספח ועיבוד מלא (החלפה של מה שהיה לך)
@client_bp.route('/upload-tz', methods=['POST'])
def upload_tz():
    file_path = request.json.get("file_path")

    if not file_path:
        return jsonify({"error": "file_path is required"}), 400

    client, spouse, child = tz_service.process_tz_file(file_path)

    try:
        client_repository.add(client)

        if spouse:
            spouses_repository.add(spouse)

        if child:
            ChildRepository.add(child)

        session.commit()

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    return jsonify({
        "client": client.to_dict(),
        "spouse": spouse.to_dict() if spouse else None,
        "child": child.to_dict() if child else None
    }), 201


# 🔹 PUT - עדכון לקוח
@client_bp.route('/<string:mispar_zehut>', methods=['PUT'])
def update_client(mispar_zehut):
    data = request.json
    updated = client_service.update_client(mispar_zehut, data)

    if not updated:
        return jsonify({'message': 'Client not found'}), 404

    return jsonify({'message': 'Client updated'})
