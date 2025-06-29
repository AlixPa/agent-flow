from sqlalchemy import TEXT, VARCHAR, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .agent_base import AgentBase
from .base import SqlBaseModel
from .graph import Graph
from .user import User


class AgentNode(SqlBaseModel):
    __tablename__ = "agent_node"

    name: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
    )
    agentBaseId: Mapped[str] = mapped_column(
        VARCHAR(255),
        ForeignKey(AgentBase.id),
        nullable=False,
        index=True,
    )
    userId: Mapped[str] = mapped_column(
        VARCHAR(255),
        ForeignKey(User.id),
        nullable=False,
        index=True,
    )
    graphId: Mapped[str] = mapped_column(
        VARCHAR(255),
        ForeignKey(Graph.id),
        nullable=False,
        index=True,
    )
    customModel: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=True,
        default_factory=lambda: None,
        server_default=None,
    )
    customPrompt: Mapped[str] = mapped_column(
        TEXT(),
        nullable=True,
        default_factory=lambda: None,
        server_default=None,
    )
    UniqueConstraint("name", "userId", "graphId")
