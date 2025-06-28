import asyncio

# from .core import GraphState, graph
from .core_v2 import GraphBuilder, GraphState

GRAPH_ID = "graph1"
USER_ID = "user1"


async def main():
    graph_builder = GraphBuilder()
    graph = graph_builder.get_graph(id=GRAPH_ID)
    await graph.ainvoke(GraphState())


if __name__ == "__main__":
    asyncio.run(main())
