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
    file_path = os.path.join(STATIC_FOLDER, filename)  # Caminho da imagem original
    
    edited_filename = f'edited_{filename}'
    edited_file_path = os.path.join(STATIC_FOLDER, edited_filename)  # Caminho correto da imagem editada

    if request.method == 'POST':
        image = Image.open(file_path)

        # Obter valores do formulário
        brightness = float(request.form.get('brightness', 1))
        contrast = float(request.form.get('contrast', 1))
        saturation = float(request.form.get('saturation', 1))
        sharpness = float(request.form.get('sharpness', 1))
        grayscale = request.form.get('grayscale')  # Checkbox
        flip_horizontal = request.form.get('flip_horizontal')  # Checkbox
        flip_vertical = request.form.get('flip_vertical')  # Checkbox

        # Aplicar efeitos
        image = ImageEnhance.Brightness(image).enhance(brightness)
        image = ImageEnhance.Contrast(image).enhance(contrast)
        image = ImageEnhance.Color(image).enhance(saturation)
        image = ImageEnhance.Sharpness(image).enhance(sharpness)

        # Aplicar efeitos adicionais
        if grayscale:
            image = image.convert("L")  # Converte para preto e branco
        if flip_horizontal:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
        if flip_vertical:
            image = image.transpose(Image.FLIP_TOP_BOTTOM)

        # **Salvar imagem editada**
        try:
            image.save(edited_file_path)
            print(f"✅ Imagem editada salva em: {edited_file_path}")
        except Exception as e:
            print(f"❌ Erro ao salvar imagem editada: {e}")

        return render_template('edit_image.html', original_image=filename, edited_image=edited_filename)

    return render_template('edit_image.html', original_image=filename, edited_image=None)
if __name__ == '__main__':
    app.run(debug=True)
