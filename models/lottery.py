from datetime import datetime
from . import db

class LotteryResult(db.Model):
    __tablename__ = 'lottery_results'
    
    id = db.Column(db.Integer, primary_key=True)
    numbers = db.Column(db.String(50), nullable=False)  # números separados por comas
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    type = db.Column(db.String(20), nullable=False)  # tipo de sorteo
    created_by = db.Column(db.String(15))  # número de teléfono del usuario

    def __repr__(self):
        return f'<LotteryResult {self.numbers}>'

class FrequentNumber(db.Model):
    __tablename__ = 'frequent_numbers'
    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    frequency = db.Column(db.Integer, default=1)
    last_seen = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    type = db.Column(db.String(20), nullable=False)  # tipo de sorteo

    def __repr__(self):
        return f'<FrequentNumber {self.number}>'

class Statistics(db.Model):
    __tablename__ = 'statistics'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)  # tipo de sorteo
    total_draws = db.Column(db.Integer, default=0)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data = db.Column(db.JSON)  # estadísticas adicionales en formato JSON

    def __repr__(self):
        return f'<Statistics {self.type}>'