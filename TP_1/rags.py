import helpers as h
import GroqModel as gm
from transformers import AutoModel
import PineconeModel as pm

from llama_index.core.node_parser import (
    SentenceSplitter,
    SemanticSplitterNodeParser,
)
from llama_index.embeddings.openai import OpenAIEmbedding

from llama_index.core import SimpleDirectoryReader


class rag ():

    def set_embedding_model(self,cv_text):
        self.embedding_model = OpenAIEmbedding() #AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-en', trust_remote_code=True)

        self.pinecone_model = pm.PineconeModel(index_name=  "-".join(["cvs","index",cv_text[2]]))
        self.groq_model = gm.GroqModel()

        if  self.pinecone_model.is_index_empty():
            #embed_model = OpenAIEmbedding()
            splitter = SemanticSplitterNodeParser(
                buffer_size=1, breakpoint_percentile_threshold=95, embed_model= self.embedding_model 
            )
            
            documents = SimpleDirectoryReader(input_files=[cv_text[1]]).load_data()
            nodes = splitter.get_nodes_from_documents(documents, show_progress=False)

            cvs_nodes =[]
            for node in nodes:
                node_content = node.get_content()
                node_embeddings = self.embedding_model.get_text_embedding(node_content)

                cvs_nodes.append({"embeddings":node_embeddings, "text": node_content}) 
                self.pinecone_model.insert(cvs_nodes)

    
    def __init__(self, cv_text = None):
        if cv_text is not None:
            self.set_embedding_model(cv_text)
        else:
            self.set_embedding_model(h.get_txt_default_cv())
        
    def set_cv_text(self,cv_text):
        self.set_embedding_model(cv_text)

    def get_rag_details(self):
        return f"Aquí se mostrarán los detalles del RAG."


    def get_response(self, user_input):
        user_input_embeddings = self.embedding_model.get_text_embedding(user_input)
        relevant_docs = self.pinecone_model.retrieve_relevant_docs(user_input_embeddings, top_k=3)
    
        
        rel = []
        for doc in relevant_docs["matches"]:
            rel.append(doc["metadata"]['text'])

        return self.groq_model.generate_response_with_llama(user_input,", ".join(rel))


#rag_bot = rag()
#rag_bot.get_response("¿Durante cuanto tiempo trabajó en kinexo?")