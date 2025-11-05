import datetime
from flask import Blueprint, jsonify, request
from auth import register_user, verify_user
import logging
from datetime import datetime
from models.session import Session
from models import db  # Importar db directamente desde models

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        logger.info('Recibida solicitud de registro')
        data = request.get_json()
        if not data:
            logger.error('No se recibieron datos JSON')
            return jsonify({'error': 'No data received'}), 400
            
        phone_number = data.get('phone_number')
        password = data.get('password')
        
        if not phone_number or not password:
            return jsonify({'error': 'Missing phone number or password'}), 400
            
        if register_user(phone_number, password):
            logger.info('Teléfono %s registrado exitosamente', phone_number)
            return jsonify({'message': 'User registered successfully'}), 201
            
        logger.warning('El número %s ya existe', phone_number)
        return jsonify({'error': 'Phone number already exists'}), 409
    except Exception as e:
        logger.error('Error en register: %s', str(e))
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    phone_number = data.get('phone_number')
    password = data.get('password')
    
    if not phone_number or not password:
        return jsonify({'error': 'Missing phone number or password'}), 400
        
    if verify_user(phone_number, password):
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/test', methods=['GET'])
def test_auth():
    return jsonify({
        'message': 'Auth routes are working',
        'endpoints': {
            'login': 'POST /api/login',
            'register': 'POST /api/register'
        }
    }), 200

@auth_bp.route('/recover-password', methods=['POST'])
def recover_password():
    try:
        data = request.get_json()
        phone_number = data.get('phone_number')
        
        if not phone_number:
            return jsonify({'error': 'Missing phone number'}), 400
            
        # Aquí implementarías la lógica de recuperación
        # Por ejemplo, enviar un SMS con un código de verificación
        # Por ahora solo simulamos una respuesta exitosa
        
        return jsonify({'message': 'Recovery code sent'}), 200
    except Exception as e:
        logger.error('Error en recover_password: %s', str(e))
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/sessions', methods=['POST'])
def create_session():
    try:
        data = request.get_json()
        phone_number = data.get('phone_number')
        
        if not phone_number:
            return jsonify({'error': 'Número de teléfono requerido'}), 400

        # Crear nueva sesión
        new_session = Session(
            phone_number=phone_number,
            timestamp=datetime.utcnow(),
            is_active=True
        )
        db.session.add(new_session)
        db.session.commit()

        return jsonify({'message': 'Sesión registrada exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
