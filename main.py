from fastapi import FastAPI
from datetime import datetime

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

@APP.get("/")
def index():
    return "Olá, DevOps!"


@APP.get("/tarefas")
def listar_tarefas():
    global LISTA_TAREFAS

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