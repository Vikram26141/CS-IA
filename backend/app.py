import os
from flask import Flask
from flask_cors import CORS
from config import Config
from routes.auth import auth_bp
from routes.coach import coach_bp

os.makedirs("data/raw", exist_ok=True)

# Serve static HTML from the frontend/public directory
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'public'))
app = Flask(__name__, static_folder=static_dir, static_url_path="")
app.config['MAX_CONTENT_LENGTH'] = 300 * 1024 * 1024  # 300 MB
app.config.from_object(Config)
CORS(app)

app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(coach_bp, url_prefix="/api")

# Root route serves the landing page
@app.route("/")
def root():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=3001)