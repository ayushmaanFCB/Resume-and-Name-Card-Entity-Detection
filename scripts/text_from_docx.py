import re
import PyPDF2
import docx2txt


def extractFromDOCX(filePath):

    filePath = filePath.name

    if filePath.endswith(".docx"):
        text = docx2txt.process(filePath)
        return escape_ansi(text)


def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line).replace("\n", ".").replace("*", "").replace("\\", "").replace(" ..", ". ").replace("..", ".")
