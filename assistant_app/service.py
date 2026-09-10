from assistant_app.retrieval import Retriever
from assistant_app.security import suspicious


class KnowledgeAssistant:
    def __init__(self,retriever=None):
        self.retriever=retriever or Retriever()

    def ask(self,question:str,role:str):
        if suspicious(question):
            return {"status":"blocked","answer":"The request was blocked by the security policy.","citations":[]}
        evidence=self.retriever.search(question,role)
        if not evidence or evidence[0]["score"]<0.12:
            return {"status":"insufficient_evidence",
                "answer":"I could not find enough authorized evidence to answer this question.","citations":[]}
        minimum_score=max(0.10,evidence[0]["score"]*0.50)
        evidence=[item for item in evidence if item["score"]>=minimum_score]
        excerpts=[]
        for item in evidence:
            sentence=item["text"].split(".")[0].strip()
            excerpts.append(f"{sentence}.")
        citations=[{"source":item["source"],"chunk":item["id"],"score":item["score"]} for item in evidence]
        return {"status":"grounded","answer":" ".join(excerpts),"citations":citations}
