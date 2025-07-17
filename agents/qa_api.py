from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from agents.qa_agent import run

app = FastAPI()

@app.post("/qa")
async def qa_endpoint(request: Request):
    data = await request.json()
    result = run(data)
    return JSONResponse(content=result)

@app.get("/ping")
def ping():
    return {"status": "ok"}
