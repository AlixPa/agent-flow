from sqlalchemy import TEXT, VARCHAR, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import Mapped, mapped_column

from .agent_node import AgentNode
from .base import BaseTableModel
from .conversation import Conversation
from .graph import Graph
from .node import Node
from .user import User


class GraphState(BaseTableModel):
    __tablename__ = "graph_state"

    message_history: Mapped[str] = mapped_column(
        TEXT(),
        nullable=False,
    )

    graphId: Mapped[str] = mapped_column(
        VARCHAR(255),
        ForeignKey(Graph.id),
        nullable=False,
    )
    entryNodeId: Mapped[str] = mapped_column(
        VARCHAR(255),
        ForeignKey(Node.id),
        nullable=False,
    )
    conversationId: Mapped[str] = mapped_column(
        VARCHAR(255),
        ForeignKey(Conversation.id),
        nullable=False,
        index=True,
    )
    userId: Mapped[str] = mapped_column(
        VARCHAR(255),
        ForeignKey(User.id),
        nullable=False,
    )
