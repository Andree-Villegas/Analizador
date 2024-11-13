from utils import http_utils
from PyPDF2 import PdfReader


def get_metadata_by_doi(doi) -> dict:
    url = f"https://api.crossref.org/works/{doi}"
    metadata = http_utils.make_get_request(url)
    return metadata


def get_metadata_by_file(file) -> dict:
    reader = PdfReader(file)
    metadata = reader.metadata
    return metadata

