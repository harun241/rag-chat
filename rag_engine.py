from sentence_transformers import SentenceTransformer, util
import os
import chromadb

class LocalRAG:
    def __init__(self, docs_dir="docs", persist_dir="db"):
        self.docs_dir = docs_dir
        self.persist_dir = persist_dir

        # Load embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        # Initialize Chroma client
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection("knowledge")

        # Load documents if DB empty
        if len(self.collection.get()) == 0:
            self.load_docs()

    def load_docs(self):
        for fname in os.listdir(self.docs_dir):
            path = os.path.join(self.docs_dir, fname)
            if os.path.isfile(path) and fname.endswith(".txt"):
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
                    emb = self.model.encode(text)
                    self.collection.add(
                        ids=[fname],
                        metadatas=[{"source": fname}],
                        embeddings=[emb.tolist()],
                        documents=[text]
                    )

    def query(self, q, top_k=1):
        q_emb = self.model.encode(q)
        results = self.collection.query(
            query_embeddings=[q_emb.tolist()],
            n_results=top_k
        )
        if results['documents'][0]:
            return results['documents'][0][0]
        else:
            return "No content found in local docs."
