from fastapi import FastAPI
from datetime import datetime

import requests

LISTA_TAREFAS = []
APP = FastAPI()

def nova_tarefa(id: int, titulo: str, descricao: str):
    return {
        "id": id,
        "titulo": titulo,
        "descricao": descricao,
        "concluido": False,
        "criado_em": datetime.now()
    }

def verificar_existencia_tarefa(id: int):
    """Função auxiliar para verificar a existência de uma tarefa com base no seu ID"""
    for tarefa in LISTA_TAREFAS:
        if id == tarefa['id']:
            return True
    return False

@APP.get("/")
def index():
    return "Olá, DevOps!"


@APP.get("/tarefas")
def listar_tarefas():
    if len(LISTA_TAREFAS) == 0:
        return LISTA_TAREFAS

    tarefas = []

    for tarefa in LISTA_TAREFAS:
        info = {"id": tarefa['id'], "titulo": tarefa['titulo']}
        tarefas.append(info)

    return tarefas

@APP.get("/tarefa/{id}")
def listar_tarefa_especifica(id: int):
    if len(LISTA_TAREFAS) == 0:
        return {"mensagem": "Não há tarefas cadastradas"}

    if id >= 0 and id < len(LISTA_TAREFAS):
        return LISTA_TAREFAS[id]

    return {"mensagem": "Não há tarefa com esse ID"}

@APP.post("/tarefas", status_code=201)
def criar_tarefa(id: int, titulo: str, descricao: str):
    global LISTA_TAREFAS

    tarefa_existe = verificar_existencia_tarefa(id)

    if tarefa_existe:
        #ex = HTTPException(status_code=202, detail={"mensagem": "TAREFA JÁ EXISTE!"})
        #raise ex
        return {"mensagem": "TAREFA JÁ EXISTE"}
    
    nova = nova_tarefa(id, titulo, descricao)

    LISTA_TAREFAS.append(nova)

    return {"mensagem": "OK"}


@APP.put("/tarefas/{id}")
def atualizar_tarefa(id: int, titulo: str = "", descricao: str = "", concluido: bool = False):
    global LISTA_TAREFAS

    tarefa_existe = verificar_existencia_tarefa(id)

    if not tarefa_existe:
        return {"mensagem": "TAREFA NÃO EXISTE!"}
    
    tarefa = None
    for indice in range(len(LISTA_TAREFAS)):
        tarefa = LISTA_TAREFAS[indice]

        # Sai do loop
        if tarefa['id'] == id:
            break
    
    if titulo != "":
        LISTA_TAREFAS[indice]['titulo'] = titulo
    
    if descricao !=  "":
        LISTA_TAREFAS[indice]['descricao'] = descricao
    
    if concluido == True:
        requests.post(
            f"http://localhost:8001/notificar?titulo={tarefa['titulo']}&data_finalizacao={datetime.now()}"
        )

    LISTA_TAREFAS[indice]['concluido'] = concluido

    return {"mensagem": "OK"}


@APP.delete("/tarefas/{id}")
def apagar_tarefa(id: int):
    global LISTA_TAREFAS

    tarefa_existe = verificar_existencia_tarefa(id)

    if not tarefa_existe:
        return {"mensagem": "TAREFA NÃO EXISTE"}

    tarefa = None
    for indice in range(len(LISTA_TAREFAS)):
        tarefa = LISTA_TAREFAS[indice]

        # Sai do loop
        if tarefa['id'] == id:
            break
    
    LISTA_TAREFAS.pop(indice)

    return {"mensagem": "OK"}