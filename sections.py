import streamlit as st
import os

def show(manager):
    st.header("🗂️ Gestione Sezioni Avanzata")

    def get_all_leaf_paths(sections):
        result = []

        def recursive_search(d, path=""):
            for k, v in d.items():
                new_path = f"{path}/{k}" if path else k
                if any(isinstance(val, dict) for val in v.values()):
                    recursive_search(v, new_path)
                else:
                    result.append(new_path)

        recursive_search(sections)
        return result

    def render_section(path, section):
        st.markdown(f"### 📁 {path}")

        # Pulsante elimina sezione con conferma
        if st.button(f"🗑️ Elimina sezione '{path}'", key=f"del_section_{path}"):
            st.session_state[f"confirm_delete_{path}"] = True

        if st.session_state.get(f"confirm_delete_{path}", False):
            st.warning(f"⚠️ Sei sicuro di voler eliminare la sezione '{path}'?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Conferma eliminazione", key=f"confirm_yes_{path}"):
                    manager.delete_section(path)
                    st.success(f"Sezione '{path}' eliminata.")
                    st.session_state[f"confirm_delete_{path}"] = False
                    st.rerun()
            with col2:
                if st.button("❌ Annulla", key=f"confirm_no_{path}"):
                    st.session_state[f"confirm_delete_{path}"] = False

        for deck_num in ["1", "2", "3", "4"]:
            cards = section.get(deck_num, [])
            if cards:
                st.markdown(f"#### 📦 Mazzo {deck_num} ({len(cards)} carte)")
                for i, card in enumerate(cards):
                    st.markdown(f"**Domanda:** {card['question']}")
                    if st.button("✏️ Modifica", key=f"mod_{path}_{deck_num}_{i}"):
                        with st.form(f"form_mod_{path}_{deck_num}_{i}"):
                            new_q = st.text_area("Modifica Domanda", value=card['question'])
                            new_a = st.text_area("Modifica Risposta", value=card['answer'])

                            st.markdown("**📷 Immagini domanda (solo visualizzazione):**")
                            for img in card.get("question_images", []):
                                st.image(img, use_container_width=True)

                            st.markdown("**📷 Immagini risposta (solo visualizzazione):**")
                            for img in card.get("answer_images", []):
                                st.image(img, use_container_width=True)

                            submitted = st.form_submit_button("💾 Salva modifiche")
                            if submitted:
                                manager.update_card(path, deck_num, i, new_q, new_a)
                                st.success("Carta modificata.")
                                st.rerun()

                    if st.button("🗑️ Elimina", key=f"del_{path}_{deck_num}_{i}"):
                        st.session_state[f"confirm_card_{path}_{deck_num}_{i}"] = True

                    if st.session_state.get(f"confirm_card_{path}_{deck_num}_{i}", False):
                        st.warning("⚠️ Sei sicuro di voler eliminare questa carta?")
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✅ Elimina", key=f"yes_card_{path}_{deck_num}_{i}"):
                                manager.delete_card(path, deck_num, i)
                                st.success("Carta eliminata.")
                                st.session_state[f"confirm_card_{path}_{deck_num}_{i}"] = False
                                st.rerun()
                        with col2:
                            if st.button("❌ Annulla", key=f"no_card_{path}_{deck_num}_{i}"):
                                st.session_state[f"confirm_card_{path}_{deck_num}_{i}"] = False

    leaf_sections = get_all_leaf_paths(manager.sections)

    if leaf_sections:
        selected = st.selectbox("📂 Seleziona una sezione:", leaf_sections)
        render_section(selected, manager.get_section(selected))
    else:
        st.info("Nessuna sezione disponibile.")
