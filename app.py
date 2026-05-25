from flask import Flask

from controllers.child_controller import child_bp
from controllers.client_controller import client_bp
from controllers.spouses_controller import spouse_bp
from db_connection import get_session
from flask import Flask

from models.base import Base

# אם צריך

app = Flask(__name__)
# הגדרת routes

# Wrapper ל-ASGI אם רוצים להריץ על uvicorn
from asgiref.wsgi import WsgiToAsgi
asgi_app = WsgiToAsgi(app)

from repository.client_repository import ClientRepository
from repository.child_repository import ChildRepository
# from repository.spouses_repository import SpouseRepository
session = get_session()
client_repo    = ClientRepository(session)
app.register_blueprint(client_bp, url_prefix='/clients')
app.register_blueprint(child_bp, url_prefix='/child')
app.register_blueprint(spouse_bp, url_prefix='/spouses')
child_repo   = ChildRepository(session)
# spouses_repo = SpouseRepository(session)
if __name__ == '__main__':
    app.run(debug=True)
