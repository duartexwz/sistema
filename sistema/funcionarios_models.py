from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column, registry

registro_tabela_funcionarios = registry()


@registro_tabela_funcionarios.mapped_as_dataclass
class Funcionarios:
    __tablename__ = "funcionarios"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    cpf: Mapped[str] = mapped_column(unique=True)
    telefone: Mapped[str] = mapped_column(unique=True)
    data_nascimento: Mapped[date] = mapped_column(Date, nullable=False)
    salario: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    passagem: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    alimentacao: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
