from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Qdrant as QdrantLangChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from set_qdrant import Set_Qdrant
import os

# ========== FastAPI 初始化 ==========
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ========== CORS ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== 啟動時延遲初始化 ==========
qa_chain = None  # 全域變數預設為 None
import requests

def ensure_model_ready(model_name: str):
    try:
        resp = requests.get("http://ollama:11434/api/tags")
        if model_name not in [m["name"] for m in resp.json()["models"]]:
            print(f"模型 {model_name} 尚未下載...")
            requests.post("http://ollama:11434/api/pull", json={"name": model_name})
    except Exception as e:
        print("無法連接 Ollama API 檢查模型：", e)
@app.on_event("startup")
async def startup_event():
    global qa_chain
    try:
        ensure_model_ready("qwen")
        ollama_host = os.getenv("OLLAMA_HOST", "localhost")
        base_url = f"http://{ollama_host}:11434"
        llm = Ollama(model="qwen", base_url=base_url)

        embedding = HuggingFaceEmbeddings(
            model_name="shibing624/text2vec-base-chinese",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        client = Set_Qdrant()
        vectorstore = QdrantLangChain(
            client=client,
            collection_name="Lawer_Qdrant",
            embeddings=embedding,
        )
        retriever = vectorstore.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")

        print("[啟動成功] QA Chain 初始化完成")

    except Exception as e:
        import traceback
        print("[錯誤] QA Chain 初始化失敗：", e)
        traceback.print_exc()
        qa_chain = None


# ========== 提供 pipeline 使用 ==========
def run_qa(query: str) -> str:
    return qa_chain.run(query)


# ========== FastAPI 模型 ==========
class Question(BaseModel):
    query: str


# ========== API ==========
@app.post("/ask")
async def ask_question(question: Question):
    if qa_chain is None:
        return {"error": "QA 系統尚未初始化完成，請稍後再試"}
    try:
        answer = run_qa(question.query)
        return {"question": question.query, "answer": answer}
    except Exception as e:
        return {"error": str(e)}


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/ping")
def root():
    return {"message": "FastAPI 啟動成功，可使用 POST /ask"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
