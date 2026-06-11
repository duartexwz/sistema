from http import HTTPStatus

from fastapi import APIRouter
from funcionarios_schemas import FuncionariosCreate, FuncionariosDB, FuncionariosResponse

router = APIRouter(prefix="/funcionarios", tags=["funcionarios"])

database = []


@router.post("/", status_code=HTTPStatus.CREATED, response_model=FuncionariosResponse)
async def cadastro_funcionario(
    funcionario: FuncionariosCreate,
):
    funcionario_teste = FuncionariosDB(**funcionario.model_dump(), id=len(database) + 1)

    database.append(funcionario_teste)

    return funcionario
