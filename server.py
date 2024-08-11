from fastapi import FastAPI, Request
from surrealdb import Surreal
from embed import embed
import dotenv
from aijson import Flow
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import wikipediaapi
import static

dotenv.load_dotenv(".env")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/basic", response_class=HTMLResponse)
def basic_page():
    return static.page()



@app.api_route("/query", methods=["POST", "GET"])
async def root(request: Request):
    body = await request.body()
    statement = body.decode("utf-8")
    result = await search(statement)
    print(result)
    return result

@app.api_route("/ingest-wiki", methods=["POST", "GET"])
async def ingest_wiki(request: Request):
    body = await request.body()
    body_str = body.decode("utf-8")
    wiki_wiki = wikipediaapi.Wikipedia('Cicero (cicero@darley.dev)', 'en')
    
    # Get the page for the given topic
    page = wiki_wiki.page(body_str)
    
    # Check if the page exists
    if page.exists():
        print(f"intesting Wikipedia article on: {body_str}")
        return await ingest_str(page.text, source=page.canonicalurl)
    else:
        return f"No Wikipedia article found for the topic: {body_str}"


@app.api_route("/ingest", methods=["POST", "GET"])
async def ingest(request: Request):
    body = await request.body()
    body_str = body.decode("utf-8")
    print(f"ingesting: {body_str}")
    await ingest_str(body_str)

async def ingest_str(doc: str, source=None):
    db = Surreal("ws://127.0.0.1:8001/rpc")
    await db.connect()
    await db.use('cicero', 'cicero')

    doc_embed = await embed(doc)

    vars={"data":doc, "embed": doc_embed} 
    if source is not None:
        vars["source"] = source

    doc_res = await db.create('fact', vars)
    doc_record = doc_res[0]["id"]
    print(f"added doc with id: {doc_record}")

    #split
    split_flow = Flow.from_file("./flows/info_to_facts.ai.yaml").set_vars(info=doc)
    fact_str = await split_flow.run()
    try: 
        facts = json.loads(fact_str)
    except:
        return "INVALID JSON: TRY AGAIN"

    #embed and insert
    for f in facts:
        f_embed = await embed(f)
        if f_embed is None: continue
        res = await db.create('fact', {"data": f, "embed": f_embed})
        print(res)
        fact_id = res[0]["id"]
        await db.query("RELATE $doc->proves->$fact SET kind ='proves'", {"fact": fact_id, "doc": doc_record})
        
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
        # await db.query("RELATE $facts->proves->$new SET kind ='proves', reason=$reason", {"new": res_id, "facts": fact_ids, "reason":})
        for rel in res["relevant_facts"]:
            await db.query("RELATE $fact->proves->$new SET kind ='proves', reason=$reason", {"new": res_id, "fact": rel["id"], "reason":rel["use"]})

        tree = await db.query("fn::get_tree($input)", {"input": res_id})
        res["tree"] = tree[0]["result"]

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
