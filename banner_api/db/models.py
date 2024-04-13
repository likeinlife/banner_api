import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.dialects.postgresql import ARRAY

from .base import Base
from .mixins import DateTimeMixin


class BannerORM(DateTimeMixin, Base):
    __tablename__ = "banner"
    feature_id: orm.Mapped[int]
    is_active: orm.Mapped[bool]
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True, init=False)
    title: orm.Mapped[str] = orm.mapped_column(sa.String(65))
    text: orm.Mapped[str] = orm.mapped_column(sa.String(512))
    url: orm.Mapped[str] = orm.mapped_column(sa.String(128))
    tag_ids: orm.Mapped[set[int]] = orm.mapped_column(ARRAY(sa.Integer), default_factory=list)
