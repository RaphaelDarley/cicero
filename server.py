from fastapi import FastAPI, Request
from surrealdb import Surreal
from embed import embed
import dotenv
from aijson import Flow
import json
from fastapi.middleware.cors import CORSMiddleware

dotenv.load_dotenv(".env")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/mock")
async def mock(request: Request):
    return {
    "isTrue": True,
    "certaintyScore": 85,
    "correctedFact": None, 
    "graphData": { 
        "nodes": [
        { "id": "1", "label": "Source A" },
        { "id": "2", "label": "Source B" },
        { "id": "3", "label": "Claim X" }
        ],
        "links": [
        { "source": "1", "target": "3" },
        { "source": "2", "target": "3" }
        ]
    }
    }

@app.get("/")
async def root(request: Request):
    body = await request.body()
    statement = body.decode("utf-8")
    facts = await search(statement)
    print(facts)
    return {"proven": facts}

@app.post("/")
async def ingest(request: Request):
    body = await request.body()
    body_str = body.decode("utf-8")

    db = Surreal("ws://127.0.0.1:8001/rpc")
    await db.connect()
    await db.use('cicero', 'cicero')

    #split
    split_flow = Flow.from_file("./flows/info_to_facts.ai.yaml").set_vars(info=body_str)
    fact_str = await split_flow.run()
    facts = json.loads(fact_str)

    #embed and insert
    for f in facts:
        f_embed = embed(f)
        if f_embed is None: continue
        res = await db.create('fact', {"data": f, "embed": f_embed})
        print(res)
        
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
    others = await db.query("SELECT id, data FROM fact WHERE embed <|5|> $input", vars={"input": fact_embed})

    #check
    check_flow = Flow.from_file("flows/facts_to_truth.ai.yaml")
    res = await check_flow.set_vars(hypothesis=fact, facts=others).run()

    print(res)
    # return "PROVEN" in res and "DISPROVEN" not in res
    if "DISPROVEN" in res:
        return "DISPROVEN"
    elif "PROVEN" in res:
        return "PROVEN"
    elif "NEITHER: IRRELEVANT" in res:
        return "NEITHER: IRRELEVANT"
    elif "NEITHER: CONTRADICTION" in res:
        return "NEITHER: CONTRADICTION"
    else:
        return "ERROR"


    #split

    #recurce

    # return 
