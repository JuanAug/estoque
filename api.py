from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI()

# 🔓 Libera CORS para qualquer origem (inclusive file://)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restrinja para ["https://seusite.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "app", "estoque.db")

class Produto(BaseModel):
    id: int
    descricao: str
    valor_compra: float
    valor_custo: float
    valor_venda: float
    quantidade: int
    quantidade_reposicao: int


# Definição das credenciais
usuarios = {
    "Suzy": "@2020",
    "Beatriz": "@2020",
    "Admin": "@dm1n"
}

class Login(BaseModel):
    login: str
    senha: str

@app.post("/login")
async def login(data: Login):
    login = data.login
    senha = data.senha
    
    # Verifica se o login e senha estão corretos
    if login in usuarios and usuarios[login] == senha:
        return {"message": "Login bem-sucedido"}
    raise HTTPException(status_code=401, detail="Login ou senha incorretos")


@app.get("/produtos", response_model=list[Produto])
def get_produtos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, descricao, valor_compra, valor_custo, valor_venda, quantidade, quantidade_reposicao FROM produtos")
    produtos = cursor.fetchall()
    conn.close()

    return [
    {
        "id": id_,
        "descricao": descricao,
        "valor_compra": vc,
        "valor_custo": cs,
        "valor_venda": vv,
        "quantidade": qt,
        "quantidade_reposicao": rep
    }
    for id_, descricao, vc, cs, vv, qt, rep in produtos
]