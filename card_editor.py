import streamlit as st
import os
import uuid

def show(manager):
    st.header("📝 Aggiungi o Modifica Carte")

    with st.form("aggiungi_carta_form"):
        section_path = st.text_input("📌 Sezione (es: 'storia/guerre')")
        question = st.text_area("❓ Domanda")
        answer = st.text_area("✅ Risposta")

        st.markdown("### 📷 Immagini per la domanda (puoi trascinare o incollare con Ctrl+V)")
        uploaded_q_images = st.file_uploader("Domanda - immagini", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="qimg")

        st.markdown("### 📷 Immagini per la risposta (puoi trascinare o incollare con Ctrl+V)")
        uploaded_a_images = st.file_uploader("Risposta - immagini", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="aimg")

        submitted = st.form_submit_button("💾 Aggiungi carta")

    if submitted:
        q_paths, a_paths = [], []
        os.makedirs("flashcard_images", exist_ok=True)

        if uploaded_q_images:
            for file in uploaded_q_images:
                filename = f"q_{uuid.uuid4().hex}.png"
                path = os.path.join("flashcard_images", filename)
                with open(path, "wb") as f:
                    f.write(file.read())
                q_paths.append(path)

        if uploaded_a_images:
            for file in uploaded_a_images:
                filename = f"a_{uuid.uuid4().hex}.png"
                path = os.path.join("flashcard_images", filename)
                with open(path, "wb") as f:
                    f.write(file.read())
                a_paths.append(path)

        if section_path and question and answer:
            if not manager.get_section(section_path.strip()):
                manager.add_section(section_path.strip())
            manager.add_card(
                section_path.strip(),
                question.strip(),
                answer.strip(),
                question_images=q_paths,
                answer_images=a_paths
            )
            st.success("✅ Carta aggiunta con successo!")
        else:
            st.warning("⚠️ Compila tutti i campi (sezione, domanda, risposta).")
