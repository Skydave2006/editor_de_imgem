import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image, ImageEnhance

app = Flask(__name__)

# Definir pasta para uploads e extensões permitidas
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['STATIC_FOLDER'] = 'static/'  # Pasta de arquivos estáticos
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Verificar se a pasta de uploads existe, caso contrário, criá-la
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Verificar se a pasta de arquivos estáticos existe
if not os.path.exists(app.config['STATIC_FOLDER']):
    os.makedirs(app.config['STATIC_FOLDER'])

# Função para verificar se o arquivo tem uma extensão permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Página inicial e upload de imagem
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verificar se o arquivo foi enviado
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return redirect(url_for('edit_image', filename=filename))
    return render_template('index.html')

# Página de edição de imagem
@app.route('/edit/<filename>', methods=['GET', 'POST'])
def edit_image(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image = Image.open(file_path)

    if request.method == 'POST':
        # Editar imagem com base nas opções do formulário
        if 'brightness' in request.form:
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(float(request.form['brightness']))
        
        if 'contrast' in request.form:
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(float(request.form['contrast']))
        
        # Salvar a imagem editada na pasta static/
        edited_filename = 'edited_' + filename
        edited_file_path = os.path.join(app.config['STATIC_FOLDER'], edited_filename)

        try:
            image.save(edited_file_path)
            print(f"Imagem editada salva com sucesso em: {edited_file_path}")
        except Exception as e:
            print(f"Erro ao salvar a imagem editada: {e}")

        # Passar o caminho da imagem editada para o template
        return render_template('edit_image.html', image_url=edited_filename)

    return render_template('edit_image.html', image_url=filename)

if __name__ == '__main__':
    app.run(debug=True)
