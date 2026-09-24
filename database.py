import sqlite3

# Define the database filename as a constant

DB_NAME = 'recipes.db'

def init_db():
    # Create a connection to the SQLite database
    conn = sqlite3.connect('DB_NAME')
    cursor = conn.cursor()

    # Create the recipes table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            prep_time TEXT,
            cook_time TEXT,
            image_url TEXT,
            tags TEXT
            )
            ''')
    conn.commit()
    conn.close()

def add_recipe(title, category, ingredients, instructions, prep_time="", cook_time="", image_url="", tags=""):
    conn = sqlite3.connect('DB_NAME')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO recipes (title, category, ingredients, instructions, prep_time, cook_time, image_url, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title, category, ingredients, instructions, prep_time, cook_time, image_url, tags))

    conn.commit()
    conn.close()

def get_recipes():
    conn = sqlite3.connect('DB_NAME')
    cursor = conn.cursor()

    cursor.execute('SELECT id, title, category, ingredients, instructions, prep_time, cook_time, image_url, tags FROM recipes')
    rows = cursor.fetchall()

    conn.close()
    return rows

def delete_recipe(recipe_id):
    conn = sqlite3.connect("DB_NAME")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    conn.commit()
    conn.close()

def update_recipe(recipe_id, title, category, ingredients, instructions, prep_time="", cook_time="", image_url="", tags=""):
    conn = sqlite3.connect("DB_NAME")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE recipes
        SET title = ?, category = ?, ingredients = ?, instructions = ?, prep_time = ?, cook_time = ?, image_url = ?, tags = ?
        WHERE id = ?
    ''', (title, category, ingredients, instructions, prep_time, cook_time, image_url, tags, recipe_id))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!")
