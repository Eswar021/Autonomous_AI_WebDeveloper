# ui_app.py
from UI.flask_app import create_app

app = create_app()

if __name__ == "__main__":
    # simple local run
    app.run(host="127.0.0.1", port=5055, debug=True)
