from mysql.connector import connect, Error
import json
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Pranav@2429',
    'database': 'rule_engine'
}

def init_db():
    try:
        with connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                # Create rules table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS rules (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        rule_string TEXT NOT NULL,
                        ast TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
    except Error as e:
        print(f"Error initializing database: {e}")
        raise

class Rule:
    def __init__(self, rule_string, ast, id=None, created_at=None, updated_at=None):
        self.id = id
        self.rule_string = rule_string
        self.ast = ast
        self.created_at = created_at
        self.updated_at = updated_at

    def save(self):
        try:
            with connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        'INSERT INTO rules (rule_string, ast) VALUES (%s, %s)',
                        (self.rule_string, self.ast)
                    )
                    conn.commit()
                    self.id = cursor.lastrowid
                    return self
        except Error as e:
            print(f"Error saving rule: {e}")
            raise

    def update(self, rule_string=None, ast=None):
        try:
            with connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    updates = []
                    values = []
                    if rule_string is not None:
                        updates.append('rule_string = %s')
                        values.append(rule_string)
                    if ast is not None:
                        updates.append('ast = %s')
                        values.append(ast)
                    
                    if updates:
                        query = f'UPDATE rules SET {", ".join(updates)} WHERE id = %s'
                        values.append(self.id)
                        cursor.execute(query, tuple(values))
                        conn.commit()
        except Error as e:
            print(f"Error updating rule: {e}")
            raise

    @staticmethod
    def get(rule_id):
        try:
            with connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        'SELECT * FROM rules WHERE id = %s',
                        (rule_id,)
                    )
                    result = cursor.fetchone()
                    if result:
                        return Rule(
                            id=result[0],
                            rule_string=result[1],
                            ast=result[2],
                            created_at=result[3],
                            updated_at=result[4]
                        )
                    return None
        except Error as e:
            print(f"Error getting rule: {e}")
            raise

    @staticmethod
    def get_multiple(rule_ids):
        try:
            with connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    placeholders = ', '.join(['%s'] * len(rule_ids))
                    cursor.execute(
                        f'SELECT * FROM rules WHERE id IN ({placeholders})',
                        tuple(rule_ids)
                    )
                    results = cursor.fetchall()
                    return [
                        Rule(
                            id=result[0],
                            rule_string=result[1],
                            ast=result[2],
                            created_at=result[3],
                            updated_at=result[4]
                        )
                        for result in results
                    ]
        except Error as e:
            print(f"Error getting multiple rules: {e}")
            raise

    @staticmethod
    def get_latest():
        try:
            with connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    cursor.execute('SELECT * FROM rules ORDER BY created_at DESC LIMIT 1')
                    result = cursor.fetchone()
                    if result:
                        return Rule(
                            id=result[0],
                            rule_string=result[1],
                            ast=result[2],
                            created_at=result[3],
                            updated_at=result[4]
                        )
                    return None
        except Error as e:
            print(f"Error getting latest rule: {e}")
            raise