import sqlite3

def create_tables():
    conn = sqlite3.connect('db/database.db', check_same_thread=False)
    statements = [
        """CREATE TABLE IF NOT EXISTS messages (message_id INTEGER PRIMARY KEY, user_id INTEGER, text TEXT, datetime TIMESTAMPTZ)"""]
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            for statement in statements:
                cursor.execute(statement)
        
            conn.commit()
    except sqlite3.Error as e:
        print(e)

def insert_messages(message_id: int, user_id: int, text: str, datetime: str):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO messages (message_id, user_id, text, datetime) VALUES (?, ?, ?, ?)', (message_id, user_id, text, datetime))
        conn.commit()
    
def get_last_commands(user_id: int):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT text FROM messages WHERE user_id = ? ORDER BY datetime DESC LIMIT 3", (user_id, ))
        result = cursor.fetchall()
        if result:
            return result