import gradio
from mongodb_connect import searchFromDB


def search(parameter, keyword):
    results = searchFromDB(parameter, keyword)
    output = """
        <html>
            <head></head>
            <body>
                <ul>
    """
    for result in results:
        for skill in result['Key Points']['expertise']['skill']:
            output = output + "<li>{0}</li>".format(skill)
    output = output + "</ul></body></html>"

    return output


interface = gradio.Interface(
    fn=search,
    inputs=[gradio.Dropdown(choices=["position", "skill", "experience",
                            "certification", "company"]), gradio.Textbox()],
    outputs="text"
)
