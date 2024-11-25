import streamlit as st
import helpers as h
import rags as rags
#Configurar el ambiente de trabajo
h.configure_environment()


# Inicializar el módulo que brinda respuestas a las preguntas.
rag_bot = rags.rag()
    
# Interacción con el múdulo que brinda respuesta a las preguntas.
def set_cv_text():
    cv_text = ""
    if st.session_state["uploaded_file"] is not None:
        cv_text = h.get_text_from_pdf(st.session_state["uploaded_file"])

    


        if (cv_text is None):
            st.error("No se pudo extraer el texto del CV.")
        else:
            rag_bot.cv_text = cv_text
            rag_bot.set_cv_text(cv_text)


def get_response(user_input):
    #set_cv_text()

    response = rag_bot.get_response(user_input)
    return response


def submit():
    # Obtener la respuesta del bot
    if st.session_state["user_input"]:
        response = get_response(st.session_state["user_input"])
        st.session_state.chat_history.append({"role": "user", "prompt": st.session_state["user_input"]})
        st.session_state.chat_history.append({"role": "system", "prompt": response})
        st.session_state["user_input"] = ""

# Preparar el estado de la sesión. 
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


#COMIENZO DEL FORMULARIO DE STREAMLIT

# Streamlit app layout
st.title("Nerd Bot")
st.image("nerd_bot.jpg", width=100)
st.header("Hazme una pregunta y te responderé:")
st.subheader("No soy el jefe de los minisupers, teneís más de tres preguntas.")



# File uploader
uploaded_file = st.file_uploader("Elige un cv. Por defecto utililza el de Fabricio Denardi", type=["pdf"], key="uploaded_file", on_change=set_cv_text)

# User input
user_input = st.text_input("",placeholder="Te escucho atentamente. Escribe tu pregunta aquí...", on_change=submit, key="user_input")



# Mostrar el historial del chat
if st.session_state.chat_history:
    st.write("Historial de chat:")

    for  ix,chat in enumerate(reversed(st.session_state.chat_history)):
        st.write(f"**{chat['role']} dijo**: {chat['prompt']}")
        st.write("---")
        
       

#FIN DEL FORMULARIO DE STREAMLIT