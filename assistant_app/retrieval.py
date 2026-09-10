from pathlib import Path
import joblib
from sklearn.metrics.pairwise import cosine_similarity


class Retriever:
    def __init__(self,path:Path=Path("artifacts/index.joblib")):
        if not path.exists():
            from assistant_app.ingest import build
            build(Path("knowledge"),path)
        data=joblib.load(path)
        self.records=data["records"]; self.vectorizer=data["vectorizer"]; self.matrix=data["matrix"]

    def search(self,query:str,role:str,k:int=3):
        allowed=[i for i,r in enumerate(self.records) if role in r["roles"] or "all" in r["roles"]]
        if not allowed: return []
        scores=cosine_similarity(self.vectorizer.transform([query]),self.matrix[allowed])[0]
        ranked=sorted(zip(allowed,scores),key=lambda x:x[1],reverse=True)[:k]
        return [self.records[i]|{"score":round(float(score),4)} for i,score in ranked if score>0.05]
