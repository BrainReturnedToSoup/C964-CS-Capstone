from flask import Flask
from .controllers.root.blueprint import bp as full_app_bp

app = Flask(__name__)
app.register_blueprint(full_app_bp)

__all__ = ["app"]   