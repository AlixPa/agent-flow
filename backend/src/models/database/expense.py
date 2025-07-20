from sqlalchemy import DECIMAL, VARCHAR, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseTableModel
from .conversation import Conversation
from .graph import Graph
from .node import Node
from .user import User


class Expense(BaseTableModel):
    __tablename__ = "expense"

    cost: Mapped[float] = mapped_column(
        DECIMAL(precision=11, scale=8),
        nullable=False,
    )
    graphId: Mapped[str] = mapped_column(
        VARCHAR(255),
        ForeignKey(Graph.id),
        nullable=False,
        index=True,
    )
    nodeId: Mapped[str] = mapped_column(
        VARCHAR(255),
        ForeignKey(Node.id),
        nullable=False,
        index=True,
    )
    source: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
        index=True,
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
        nullable=True,
        index=True,
        default_factory=lambda: None,
        server_default=None,
    )
