import gradio

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from resume_NER import block as resumeBlock
from namecard_NER import iface as namecardBlock

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


app = gradio.mount_gradio_app(app, resumeBlock, path="/resumeNER")
app = gradio.mount_gradio_app(app, namecardBlock, path="/namecardNER")
