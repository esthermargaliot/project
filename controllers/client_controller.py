from selenium import webdriver

from selenium.webdriver.common.by import By
from flask import Blueprint, request, jsonify, Response
from selenium.webdriver.support.wait import WebDriverWait
from db_connection import get_session
from mappers.form_mapper import map_form_to_db, detect_children_count, click_add_child
from mappers.html_filler import fill_html
from repository.child_repository import ChildRepository
from repository.client_repository import ClientRepository
from repository.spouses_repository import SpouseRepository
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

@client_bp.route("/map")
def map_data():
    return {
        "client.firstName": "דוד",
        "client.lastName": "כהן"
    }
# 🔥 POST - העלאת ספח ועיבוד מלא (החלפה של מה שהיה לך)
@client_bp.route('/upload-tz', methods=['POST'])
def upload_tz():
    session = get_session()

    file_path = request.json.get("file_path")

    if not file_path:
        return jsonify({"error": "file_path is required"}), 400

    client, spouse, child = tz_service.process_tz_file(file_path)

    try:
        client_repo = ClientRepository(session)
        spouse_repo = SpouseRepository(session)
        child_repo = ChildRepository(session)

        client_repo.add(client)

        if spouse:
            spouse_repo.add(spouse)

        if child:
            child_repo.add(child)

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
@client_bp.route("/fill", methods=["POST"])
def fill():
    session = get_session()

    data = request.get_json()
    client_id = data.get("id")

    client = ClientRepository(session).get_by_id(client_id)
    print("CLIENT ID:", client_id)
    print("CLIENT:", client)
    if client is None:
        return jsonify({
            "error": "Client not found",
            "id": client_id
        }), 404


    flat_data = ClientService().flatten_client(client)

    return jsonify({
        "childrenCount": detect_children_count(flat_data)
    })
@client_bp.route("/map", methods=["POST"])
def map():

    session = get_session()

    data = request.get_json()

    client_id = data.get("id")


    client = ClientRepository(session).get_by_id(client_id)

    flat_data = ClientService().flatten_client(client)


    html_sources = []


    # HTML של הדף הראשי
    main_html = data.get("html")

    if main_html:
        html_sources.append(main_html)



    # HTML של iframe-ים
    for frame in data.get("frames", []):

        frame_html = frame.get("html")

        if frame_html:
            html_sources.append(frame_html)



    print(
        "HTML sources:",
        len(html_sources)
    )


    mapped = {}


    for html in html_sources:

        print(
            "Mapping HTML length:",
            len(html)
        )


        result = map_form_to_db(
            html,
            flat_data
        )


        mapped.update(result)



    return jsonify({
        "mapped": mapped
    })