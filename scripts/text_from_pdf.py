import re
import PyPDF2


def extractFromPDF(filePath):

    filePath = filePath.name

    if filePath.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(filePath)
        text = ''
        for page in range(len(pdf_reader.pages)):
            page_obj = pdf_reader.pages[page]
            text += escape_ansi(page_obj.extract_text())
        return text


def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line).replace("\n", ".").replace("*", "").replace("\\", "").replace(" ..", ". ").replace("..", ".")
