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

@app.get("/")
async def root(request: Request):
    body = await request.body()
    statement = body.decode("utf-8")
    result = await search(statement)
    print(result)
    return result

@app.post("/ingest")
async def ingest(request: Request):
    body = await request.body()
    body_str = body.decode("utf-8")

    db = Surreal("ws://127.0.0.1:8001/rpc")
    await db.connect()
    await db.use('cicero', 'cicero')

    doc_embed = await embed(body_str)
    doc_res = await db.create('fact', {"data":body_str, "embed": doc_embed, "source": "ingested by endpoint"})
    doc_record = doc_res[0]["id"]

    #split
    split_flow = Flow.from_file("./flows/info_to_facts.ai.yaml").set_vars(info=body_str)
    fact_str = await split_flow.run()
    facts = json.loads(fact_str)

    #embed and insert
    for f in facts:
        f_embed = await embed(f)
        if f_embed is None: continue
        res = await db.create('fact', {"data": f, "embed": f_embed})
        print(res)
        fact_id = res[0]["id"]
        await db.query("RELATE $doc->related->$fact SET kind ='proves'", {"fact": fact_id, "doc": doc_record})
        
    return None


async def search(statement: str):
    db = Surreal("ws://127.0.0.1:8001/rpc")
    await db.connect()
    await db.use('cicero', 'cicero')

    return await rec_fact_find(db, statement)

async def rec_fact_find(db: Surreal, fact: str):
    #embed
    fact_embed = await embed(fact)

    #lookup
    others = await db.query("SELECT id, data FROM fact WHERE embed <|5|> $input", vars={"input": fact_embed})
    facts = others[0]["result"]
    print(facts)

    #check
    check_flow = Flow.from_file("flows/facts_to_truth.ai.yaml")
    res_str = await check_flow.set_vars(hypothesis=fact, facts=others).run()
    print(res_str)
    res = json.loads(res_str)

    print(res)
    conc= res["conclusion"]
    if conc == "DISPROVEN":
        return res
        # return "DISPROVEN"
    elif conc == "PROVEN":
        # add to graph then return
        res_embed = await embed(res["hypothesis"])
        res_id = (await db.create("fact", {"data": res["hypothesis"], "embed": res_embed}))[0]["id"]
        # fact_ids = [rel["id"] for rel in res["relevant_facts"]]
        # await db.query("RELATE $facts->related->$new SET kind ='proves', reason=$reason", {"new": res_id, "facts": fact_ids, "reason":})
        for rel in res["relevant_facts"]:
            await db.query("RELATE $fact->related->$new SET kind ='proves', reason=$reason", {"new": res_id, "fact": rel["id"], "reason":rel["use"]})


        return res
        # return "PROVEN"
    elif conc == "IRRELEVANT":
        # split and recurse
        return "IRRELEVANT"
    elif conc == "CONTRADICTION":
        return "CONTRADICTION"
    else:
        return "ERROR"


    #split

    #recurce

    # return 
