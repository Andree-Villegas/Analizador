import re
from PyPDF2 import PdfReader
import pdfplumber


def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        if pdf.pages:
            text = pdf.pages[0].extract_text()
    return text




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


def extract_year(text):
    # Extraer el año usando regex buscando un numero con 4 digitos
    year_match = re.findall(r'\b(\d{4})\b', text)
    year = year_match[-1] if year_match else "Año no encontrado"
    return year


def extract_author(text):
    # Extraer el nombre del autor/autores antes de palabras clave como "para optar e" o similares
    author_match = re.search(r'Autor(?:es)?:\s*(.*?)(?=\n|para optar el|$)', text, re.DOTALL | re.IGNORECASE)
    author = author_match.group(1).strip() if author_match else "Autor no encontrado"
    return author


def extract_keywords(text):
    """
    Extracts the keywords from the text. The keywords are assumed to appear after the word 'Keywords' or 'Palabras clave',
    potentially spanning multiple lines.
    
    :param text: The full text extracted from the PDF article.
    :return: A string containing the keywords.
    """
    # Search for "Keywords" or "Palabras clave" (supports both English and Spanish)
    keywords_start = re.search(r'\b(?:Keywords|Palabras clave)\b[:\s]*', text, re.IGNORECASE)
    
    if not keywords_start:
        return "Keywords not found."
    
    # Start reading after the "Keywords" label
    start_index = keywords_start.end()
    
    # Get the text starting from the location of the keywords
    keywords_section = text[start_index:]
    
    # Split the remaining text into lines
    lines = keywords_section.splitlines()
    
    # Collect lines that are part of the keywords section
    keywords_lines = []
    
    for line in lines:
        # Clean the line
        cleaned_line = line.strip()
        
        # Stop if we hit an empty line or a new section heading
        if not cleaned_line or re.match(r'\b(?:Introduction|Background|Resumen|1\.|I\.)\b', cleaned_line, re.IGNORECASE):
            break
        
        # Add the current line to the list if it's not empty
        keywords_lines.append(cleaned_line)
    
    # Join all lines to form the full keywords string
    keywords = " ".join(keywords_lines).strip()
    
    return keywords if keywords else "Keywords not found."

def extract_abstract(text):
    # Define the regular expression for detecting the "Abstract" section
    abstract_start = re.search(r'\bAbstract\b[:\s]*', text, re.IGNORECASE)
    
    if not abstract_start:
        return "Abstract no encontrado"
    
    start_index = abstract_start.end()
    
    abstract_end = re.search(r'\b(?:Introduction|Background|Keywords|1\.|I\.)\b', text[start_index:], re.IGNORECASE)
    
    if abstract_end:
        end_index = start_index + abstract_end.start()
        return text[start_index:end_index].strip()
    else:
        return text[start_index:].strip()

def extract_info(file):
    reader = PdfReader(file)
    metadata = reader.metadata
    print(metadata)