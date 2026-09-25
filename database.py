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

def add_multiple_recipes(recipes_list):
    """Insert multiple recipes into the database at once using executemany.
    recipes_list expected format:
    List of tuples -> [(title, category, ingredients, instructions, prep_time, cook_time, image_url, tags), ...]
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO recipes (title, category, ingredients, instructions, prep_time, cook_time, image_url, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', recipes_list)
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

    new_recipes_to_add = [
        (
            "Pasta cremosa de pollo y champiñones",
            "Pasta",
            "100 g de pasta (la variedad que prefieras), 150 g de pollo, 125 g de champiñones, 100 ml de nata para cocinar, 20 g de parmesano rallado",
            "Paso 1 — Cocer la pasta: Pon a hervir abundante agua con sal en una olla. Cuando rompa a hervir, añade la pasta y cuécela según las instrucciones del fabricante (normalmente 8-10 minutos) hasta que esté al dente. Escúrrela y reserva.\nPaso 2 — Saltear el pollo: Mientras la pasta se cuece, corta el pollo en dados de tamaño bocado (unos 2-3 cm). Calienta una sartén a fuego medio-alto con un poco de aceite y saltea el pollo durante 4-5 minutos, removiendo ocasionalmente, hasta que esté dorado por fuera y cocinado por dentro. Salpimienta al gusto.\nPaso 3 — Añadir los champiñones (5-6 min): Limpia los champiñones con un paño húmedo y córtalos en láminas. Añádelos a la sartén con el pollo y cocina a fuego medio durante 5-6 minutos, removiendo de vez en cuando, hasta que suelten su agua y queden tiernos y ligeramente dorados.\nPaso 4 — Incorporar la nata y el parmesano: Baja el fuego a medio-bajo. Vierte los 100 ml de nata sobre el pollo y los champiñones y añade el parmesano rallado. Remueve continuamente durante 1-2 minutos hasta que la salsa espese ligeramente y el queso se integre por completo.\nPaso 5 — Mezclar con la pasta: Añade la pasta escurrida a la sartén y mezcla bien para que se impregne de la salsa cremosa. Rectifica de sal y pimienta si es necesario. Sirve de inmediato.\nTáper: Guarda en un táper hermético. Aguanta perfectamente 3 días en la nevera.\nMicroondas: Calienta 2 minutos a potencia media. Añade 1 cucharada de agua antes de calentar para que la salsa no se seque y recupere su cremosidad.",
            "30",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfuPQ_lVsLz33SaUdElYGNZcRGjXk41cbeayY69eOhTQ&s=10",
            ""
        ),
        (
            "Arroz con pollo mediterráneo",
            "Platos principales",
            "100 g de arroz, 150 g de pollo, ½ cebolla, 150 g de tomate triturado, 250 ml de caldo (de pollo o verduras), Pimentón dulce al gusto",
            "Paso 1 — Dorar el pollo: Corta el pollo en trozos medianos. Calienta una cazuela o sartén honda a fuego medio-alto con un poco de aceite. Añade el pollo y dóralo durante 4-5 minutos por cada lado, hasta que tenga un color dorado uniforme. Retira y reserva.\nPaso 2 — Pochar la cebolla: En la misma cazuela, baja el fuego a medio. Pica la cebolla muy fina y añádela. Sofríe durante 5-6 minutos, removiendo con frecuencia, hasta que esté transparente y blanda. Si se pega, añade un chorrito de agua.\nPaso 3 — Añadir tomate y pimentón: Incorpora el tomate triturado y el pimentón dulce. Mezcla bien y cocina a fuego medio durante 3-4 minutos, removiendo, hasta que el tomate pierda el exceso de agua y la mezcla se concentre ligeramente.\nPaso 4 — Incorporar el arroz y el caldo: Devuelve el pollo a la cazuela. Añade el arroz y remueve para que se impregne del sofrito durante 1 minuto. Vierte los 250 ml de caldo caliente, sube el fuego hasta que hierva y luego bájalo a fuego medio-bajo.\nPaso 5 — Cocinar hasta que el arroz esté hecho: Cocina sin tapar (o semitapado) durante 18-20 minutos, removiendo ocasionalmente, hasta que el arroz haya absorbido el caldo y esté en su punto. Si ves que se queda seco antes de tiempo, añade un poco más de caldo o agua caliente.\nTáper: Perfecto para preparar con antelación. Guarda en táper hermético en la nevera.\nMicroondas: Calienta 2-3 minutos a potencia media. Añade unas gotas de agua antes de calentar para que el arroz recupere su textura jugosa.",
            "40",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRew8sH_RuUcA7cE0O3Vt3CUU3mY0j6CwqX5mF6yaTiOg&s=10",
            ""
        ),
        (
            "Lentejas con chorizo y patata",
            "Platos principales",
            "250 g de lentejas cocidas (de bote o cocidas previamente), 100 g de patata, ½ chorizo, ½ cebolla, 100 g de tomate triturado, Caldo (de verduras o pollo) al gusto",
            "Paso 1 — Sofreír cebolla y chorizo: Pica la cebolla en trozos pequeños. Corta el chorizo en rodajas o medias lunas. Calienta una cazuela a fuego medio con un poco de aceite. Añade la cebolla y el chorizo y sofríe durante 5-6 minutos, removiendo, hasta que la cebolla esté blanda y el chorizo haya soltado su grasa y aroma.\nPaso 2 — Añadir la patata en dados: Pela la patata y córtala en dados de unos 2 cm. Añádela a la cazuela y mezcla bien con el sofrito durante 1-2 minutos para que se impregne de los sabores.\nPaso 3 — Incorporar tomate y caldo: Incorpora el tomate triturado y remueve. Vierte el caldo hasta cubrir todos los ingredientes (aproximadamente 300-400 ml). Sube el fuego hasta que hierva y luego bájalo a fuego medio.\nPaso 4 — Cocinar 20 minutos: Cocina a fuego medio durante 20 minutos, hasta que la patata esté tierna al pincharla con un tenedor. Rectifica de sal si es necesario (el chorizo ya aporta sal).\nPaso 5 — Añadir las lentejas (últimos 5 min): Escurre y aclara las lentejas cocidas bajo el grifo. Añádelas a la cazuela durante los últimos 5 minutos de cocción, removiendo suavemente para que se integren sin deshacerse. Deja que cojan temperatura y absorban el sabor del guiso.\nTáper: Este guiso mejora notablemente al día siguiente, cuando los sabores se asientan. Guarda en táper hermético en la nevera hasta 3 días.\nMicroondas: Calienta 2-3 minutos a potencia media. Si ha espesado mucho, añade un poco de agua o caldo antes de calentar.",
            "35",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTXEgqJHGFF4iwjpvr8QY-maLae2IL6vn8PDROdI9DEbQ&s=10",
            "",
        ),
        (
            "Pasta boloñesa",
            "Pasta",
            "100 g de pasta (espaguetis, penne o similar), 125 g de carne picada (ternera, cerdo o mixta), ½ cebolla, 200 g de tomate triturado, 20 g de queso rallado",
            "Paso 1 — Sofreír la cebolla: Pica la cebolla muy fina. Calienta una sartén a fuego medio con un poco de aceite. Añade la cebolla y sofríe durante 6-7 minutos, removiendo con frecuencia, hasta que esté completamente blanda y ligeramente dorada.\nPaso 2 — Añadir la carne y dorarla: Sube el fuego a medio-alto. Añade la carne picada y dórala durante 4-5 minutos, desmenuzándola con una cuchara de madera para que quede suelta y sin grumos. Salpimienta al gusto.\nPaso 3 — Agregar el tomate: Incorpora el tomate triturado, mezcla bien con la carne y la cebolla. Baja el fuego a medio-bajo.\nPaso 4 — Cocinar la salsa (15-20 min): Cocina la salsa a fuego medio-bajo durante 15-20 minutos, removiendo de vez en cuando, hasta que el tomate pierda su acidez, la salsa espese y los sabores se concentren. Si se seca demasiado, añade un chorrito de agua.\nPaso 5 — Cocer la pasta: Mientras la salsa termina, cuece la pasta en abundante agua con sal según las instrucciones del fabricante. Escúrrela reservando un poco del agua de cocción.\nPaso 6 — Mezclar y terminar con queso: Mezcla la pasta escurrida con la salsa boloñesa en la sartén. Si la salsa está muy espesa, añade una cucharada del agua de cocción de la pasta para aligerar. Sirve con el queso rallado por encima.\nTáper: Guarda en táper hermético. La salsa boloñesa aguanta 3-4 días en nevera y también se puede congelar.\nMicroondas: Calienta 2-3 minutos a potencia media. Añade una cucharada de agua si la pasta ha absorbido demasiada salsa.",
            "35",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRzQdW8x2e0xOKBNyiIEy20qaYUFZlQ62FJ206eBS3Weg&s=10",
            "",
        ),
        (
            "Fajita-bowl de pollo",
            "Platos principales",
            "150 g de pollo, 100 g de arroz, 50 g de maíz (de lata o congelado), 30 g de queso rallado, Tomate picado al gusto, Pimentón dulce y comino al gusto",
            "Paso 1 — Cocinar el arroz: Pon el arroz en un cazo con el doble de su volumen en agua y una pizca de sal. Lleva a ebullición, baja el fuego al mínimo, tapa y cocina durante 15-18 minutos hasta que el agua se absorba por completo. Retira del fuego y deja reposar 5 minutos tapado.\nPaso 2 — Saltear el pollo con las especias: Corta el pollo en tiras o dados. Calienta una sartén a fuego medio-alto con un poco de aceite. Añade el pollo y espolvorea el pimentón dulce y el comino al gusto. Saltea durante 6-8 minutos, removiendo, hasta que el pollo esté bien cocinado y ligeramente dorado con las especias.\nPaso 3 — Preparar el maíz y el tomate: Si usas maíz de lata, escúrrelo y acláralo. Si es congelado, caliéntalo en el microondas 1 minuto. Pica el tomate en dados pequeños.\nPaso 4 — Montar el bowl: En el táper o en un plato hondo, coloca primero el arroz como base. Añade encima el pollo con las especias, el maíz, el tomate picado y termina con el queso rallado por encima.\nTáper: Guarda todos los ingredientes juntos en un táper hermético. El queso puede guardarse aparte si prefieres que no se funda.\nMicroondas: Calienta 2 minutos a potencia media. El queso se fundirá ligeramente con el calor, lo que añade cremosidad al bowl.",
            "35",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSCuWdSdABRaxpFSUyLh6mgMw39zPRX4h8F35LSeP_wug&s=10",
            "",
        ),
    (
    "Macarrones con pollo y mozzarella",
    "Pasta",
    "100 g de macarrones, 150 g de pollo, 150 g de tomate (triturado o natural picado), 50 g de mozzarella",
    "Paso 1 — Cocer la pasta: Cuece los macarrones en abundante agua con sal según las instrucciones del fabricante (normalmente 8-10 minutos) hasta que estén al dente. Escúrrelos y reserva.\nPaso 2 — Cocinar el pollo: Corta el pollo en dados o tiras. Calienta una sartén a fuego medio-alto con un poco de aceite. Cocina el pollo durante 5-6 minutos, removiendo, hasta que esté dorado y bien cocinado por dentro. Salpimienta al gusto.\nPaso 3 — Añadir el tomate: Añade el tomate a la sartén con el pollo. Mezcla bien y cocina a fuego medio durante 3-4 minutos hasta que el tomate se integre y la salsa se concentre ligeramente.\nPaso 4 — Mezclar y añadir la mozzarella: Incorpora los macarrones escurridos a la sartén y mezcla bien con el pollo y el tomate. Corta o desmenuza la mozzarella y distribúyela por encima.\nPaso 5 — Gratinar (opcional, 5 min): Opcional pero muy recomendable: si tienes horno o gratinador en casa, introduce la sartén o una fuente apta para horno y gratina durante 5 minutos a 200 °C hasta que la mozzarella se funda y dore ligeramente. Puedes llevarlo ya preparado al trabajo.\nTáper: Guarda en táper hermético. Si lo has gratinado, la mozzarella se mantendrá fundida y sabrosa al recalentar.\nMicroondas: Calienta 2-3 minutos a potencia media. Añade una cucharada de agua si la pasta está muy seca.",
    "30",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQXsoeubn8QXCyZMEmNhm11zumZrXl0Sto74D30LMIrwQ&s=10",
    "",
    ),
    ]
    add_multiple_recipes(new_recipes_to_add)
    print(f"Successfully added {len(new_recipes_to_add)} new recipes!")
