  #port 5432
"""
    In PgAdmin, execute the following command:
    CREATE USER al01 WITH PASSWORD 'actionlearning1';
    GRANT ALL PRIVILEGES ON DATABASE action_learning_reviews TO al01;
    CREATE TABLE customer_reviews (
    id SERIAL PRIMARY KEY,
    ip VARCHAR(45),
    satisfaction INT,
    commentary TEXT
    );
"""

import streamlit as st
import psycopg2
from googletrans import Translator
import socket

# Translation dictionaries
translations = {
    "title": {
        "English": "Customer Reviews",
        "Français": "Avis des clients",
        "Español": "Opiniones de los clientes"
    },
    "rate_satisfaction": {
        "English": "### Please rate your level of satisfaction with the app (0-5):",
        "Français": "### Veuillez évaluer votre niveau de satisfaction avec l'application (0-5) :",
        "Español": "### Por favor, califique su nivel de satisfacción con la aplicación (0-5):"
    },
    "additional_comments": {
        "English": "### Any additional comments?",
        "Français": "### Des commentaires supplémentaires ?",
        "Español": "### ¿Algún comentario adicional?"
    },
    "submit_button": {
        "English": "Submit",
        "Français": "Soumettre",
        "Español": "Enviar"
    },
    "success_message": {
        "English": "Thank you for your feedback!",
        "Français": "Merci pour votre retour !",
        "Español": "¡Gracias por sus comentarios!"
    },
    "error_message": {
        "English": "An error occurred:",
        "Français": "Une erreur s'est produite :",
        "Español": "Ocurrió un error:"
    }
}

# Initialize the translator
translator = Translator()

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="action_learning_reviews",
        user="postgres",
        password="actionlearning1",
        port='5432'
    )

def get_user_ip():
    return socket.gethostbyname(socket.gethostname())

def translate_comment(comment, lang):
    if lang != 'en':
        translated = translator.translate(comment, src=lang, dest='en')
        return translated.text
    return comment

def save_review_to_db(ip, satisfaction, commentary):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO customer_reviews (ip, satisfaction, commentary) VALUES (%s, %s, %s)",
        (ip, satisfaction, commentary)
    )
    connection.commit()
    cursor.close()
    connection.close()

def customer_reviews_page():
    lang = st.session_state.get("selected_lang", "English")
    
    st.title(translations["title"][lang])
    st.write(translations["rate_satisfaction"][lang])
    satisfaction = st.radio("", [0, 1, 2, 3, 4, 5])

    st.write(translations["additional_comments"][lang])
    commentary = st.text_area("")

    if st.button(translations["submit_button"][lang]):
        try:
            user_ip = get_user_ip()
            translated_commentary = translate_comment(commentary, lang)
            save_review_to_db(user_ip, satisfaction, translated_commentary)
            st.success(translations["success_message"][lang])
        except Exception as e:
            st.error(f"{translations['error_message'][lang]} {e}")

if __name__ == "__main__":
    customer_reviews_page()
