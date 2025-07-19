import asyncio

from src.clients import AMysqlClientReader, AMysqlClientWriter
from src.models.database import EdgeTable


async def main():
    reader = AMysqlClientReader()

    print(
        await reader.select(table=EdgeTable, cond_equal={"fromNodeId": "nodeOutput1"})
    )


if __name__ == "__main__":
    asyncio.run(main())
