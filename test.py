import aijson
from aijson import Flow
import dotenv
import os

dotenv.load_dotenv(dotenv_path=".env")

#flow = Flow.from_file("./flows/facts_to_truth.ai.yaml")

async def main():
    flow1 = Flow.from_file("./flows/facts_to_truth.ai.yaml").set_vars(facts = '''
["Bob is a hacker", "All hackers like cats", "Cats are mammals", "Dogs are mammals", "Bob likes dogs", "Bob hates all mammals", "Horses are mammals", "Bob hates horses", "Mammals nurse their young"]
''',
hypothesis = "Bob hates cats")
    res1 = await flow1.run()
    print(res1)

    flow2 = Flow.from_file("./flows/get_relevant_facts.ai.yaml").set_vars(para = res1)
    res2 = await flow2.run()
    print(res2)
    


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())