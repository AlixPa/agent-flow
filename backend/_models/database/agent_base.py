from sqlalchemy import TEXT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from .base import SqlBaseModel


class AgentBase(SqlBaseModel):
    __tablename__ = "agent_base"

    name: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
        unique=True,
    )
    basePrompt: Mapped[str] = mapped_column(
        TEXT(),
        nullable=False,
    )
