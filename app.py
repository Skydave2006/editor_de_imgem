import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image, ImageEnhance
import shutil  # Para copiar arquivos

app = Flask(__name__)

# Configuração de diretórios
UPLOAD_FOLDER = 'uploads/'
STATIC_FOLDER = 'static/images/'  # Local onde as imagens serão servidas pelo Flask
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Criar pastas caso não existam
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER

# Função para verificar se a extensão do arquivo é permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Página inicial e upload de imagem
@app.route('/', methods=['GET', 'POST'])
def index():
    uploaded_image = None  # Variável para armazenar o nome da imagem enviada
    
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            # Copiar a imagem para static/images/
            static_image_path = os.path.join(STATIC_FOLDER, filename)
            shutil.copy(file_path, static_image_path)

            uploaded_image = filename  # Guardar o nome da imagem para exibição

    return render_template('index.html', uploaded_image=uploaded_image)

# Página de edição de imagem
@app.route('/edit/<filename>', methods=['GET', 'POST'])
def edit_image(filename):
    file_path = os.path.join(STATIC_FOLDER, filename)  # A imagem original já está na pasta static/images/
    
    edited_filename = f'edited_{filename}'
    edited_file_path = os.path.join(STATIC_FOLDER, edited_filename)

    if request.method == 'POST':
        image = Image.open(file_path)

        # Aplicar efeitos conforme a escolha do usuário
        brightness = float(request.form.get('brightness', 1))
        contrast = float(request.form.get('contrast', 1))

        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(brightness)

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(contrast)

        # Salvar imagem editada na pasta static/images/
        try:
            image.save(edited_file_path)
            print(f"Imagem editada salva em: {edited_file_path}")
        except Exception as e:
            print(f"Erro ao salvar imagem editada: {e}")

        return render_template('edit_image.html', original_image=filename, edited_image=edited_filename)

    return render_template('edit_image.html', original_image=filename, edited_image=None)

if __name__ == '__main__':
    app.run(debug=True)
