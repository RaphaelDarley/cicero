import aijson
from aijson import Flow
import dotenv
import os

dotenv.load_dotenv(dotenv_path=".env")

async def main():

    print(os.environ["AWS_ACCESS_KEY_ID"])


    flow = Flow.from_file("./flows/test.ai.yaml")

    res = await flow.run()
    print(res)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())