from io import StringIO
import os
import fitz
import openai
from dotenv import load_dotenv
from nltk.tokenize import sent_tokenize

load_dotenv()


def open_file(filepath):
    with open(filepath, "r", encoding="utf-8") as infile:
        return infile.read()


openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")


def read_pdf(filename):
    context = ""

    # Open the PDF file
    with fitz.open(filename) as pdf_file:
        # Get the number of pages in the PDF file
        num_pages = pdf_file.page_count

        # Loop through each page in the PDF file
        for page_num in range(num_pages):
            # Get the current page
            page = pdf_file[page_num]

            # Get the text from the current page
            page_text = page.get_text().replace("\n", "")

            # Append the text to context
            context += page_text
    return context


def read_txt(filename):
    f = open(filename, "r")
    message = f.read()
    f.close()
    return message


def split_text(text, chunk_size=5000):
    """
    Splits the given text into chunks of the specified chunk size.

    Args:
    text (str): The text to split.

    chunk_size (int): The desired size of each chunk (in characters).

    Returns:
    List[str]: A list of chunks, each of the specified chunk size.
    """

    chunks = []
    current_chunk = StringIO()
    current_size = 0
    sentences = sent_tokenize(text)
    for sentence in sentences:
        sentence_size = len(sentence)
        if sentence_size > chunk_size:
            while sentence_size > chunk_size:
                chunk = sentence[:chunk_size]
                chunks.append(chunk)
                sentence = sentence[chunk_size:]
                sentence_size -= chunk_size
                current_chunk = StringIO()
                current_size = 0
        if current_size + sentence_size < chunk_size:
            current_chunk.write(sentence)
            current_size += sentence_size
        else:
            chunks.append(current_chunk.getvalue())
            current_chunk = StringIO()
            current_chunk.write(sentence)
            current_size = sentence_size
    if current_chunk:
        chunks.append(current_chunk.getvalue())
    return chunks


os.listdir(os.path.dirname(__file__))
filename = os.path.join(os.path.dirname(__file__), "filename.pdf")


def gpt3_completion(question, text):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a teacher"},
            {"role": "user", "content": question},
            {"role": "user", "content": text},
        ],
    )


def find_doc():
    L = os.listdir(os.path.dirname(__file__))
    Liste_doc = []
    for i in range(len(L)):
        if (L[i][-3:] == "pdf") or (L[i][-3:] == "txt"):
            Liste_doc.append(L[i])
    return Liste_doc


def ask_question_to_pdf(question, filename):
    path_file = os.path.join(os.path.dirname(__file__), filename)
    if filename[-3:] == "pdf":
        document = read_pdf(path_file)
    if filename[-3:] == "txt":
        document = read_txt(path_file)
    # chunks = split_text(document)
    return gpt3_completion(question, document)["choices"][0]["message"]["content"]
