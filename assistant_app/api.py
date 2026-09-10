from fastapi import FastAPI
from pydantic import BaseModel,Field
from assistant_app.evaluate import evaluate
from assistant_app.service import KnowledgeAssistant


class Question(BaseModel):
    question:str=Field(min_length=3,max_length=1000)
    role:str=Field(pattern="^(employee|manager|hr|admin)$")


app=FastAPI(title="Enterprise AI Knowledge Assistant",version="1.0.0")
assistant=KnowledgeAssistant()


@app.get("/health")
def health():
    return {"status":"healthy","indexed_chunks":len(assistant.retriever.records)}


@app.post("/ask")
def ask(request:Question):
    return assistant.ask(request.question,request.role)


@app.post("/evaluate")
def run_evaluation():
    return evaluate(assistant.retriever)
