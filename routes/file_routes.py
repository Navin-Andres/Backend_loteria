from flask import Blueprint, jsonify, request
import os
import logging

logger = logging.getLogger(__name__)
file_bp = Blueprint('file', __name__)

@file_bp.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file and file.filename.endswith('.xlsx'):
            file_path = os.path.join('/tmp', 'baloto1.xlsx')
            file.save(file_path)
            return jsonify({'message': 'File uploaded successfully'}), 200
        return jsonify({'error': 'Invalid file format'}), 400
    except Exception as e:
        logger.error("Error en upload_file: %s", e)
        return jsonify({'error': 'Internal server error'}), 500
