import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path='pokemon_game.db'):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        """Создаёт соединение с базой"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Создаёт таблицы, если их нет"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                pokemon_balance INTEGER DEFAULT 0,
                ton_balance REAL DEFAULT 0,
                pokemon_per_hour INTEGER DEFAULT 0,
                mint_bought INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ База данных SQLite готова")
    
    def get_user(self, user_id, username=None, first_name=None):
        """Получает пользователя или создаёт нового"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Ищем пользователя
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        
        if not user and username is not None:
            # Создаём нового
            cursor.execute('''
                INSERT INTO users (user_id, username, first_name)
                VALUES (?, ?, ?)
            ''', (user_id, username, first_name))
            conn.commit()
            
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()
            print(f"🆕 Новый пользователь: {user_id}")
        
        conn.close()
        return user
    
    def update_pokemon_balance(self, user_id, amount):
        """Изменяет баланс покемонов"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users 
            SET pokemon_balance = pokemon_balance + ? 
            WHERE user_id = ?
        ''', (amount, user_id))
        conn.commit()
        conn.close()