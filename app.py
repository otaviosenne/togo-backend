from fastapi import FastAPI

app = FastAPI()

pessoas = {
    "results": [
        {
            "name": {
                "first": "Carlos",
                "last": "Silva"
            },
            "email": "carlos.silva@email.com",
            "picture": {
                "medium": "https://randomuser.me/api/portraits/med/men/1.jpg"
            },
            "id": 0
        },
        {
            "name": {
                "first": "Roberta",
                "last": "Souza"
            },
            "email": "roberta.souza@email.com",
            "picture": {
                "medium": "https://randomuser.me/api/portraits/med/women/2.jpg"
            },
            "id": 1
        },
        {
            "name": {
                "first": "Enzo",
                "last": "Tavares"
            },
            "email": "enzo.ferreira@email.com",
            "picture": {
                "medium": "https://randomuser.me/api/portraits/med/men/3.jpg"
            },
            "id": 2
        }
    ]
}

contador_id = len(pessoas["results"])  # Inicia com o tamanho atual da lista

# Rota para a página inicial
@app.get("/pessoas")
async def home():
    return pessoas

# Rota para retornar uma pessoa específica
@app.get("/pessoas/{id}")
async def pessoa(id: int):
    return pessoas["results"][id]

# Rota para editar uma pessoa
@app.put("/pessoas/{id}")
async def pessoa(id: int, pessoa: dict):
    pessoas["results"][id] = pessoa
    return pessoas["results"][id]

# Rota para adicionar uma pessoa
@app.post("/pessoas")
async def adicionar_pessoa(pessoa: dict):
    global contador_id
    pessoa["id"] = contador_id  # Usa o contador como ID
    contador_id += 1  # Incrementa o contador para o próximo ID
    pessoas["results"].append(pessoa)
    return pessoa

# Rota para deletar uma pessoa
@app.delete("/pessoas/{id}")
async def deletar_pessoa(id: int):
    pessoa = pessoas["results"][id]
    pessoas["results"].pop(id)
    return pessoa

# pip install fastapi uvicorn (🛠 Instalar fastAPI e Uvicorn)
# uvicorn app:app --reload (rodar o servidor)
# uvicorn app:app --host 127.0.0.1 --port 8000 --reload (rodar o servidor em uma porta específica)