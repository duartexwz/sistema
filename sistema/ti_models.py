from sqlalchemy.orm import Mapped, mapped_column, registry

registro_tabela_ti = registry()


@registro_tabela_ti.mapped_as_dataclass
class UsuariosTi:
    __tablename__ = "usuarios_ti"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    usuario: Mapped[str] = mapped_column(unique=True)
    email_corp: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str] = mapped_column(nullable=False)
