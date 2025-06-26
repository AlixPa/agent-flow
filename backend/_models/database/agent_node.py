from sqlalchemy import TEXT, VARCHAR, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .agent_base import AgentBase
from .base import SqlBaseModel


class AgentNode(SqlBaseModel):
    __tablename__ = "agent_node"

    id: Mapped[str] = mapped_column(
        VARCHAR(255),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
    )
    agentBaseId: Mapped[str] = mapped_column(
        VARCHAR(255),
        ForeignKey(AgentBase.id),
        nullable=False,
    )
    prompt: Mapped[str] = mapped_column(
        TEXT(),
        nullable=True,
        server_default=None,
    )
