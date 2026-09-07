import streamlit as st
import json
from grafo import GrafoCurso

st.set_page_config(page_title="Fluxograma", layout="wide")

if "grafo" not in st.session_state:
    st.session_state.grafo = GrafoCurso()

grafo = st.session_state.grafo

st.title("Gerador de Fluxograma")

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
        prereq = st.selectbox("Pré-requisito (Libera):", [""] + materias_lista)
        materia_alvo = st.selectbox("Matéria Dependente:", [""] + materias_lista)
        btn_prereq = st.form_submit_button("Vincular Pré-requisito")

        if btn_prereq:
            try:
                grafo.adicionar_prerequisito(prereq, materia_alvo)
                st.success(f"Vínculo '{prereq} ➔ {materia_alvo}' criado!")
                st.rerun()
            except Exception as e:
                st.error(str(e))

with col2:
    st.subheader("Matérias Cadastradas")
    if grafo.materias:
        for m_id, info in grafo.materias.items():
            deps = grafo.adj.get(m_id, [])
            st.write(f"• **{m_id}** ({info['nome']}) — {info['creditos']} cred ➔ Libera: `{deps if deps else 'Nenhuma'}`")
    else:
        st.info("Nenhuma matéria cadastrada.")

    st.divider()
    st.subheader("Validação de Ciclos")
    if st.button("Verificar se o Grafo é Acíclico"):
        if grafo.tem_ciclo():
            st.session_state.ciclo_resultado = "ciclo"
        else:
            st.session_state.ciclo_resultado = "valido"

    if st.session_state.get("ciclo_resultado") == "ciclo":
        st.error("Ciclo detectado! Há dependências circulares inválidas na grade.")
    elif st.session_state.get("ciclo_resultado") == "valido":
        st.success("Grafo Válido! É um Grafo Acíclico Direcionado (DAG).")
st.divider()

st.subheader("Fluxograma")

max_cred = st.slider("Limite máximo de créditos por semestre:", min_value=2, max_value=40, value=20)

if st.button("Gerar Fluxograma Visual"):
    if not grafo.materias:
        st.warning("Cadastre matérias antes de gerar o fluxograma.")
    else:
        try:
            semestres = grafo.gerar_semestres(max_cred)
            st.session_state.semestres_calculados = semestres
            st.success(f"Curso organizado em {len(semestres)} semestres!")
        except Exception as e:
            st.error(f"Erro ao processar fluxograma: {str(e)}")

if "semestres_calculados" in st.session_state and st.session_state.semestres_calculados:
    semestres = st.session_state.semestres_calculados
    dot_code = grafo.exportar_dot(semestres)

    st.graphviz_chart(dot_code)

    st.divider()

    st.subheader("🔍 Detalhes do Semestre")

    opcoes_semestres = [f"{i + 1}º" for i in range(len(semestres))]

    semestre_selecionado_str = st.pills(
        "Clique no semestre para visualizar as disciplinas:",
        options=opcoes_semestres,
        default=opcoes_semestres[0]
    )

    if semestre_selecionado_str:
        idx_semestre = opcoes_semestres.index(semestre_selecionado_str)
        materias_semestre = semestres[idx_semestre]
        total_creditos = sum(grafo.materias[m]['creditos'] for m in materias_semestre)

        st.markdown(f"### {idx_semestre + 1}º Semestre ({total_creditos} créditos totais)")

        for m in materias_semestre:
            info = grafo.materias[m]
            st.markdown(f"* **{m}** — {info['nome']} (`{info['creditos']} créditos`)")

st.subheader("Import/Export")
col_exp, col_imp = st.columns(2)

with col_exp:
    data_str = json.dumps(grafo.para_dict(), indent=2, ensure_ascii=False)
    st.download_button(
        label="Baixar Grade Atual (JSON)",
        data=data_str,
        file_name="grade_curricular.json",
        mime="application/json"
    )

with col_imp:
    uploaded_file = st.file_uploader(
        "Carregar Grade de Arquivo JSON",
        type=["json"]
    )

    if uploaded_file is not None:
        arquivo_id = f"{uploaded_file.name}:{uploaded_file.size}"

        if st.session_state.get("arquivo_importado") != arquivo_id:
            try:
                dados = json.load(uploaded_file)
                grafo.carregar_dict(dados)

                st.session_state.ciclo_resultado = None
                st.session_state.semestres_calculados = None
                st.session_state.arquivo_importado = arquivo_id

                st.success("Grade curricular carregada com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao carregar arquivo: {str(e)}")
