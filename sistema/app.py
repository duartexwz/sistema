from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from sistema.database import get_session
from sistema.funcionarios_models import Funcionarios
from sistema.funcionarios_schemas import FilterPage, FuncionariosCreate, FuncionariosList, FuncionariosResponse, FuncionariosUpdate, Message
from sistema.funcoes_auxiliares import converter_cpf, converter_data_br

app = FastAPI()

T_session = Annotated[Session, Depends(get_session)]


@app.post("/funcionarios", status_code=HTTPStatus.CREATED, response_model=FuncionariosResponse)
async def cadastro_funcionario(funcionario: FuncionariosCreate, session: T_session):
    funcionario_db = session.scalar(
        select(Funcionarios).where(
            (Funcionarios.nome == funcionario.nome) | (Funcionarios.email == funcionario.email) | (Funcionarios.cpf == funcionario.cpf)
        )
    )

    if funcionario_db:
        if funcionario_db.nome == funcionario.nome:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um funcionário com esse nome.")
        if funcionario_db.email == funcionario.email:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um funcionário com esse email.")
        if funcionario_db.cpf == funcionario.cpf:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um funcionário com esse CPF.")

    funcionario_db = Funcionarios(
        nome=funcionario.nome,
        email=funcionario.email,
        cpf=converter_cpf(funcionario.cpf),
        data_nascimento=converter_data_br(funcionario.data_nascimento),
        telefone=funcionario.telefone,
        salario=funcionario.salario,
        passagem=funcionario.passagem,
        alimentacao=funcionario.alimentacao,
    )

    session.add(funcionario_db)
    session.commit()
    session.refresh(funcionario_db)

    return funcionario_db


@app.get("/funcionarios", response_model=FuncionariosList, status_code=HTTPStatus.OK)
def buscar_funcionarios(session: T_session, filter_funcionarios: Annotated[FilterPage, Query()]):
    get_funcionarios = session.scalars(select(Funcionarios).offset(filter_funcionarios.offset).limit(filter_funcionarios.limit))

    funcionarios = get_funcionarios.all()

    return {"funcionarios": funcionarios}


@app.patch("/funcionarios/{funcionarios_id}", response_model=FuncionariosResponse)
def atualizar_funcionario(
    funcionarios_id: int,
    session: T_session,
    funcionario: FuncionariosUpdate,
):
    funcionarios_db = session.scalar(select(Funcionarios).where(Funcionarios.id == funcionarios_id))

    if not funcionarios_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Funcionário não encontrado.")

    if funcionario.nome:
        existe = session.scalar(select(Funcionarios).where(Funcionarios.nome == funcionario.nome, Funcionarios.id != funcionarios_id))

        if existe:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um funcionário com esse nome.")
    if funcionario.email:
        existe = session.scalar(select(Funcionarios).where(Funcionarios.email == funcionario.email, Funcionarios.id != funcionarios_id))
        if existe:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um funcionário com esse email.")
    if funcionario.cpf:
        existe = session.scalar(select(Funcionarios).where(Funcionarios.cpf == funcionario.cpf, Funcionarios.id != funcionarios_id))
        if existe:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um funcionário com esse CPF.")

    for campo, valor in funcionario.model_dump(exclude_none=True).items():
        setattr(funcionarios_db, campo, valor)

    session.add(funcionarios_db)
    session.commit()
    session.refresh(funcionarios_db)

    return funcionarios_db


@app.delete("/funcionarios/{funcionarios_id}", response_model=Message, status_code=HTTPStatus.OK)
def deletar_funcionario(
    funcionarios_id: int,
    session: T_session,
):
    funcionarios_db = session.scalar(select(Funcionarios).where(Funcionarios.id == funcionarios_id))

    if not funcionarios_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Funcionário não encontrado.")

    session.delete(funcionarios_db)
    session.commit()

    return {"message": "Funcionário deletado com sucesso!"}
