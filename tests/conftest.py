from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from sistema.app import app
from sistema.database import get_session
from sistema.funcionarios_models import Funcionarios, registro_tabela_funcionarios
from sistema.funcoes_auxiliares import converter_cpf, converter_data_br
from sistema.ti_models import registro_tabela_ti


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    registro_tabela_funcionarios.metadata.create_all(engine)
    registro_tabela_ti.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    registro_tabela_funcionarios.metadata.drop_all(engine)
    registro_tabela_ti.metadata.drop_all(engine)


@pytest.fixture
def funcionarios(session):
    funcionario = Funcionarios(
        nome="Mayckon Kennedy Santos Carvalho Duarte",
        email="mayckonkennedy877@gmail.com",
        cpf=converter_cpf("71207195138"),
        data_nascimento=converter_data_br("30/09/2006"),
        salario=Decimal("25650.9"),
        telefone="61984092729",
        passagem=Decimal("420.10"),
        alimentacao=Decimal("1580.10"),
    )

    session.add(funcionario)
    session.commit()
    session.refresh(funcionario)

    return funcionario


@pytest.fixture
def outro_funcionario(session):
    funcionario2 = Funcionarios(
        nome="Maria Eduarda da Costa Silva",
        email="ms.mariasilva@gmail.com",
        cpf=converter_cpf("71568266111"),
        data_nascimento=converter_data_br("16/01/2008"),
        salario=Decimal("25650.9"),
        telefone="(61) 98174 - 1089",
        passagem=Decimal("420.10"),
        alimentacao=Decimal("1580.10"),
    )

    session.add(funcionario2)
    session.commit()
    session.refresh(funcionario2)

    return funcionario2
