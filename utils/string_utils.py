import re
from PyPDF2 import PdfReader
import pdfplumber


def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        if pdf.pages:
            text = pdf.pages[0].extract_text()
    return text


def extract_content(file, key):
    metadata = extract_metadata(file)
    keywords = metadata.get(f'/{key}', f"No cuenta con {key}") 
    if keywords == "":
        if key is not "doi":
            return f"No cuenta con {key}"
        else:
            contenido = extract_text_from_pdf(file)
            # logica para obtener el doi mediante regex 
            doi_pattern = r'(?:doi:\s*|digital\s+object\s+identifier\s*|https?://(?:dx\.)?doi\.org/)?(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)'
    
            # Buscar el primer DOI que coincida en el texto
            match = re.search(doi_pattern, contenido, flags=re.IGNORECASE)
            
            # Si hay coincidencia, devolver el DOI encontrado
            if match:
                return match.group(1)
            else:
                return f"No cuenta con {key}"

    return keywords


def extract_year(text):
    # Extraer el año usando regex buscando un numero con 4 digitos
    year_match = re.findall(r'\b(\d{4})\b', text)
    year = year_match[0] if year_match else "Año no encontrado"
    return year


# def extract_author(text):
#     # Extraer el nombre del autor/autores antes de palabras clave como "para optar e" o similares
#     author_match = re.search(r'Autor(?:es)?:\s*(.*?)(?=\n|para optar el|$)', text, re.DOTALL | re.IGNORECASE)
#     author = author_match.group(1).strip() if author_match else "Autor no encontrado"
#     return author


# def extract_abstract(text):
#     # Define the regular expression for detecting the "Abstract" section
#     abstract_start = re.search(r'\bAbstract\b[:\s]*', text, re.IGNORECASE)
    
#     if not abstract_start:
#         return "Abstract no encontrado"
    
#     start_index = abstract_start.end()
    
#     abstract_end = re.search(r'\b(?:Introduction|Background|Keywords|1\.|I\.)\b', text[start_index:], re.IGNORECASE)
    
#     if abstract_end:
#         end_index = start_index + abstract_end.start()
#         return text[start_index:end_index].strip()
#     else:
#         return text[start_index:].strip()

def extract_metadata(file):
    reader = PdfReader(file)
    metadata = reader.metadata
    print(metadata)
    return metadata