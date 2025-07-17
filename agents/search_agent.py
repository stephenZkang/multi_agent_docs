from core.vectordb import vectordb

def run(input):
    results = vectordb.search(input, k=3)
    return {"search_result": "\n".join(results)}
