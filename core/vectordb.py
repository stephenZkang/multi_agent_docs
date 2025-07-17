
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

class VectorDB:
    def __init__(self):
        self.DIM = 384
        self.VEC_PATH = os.path.join(os.path.dirname(__file__), "vector.index")
        self.META_PATH = os.path.join(os.path.dirname(__file__), "metadata.pkl")
        self.index = faiss.IndexFlatL2(self.DIM)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.documents = []
        self.sources = []
        if os.path.exists(self.VEC_PATH) and os.path.exists(self.META_PATH):
            self.index = faiss.read_index(self.VEC_PATH)
            with open(self.META_PATH, 'rb') as f:
                self.documents, self.sources = pickle.load(f)

    def add_text(self, text, source="unknown"):
        vector = self.model.encode([text])[0]
        self.index.add(np.array([vector]))
        self.documents.append(text)
        self.sources.append(source)
        self.save()


    def search(self, query, k=3):
        vector = self.model.encode([query])[0]
        D, I = self.index.search(np.array([vector]), k)
        results = []
        for i in I[0]:
            if 0 <= i < len(self.documents):
                results.append(self.documents[i])
        return results


    def search_with_source(self, query, k=3):
        vector = self.model.encode([query])[0]
        D, I = self.index.search(np.array([vector]), k)
        results = []
        for i in I[0]:
            if 0 <= i < len(self.documents):
                results.append((self.documents[i], self.sources[i]))
        return results

    def save(self):
        faiss.write_index(self.index, self.VEC_PATH)
        with open(self.META_PATH, 'wb') as f:
            pickle.dump((self.documents, self.sources), f)

# 实例化 vectordb 供外部导入
vectordb = VectorDB()
