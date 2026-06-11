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
        "id": 1,
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

    # breakpoint()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"funcionarios": []}


def test_atualizar_funcionario(client, funcionarios):
    response = client.patch(
        f"/funcionarios/{funcionarios.id}",
        json={
            "id": funcionarios.id,
            "nome": "funcionario2",
            "email": "funcionario2@teste.com",
            "cpf": "111.222.333-44",
            "telefone": "(00) 10000-0000",
            "data_nascimento": "30/09/2006",
            "salario": "9950.10",
            "passagem": "520.10",
            "alimentacao": "1950.00",
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["nome"] == "funcionario2"


def test_atualizar_nome_ja_existe(client, outro_funcionario, funcionarios):
    response = client.patch(
        f"/funcionarios/{outro_funcionario.id}",
        json={
            "nome": "Mayckon Kennedy Santos Carvalho Duarte",
        },
    )
    # breakpoint()
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Já existe um funcionário com esse nome."}


def test_atualizar_cpf_ja_existe(client, outro_funcionario, funcionarios):
    response = client.patch(f"/funcionarios/{outro_funcionario.id}", json={"email": "mayckonkennedy877@gmail.com"})

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Já existe um funcionário com esse email."}


def test_atualizar_email_ja_existe(client, outro_funcionario, funcionarios):
    response = client.patch(f"/funcionarios/{outro_funcionario.id}", json={"cpf": "712.071.951-38"})

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Já existe um funcionário com esse CPF."}


def test_atualizar_funcionario_nao_encontrado(client, funcionarios):
    response = client.patch("/funcionarios/999", json={"nome": "Não Encontrado"})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Funcionário não encontrado."}


def test_deletar_usuario(client, funcionarios):
    response = client.delete(f"/funcionarios/{funcionarios.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Funcionário deletado com sucesso!"}


def test_deletar_funcionario_nao_encontrado(client, funcionarios):
    response = client.delete("/funcionarios/999")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Funcionário não encontrado."}
