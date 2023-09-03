import gradio
import numpy as np
import pandas as pd
import cv2
import pytesseract
from glob import glob
import spacy
import re
import string
import io
import warnings
warnings.filterwarnings('ignore')


try:
    # Load NER model
    model_ner = spacy.load('./model_Namecard/model-best')
    print("\nNAMECARD NER model loaded successfully.......... \Mounting Gradio App........\n")
except Exception as e:
    print(e)


def cleanText(txt):
    whitespace = string.whitespace
    punctuation = "!#$%&\'()*+:;<=>?[\\]^`{|}~"
    tableWhitespace = str.maketrans('', '', whitespace)
    tablePunctuation = str.maketrans('', '', punctuation)
    text = str(txt)
    text = text.lower()
    removewhitespace = text.translate(tableWhitespace)
    removepunctuation = removewhitespace.translate(tablePunctuation)

    return str(removepunctuation)


def namecard_ner(filePath):
    # Load Image
    image = cv2.imread(
        'D:\\RecruitNXT - Internship (2023)\\Text Extraction Course\\data\\6.jpg')

    # Extract data using Pytesseract
    tessData = pytesseract.image_to_data(image)

    # Convert into dataframe
    tessList = list(map(lambda x: x.split('\t'), tessData.split('\n')))
    df = pd.DataFrame(tessList[1:], columns=tessList[0])
    df.dropna(inplace=True)  # drop missing values
    df['text'] = df['text'].apply(cleanText)

    # Convet data into content
    df_clean = df.query('text != "" ')
    content = " ".join([w for w in df_clean['text']])

    # Get prediction from NER model
    doc = model_ner(content)

    docjson = doc.to_json()
    docjson.keys()

    doc_text = docjson['text']

    datafram_tokens = pd.DataFrame(docjson['tokens'])
    datafram_tokens['token'] = datafram_tokens[['start', 'end']].apply(
        lambda x: doc_text[x[0]:x[1]], axis=1)
    datafram_tokens.head(5)

    right_table = pd.DataFrame(docjson['ents'])[['start', 'label']]
    datafram_tokens = pd.merge(
        datafram_tokens, right_table, how='left', on='start')

    datafram_tokens.fillna('O', inplace=True)

    # Join lable to df_clean dataframe
    df_clean['end'] = df_clean['text'].apply(lambda x: len(x)+1).cumsum() - 1
    df_clean['start'] = df_clean[['text', 'end']].apply(
        lambda x: x[1] - len(x[0]), axis=1)

    # Inner Join with start
    dataframe_info = pd.merge(
        df_clean, datafram_tokens[['start', 'token', 'label']], how='inner', on='start')

    bb_df = dataframe_info.query("label != 'O' ")
    img = image.copy()

    for x, y, w, h, label in bb_df[['left', 'top', 'width', 'height', 'label']].values:
        x = int(x)
        y = int(y)
        w = int(w)
        h = int(h)

        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(img, str(label), (x, y),
                    cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 2)

    _, buffer = cv2.imencode('.jpg', img)

    # cv2.imshow('Predictions', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    img_array = cv2.imdecode(np.frombuffer(
        buffer, dtype=np.uint8), cv2.IMREAD_COLOR)
    return img_array


gradio.Interface(
    fn=namecard_ner,
    inputs=gradio.File(label="Upload Business Card Picture"),
    outputs=gradio.Image(label="Entities detected")
).launch()
