import helpers as h
import GroqModel as gm
from transformers import AutoModel
import PineconeModel as pm

class rag ():

    def set_embedding_model(self,text):
        self.embedding_model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-en', trust_remote_code=True)
        self.embedding_model.max_seq_length = 128

        self.embeddings = self.embedding_model.encode(text)

        self.pinecone_model = pm.PineconeModel()
        self.groq_model = gm.GroqModel()

        cvs =[]
        cvs.append({"embeddings":self.embeddings, "text": text}) #Para la presentación de este tp solo se incluye un solo cv (el de Fabricio Denardi)

        self.pinecone_model.insert(cvs)


    

    def __init__(self):
        self.set_embedding_model(h.get_txt_default_cv())
        
    def set_cv_text(self,cv_text):
        self.set_embedding_model(cv_text)

    def get_rag_details(self):
        return f"Aquí se mostrarán los detalles del RAG."


    def get_response(self, user_input):
        user_input_embeddings = self.embedding_model.encode(user_input)
        relevant_docs = self.pinecone_model.retrieve_relevant_docs(user_input_embeddings, top_k=5)
    
        cv = relevant_docs["matches"][0]["metadata"]['text']

        return self.groq_model.generate_response_with_llama(user_input, cv)