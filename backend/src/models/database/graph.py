from sqlalchemy import VARCHAR, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseTableModel
from .user import User


class Graph(BaseTableModel):
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
