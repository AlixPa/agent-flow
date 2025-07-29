from sqlalchemy import VARCHAR, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseTableModel
from .graph import Graph
from .user import User


class Conversation(BaseTableModel):
    __tablename__ = "conversation"

    graphId: Mapped[str] = mapped_column(
        VARCHAR(255),
        ForeignKey(Graph.id),
        nullable=False,
        index=True,
    )
    userId: Mapped[str | None] = mapped_column(
        VARCHAR(255),
        ForeignKey(User.id),
        nullable=True,
        index=True,
        default_factory=lambda: None,
        server_default=None,
    )
