import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    print("Table 'users' created successfully")

    conn.execute('''
    CREATE TABLE IF NOT EXISTS prompts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT
    )
    ''')
    print("Table 'prompts' created successfully")

    conn.execute('''
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prompt_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        text_response TEXT,
        file_path TEXT,
        FOREIGN KEY(prompt_id) REFERENCES prompts(id),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')
    print("Table 'responses' created successfully")

    # Add sample prompts
    prompts = [
        ('Abstract Emotions', 'Create a piece that visually represents a complex emotion.'),
        ('Futuristic Cityscape', 'Imagine and design a city from the year 2200.'),
        ('Mythical Creatures', 'Illustrate a creature from your favorite mythology.')
    ]

    cursor = conn.cursor()
    cursor.executemany('INSERT INTO prompts (title, description) VALUES (?,?)', prompts)
    conn.commit()
    print("Sample prompts inserted successfully")

    conn.close()

if __name__ == '__main__':
    init_db()