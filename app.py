import streamlit as st
from grafo import GrafoCurso

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
        btn_materia = st.form_submit_button("Cadastrar Matéria")

        if btn_materia:
            try:
                grafo.adicionar_materia(id_materia, nome_materia, creditos)
                st.success(f"Matéria '{id_materia.upper()}' cadastrada!")
                st.rerun()
            except Exception as e:
                st.error(str(e))

    st.subheader("Cadastrar Pré-requisito")
    with st.form("form_prereq", clear_on_submit=True):
        materias_lista = list(grafo.materias.keys())
        prereq = st.selectbox("Pré-requisito (Matéria que libera):", [""] + materias_lista)
        materia_alvo = st.selectbox("Matéria Dependente:", [""] + materias_lista)
        btn_prereq = st.form_submit_button("Vincular Pré-requisito")

        if btn_prereq:
            try:
                grafo.adicionar_prerequisito(prereq, materia_alvo)
                st.success(f"Vínculo '{prereq} ➔ {materia_alvo}' criado com sucesso!")
            except Exception as e:
                st.error(str(e))

with col2:
    st.subheader("Matérias e Dependências")
    if grafo.materias:
        for m_id, info in grafo.materias.items():
            deps = grafo.adj.get(m_id, [])
            st.write(f"• **{m_id}** ({info['nome']}) ➔ Libera: `{deps if deps else 'Nenhuma'}`")
    else:
        st.info("Nenhuma matéria cadastrada.")

    st.divider()
    st.subheader("Validação da Grade")
    if st.button("Verificar se o Grafo é Acíclico"):
        if grafo.tem_ciclo():
            st.error("Ciclo detectado! Há pré-requisitos circulares na grade.")
        else:
            st.success("Grafo Válido! É um Grafo Acíclico Direcionado (DAG).")