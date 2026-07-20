from flask import Flask

from controllers.child_controller import child_bp
from controllers.client_controller import client_bp
from controllers.spouses_controller import spouse_bp
from flask import Flask
from flask_cors import CORS
app = Flask(__name__)

CORS(app)
# Wrapper ל-ASGI אם רוצים להריץ על uvicorn
from asgiref.wsgi import WsgiToAsgi
# register routes
app.register_blueprint(client_bp, url_prefix='/clients')
app.register_blueprint(child_bp, url_prefix='/child')
app.register_blueprint(spouse_bp, url_prefix='/spouses')
asgi_app = WsgiToAsgi(app)
if __name__ == '__main__':
    app.run(debug=True)
