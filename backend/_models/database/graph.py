from sqlalchemy import VARCHAR, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import SqlBaseModel
from .user import User


class Graph(SqlBaseModel):
    __tablename__ = "graph"

    name: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
    )
    userId: Mapped[str] = mapped_column(
        VARCHAR(255),
        ForeignKey(User.id),
        nullable=False,
        index=True,
    )
    UniqueConstraint("name", "userId")
