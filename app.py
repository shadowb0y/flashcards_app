# app.py
import streamlit as st
from flashcards_manager import FlashcardManager
import card_editor
import practice
import sections

st.set_page_config(layout="wide")

manager = FlashcardManager()

menu = st.sidebar.radio("\U0001F4DA Menu", ["Aggiungi Carta", "Pratica", "Gestisci Sezioni"])

if menu == "Aggiungi Carta":
    card_editor.show(manager)

elif menu == "Pratica":
    practice.show(manager)

elif menu == "Gestisci Sezioni":
    sections.show(manager)
