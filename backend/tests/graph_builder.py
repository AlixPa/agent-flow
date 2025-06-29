import asyncio
import sys
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_PATH))

from _config import ENV, ServiceEnv
from _logger import get_logger
from _models import GraphTable, NodeTable, UserTable
from workflow import GraphBuilder, GraphState

logger = get_logger()


GRAPH_ID = "graph1"


async def main():
    graph_builder = GraphBuilder()
    graph = graph_builder.get_graph(id=GRAPH_ID)
    await graph.ainvoke(GraphState())


if __name__ == "__main__":
    if ENV != ServiceEnv.LOCAL:
        raise Exception("Should run this particular unit test locally")
    asyncio.run(main())
