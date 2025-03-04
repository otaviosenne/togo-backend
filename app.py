from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

# Configuração do Banco de Dados (AWS RDS)
DATABASE_URL = "postgresql://postgres_togo1:Togo11022025@database-togo1.cr8yc0ugg66q.us-east-1.rds.amazonaws.com:5432/postgres"

# Configuração do SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo SQLAlchemy para a Tabela 'client'
class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    profile_picture = Column(String, nullable=False)

# Criar tabelas no banco (se necessário)
Base.metadata.create_all(bind=engine)

# Dependência para conexão com o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🚀 FastAPI App
app = FastAPI()

# ✅ Modelos Pydantic para Entrada e Saída de Dados
class ClientBase(BaseModel):
    name: str
    email: str
    profile_picture: str

class ClientResponse(ClientBase):
    id: int

    class Config:
        from_attributes = True  # Permite conversão automática de ORM para Pydantic

# 🟢 Rota para listar todos os clientes
@app.get("/clients", response_model=list[ClientResponse])
def listar_clients(db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    return clients

# 🔵 Rota para buscar um cliente específico pelo ID
@app.get("/clients/{id}", response_model=ClientResponse)
def buscar_client(id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client

# 🟡 Rota para adicionar um novo cliente
@app.post("/clients", response_model=ClientResponse)
def adicionar_client(client_data: ClientBase, db: Session = Depends(get_db)):
    new_client = Client(**client_data.dict())  # Converte Pydantic para SQLAlchemy
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

# 🟠 Rota para atualizar um cliente existente
@app.put("/clients/{id}", response_model=ClientResponse)
def atualizar_client(id: int, updated_client: ClientBase, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    client.name = updated_client.name
    client.email = updated_client.email
    client.profile_picture = updated_client.profile_picture

    db.commit()
    db.refresh(client)
    return client

# 🔴 Rota para deletar um cliente
@app.delete("/clients/{id}")
def deletar_client(id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    db.delete(client)
    db.commit()
    return {"message": "Cliente deletado com sucesso"}