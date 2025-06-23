from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import random
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:*", "https://backend-loteria-sn12.onrender.com"]}})  # Ajusta la URL del frontend

# Cargar y procesar el archivo Excel
def load_historical_data(file_path='/tmp/baloto1.xlsx'):
    try:
        df = pd.read_excel(file_path, sheet_name='Hoja1')
        print("Loaded DataFrame:", df)
        if df.empty:
            raise Exception("Archivo Excel vacío")
        
        def parse_resultado(resultado):
            numbers = [int(num.strip()) for num in resultado.split('-')]
            if len(numbers) != 6 or not all(1 <= num <= 43 for num in numbers[:5]) or not 1 <= numbers[5] <= 16:
                raise ValueError("Formato de balotas inválido")
            return numbers
        
        df['balotas'] = df['resultado'].apply(parse_resultado)
        print("After applying parse_resultado:", df)
        if 'balotas' in df.columns and not df['balotas'].empty:
            df[['balota1', 'balota2', 'balota3', 'balota4', 'balota5', 'balota6']] = pd.DataFrame(df['balotas'].tolist(), index=df.index)
        else:
            print("No 'balotas' column or data available")
            return pd.DataFrame()
        return df
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return pd.DataFrame()

# Obtener los tres números más frecuentes para balotas 1-43
def get_top_3_frequent():
    df = load_historical_data()
    if df.empty:
        return random.sample(range(1, 44), 3)  # Fallback if no data
    all_numbers = pd.concat([df[f'balota{j}'] for j in range(1, 6)])
    top_3 = all_numbers.value_counts().head(3).index.tolist()
    return top_3 if top_3 else random.sample(range(1, 44), 3)

# Endpoint para subir el archivo Excel
@app.route('/api/upload', methods=['POST'])
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
            print(f"Archivo guardado en {file_path}")
            return jsonify({'message': 'File uploaded successfully'}), 200
        return jsonify({'error': 'Invalid file format'}), 400
    except Exception as e:
        print(f"Error en upload_file: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Nuevo endpoint para procesar el archivo
@app.route('/api/process', methods=['GET'])
def process_file():
    df = load_historical_data()
    if df.empty:
        return jsonify({'error': 'No data available or file invalid'}), 400
    top_three = get_top_3_frequent()
    return jsonify({'top_three_numbers': top_three}), 200

# Endpoint para generar el sorteo
@app.route('/api/sorteo', methods=['GET'])
def sorteo():
    top_three = get_top_3_frequent()
    available_numbers = [x for x in range(1, 44) if x not in top_three]
    three_random = random.sample(available_numbers, 3)
    all_five_balotas = top_three + three_random
    random.shuffle(all_five_balotas)
    sixth_balota = random.randint(1, 16)
    balotas = all_five_balotas
    balotas.append(sixth_balota)
    print(f"Generated balotas: {balotas}")
    if not (1 <= sixth_balota <= 16):
        print(f"Warning: Sixth balota {sixth_balota} is out of range 1-16")
    return jsonify({'balotas': balotas})

# Endpoint para obtener estadísticas
@app.route('/api/statistics', methods=['GET'])
def statistics():
    top_three = get_top_3_frequent()
    return jsonify({'top_three_numbers': top_three})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)