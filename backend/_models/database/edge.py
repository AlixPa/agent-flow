from sqlalchemy import VARCHAR, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import SqlBaseModel
from .graph import Graph
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
    graphId: Mapped[str] = mapped_column(
        VARCHAR(255),
        ForeignKey(Graph.id),
        nullable=False,
        index=True,
    )
    UniqueConstraint("fromNodeId", "toNodeId")
