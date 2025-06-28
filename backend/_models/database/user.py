from .base import SqlBaseModel


class User(SqlBaseModel):
    __tablename__ = "user"
