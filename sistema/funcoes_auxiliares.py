from datetime import date, datetime
from typing import Annotated

from pydantic import BeforeValidator


def converter_cpf(cpf):  # pragma: no cover
    cpf_formatado = "".join(filter(str.isdigit, cpf))

    cpf_formatado = cpf_formatado.zfill(11)

    return f"{cpf_formatado[:3]}.{cpf_formatado[3:6]}.{cpf_formatado[6:9]}-{cpf_formatado[9:]}"


def converter_data_br(value):  # pragma: no cover
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%d/%m/%Y").date()
        except ValueError:
            raise ValueError("Formato de data inválido. Use DD/MM/YYYYY")
    return value


DataBR = Annotated[date, BeforeValidator(converter_data_br)]
