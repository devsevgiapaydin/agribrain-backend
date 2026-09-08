from flask import Flask, render_template
from routes import main
from database import create_tables

app = Flask(
    __name__,
    template_folder="../website/templates",
    static_folder="../website/static"
)
app.secret_key = "agribrain_secret_key"
create_tables()

app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True, port=5001)

    