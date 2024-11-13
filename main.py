from flask import Flask, request, render_template, send_file, redirect, url_for
from utils import metadata
import pandas as pd
from utils import string_utils
from utils import http_utils
from io import BytesIO

app = Flask(__name__)

# Lista global para almacenar los datos extraídos de múltiples PDFs
articles = []

@app.route('/')
def index():
    return render_template('index.html', data=articles)

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist("file")

    for file in uploaded_files:
        # Extraer texto del PDF
        data = metadata.get_metadata_by_file(file)
        doi = string_utils.get_by_key(file, data, 'doi')
        keywords = string_utils.get_by_key(file, data, 'Keywords')

        if doi == "":
            content = string_utils.return_empty_result
        else:
            data = metadata.get_metadata_by_doi(doi)
            if data == []:
                print("no cuenta con metadatos en linea")
                content = string_utils.return_empty_result
            else:
                contenido = data['message']
                title = contenido['title'][0]
                autores = contenido.get('author', [{}])
                autores = [author.get('given', 'No cuenta con autores') for author in autores]
                year = contenido['published']['date-parts'][0][0]
                cantidad_referencias = contenido['references-count']
                type = contenido['type']
                revista = contenido['publisher']

                print(title)
                print(year)
                print(autores)
                print(keywords)
                print(type)
                print(revista)
                print(doi)
                print(cantidad_referencias)
                content = {
                    'title': title,
                    'year':year,
                    'author': ", ".join(autores),
                    'keywords': keywords,
                    'type': type,
                    'revista': revista,
                    'doi': doi,
                    'cantidad_referencias': cantidad_referencias
                }
        # author = string_utils.extract_content(text, '/Author')
        # abstract = string_utils.extract_abstract(text)

        # # Agregar el título, el año y el autor a la lista de datos extraídos con un identificador único
        articles.append(content)

    return redirect(url_for('index'))

@app.route('/export', methods=['POST'])
def export():
    global articles
    
    # Crear un DataFrame con los datos extraídos
    df = pd.DataFrame(articles)

    # Guardar el DataFrame en un buffer en memoria como un archivo Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Datos')
    output.seek(0)

    # Enviar el archivo Excel al usuario
    return send_file(output, download_name='datos.xlsx', as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# @app.route('/delete/<int:title_id>', methods=['POST'])
# def delete(title_id):
#     global extracted_data_list
#     extracted_data_list = [item for item in extracted_data_list if item['id'] != title_id]
#     return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)