import gradio
# from test import block_test

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from resume_NER import block as resumeBlock
from namecard_NER import block as namecardBlock
from search_database import block as search_block

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

app.mount("/static", StaticFiles(directory="static"), name="static")

app = gradio.mount_gradio_app(app, resumeBlock, path="/resumeNER")
app = gradio.mount_gradio_app(app, namecardBlock, path="/namecardNER")
app = gradio.mount_gradio_app(app, search_block, path="/search")
# app = gradio.mount_gradio_app(app, block_test, path="/test")


# @app.get("/saveResume", response_class=HTMLResponse)
# async def read_item(request: Request):
#     return templates.TemplateResponse("database.html", {"request": request})
