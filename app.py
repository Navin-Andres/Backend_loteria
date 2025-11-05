from flask import Flask
from flask_cors import CORS
import logging
import os
from dotenv import load_dotenv
from models import db
from routes.auth_routes import auth_bp
from routes.lottery_routes import lottery_bp
from routes.file_routes import file_bp

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {
    "origins": "*",
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type"],
    "expose_headers": ["Content-Type"],
    "supports_credentials": True
}})

# Configurar la base de datos
database_url = os.getenv('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(lottery_bp, url_prefix='/api')
app.register_blueprint(file_bp, url_prefix='/api')

@app.route('/')
def home():
    return {"message": "Backend server is running"}, 200

@app.route('/init')
def init_db():
    try:
        db.create_all()
        return {"message": "Database initialized successfully"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)