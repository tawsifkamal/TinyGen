from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse, StreamingResponse
from api.tiny_gen_one import TinyGenOne
from api.tiny_gen_two import TinyGenTwo
from api.db import fetch_all_calls

app = FastAPI(docs_url="/")

class TinyGenInput(BaseModel):
    prompt: str
    repoUrl: str

@app.post("/tiny_gen_one/call")
async def create_diff(tiny_gen_input: TinyGenInput):
    prompt = tiny_gen_input.prompt
    repo_url = tiny_gen_input.repoUrl

    tiny_gen_one = TinyGenOne()
    response = tiny_gen_one.call(repoUrl=repo_url, prompt=prompt)
    return response


@app.post("/tiny_gen_one/stream")
async def create_diff(tiny_gen_input: TinyGenInput):
    prompt = tiny_gen_input.prompt
    repo_url = tiny_gen_input.repoUrl

    tiny_gen_one = TinyGenOne()
    response = tiny_gen_one.stream(repoUrl=repo_url, prompt=prompt)
    
    return StreamingResponse(response, media_type='text/event-stream')

@app.post("/tiny_gen_two/call")
async def create_diff(tiny_gen_input: TinyGenInput):
    prompt = tiny_gen_input.prompt
    repo_url = tiny_gen_input.repoUrl

    tiny_gen_two = TinyGenTwo()
    response = tiny_gen_two.call(repoUrl=repo_url, prompt=prompt)
    return response

@app.post("/tiny_gen_two/stream")
async def create_diff(tiny_gen_input: TinyGenInput):
    prompt = tiny_gen_input.prompt
    repo_url = tiny_gen_input.repoUrl

    tiny_gen_two = TinyGenTwo()
    response = tiny_gen_two.stream(repoUrl=repo_url, prompt=prompt)
    
    return StreamingResponse(response, media_type='text/event-stream')

@app.get("/tiny_gen_one/get_past_calls")
async def fetch_data():
    return JSONResponse(fetch_all_calls("tiny_gen_one_calls"))


@app.get("/tiny_gen_two/get_past_calls")
async def fetch_data():
    res = fetch_all_calls("tiny_gen_two_calls")
    return JSONResponse(res)