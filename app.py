import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from PIL import Image, ImageEnhance
import shutil

app = Flask(__name__)

# Obtém o caminho absoluto do diretório do script atual
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Caminhos corrigidos para usar o diretório correto
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/uploads')
STATIC_FOLDER = os.path.join(BASE_DIR, 'static/images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Criar as pastas dentro do repositório, se não existirem
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

# Configuração no Flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER



"""
    Verifica se o ficheiro possui uma extensão permitida para upload.
    
    @param filename Nome do ficheiro enviado pelo utilizador.
    @return True se a extensão for permitida, False caso contrário.
    """

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

"""
    Rota principal para carregamento e exibição de imagens.
    
    Se a requisição for do tipo POST e incluir um ficheiro válido,
    ele será armazenado no diretório apropriado e exibido na interface.
    
    @return Página renderizada com a imagem carregada pelo utilizador.
    """

@app.route('/', methods=['GET', 'POST'])
def index():
    
    uploaded_image = None  
    
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            static_image_path = os.path.join(STATIC_FOLDER, filename)
            shutil.copy(file_path, static_image_path)

            uploaded_image = filename

    return render_template('index.html', uploaded_image=uploaded_image)

"""
    Rota para edição de imagens aplicando diversos filtros e ajustes.
    
    Permite modificar brilho, contraste, saturação, nitidez,
    converter para escala de cinzento e realizar espelhamento horizontal e vertical.
    
    @param filename Nome do ficheiro a ser editado.
    @return Página renderizada com a imagem original e a versão editada.
    """

@app.route('/edit/<filename>', methods=['GET', 'POST'])
def edit_image(filename):
    
    file_path = os.path.join(STATIC_FOLDER, filename)
    edited_filename = f'edited_{filename}'
    edited_file_path = os.path.join(STATIC_FOLDER, edited_filename)

    if request.method == 'POST':
        image = Image.open(file_path)
        brightness = float(request.form.get('brightness', 1))
        contrast = float(request.form.get('contrast', 1))
        saturation = float(request.form.get('saturation', 1))
        sharpness = float(request.form.get('sharpness', 1))
        grayscale = request.form.get('grayscale')
        flip_horizontal = request.form.get('flip_horizontal')
        flip_vertical = request.form.get('flip_vertical')

        image = ImageEnhance.Brightness(image).enhance(brightness)
        image = ImageEnhance.Contrast(image).enhance(contrast)
        image = ImageEnhance.Color(image).enhance(saturation)
        image = ImageEnhance.Sharpness(image).enhance(sharpness)

        if grayscale:
            image = image.convert("L")
        if flip_horizontal:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
        if flip_vertical:
            image = image.transpose(Image.FLIP_TOP_BOTTOM)

        try:
            image.save(edited_file_path)
            print(f"✅ Imagem editada guardada em: {edited_file_path}") 
        except Exception as e:
            print(f"❌ Erro ao guardar imagem editada: {e}")

        return render_template('edit_image.html', original_image=filename, edited_image=edited_filename)

    return render_template('edit_image.html', original_image=filename, edited_image=None)



if __name__ == '__main__':
    app.run(debug=True)
