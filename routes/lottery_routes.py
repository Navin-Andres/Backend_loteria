from flask import Blueprint, jsonify, request
from models import db, LotteryResult, FrequentNumber, Statistics
import random
import logging
from collections import Counter
from datetime import datetime

logger = logging.getLogger(__name__)
lottery_bp = Blueprint('lottery', __name__)

def get_top_3_frequent():
    try:
        # Obtener números frecuentes de la base de datos
        frequent_numbers = FrequentNumber.query.order_by(FrequentNumber.frequency.desc()).limit(3).all()
        return [num.number for num in frequent_numbers]
    except Exception as e:
        logger.error(f"Error getting top 3 frequent numbers: {str(e)}")
        return []

@lottery_bp.route('/lottery/results', methods=['POST'])
def save_lottery_result():
    try:
        data = request.json
        numbers = data.get('numbers')
        lottery_type = data.get('type', 'standard')
        phone_number = data.get('phone_number')

        # Guardar el resultado
        new_result = LotteryResult(
            numbers=','.join(map(str, numbers)),
            type=lottery_type,
            created_by=phone_number
        )
        db.session.add(new_result)

        # Actualizar números frecuentes
        for number in numbers:
            freq_num = FrequentNumber.query.filter_by(
                number=number,
                type=lottery_type
            ).first()
            
            if freq_num:
                freq_num.frequency += 1
                freq_num.last_seen = datetime.utcnow()
            else:
                freq_num = FrequentNumber(
                    number=number,
                    type=lottery_type
                )
                db.session.add(freq_num)

        db.session.commit()
        return jsonify({"message": "Result saved successfully"}), 200
    except Exception as e:
        logger.error(f"Error saving lottery result: {str(e)}")
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@lottery_bp.route('/lottery/results', methods=['GET'])
def get_lottery_results():
    try:
        lottery_type = request.args.get('type', 'standard')
        results = LotteryResult.query.filter_by(type=lottery_type)\
            .order_by(LotteryResult.timestamp.desc())\
            .limit(10)\
            .all()
        
        return jsonify([{
            'id': r.id,
            'numbers': [int(n) for n in r.numbers.split(',')],
            'timestamp': r.timestamp.isoformat(),
            'created_by': r.created_by
        } for r in results]), 200
    except Exception as e:
        logger.error(f"Error getting lottery results: {str(e)}")
        return jsonify({"error": str(e)}), 500
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
