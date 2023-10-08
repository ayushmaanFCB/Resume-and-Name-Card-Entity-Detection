# MODULES AND CUSTOM SCRIPTS

from scripts.text_from_docx import extractFromDOCX
from scripts.text_from_pdf import extractFromPDF
from scripts.structure_resume_data import structureData

from mongodb_connect import pushToDB

import gradio
import spacy
from spacy import displacy
import json
import warnings
from pprint import pprint
warnings.filterwarnings('ignore')


# LOADING THE CUSTOM TRAINED SPACY MODEL

try:
    resume_nlp = spacy.load("./model_combined")
    print("\n\x1b[35mRESUME NER model loaded successfully..........\x1b[0m \n \x1b[36mMounting Gradio App........\n\x1b[0m")

except Exception as e:
    print(e)

with open("./static/jsons/label_config.json", "r") as file:
    datas = json.load(file)
color_schemes = {}
for data in datas:
    color_schemes.update({data['text']: data['backgroundColor']})

# TEXT EXTRACTION FROM RESUME AND ENTITY DETECTION


def resume_ner(filePath):
    if filePath.name.endswith(".pdf"):
        text = extractFromPDF(filePath)
    if filePath.name.endswith(".docx"):
        text = extractFromDOCX(filePath)

    # DETECTING ENTITIES
    doc = resume_nlp(text)

    # DISPLAYING ENTITIES USING DISPLACY
    output = displacy.render(doc, style="ent", page=True, options={
                             "colors": color_schemes})

    html = "<div style='text-align:justify'>" + \
        output + "</div>"

    tokens = []
    for ent in doc.ents:
        tokens.append({ent.text: ent.label_})

    details = {
        "character_count": len(text),
        "token_count": len(doc.ents),
    }

    structured_data = structureData(doc)

    details.update({"Key Points": structured_data})

    return html, details


# PUSH TO DATABASE

def uploadData(post):
    if post != None:
        try:
            result = pushToDB(post)
            print("\n\033[31mData pushed to database successfully : \033[0m\n")
            return "<h2 style='color:green'>DATA UPDATED SUCCESSFULLY !!!</h2> <h3 style='color:green'>ID : {0}</h3>".format(result.inserted_id)
        except Exception as e:
            print("Error pushing the Data :: ", e)
            return None
    else:
        raise gradio.Error("Upload a Resume First")


# OUTPUT USING GRADIO (Python Web Framework)
with gradio.Blocks(theme=gradio.themes.Monochrome(), title="NER from Resume") as block:
    with gradio.Row():
        gradio.HTML(
            "<h1 style='text-align:center; font-size:40px'>Entity Recognition from Resume using Custom Trained Model</h1><hr>")
    with gradio.Row():
        with gradio.Column(scale=1):
            upload_button = gradio.UploadButton(
                "Click to Upload a Resume File", file_count="single", size='lg')
            save_button = gradio.Button(
                value="Save to Cloud Database", visible=True, interactive=True)
            id_area = gradio.HTML(
                "<h2>Reference ID will be shown here on upload : </h2>", label="REFERENCE ID")

        with gradio.Column(scale=2.5):
            # EXAMPLES
            gradio.HighlightedText(value=[("Ayushmaan Das", "name"),
                                          ("+91 8145328571", "phone"),
                                          ("dasayush5maan@gmail.com", "email"),
                                          ("http://www.github.com/ayushmaanFCB", "url"),
                                          ("Chennai, TN", "location"),
                                          ("English", "language"),
                                          ("B.Tech AI and ML", "course"),
                                          ("B. Tech CSE AI and ML", "education"),
                                          ("Recruit NXT", "company"),
                                          ("Python Developer", "position"),
                                          ("Worked 2 years", "experience"),
                                          ("Developing ML Models", "role"),
                                          ("Angular, Spring, Python", "skill"),
                                          ("Resume Parsing and NER", "project"),
                                          ("Certified in Power BI",
                                           "certification"),
                                          ("Beest intern award", "award"),
                                          ("Published research paper on Twitter API",
                                           "publication")
                                          ], label="SAMPLE ENTITIES")

    with gradio.Row():
        gradio.HTML(
            "<br><h1>Detected Entities will appear here: </h1>")
    with gradio.Row():
        with gradio.Tab("DisplaCy Output"):
            output_html = gradio.HTML(label="DETECTED ENTITIES")
        with gradio.Tab("JSON Output"):
            output_details = gradio.JSON(label="DETECTED ENTITIES")
        upload_button.upload(resume_ner, inputs=upload_button, outputs=[
                             output_html, output_details], show_progress=True, scroll_to_output=True)
        save_button.click(fn=uploadData, inputs=[
                          output_details], outputs=[id_area])
