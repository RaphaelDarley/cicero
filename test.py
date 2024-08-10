import aijson
from aijson import Flow
import dotenv
import os

dotenv.load_dotenv(dotenv_path=".env")

async def main():

    flow = Flow.from_file("./flows/statements_to_facts.ai.yaml").set_vars(info = '''
["Hackers like dogs", "Hackers like cats"]
''')

    #flow = Flow.from_file("./flows/facts_to_truth.ai.yaml")

    res = await flow.run()
    print(res)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())