from sqlalchemy import VARCHAR, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .agent_node import AgentNode
from .base import SqlBaseModel


class Node(SqlBaseModel):
    __tablename__ = "node"

    type: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
    )
    agent_node_id: Mapped[str] = mapped_column(
        VARCHAR(255),
        ForeignKey(AgentNode.id),
        nullable=True,
        server_default=None,
    )
