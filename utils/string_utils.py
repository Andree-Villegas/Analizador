
import pdfplumber
import re

def extract_title(text):
    # Patrón 1: Después de "Tesis:" y permite comillas alrededor del título
    match_1 = re.search(r'Tesis:\s*["\']?([\s\S]*?)(?=\n\s*\n|$)["\']?(?:\s+\d{4})?', text, re.IGNORECASE)

    # Patrón 2: Después de "Tesis" y permite comillas alrededor del título
    match_2 = re.search(r'Tesis\s*["\']?([\s\S]*?)(?=\n\s*\n|$)["\']?(?:\s+\d{4})?', text, re.IGNORECASE)
    
    # Patrón 3: Después de "TRABAJO DE INVESTIGACIÓN" y permite comillas alrededor del título
    match_3 = re.search(r'TRABAJO DE INVESTIGACIÓN\s*["\']?([\s\S]*?)(?=\n\s*\n|$)["\']?(?:\s+\d{4})?', text, re.IGNORECASE)
    
    # Patrón 4: Antes de "Tesis para obtener el" y permite comillas alrededor del título
    match_4 = re.search(r'["\']?([\s\S]*?)(?=\s*Tesis para obtener el)["\']?(?:\s+\d{4})?', text, re.IGNORECASE)
    
    # Determinar cuál coincidencia utilizar
    if match_1:
        title = match_1.group(1).strip()
    elif match_2:
        title = match_2.group(1).strip()
    elif match_3:
        title = match_3.group(1).strip()
    elif match_4:
        title = match_4.group(1).strip()
    else:
        title = "Título no encontrado"
    
    return title


def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        if pdf.pages:
            text = pdf.pages[0].extract_text()
    return text



def extract_year(text):
    # Extraer el año como los últimos cuatro dígitos en el texto
    year_match = re.findall(r'\b(\d{4})\b', text)
    year = year_match[-1] if year_match else "Año no encontrado"
    return year


def extract_author(text):
    # Extraer el nombre del autor/autores antes de palabras clave como "para optar e" o similares
    author_match = re.search(r'Autor(?:es)?:\s*(.*?)(?=\n|para optar el|$)', text, re.DOTALL | re.IGNORECASE)
    author = author_match.group(1).strip() if author_match else "Autor no encontrado"
    return author
