from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .lottery import LotteryResult, FrequentNumber, Statistics
from .session import Session
from .user import User

__all__ = ['db', 'LotteryResult', 'FrequentNumber', 'Statistics', 'Session', 'User']
