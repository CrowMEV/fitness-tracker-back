import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, intpk


class User(Base):
    __tablename__ = "users"
    id: Mapped[intpk] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(128))
    email: Mapped[str] = mapped_column(sa.String, unique=True)
    password: Mapped[str]
    is_trainer: Mapped[bool] = mapped_column(server_default=sa.false())
    is_active: Mapped[bool] = mapped_column(server_default=sa.true())
