
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

class VectorDB:
    def __init__(self):
        self.DIM = 384
        # 新增data目录支持
        self.DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        if not os.path.exists(self.DATA_DIR):
            os.makedirs(self.DATA_DIR)
        self.VEC_PATH = os.path.join(self.DATA_DIR, "vector.index")
        print(f"VectorDB vector.index 的path: {self.VEC_PATH}\n")
        self.META_PATH = os.path.join(self.DATA_DIR, "metadata.pkl")
        print(f"VectorDB metadata.pkl 的path: {self.META_PATH}\n")
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
        self.index.add(np.array([vector], dtype=np.float32))
        self.documents.append(text)
        self.sources.append(source)
        self.save()


    def search(self, query, k=3):
        vector = self.model.encode([query])[0]
        D, I = self.index.search(np.array([vector], dtype=np.float32), k)
        results = []
        for i in I[0]:
            if 0 <= i < len(self.documents):
                results.append(self.documents[i])
        return results


    def search_with_source(self, query, k=3):
        vector = self.model.encode([query])[0]
        D, I = self.index.search(np.array([vector], dtype=np.float32), k)
        results = []
        for i in I[0]:
            if 0 <= i < len(self.documents):
                results.append((self.documents[i], self.sources[i]))
        return results

    def clear(self):
        self.index = faiss.IndexFlatL2(self.DIM)
        self.documents = []
        self.sources = []
        # 删除持久化文件
        if os.path.exists(self.VEC_PATH):
            os.remove(self.VEC_PATH)
        if os.path.exists(self.META_PATH):
            os.remove(self.META_PATH)

    def save(self):
        faiss.write_index(self.index, self.VEC_PATH)
        with open(self.META_PATH, 'wb') as f:
            pickle.dump((self.documents, self.sources), f)

# 实例化 vectordb 供外部导入
vectordb = VectorDB()
