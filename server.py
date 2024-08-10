from fastapi import FastAPI, Request
from surrealdb import Surreal
from embed import embed
import dotenv

dotenv.load_dotenv(".env")
app = FastAPI()


@app.get("/{statement}")
async def root(statement: str):
    facts = await search(statement)
    print(facts)
    return {"facts": facts}

@app.post("/")
async def ingest(request: Request):
    body = await request.body()
    body_str = body.decode("utf-8")

    db = Surreal("ws://127.0.0.1:8001/rpc")
    await db.connect()
    await db.use('cicero', 'cicero')

    #split
    facts = [body_str]

    #embed
    # embeded = [(fact) for fact in facts]
    for f in facts:
        f_embed = embed(f)
        if f_embed is None: continue
        res = await db.create('fact', {"data": f, "embed": f_embed})
        print(res)
        


    #insert
    return None


async def search(statement: str):
    db = Surreal("ws://127.0.0.1:8001/rpc")
    await db.connect()
    await db.use('cicero', 'cicero')
    # facts = await db.select('fact')

    return await rec_fact_find(db, statement)

async def rec_fact_find(db: Surreal, fact: str):
    #embed
    fact_embed = embed(fact)

    #lookup

    #check

    #split

    #recurce

    return fact_embed
