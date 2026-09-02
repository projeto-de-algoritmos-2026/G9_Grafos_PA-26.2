import streamlit as st
from Grafo import GrafoCurso

st.set_page_config(page_title="Fluxograma Acadêmico", layout="wide")

if "grafo" not in st.session_state:
    st.session_state.grafo = GrafoCurso()

grafo = st.session_state.grafo

st.title("🎓 Gerador de Fluxograma Acadêmico")
st.write("Sistema para gestão e visualização de grades curriculares.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Cadastrar Matéria")
    with st.form("form_materia", clear_on_submit=True):
        id_materia = st.text_input("Código (ex: FGA0313):")
        nome_materia = st.text_input("Nome (ex: Requisitos de Software):")
        creditos = st.number_input("Créditos:", min_value=1, max_value=20, value=4)
        btn_submit = st.form_submit_button("Cadastrar")

        if btn_submit:
            try:
                grafo.adicionar_materia(id_materia, nome_materia, creditos)
                st.success(f"Matéria '{id_materia.upper()}' cadastrada com sucesso!")
            except Exception as e:
                st.error(str(e))

with col2:
    st.subheader("Matérias Cadastradas")
    if grafo.materias:
        for m_id, info in grafo.materias.items():
            st.write(f"• **{m_id}** — {info['nome']} ({info['creditos']} créditos)")
    else:
        st.info("Nenhuma matéria cadastrada até o momento.")