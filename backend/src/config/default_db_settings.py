from src.models.database import ConversationTable, GraphTable, NodeTable, UserTable


class DefaultDbSettings:
    DEFAULT_NAME = "default"
    DEFAULT_ID = "default_id"

    USER = UserTable(
        id=DEFAULT_ID,
        name=DEFAULT_NAME,
    )

    GRAPH = GraphTable(
        name=DEFAULT_NAME,
        userId=USER.id,
        id=DEFAULT_ID,
    )

    CONVERSATION = ConversationTable(
        graphId=GRAPH.id,
        userId=USER.id,
        id=DEFAULT_ID,
    )

    NODE = NodeTable(
        type=DEFAULT_NAME,
        graphId=GRAPH.id,
        id=DEFAULT_ID,
    )
