import datetime as dt
import uuid
from dataclasses import dataclass

import sqlalchemy as sa
import sqlalchemy.orm as orm


@dataclass
class ReprSettings:
    cols: tuple[str, ...] = ("created_at", "updated_at")
    num: int = 3


class Base(orm.MappedAsDataclass, orm.DeclarativeBase):
    repr = ReprSettings()
    type_annotation_map = {
        dt.datetime: sa.DateTime(True),
        uuid.UUID: sa.UUID(True),
    }

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr.cols or idx < self.repr.num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
