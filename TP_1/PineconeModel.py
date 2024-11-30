import os

from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import time





PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

#Crear índice
INDEX_NAME = "cvs-index-fabriciodenardi"

class PineconeModel:

    def create_index(self, dimension=1536, metric="cosine", cloud='aws', region='us-east-1'):
        if not self.pc.has_index(self.index_name):
            self.pc.create_index(
                name=self.index_name,
                dimension=dimension,
                metric=metric,
                spec=ServerlessSpec(
                    cloud=cloud, 
                    region= region
                ) 
            )

            # Wait for the index to be ready
            while not self.pc.describe_index(self.index_name).status['ready']:
                time.sleep(1)


    def __init__(self,index_name=INDEX_NAME):
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index_name = index_name
        self.create_index()


    def insert(self,cvs):
        records = []
        idx = 0
        
        for cv in cvs:
            records.append({
                    "id": str(idx),
                    "values": cv["embeddings"],
                    "metadata": {'text': cv["text"]}
                })
            
            idx += 1
        
        index = self.pc.Index(self.index_name)
        
        index.upsert(
            vectors=records,
            namespace="cv-namespace"
        )

    def is_index_empty(self):
        stats = self.pc.Index(self.index_name).describe_index_stats()
        num_vectors = stats["total_vector_count"]
        return num_vectors == 0

    def retrieve_relevant_docs(self,query_embedding, top_k=5):
        index = self.pc.Index(self.index_name)
        results = index.query(query_embedding, top_k=top_k, include_metadata=True,namespace="cv-namespace")
        return results
    