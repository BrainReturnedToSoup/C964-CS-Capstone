from flask import Flask
from pathlib import Path
from back_end.controllers.root.bp import bp as root_bp

parent_path=Path(__file__).parent
template_folder_path=parent_path / "templates"
ssl_context_path=parent_path / "static" / "https_assets"

def create_app():
    app = Flask(__name__, template_folder=template_folder_path)
    print(f"template_folder_path={template_folder_path}")
    app.url_map.strict_slashes = False
    app.register_blueprint(root_bp)
    app.config["TESTING"] = True
    return app

if __name__ == "__main__":
    create_app().run(ssl_context="adhoc")