import streamlit as st

def show(manager):
    st.header("🗂️ Gestione Sezioni")

    # === Sezioni esistenti ===
    all_paths = manager.get_all_section_paths()
    if all_paths:
        st.markdown("### 📁 Sezioni attuali:")
        for path in all_paths:
            st.markdown(f"- {path}")
    else:
        st.info("Nessuna sezione creata al momento.")

    st.markdown("---")

    # === Aggiunta nuova sezione ===
    st.markdown("### ➕ Aggiungi nuova sezione")
    new_section = st.text_input("Percorso sezione (es: 'storia/guerre/medioevo')")

    if st.button("➕ Crea sezione"):
        if new_section.strip():
            manager.add_section(new_section.strip())
            st.success(f"Sezione '{new_section}' creata con successo.")
        else:
            st.warning("Inserisci un percorso valido.")
