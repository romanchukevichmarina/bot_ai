import sqlite3
 
def create_db():
    try:
        conn = sqlite3.connect('bot_messages.db')
        print('db created')
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_tables():
    statements = [ 
        "CREATE TABLE IF NOT EXISTS dialogs (user_id INTEGER PRIMARY KEY, username TEXT, message_limit INTEGER DEFAULT 5)",
        "CREATE TABLE IF NOT EXISTS messages (message_id INTEGER PRIMARY KEY, text TEXT, datetime TIMESTAMPTZ)"]
    try:
        with sqlite3.connect('bot_messages.db') as conn:
            cursor = conn.cursor()
            for statement in statements:
                cursor.execute(statement)
            
            conn.commit()
    except sqlite3.Error as e:
        print(e)