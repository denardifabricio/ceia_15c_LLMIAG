from groq import Groq
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")




class GroqModel():
    def __init__(self, model = "llama3-8b-8192"):
        # Inicializa el modelo LLaMA en Groq
        self.llama = Groq(api_key=GROQ_API_KEY)
        self.model = model

        # Set the system prompt
        self.system_prompt = {
            "role": "system",
            "content":
            "Te escucho atentamente. Escribe tu pregunta aquí..."
        }

        self.chat_history = [self.system_prompt]
        

    
    def generate_response_with_llama(self,query, relevant_doc, max_tokens=1024, temperature=1):
        self.chat_history.append({"role": "user", "content":f"Contexto: {relevant_doc}, Pregunta: {query}"})

        response = self.llama.chat.completions.create(model= self.model,
                                                    messages=self.chat_history,
                                                    max_tokens=max_tokens,
                                                    temperature=temperature)
        # Append the response to the chat history
        self.chat_history.append({
            "role": "assistant",
            "content": response.choices[0].message.content
        })

        return response.choices[0].message.content