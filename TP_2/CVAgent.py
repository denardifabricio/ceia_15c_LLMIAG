
import GroqModel as gm
import PineconeModel as pm
import helpers as h
import rags

from llama_index.core.node_parser import (
    SentenceSplitter,
    SemanticSplitterNodeParser,
)
from llama_index.embeddings.openai import OpenAIEmbedding

from llama_index.core import SimpleDirectoryReader


class CVAgent():
    def set_embedding_model(self,cv_text):
        self.embedding_model = OpenAIEmbedding() 
        self.pinecone_model = pm.PineconeModel(index_name=  "-".join(["cvs","index",cv_text[2]]))
        self.groq_model = gm.GroqModel()

        if  self.pinecone_model.is_index_empty():
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


    def __init__(self, agent_person_cv="FabricioDenardi"):
        self.agent_person_cv = agent_person_cv
        self.index_name = "-".join(["cvs", "index", agent_person_cv])
        self.set_embedding_model(h.get_txt_agent_cv_text(agent_person_cv))

    def __call__(self, user_input):
        result = self.execute(user_input)
        return result

    def execute(self, user_input):    
        user_input_embeddings = self.embedding_model.get_text_embedding(user_input)
        relevant_docs = self.pinecone_model.retrieve_relevant_docs(user_input_embeddings, top_k=3)
      
        rel = []
        for doc in relevant_docs["matches"]:
            rel.append(doc["metadata"]['text'])

        return ", ".join(rel)
    
rag_bot = rags.rag()
