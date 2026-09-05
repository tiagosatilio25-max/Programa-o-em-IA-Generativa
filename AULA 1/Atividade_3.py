import streamlit as st

st.title("Seletor de Cursos")

st.header("Escolha qual curso deseja:")

cursos = st.selectbox(
    "Escolha seu curso 😊",
    ("Administração", "Arquitetura", "Odontologia")
)

st.write("Você escolheu", cursos)


if cursos == "Administração":
    cursos = ["Gestão Financeira", "Recursos Humanos", "Consultoria"]

elif cursos == "Arquitetura":
    cursos = ["Projeto Arquitetônico", "Arquitetura de Interiores", "Paisagismo"]

elif cursos == "Odontologia":
    cursos = ["Endodontia", "Harmonização Orofacial", "Cirurgia e Traumatologia Bucomaxilofacial"]


cursos = st.multiselect(
    "Escolha",
    cursos
)

st.write("Você escolheu:", cursos)