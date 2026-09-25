import os
import sqlite3

# Anchor the database file to this script's own folder, not to whatever
# directory the app happens to be launched from. Without this, running
# `streamlit run script.py` from a different terminal/working directory
# silently creates a brand-new, empty recipes.db elsewhere on disk --
# which looks exactly like "all my recipes disappeared".
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recipes.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
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
            cook_time TEXT
            )
            ''')
    # Safely add columns if this table was created in an earlier step
    for column in ['prep_time', 'cook_time', "image_url", "tags"]:
        try:
            cursor.execute(f"ALTER TABLE recipes ADD COLUMN {column} TEXT")
        except sqlite3.OperationalError:
            # Column already exists, ignore the error
            pass
    conn.commit()
    conn.close()


def add_recipe(title, category, ingredients, instructions, prep_time="", cook_time="", image_url="", tags=""):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO recipes (title, category, ingredients, instructions, prep_time, cook_time, image_url, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title, category, ingredients, instructions, prep_time, cook_time, image_url, tags))

    conn.commit()
    conn.close()


def get_recipes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT id, title, category, ingredients, instructions, prep_time, cook_time, image_url, tags FROM recipes')
    rows = cursor.fetchall()

    conn.close()
    return rows


def delete_recipe(recipe_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    conn.commit()
    conn.close()


def update_recipe(recipe_id, title, category, ingredients, instructions, prep_time="", cook_time="", image_url="", tags=""):
    conn = get_connection()
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
    # Add a sample recipe for testing purposes
    add_recipe(
        "Tomato Pasta",
        "Pasta",
        "Pasta, Tomato Sauce, Garlic, Olive oil",
        "Boil pasta. In a separate pan, sauté garlic in olive oil, add tomato sauce, and simmer. Combine with cooked pasta."
    )
    saved_recipes = get_recipes()
    print("Recipes in the database:", saved_recipes)
