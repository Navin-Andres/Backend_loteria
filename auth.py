import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

# Crear directorio data si no existe
os.makedirs('data', exist_ok=True)
DB_PATH = os.path.join('data', 'users.db')

def recreate_db():
    """Elimina y recrea la base de datos"""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()

def init_db():
    """Inicializa la base de datos y crea la tabla users si no existe"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS users''')  # Asegura eliminar tabla anterior
    c.execute('''CREATE TABLE users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  phone_number TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def register_user(phone_number, password):
    """Registra un nuevo usuario"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        hashed_password = generate_password_hash(password)
        c.execute('INSERT INTO users (phone_number, password) VALUES (?, ?)',
                 (phone_number, hashed_password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def verify_user(phone_number, password):
    """Verifica las credenciales del usuario"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE phone_number = ?', (phone_number,))
    result = c.fetchone()
    conn.close()
    
    if result and check_password_hash(result[0], password):
        return True
    return False
