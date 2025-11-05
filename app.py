from flask import Flask
from flask_cors import CORS
import logging
import os
import datetime
from dotenv import load_dotenv
from models import db
from flask import jsonify
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
if not database_url:
    logger.error("DATABASE_URL no está configurada en las variables de entorno")
    raise ValueError("DATABASE_URL environment variable is not set")

# Asegurarse de que la URL use postgresql:// en lugar de postgres://
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

logger.info(f"Configurando base de datos con URL: {database_url.split('@')[1]}")  # Log seguro sin credenciales

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Esto mostrará las consultas SQL en los logs

try:
    db.init_app(app)
    # Verificar la conexión
    with app.app_context():
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        logger.info("Conexión a la base de datos establecida exitosamente")
except Exception as e:
    logger.error(f"Error al conectar con la base de datos: {str(e)}")
    raise

# Manejador de errores global
@app.errorhandler(Exception)
def handle_error(e):
    logger.error(f"Error no manejado: {str(e)}")
    return jsonify({
        "error": "Internal server error",
        "message": str(e),
        "type": str(type(e))
    }), 500

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(lottery_bp, url_prefix='/api')
app.register_blueprint(file_bp, url_prefix='/api')

@app.route('/')
def home():
    try:
        # Verificar la conexión a la base de datos
        db.session.execute('SELECT 1')
        db_status = "Database connection OK"
    except Exception as e:
        db_status = f"Database error: {str(e)}"

    return {
        "message": "Backend server is running",
        "status": {
            "database": db_status,
            "timestamp": datetime.datetime.now().isoformat(),
            "env_vars": {
                "database_url_set": bool(os.getenv('DATABASE_URL'))
            }
        }
    }, 200

@app.route('/status')
def status():
    try:
        # Verificar base de datos
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        db_status = "Connected"
    except Exception as e:
        db_status = f"Error: {str(e)}"

    return jsonify({
        "status": "up",
        "timestamp": datetime.datetime.now().isoformat(),
        "database": {
            "status": db_status,
            "url_configured": bool(os.getenv('DATABASE_URL'))
        },
        "environment": os.getenv('FLASK_ENV', 'production')
    })

@app.route('/init')
def init_db():
    try:
        db.create_all()
        tables = db.engine.table_names()
        return {
            "message": "Database initialized successfully",
            "tables": tables,
            "database_url": os.getenv('DATABASE_URL', 'Not set').split('@')[1] if os.getenv('DATABASE_URL') else 'Not set'
        }, 200
    except Exception as e:
        return {"error": str(e), "type": str(type(e))}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)