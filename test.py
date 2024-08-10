import aijson
from aijson import Flow
import dotenv
import os

dotenv.load_dotenv(dotenv_path=".env")

async def main():

    flow = Flow.from_file("./flows/info_to_facts.ai.yaml").set_vars(info = '''Tigray Stadium is a multi-purpose stadium in Mekelle, Ethiopia. The stadium has a capacity of 60,000.[3]
Tigray Stadium was opened to the public in 2017, before the completion of the final phase of construction. As a result, football matches and other public events have been held without adequate seating and roofing. The stadium is home to five football clubs based in the Tigray region, including Mekelle 70 Enderta FC, Shire Endaselassie F.C., Welwalo Adigrat University F.C. and Dedebit FC. Notably, the overuse of the stadium's facilities has contributed to construction delays.''')

    res = await flow.run()
    print(res)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())