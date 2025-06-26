from sqlalchemy import VARCHAR, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import SqlBaseModel
from .node import Node


class Edge(SqlBaseModel):
    __tablename__ = "edge"

    name: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
    )
    fromNodeId: Mapped[str] = mapped_column(
        VARCHAR(255),
        ForeignKey(Node.id),
        nullable=False,
    )
    toNodeId: Mapped[str] = mapped_column(
        VARCHAR(255),
        ForeignKey(Node.id),
        nullable=False,
    )
