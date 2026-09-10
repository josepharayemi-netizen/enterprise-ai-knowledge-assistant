from pathlib import Path
import argparse,re,joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from assistant_app.security import suspicious


def parse(path:Path):
    text=path.read_text(encoding="utf-8")
    metadata={"title":path.stem,"roles":["employee"]}
    if text.startswith("---"):
        _,head,text=text.split("---",2)
        for line in head.strip().splitlines():
            key,value=line.split(":",1)
            if key.strip()=="title": metadata["title"]=value.strip()
            if key.strip()=="roles": metadata["roles"]=[v.strip() for v in value.split(",")]
    return metadata,text.strip()


def chunks(text:str,size:int=500):
    paragraphs=[p.strip() for p in re.split(r"\n\s*\n",text) if p.strip()]
    output=[]; current=""
    for paragraph in paragraphs:
        if current and len(current)+len(paragraph)>size:
            output.append(current); current=paragraph
        else: current=(current+"\n\n"+paragraph).strip()
    if current: output.append(current)
    return output


def build(source:Path,output:Path):
    records=[]
    for path in sorted(list(source.glob("*.md"))+list(source.glob("*.txt"))):
        metadata,text=parse(path)
        for number,chunk in enumerate(chunks(text),1):
            if not suspicious(chunk):
                records.append({"id":f"{path.name}#{number}","source":path.name,
                    "title":metadata["title"],"roles":metadata["roles"],"text":chunk})
    if not records: raise ValueError("No safe documents were available for indexing")
    vectorizer=TfidfVectorizer(stop_words="english",ngram_range=(1,2))
    matrix=vectorizer.fit_transform([r["text"] for r in records])
    output.parent.mkdir(parents=True,exist_ok=True)
    joblib.dump({"records":records,"vectorizer":vectorizer,"matrix":matrix},output)
    print(f"Indexed {len(records)} chunks from {source}")
    return output


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--source",type=Path,default=Path("knowledge"))
    parser.add_argument("--output",type=Path,default=Path("artifacts/index.joblib"))
    args=parser.parse_args(); build(args.source,args.output)


if __name__=="__main__":
    main()
