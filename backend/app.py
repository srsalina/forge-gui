from flask import Flask
from flask_cors import CORS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

# Import and register Blueprints
from routes.nmap_routes import nmap_bp
app.register_blueprint(nmap_bp)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
