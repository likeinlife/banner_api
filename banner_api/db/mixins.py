import datetime as dt

import sqlalchemy as sa
import sqlalchemy.orm as orm


class DateTimeMixin:
    created_at: orm.Mapped[dt.datetime] = orm.mapped_column(server_default=sa.func.now(), init=False)
    updated_at: orm.Mapped[dt.datetime] = orm.mapped_column(
        onupdate=sa.func.now(), init=False, server_default=sa.func.now()
    )
