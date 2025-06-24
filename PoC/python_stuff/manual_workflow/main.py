import asyncio

from .workflow import graph


async def main():
    await graph.ainvoke({})


if __name__ == "__main__":
    asyncio.run(main())
