from http import HTTPStatus


def test_create_funcionario(client):
    response = client.post(
        "/funcionarios",
        json={
            "nome": "funcionario",
            "email": "funcionario@teste.com",
            "cpf": "000.000.000-00",
            "telefone": "(00) 00000-0000",
            "data_nascimento": "30/09/2006",
            "salario": "9950.10",
            "passagem": "520.10",
            "alimentacao": "1950.00",
        },
    )

    # breakpoint()
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "nome": "funcionario",
        "email": "funcionario@teste.com",
        "cpf": "000.000.000-00",
        "telefone": "(00) 00000-0000",
        "data_nascimento": "2006-09-30",
        "salario": "9950.10",
        "passagem": "520.10",
        "alimentacao": "1950.00",
    }


def test_nome_ja_existe(client):
    client.post(
        "/funcionarios",
        json={
            "nome": "funcionario",
            "email": "funcionario@teste.com",
            "cpf": "000.000.000-00",
            "telefone": "(00) 00000-0000",
            "data_nascimento": "30/09/2006",
            "salario": "9950.10",
            "passagem": "520.10",
            "alimentacao": "1950.00",
        },
    )
    response = client.post(
        "/funcionarios",
        json={
            "nome": "funcionario",
            "email": "funcionario1@teste.com",
            "cpf": "000.000.009-00",
            "telefone": "(00) 10000-0000",
            "data_nascimento": "30/09/2006",
            "salario": "9950.10",
            "passagem": "520.10",
            "alimentacao": "1950.00",
        },
    )
    # breakpoint()
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Já existe um funcionário com esse nome."}


def test_email_ja_existe(client):
    client.post(
        "/funcionarios",
        json={
            "nome": "funcionario",
            "email": "funcionario@teste.com",
            "cpf": "000.000.000-00",
            "telefone": "(00) 00000-0000",
            "data_nascimento": "30/09/2006",
            "salario": "9950.10",
            "passagem": "520.10",
            "alimentacao": "1950.00",
        },
    )

    response = client.post(
        "/funcionarios",
        json={
            "nome": "funcionario1",
            "email": "funcionario@teste.com",
            "cpf": "000.000.009-00",
            "telefone": "(00) 10000-0000",
            "data_nascimento": "30/09/2006",
            "salario": "9950.10",
            "passagem": "520.10",
            "alimentacao": "1950.00",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Já existe um funcionário com esse email."}


def test_cpf_ja_existe(client):
    client.post(
        "/funcionarios",
        json={
            "nome": "funcionario",
            "email": "funcionario@teste.com",
            "cpf": "000.000.000-00",
            "telefone": "(00) 00000-0000",
            "data_nascimento": "30/09/2006",
            "salario": "9950.10",
            "passagem": "520.10",
            "alimentacao": "1950.00",
        },
    )

    response = client.post(
        "/funcionarios",
        json={
            "nome": "funcionario1",
            "email": "funcionario1@teste.com",
            "cpf": "000.000.000-00",
            "telefone": "(00) 10000-0000",
            "data_nascimento": "30/09/2006",
            "salario": "9950.10",
            "passagem": "520.10",
            "alimentacao": "1950.00",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Já existe um funcionário com esse CPF."}


def test_buscar_funcionarios(client):
    response = client.get("/funcionarios/")

    breakpoint()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"funcionarios": []}
