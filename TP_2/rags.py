import helpers as h
import GroqModel as gm
from transformers import AutoModel
import PineconeModel as pm




class rag ():
    

    
    def __init__(self):
        self.agents = []
        self.groq_model = gm.GroqModel()

    def append_agent(self,agent):
        self.agents.append(agent)


    
    def get_response(self, user_input, agent_filter="All"):
        enabled_agents = {agent.agent_person_cv: agent(user_input) for agent in self.agents if agent_filter == "All" or agent_filter == agent.agent_person_cv}
        
        # Formatear el diccionario como {clave: valor, clave: valor}
        enabled_agents_str = "{" + ", ".join(f"{k}: {v}" for k, v in enabled_agents.items()) + "}"


        prompt= '''Eres un experto en el sector de recursos humanos y te especializas en la contratación de personal. Tu trabajo
        es ayudar a las empresas a encontrar a los mejores candidatos para sus vacantes. Para ello, analizas los currículums de los
        candidatos que se especifican en el contexto. Dicho contexto puede contener 1 a n currículums. El formato del contexto es un diccionario
        donde la clave es el nombre del candidato y el valor es el texto del currículum. Por ejemplo, si el contexto contiene dos currículums
        de dos candidatos, el formato sería el siguiente:
        {
            "FabricioDenardi": "texto del currículum 1",
            "JoseContreras": "texto del currículum 2"
        }. El nombre del candidato está en formato CamelCase y sin espacios. El texto del currículum es un texto en formato libre.
        Tener en cuenta que puede haber preguntas relacionadas a todos los currículums o a un currículum en específico.
        '''

        context = f"{prompt}. Contexto:{enabled_agents_str}"

        query  = f"{context} Pregunta: {user_input}"


        return self.groq_model.generate_response_with_llama(query)
