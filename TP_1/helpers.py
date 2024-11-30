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

        output_path = os.path.splitext(file)[0] + ".txt"
        with open(output_path, 'w') as output_file:
            output_file.write(text)

        return (text, output_path,os.path.splitext(file)[0].lower())
    except FileNotFoundError:
        return None
    except Exception as e:
        return None
    

def get_default_cv():
    configure_environment()
    cv_path = "FabricioDenardi.pdf"
    return cv_path

def get_txt_default_cv():
    cv_path = get_default_cv()
    return get_text_from_pdf(cv_path)

def save_file(file_name, content):
    with open( file_name, "wb") as f:
        f.write(content)
    

def read_file(file_path):
    '''Lee un archivo y devuelve su contenido. Adicionalmente graba el contenido de este en un txt con el mismo nombre.'''
    try:
        with open(file_path, 'r') as file:
            output_path = os.path.splitext(file_path)[0] + ".txt"
            with open(output_path, 'w') as output_file:
                output_file.write(file.read())
            return file.read()
    except FileNotFoundError:
        return "El archivo no fue encontrado."
    except Exception as e:
        return f"Se produjo un error: {e}"