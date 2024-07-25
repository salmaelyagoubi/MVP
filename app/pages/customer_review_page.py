import streamlit as st
import psycopg2
from googletrans import Translator
import socket

# Initialize the translator
translator = Translator()

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="action_learning_reviews",
        user="al01",
        password="actionlearning1",
        port='5342'
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

def customer_reviews_page(selected_lang):
    st.title("Customer Reviews")

    st.write("### Please rate your level of satisfaction with the app (0-5):")
    satisfaction = st.radio("", [0, 1, 2, 3, 4, 5])

    st.write("### Any additional comments?")
    commentary = st.text_area("")

    if st.button("Submit"):
        try:
            user_ip = get_user_ip()
            translated_commentary = translate_comment(commentary, selected_lang)
            save_review_to_db(user_ip, satisfaction, translated_commentary)
            st.success("Thank you for your feedback!")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Call the function to display the page
if __name__ == "__main__":
    customer_reviews_page(selected_lang='en') 
