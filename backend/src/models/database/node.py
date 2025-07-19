from sqlalchemy import VARCHAR, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import Mapped, mapped_column

from .agent_node import AgentNode
from .base import BaseTableModel
from .graph import Graph


class Node(BaseTableModel):
    __tablename__ = "node"

    type: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
        index=True,
    )
    graphId: Mapped[str] = mapped_column(
        VARCHAR(255),
        ForeignKey(Graph.id),
        nullable=False,
        index=True,
    )
    agentNodeId: Mapped[str] = mapped_column(
        VARCHAR(255),
        ForeignKey(AgentNode.id),
        nullable=True,
        default_factory=lambda: None,
        server_default=None,
    )
    isBaseEntryPoint: Mapped[bool] = mapped_column(
        TINYINT(1),
        nullable=False,
        default_factory=lambda: False,
        server_default="0",
    )
