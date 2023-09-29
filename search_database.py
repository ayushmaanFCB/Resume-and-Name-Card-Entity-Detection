import gradio
from mongodb_connect import searchFromDB


def search(keyword):
    output = searchFromDB(keyword)
    print(output)
    return output


interface = gradio.Interface(
    fn=search,
    inputs=[gradio.Textbox()],
    outputs="text"
)
