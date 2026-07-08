from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, mapped_column
from typing_extensions import Annotated

intpk = Annotated[int, mapped_column(primary_key=True)]
# pylint: disable=E1102
created_at = Annotated[datetime, mapped_column(server_default=sa.func.now())]


class Base(DeclarativeBase):
    metadata = sa.MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%"
            "(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )
