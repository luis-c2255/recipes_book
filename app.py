from urllib.parse import urlparse

import requests
import streamlit as st

from database import init_db, get_recipes, add_recipe, delete_recipe, update_recipe

# Set up page configuration and title
st.set_page_config(page_title="Mis Recetas", layout="wide")

CATEGORIES = ["Platos principales", "Pasta", "Postres", "Ensaladas", "Sopas", "Otro"]

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Lacquer&family=Cutive+Mono&display=swap');

    /* Apply Lacquer to titles, headers, and subheaders */
    h1, h2, h3, h4, h5, h6, [data-testid="stHeader"] {
        font-family: 'Lacquer', sans-serif !important;
        letter-spacing: 1px;
        text-align: center;
        color: #eb5e28 !important;
    }

    /* Apply Cutive Mono to standard body text and inputs */
    html, body, p, span, label, input, textarea, [data-testid="stMarkdown"] {
        font-family: 'Cutive Mono', monospace !important;
    }

    /* Style recipe expander cards with Dust Grey borders */
    [data-testid="stExpander"] {
        border: 1px solid #ccc5b9 !important;
        border-radius: 8px !important;
        background-color: #403d39 !important;
        margin-bottom: 0.75rem;
    }

    /* Keep the expander header readable and cleanly spaced */
    [data-testid="stExpander"] summary {
        color: #eb5e28 !important;
        font-weight: bold !important;
    }

    /* Ensure icons retain their native icon font */
    [data-testid="stExpanderToggleIcon"], [data-testid="stIconMaterial"], [class*="material-symbols"] {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
    }

    /* Style tag pills with spicy paprika border and accent tone */
    code {
        color: #eb5e28 !important;
        background-color: #252422 !important;
        border: 1px solid #eb5e28 !important;
        border-radius: 12px !important;
        padding: 0.15rem 0.5rem !important;
        font-family: inherit !important;
        font-weight: bold !important;
    }

    /* Style primary form buttons with spicy paprika */
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #eb5e28 !important;
        color: #fffcf2 !important;
        border: none !important;
        border-radius: 6px !important;
        font-family: 'Cutive Mono', monospace !important;
        letter-spacing: 1px !important;
        transition: 0.2s ease-in-out;
    }

    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #d44d1b !important;
        color: #fffcf2 !important;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title("Mis Recetas")

# Ensure the database is initialized
init_db()

MAX_IMAGE_BYTES = 8 * 1024 * 1024  # 8 MB ceiling so a huge file can't stall the app


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_image(url: str):
    """Download an image URL server-side.

    Returns the raw bytes when the URL really is a reachable image, or None
    otherwise, so the caller can show a proper message instead of leaving a
    broken image in the page.
    """
    if not url or not url.strip():
        return None

    parsed = urlparse(url.strip())
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return None

    try:
        response = requests.get(
            url.strip(),
            timeout=5,
            stream=True,
            headers={"User-Agent": "Mozilla/5.0 (MisRecetas)"},
        )
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "").split(";")[0].strip().lower()
        if not content_type.startswith("image/"):
            return None

        data = bytearray()
        for chunk in response.iter_content(chunk_size=64 * 1024):
            data.extend(chunk)
            if len(data) > MAX_IMAGE_BYTES:
                return None
        return bytes(data)
    except requests.RequestException:
        return None
    finally:
        try:
            response.close()
        except (NameError, UnboundLocalError):
            pass

if "editing_recipe_id" not in st.session_state:
    st.session_state.editing_recipe_id = None

# Success message from the previous run (survives the rerun after saving)
if "flash_message" not in st.session_state:
    st.session_state.flash_message = None


@st.dialog("Editar Receta")
def show_edit_dialog(recipe_to_edit):
    """Dialog for editing an existing recipe. Defined once, at module level."""
    with st.form("edit_recipe_form"):
        edit_title = st.text_input("Título de la Receta", value=recipe_to_edit[1] or "")
        edit_category = st.selectbox(
            "Categoría",
            CATEGORIES,
            index=CATEGORIES.index(recipe_to_edit[2]) if recipe_to_edit[2] in CATEGORIES else 0,
        )
        edit_ingredients = st.text_area("Ingredientes", value=recipe_to_edit[3] or "")
        edit_instructions = st.text_area("Instrucciones", value=recipe_to_edit[4] or "")
        edit_prep = st.text_input("Tiempo de Preparación", value=recipe_to_edit[5] or "")
        edit_cook = st.text_input("Tiempo de Cocinado", value=recipe_to_edit[6] or "")
        edit_image = st.text_input("URL de la Imagen (opcional)", value=recipe_to_edit[7] or "")
        edit_tags = st.text_input("Etiquetas (separadas por comas)", value=recipe_to_edit[8] or "")

        save_col, cancel_col = st.columns(2)
        with save_col:
            saved = st.form_submit_button("Guardar Cambios")
        with cancel_col:
            cancelled = st.form_submit_button("Cancelar")

        if saved:
            if not edit_title.strip():
                st.error("El título no puede estar vacío.")
            else:
                update_recipe(
                    recipe_to_edit[0], edit_title, edit_category,
                    edit_ingredients, edit_instructions,
                    edit_prep, edit_cook, edit_image, edit_tags
                )
                st.session_state.editing_recipe_id = None
                st.session_state.flash_message = f"Receta '{edit_title}' actualizada."
                st.rerun()

        if cancelled:
            st.session_state.editing_recipe_id = None
            st.rerun()


if st.session_state.flash_message:
    st.success(st.session_state.flash_message)
    st.session_state.flash_message = None

search_col, filter_col = st.columns([2, 1])

with search_col:
    search_term = st.text_input(
        "🔍 Busca recetas por título, etiqueta o ingrediente",
        placeholder="Introduce el título, la etiqueta o la categoría de la receta",
    )

with filter_col:
    category_filter = st.selectbox("Filtrar por categoría", ["Todo"] + CATEGORIES)

# Fetch recipes from the database
recipes = get_recipes()

# Apply search and category filters
search_lower = search_term.lower().strip()
filtered_recipes = []
for recipe in recipes:
    recipe_id, title, category, ingredients, instructions, prep_time, cook_time, image_url, tags = recipe

    matches_category = (category_filter == "Todo") or (category == category_filter)

    haystack = " ".join([(title or ""), (ingredients or ""), (tags or "")]).lower()
    matches_search = search_lower in haystack

    if matches_category and matches_search:
        filtered_recipes.append(recipe)

st.subheader(f"Recetas ({len(filtered_recipes)})")

if not recipes:
    st.info("👋 ¡Tu recetario está vacío! Utiliza el formulario de la barra lateral de la izquierda para añadir tu primer plato delicioso.")
elif not filtered_recipes:
    st.warning("🔍 No hay recetas que se ajusten a tus criterios de búsqueda o filtro. Intenta modificar tu búsqueda o la selección de categorías.")
else:
    for recipe in filtered_recipes:
        recipe_id, title, category, ingredients, instructions, prep_time, cook_time, image_url, tags = recipe
        with st.expander(f"{title} ({category})"):
            if image_url:
                img_col1, img_col2, img_col3 = st.columns([1, 2, 1])
                with img_col2:
                    image_bytes = fetch_image(image_url)
                    if image_bytes is None:
                        st.caption("⚠️ No se puede cargar la imagen desde la URL proporcionada. Por favor, verifica la URL o intenta con una diferente.")
                    else:
                        try:
                            st.image(image_bytes, width="stretch")
                        except Exception:
                            st.caption("⚠️ El archivo de la URL no es una imagen válida.")

            meta_col1, meta_col2 = st.columns(2)
            with meta_col1:
                if prep_time:
                    st.markdown(f"⏱️ **Tiempo de Preparación:** {prep_time}")
            with meta_col2:
                if cook_time:
                    st.markdown(f"⏱️ **Tiempo de Cocinado:** {cook_time}")

            if tags:
                tag_list = [t.strip() for t in tags.split(",") if t.strip()]
                tag_badges = " ".join([f"`#{t}`" for t in tag_list])
                st.markdown(f"🏷️ **Tags:** {tag_badges}")

            st.markdown(f"**Ingredientes:** \n{ingredients}")
            st.markdown(f"**Instrucciones:** \n{instructions}")

            btn_col1, btn_col2 = st.columns([1, 1])
            with btn_col1:
                if st.button("✏️ Editar Receta", key=f"edit_{recipe_id}"):
                    st.session_state.editing_recipe_id = recipe_id
                    st.rerun()

            with btn_col2:
                with st.popover("🗑️ Eliminar Receta"):
                    st.write("¿Estás seguro de que quieres eliminar esta receta? Esta acción no se puede deshacer.")
                    if st.button("Sí, Eliminar", key=f"confirm_delete_{recipe_id}", type="primary"):
                        delete_recipe(recipe_id)
                        if st.session_state.editing_recipe_id == recipe_id:
                            st.session_state.editing_recipe_id = None
                        st.rerun()

# Open the edit dialog once, outside the recipe loop
if st.session_state.editing_recipe_id is not None:
    recipe_to_edit = next(
        (r for r in recipes if r[0] == st.session_state.editing_recipe_id), None
    )
    if recipe_to_edit:
        show_edit_dialog(recipe_to_edit)
    else:
        # The recipe no longer exists (e.g. it was deleted)
        st.session_state.editing_recipe_id = None

st.sidebar.header("Añadir Nueva Receta")

with st.sidebar.form("new_recipe_form", clear_on_submit=True):
    new_title = st.text_input("Título de la Receta")
    new_category = st.selectbox("Categoría", CATEGORIES)
    new_prep_time = st.text_input("Tiempo de Preparación (e.g., 25 mins)")
    new_cook_time = st.text_input("Tiempo de Cocinado (e.g., 30 mins)")
    new_image_url = st.text_input("URL de la Imagen (opcional)")
    new_tags = st.text_input("Etiquetas (separadas por comas, opcional)")
    new_ingredients = st.text_area("Ingredientes (separados por comas o enumerados)")
    new_instructions = st.text_area("Instrucciones")

    submitted = st.form_submit_button("Guardar Receta")

    if submitted:
        if new_title.strip() and new_ingredients.strip() and new_instructions.strip():
            add_recipe(
                new_title,
                new_category,
                new_ingredients,
                new_instructions,
                new_prep_time,
                new_cook_time,
                new_image_url,
                new_tags
            )
            st.session_state.flash_message = f"Receta '{new_title}' añadida exitosamente!"
            st.rerun()
        else:
            st.sidebar.error("Por favor, completa el título, los ingredientes y las instrucciones antes de enviar.")
