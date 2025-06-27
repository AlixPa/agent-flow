from sqlalchemy import VARCHAR, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import SqlBaseModel
from .node import Node


class Edge(SqlBaseModel):
    __tablename__ = "edge"

    fromNodeId: Mapped[str] = mapped_column(
        VARCHAR(255),
        ForeignKey(Node.id),
        nullable=False,
        index=True,
    )
    toNodeId: Mapped[str] = mapped_column(
        VARCHAR(255),
        ForeignKey(Node.id),
        nullable=False,
        index=True,
    )
