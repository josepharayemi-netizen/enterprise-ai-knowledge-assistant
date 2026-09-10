from assistant_app.retrieval import Retriever

CASES=[
    ("How quickly must a security incident be reported?","employee","security_policy.md"),
    ("How many annual leave days do employees receive?","employee","employee_handbook.md"),
    ("Who can approve a customer refund?","employee","operations_manual.md"),
]


def evaluate(retriever=None):
    retriever=retriever or Retriever()
    reciprocal=[]; hits=0
    details=[]
    for question,role,expected in CASES:
        results=retriever.search(question,role,3)
        sources=[r["source"] for r in results]
        rank=next((i+1 for i,s in enumerate(sources) if s==expected),None)
        hits+=int(rank is not None); reciprocal.append(1/rank if rank else 0)
        details.append({"question":question,"expected":expected,"rank":rank})
    return {"recall_at_3":round(hits/len(CASES),4),
        "mean_reciprocal_rank":round(sum(reciprocal)/len(CASES),4),"cases":details}


if __name__=="__main__":
    print(evaluate())
