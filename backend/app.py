import os

from flask import Flask
from flask_cors import CORS

from routes import main
from database import create_tables

app = Flask(
    __name__,
    template_folder="../website/templates",
    static_folder="../website/static"
)

# CORS, app nesnesi OLUSTUKTAN SONRA cagrilir.
# Wix sitesi farkli bir alan adinda calisir; bu izin olmadan tarayici
# wix-fetch isteklerini engeller. Sadece /api/* yollari acilir.
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.secret_key = os.environ.get("SECRET_KEY", "agribrain_secret_key")

create_tables()

app.register_blueprint(main)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
