from decimal import Decimal

from pydantic import BaseModel, EmailStr

from sistema.funcoes_auxiliares import DataBR


class FuncionariosCreate(BaseModel):
    nome: str
    email: EmailStr
    telefone: str
    data_nascimento: DataBR
    cpf: str
    salario: Decimal
    passagem: Decimal
    alimentacao: Decimal


class FuncionariosResponse(BaseModel):
    id: int
    nome: str
    email: str
    telefone: str
    data_nascimento: DataBR
    cpf: str
    salario: Decimal
    passagem: Decimal
    alimentacao: Decimal


class FuncionariosDB(FuncionariosCreate):
    id: int


class Message(BaseModel):
    message: str


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 10


class FilterFuncionarios(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    telefone: str | None = None
    data_nascimento: DataBR | None = None
    cpf: str | None = None
    salario: Decimal | None = None
    passagem: Decimal | None = None
    alimentacao: Decimal | None = None


class FuncionariosList(BaseModel):
    funcionarios: list[FuncionariosResponse]


class FuncionariosUpdate(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    telefone: str | None = None
    data_nascimento: DataBR | None = None
    cpf: str | None = None
    salario: Decimal | None = None
    passagem: Decimal | None = None
    alimentacao: Decimal | None = None
