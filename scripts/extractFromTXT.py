from scripts.text_from_docx import escape_ansi


import docx2txt


def extractFromTXT(filePath):

    filePath = filePath.name

    if filePath.endswith(".docx"):
        text = docx2txt.process(filePath)
        return escape_ansi(text)
