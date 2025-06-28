from sqlalchemy import VARCHAR, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import Mapped, mapped_column

from .agent_node import AgentNode
from .base import SqlBaseModel
from .graph import Graph


class Node(SqlBaseModel):
    __tablename__ = "node"

    type: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
        index=True,
    )
    agentNodeId: Mapped[str] = mapped_column(
        VARCHAR(255),
        ForeignKey(AgentNode.id),
        nullable=True,
        server_default=None,
    )
    graphId: Mapped[str] = mapped_column(
        VARCHAR(255),
        ForeignKey(Graph.id),
        nullable=False,
        index=True,
    )
    isBaseEntryPoint: Mapped[bool] = mapped_column(
        TINYINT(1),
        nullable=False,
        server_default="0",
    )
