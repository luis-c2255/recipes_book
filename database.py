import os

import libsql
import streamlit as st


def _get_credentials():
    """Read Turso connection details from Streamlit secrets.

    Locally these come from .streamlit/secrets.toml; on Streamlit Community
    Cloud they come from the app's Settings -> Secrets. Falling back to
    environment variables lets `python database.py` still work standalone.
    """
    url = None
    token = None
    try:
        url = st.secrets["TURSO_DATABASE_URL"]
        token = st.secrets["TURSO_AUTH_TOKEN"]
    except Exception:
        pass

    url = url or os.environ.get("TURSO_DATABASE_URL")
    token = token or os.environ.get("TURSO_AUTH_TOKEN")

    if not url or not token:
        raise RuntimeError(
            "Missing Turso credentials. Set TURSO_DATABASE_URL and "
            "TURSO_AUTH_TOKEN in .streamlit/secrets.toml (or as environment "
            "variables), then try again."
        )
    return url, token


def get_connection():
    url, token = _get_credentials()
    return libsql.connect(database=url, auth_token=token)


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
        except Exception:
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