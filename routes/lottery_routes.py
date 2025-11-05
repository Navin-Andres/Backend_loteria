from flask import Blueprint, jsonify
import pandas as pd
import random
import logging

logger = logging.getLogger(__name__)
lottery_bp = Blueprint('lottery', __name__)

def get_top_3_frequent():
    try:
        df = pd.read_excel('/tmp/baloto1.xlsx', sheet_name='Hoja1')
        all_numbers = []
        for i in range(1, 6):  # Solo las primeras 5 balotas (no incluir la roja)
            all_numbers.extend(df[f'balota{i}'].tolist())
        
        # Contar frecuencias y obtener top 3
        freq = pd.Series(all_numbers).value_counts()
        top_3 = freq.head(3).index.tolist()
        return top_3
    except Exception as e:
        print(f"Error getting frequent numbers: {e}")
        return []

@lottery_bp.route('/sorteo', methods=['GET'])
def sorteo():
    top_three = get_top_3_frequent()
    available_numbers = [x for x in range(1, 44) if x not in top_three]
    three_random = random.sample(available_numbers, 3)
    all_five_balotas = top_three + three_random
    random.shuffle(all_five_balotas)
    sixth_balota = random.randint(1, 16)
    balotas = all_five_balotas
    balotas.append(sixth_balota)
    return jsonify({'balotas': balotas})

@lottery_bp.route('/statistics', methods=['GET'])
def statistics():
    top_three = get_top_3_frequent()
    return jsonify({'top_three_numbers': top_three})
