import streamlit as st
import helpers as h
import rags as rags
import CVAgent as agent
#Configurar el ambiente de trabajo
h.configure_environment()


def init_process():
     # Inicializar el módulo que brinda respuestas a las preguntas.
    st.session_state.rag_bot = rags.rag()


    fabricioAgent = agent.CVAgent(agent_person_cv="FabricioDenardi")
    joseAgent = agent.CVAgent(agent_person_cv="JoseContreras")

    st.session_state.rag_bot.append_agent(fabricioAgent)
    st.session_state.rag_bot.append_agent(joseAgent)

if 'rag_bot' not in st.session_state:
    init_process()

if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []


def get_response(user_input):
    response = st.session_state.rag_bot.get_response(user_input = user_input, agent_filter = st.session_state.selected_user["value"])
    return response

def cv_changed():
    st.session_state.chat_history = []
    init_process()

def submit():
    # Obtener la respuesta del bot
    if st.session_state["user_input"]:
        response = get_response(st.session_state["user_input"])
        st.session_state.chat_history.append({"role": "user", "prompt": st.session_state["user_input"]})
        st.session_state.chat_history.append({"role": "system", "prompt": response})
        st.session_state["user_input"] = ""




#COMIENZO DEL FORMULARIO DE STREAMLIT

# Streamlit app layout
st.title("Nerd Bot")
st.image("nerd_bot.jpg", width=100)
st.header("Hazme una pregunta y te responderé:")
st.subheader("No soy el jefe de los minisupers, teneís más de tres preguntas.")


# Select
selected_user = st.selectbox(
    "Selecciona un usuario:",
    options=[{"label": "Todos", "value": "All"},{"label": "Fabricio Denardi", "value": "FabricioDenardi"}, {"label": "Jose Contreras", "value": "JoseContreras"}],
    format_func=lambda option: option["label"],
    key="selected_user",
    on_change=cv_changed
)


# User input
user_input = st.text_input("",placeholder="Te escucho atentamente. Escribe tu pregunta aquí...", on_change=submit, key="user_input")


# Button to clear chat history
if st.button("Limpiar historial"):
    st.session_state.chat_history = []

# Mostrar el historial del chat
if st.session_state.chat_history:
    st.write("Historial de chat:")

    for  ix,chat in enumerate(reversed(st.session_state.chat_history)):
        st.write(f"**{chat['role']} dijo**: {chat['prompt']}")
        st.write("---")
        
       

#FIN DEL FORMULARIO DE STREAMLIT
