import re
import pdfplumber
from utils.metadata import get_metadata_by_file


def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        if pdf.pages:
            text = pdf.pages[0].extract_text()
    return text


def get_by_key(file, metadata, key):
    keywords = metadata.get(f'/{key}', "") 
    error_response = f"No cuenta con {key}"
    if keywords is "":
        if key != "doi":
            return error_response
        else:
            # logica para obtener el doi mediante regex 
            contenido = extract_text_from_pdf(file)
            doi_pattern = r'(?:doi:\s*|digital\s+object\s+identifier\s*|https?://(?:dx\.)?doi\.org/)?(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)'
    
            # Buscar el primer DOI que coincida en el texto
            match = re.search(doi_pattern, contenido, flags=re.IGNORECASE)
            
            # Si hay coincidencia, devolver el DOI encontrado
            # return match.group(1) if match else error_response
            if match:
                return match.group(1)
            else:
                # tratando de obtener el doi mediante el contenido de subject
                doi_pattern2 = r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+'
                subject = metadata.get('/Subject', "")

                if subject == "":
                    return error_response

                match2 = re.search(doi_pattern2, subject)
                if match2:
                    return match2.group(0) 
                else:
                    # print(metadata)
                    return error_response

    return keywords


def extract_year(text):
    # Extraer el año usando regex buscando un numero con 4 digitos
    year_match = re.findall(r'\b(\d{4})\b', text)
    year = year_match[0] if year_match else "Año no encontrado"
    return year


def return_empty_result() -> dict:
    return {
        'Title': '',
    }