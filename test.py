import aijson
from aijson import Flow
import dotenv
import os

dotenv.load_dotenv(dotenv_path=".env")

async def main():

    flow = Flow.from_file("./flows/statements_to_facts.ai.yaml")

    res = await flow.run()
    print(res)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())