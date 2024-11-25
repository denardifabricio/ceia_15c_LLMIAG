import os
from PyPDF2 import PdfReader

def configure_environment():
    # Por alguna razón en mi entorno de ios no me tomaba los path relativos. 
    # Este hack me evita tener que poner los path absolutos en el código.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)


def get_text_from_pdf(file):    
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except FileNotFoundError:
        return None
    except Exception as e:
        return None
    

def get_default_cv():
    configure_environment()
    cv_path = "CVFabricioDenardi.pdf"
    return cv_path

def get_txt_default_cv():
    cv_path = get_default_cv()
    return get_text_from_pdf(cv_path)

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "El archivo no fue encontrado."
    except Exception as e:
        return f"Se produjo un error: {e}"