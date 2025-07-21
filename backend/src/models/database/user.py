from sqlalchemy import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseTableModel


class User(BaseTableModel):
    __tablename__ = "user"

    name: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
    )
