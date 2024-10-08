from flask import Flask, request, render_template, send_file, redirect, url_for
import pdfplumber
import re
import pandas as pd
from io import BytesIO

app = Flask(__name__)

# Lista global para almacenar los datos extraídos de múltiples PDFs
extracted_data_list = []

@app.route('/')
def index():
    return render_template('index.html', data=extracted_data_list)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    # Extraer texto del PDF
    text = extract_text_from_pdf(file)

    # Extraer el título, el año y el autor del texto usando las funciones separadas
    title = extract_title(text)
    year = extract_year(text)
    author = extract_author(text)

    # Agregar el título, el año y el autor a la lista de datos extraídos con un identificador único
    title_id = len(extracted_data_list) + 1
    extracted_data_list.append({'id': title_id, 'Título': title, 'Año': year, 'Autor': author})

    return redirect(url_for('index'))

@app.route('/export', methods=['POST'])
def export():
    global extracted_data_list
    
    # Crear un DataFrame con los datos extraídos
    df = pd.DataFrame(extracted_data_list)

    # Guardar el DataFrame en un buffer en memoria como un archivo Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Datos')
    output.seek(0)

    # Enviar el archivo Excel al usuario
    return send_file(output, download_name='datos.xlsx', as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/delete/<int:title_id>', methods=['POST'])
def delete(title_id):
    global extracted_data_list
    extracted_data_list = [item for item in extracted_data_list if item['id'] != title_id]
    return redirect(url_for('index'))

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
    # Extraer el año como los últimos cuatro dígitos en el texto
    year_match = re.findall(r'\b(\d{4})\b', text)
    year = year_match[-1] if year_match else "Año no encontrado"
    return year

def extract_author(text):
    # Extraer el nombre del autor/autores antes de palabras clave como "para optar e" o similares
    author_match = re.search(r'Autor(?:es)?:\s*(.*?)(?=\n|para optar el|$)', text, re.DOTALL | re.IGNORECASE)
    author = author_match.group(1).strip() if author_match else "Autor no encontrado"
    return author

if __name__ == '__main__':
    app.run(debug=True)