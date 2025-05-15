import streamlit as st
import random
from PIL import Image

def show(manager):
    st.header("📚 Modalità Ripasso")

    sections = manager.get_all_section_paths()
    if not sections:
        st.warning("Nessuna sezione disponibile.")
        return

    section = st.selectbox("📂 Seleziona una sezione:", sections)

    if st.button("🎲 Estrai una carta"):
        card_data = manager.extract_random_card(section)
        if not card_data:
            st.info("Nessuna carta disponibile per questa sezione.")
            return

        deck, card, index = card_data

        st.markdown(f"### ❓ Domanda:")
        st.markdown(card["question"])
        for img_path in card.get("question_images", []):
            st.image(img_path, use_column_width=True)

        if st.button("👁️ Mostra risposta"):
            st.markdown(f"### ✅ Risposta:")
            st.markdown(card["answer"])
            for img_path in card.get("answer_images", []):
                st.image(img_path, use_column_width=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("⬆️ Mazzo Successivo"):
                    manager.move_card(section, deck, index, direction="up")
                    st.success("Carta spostata avanti.")
            with col2:
                if st.button("➡️ Mantieni Mazzo"):
                    st.info("Carta mantenuta nel mazzo.")
            with col3:
                if st.button("⬇️ Mazzo Precedente"):
                    manager.move_card(section, deck, index, direction="down")
                    st.success("Carta spostata indietro.")
