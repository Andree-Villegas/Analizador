from flask import Flask, request, render_template, send_file, redirect, url_for
import pandas as pd
from utils import string_utils
from io import BytesIO

app = Flask(__name__)

# Lista global para almacenar los datos extraídos de múltiples PDFs
extracted_data_list = []

@app.route('/')
def index():
    return render_template('index.html', data=extracted_data_list)

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist("file")

    for file in uploaded_files:
        # Extraer texto del PDF
        text = string_utils.extract_text_from_pdf(file)
        string_utils.extract_info(file)

        # Extraer el título, el año y el autor del texto usando las funciones separadas
        title = string_utils.extract_title(text)
        year = string_utils.extract_year(text)
        author = string_utils.extract_author(text)
        abstract = string_utils.extract_abstract(text)
        keywords = string_utils.extract_keywords(text)

        # # Agregar el título, el año y el autor a la lista de datos extraídos con un identificador único
        title_id = len(extracted_data_list) + 1
        extracted_data_list.append({'id': title_id, 'Título': title, 'Año': year, 'Autor': author, 'Abstract': abstract, 'Keywords': keywords})

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

if __name__ == '__main__':
    app.run(debug=True)