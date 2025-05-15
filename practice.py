import streamlit as st
import random
from PIL import Image

def show(manager):
    st.header("📚 Modalità Ripasso")

    sections = manager.get_all_sections()
    if not sections:
        st.warning("Nessuna sezione disponibile.")
        return

    section = st.selectbox("📂 Seleziona una sezione:", sections)

    # === Estrai una nuova carta e salvala nello stato
    if st.button("🎲 Estrai una carta"):
        card_data = manager.extract_random_card(section)
        if not card_data:
            st.info("Nessuna carta disponibile per questa sezione.")
            return
        st.session_state["current_card"] = {
            "section": section,
            "deck": card_data[0],
            "card": card_data[1],
            "index": card_data[2]
        }
        st.session_state["show_answer"] = False  # reset risposta

    # === Mostra la carta corrente (se esiste)
    current = st.session_state.get("current_card", None)
    if current:
        card = current["card"]
        deck = current["deck"]
        index = current["index"]
        section = current["section"]

        st.markdown(f"### ❓ Domanda:")
        st.markdown(card["question"])
        for img_path in card.get("question_images", []):
            st.image(img_path, use_container_width=True)


        if st.button("👁️ Mostra risposta"):
            st.session_state["show_answer"] = True

        if st.session_state.get("show_answer", False):
            st.markdown("### ✅ Risposta:")
            st.markdown(card["answer"])
            for img_path in card.get("answer_images", []):
                st.image(img_path, use_container_width=True)


            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("⬆️ Mazzo Successivo"):
                    manager.move_card(section, deck, index, direction="up")
                    st.success("Carta spostata avanti.")
                    st.session_state["current_card"] = None
                    st.session_state["show_answer"] = False

            with col2:
                if st.button("➡️ Mantieni Mazzo"):
                    st.info("Carta mantenuta nel mazzo.")
                    st.session_state["current_card"] = None
                    st.session_state["show_answer"] = False

            with col3:
                if st.button("⬇️ Mazzo Precedente"):
                    manager.move_card(section, deck, index, direction="down")
                    st.success("Carta spostata indietro.")
                    st.session_state["current_card"] = None
                    st.session_state["show_answer"] = False
