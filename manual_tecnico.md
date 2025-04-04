# Manual Técnico para o Projeto "Editor de Imagens"
## Visão Geral
Este projeto é uma aplicação web simples de edição de imagens, construída com o Flask, uma framework Python. Ele permite aos usuários realizar upload de imagens, aplicar efeitos e editar as imagens de diversas maneiras, como ajustar brilho, contraste, saturação, nitidez, e aplicar efeitos de espelhamento ou conversão para tons de cinza. O resultado pode ser visualizado e salvo.

## Estrutura do Projeto
A estrutura do projeto é a seguinte:

```bash
editor_de_imagem/
├── static/
│   ├── images/        # Armazena as imagens enviadas e editadas
├── ├── uploads/       # Armazena as imagens do modo desenho
│   └── styles.css     # Arquivo CSS para estilização da interface
├── templates/
│   ├── index.html     # Página inicial de upload de imagem
│   └── edit_image.html # Página para edição da imagem
├── app.py             # Arquivo principal da aplicação Flask

```
## Descrição dos Arquivos
### 1. app.py
Este é o arquivo principal onde a aplicação Flask é configurada e onde a lógica para upload e edição de imagens é implementada.

Funcionalidades:
Configuração de Diretórios:

O diretório de upload é uploads/, onde as imagens enviadas são armazenadas temporariamente.

O diretório static/images/ armazena as imagens que serão servidas ao usuário.

Funções Principais:

allowed_file(filename): Verifica se o arquivo enviado possui uma extensão permitida (png, jpg, jpeg, gif).

Rota '/': Página inicial onde o usuário faz upload de imagens.

Rota '/edit/<filename>': Página de edição da imagem, onde o usuário pode aplicar efeitos.

Funcionalidade de Edição de Imagens:
Utiliza a biblioteca Pillow (PIL) para manipulação de imagens. As edições incluem:

Ajuste de brilho, contraste, saturação e nitidez.

Conversão para tons de cinza.

Espelhamento horizontal e vertical.

Execução:
Para executar a aplicação, basta rodar o seguinte comando no terminal:

```bash
python app.py
```
A aplicação estará disponível em http://127.0.0.1:5000/.

### 2. index.html
Esta é a página inicial onde o usuário pode fazer upload de uma imagem e utiliza a ferramenta de desenho.

Funcionalidades:
Formulário de Upload: Permite ao usuário selecionar e fazer upload de uma imagem.

Exibição da Imagem Enviada: Após o upload, a imagem é exibida e um link para a página de edição é fornecido.

Ferramenta de desenho:  Permite ao usuário selecionar e fazer upload de uma imagem. Após o upload, é possivel desenhar na imagem.

Estrutura:
O formulário de upload usa o método POST para enviar o arquivo.

A imagem enviada é exibida abaixo do formulário, com um botão para redirecionar para a página de edição.

### 3. edit_image.html
Esta página permite ao usuário aplicar efeitos à imagem enviada. Após a edição, a imagem editada é exibida.

Funcionalidades:
Controles de Efeitos: O usuário pode ajustar os parâmetros de brilho, contraste, saturação, nitidez e selecionar opções para conversão para tons de cinza e espelhamento.

Exibição de Imagem Editada: Após o envio do formulário de edição, a imagem editada é mostrada com as modificações.

Estrutura:
Formulários de controle para cada efeito (brilho, contraste, etc.).

Após a aplicação dos efeitos, a imagem editada é exibida na página.

### 4. styles.css
Arquivo CSS responsável pela estilização das páginas da aplicação.

Principais Estilos:
Fundo Escuro: A cor de fundo da página é definida para um tom escuro (#121212), para um visual mais moderno e sóbrio.

Imagens: As imagens exibidas têm bordas arredondadas e uma borda branca.

Botões: Botões de envio têm um fundo escuro com texto branco, e ao passar o mouse sobre eles, o fundo escurece para indicar interação.

## Fluxo da Aplicação
### 1. Página Inicial (index.html)
O usuário acessa a página inicial e faz o upload de uma imagem.

Se o upload for bem-sucedido, a imagem é exibida com um link para editar a imagem.

### 2. Edição da Imagem (edit_image.html)
O usuário é redirecionado para a página de edição, onde pode ajustar os parâmetros da imagem.

A imagem editada é exibida após a aplicação dos efeitos.

Como Funciona o Código
Flask e Upload de Imagens
Flask: Usamos o Flask para criar rotas que atendem os usuários com páginas HTML e manipulam os uploads de imagens.

Werkzeug: A biblioteca secure_filename é usada para garantir que os nomes dos arquivos enviados sejam seguros para uso no sistema de arquivos.

Pillow: A biblioteca Pillow é utilizada para realizar as edições nas imagens, aplicando efeitos como brilho, contraste e saturação.

Como Editar as Imagens
Quando a imagem é carregada na página de edição, os valores dos efeitos são obtidos do formulário. Em seguida, as alterações são aplicadas à imagem utilizando as classes de aprimoramento da biblioteca Pillow. Caso o usuário escolha opções como "Grayscale" ou "Flip", essas também são aplicadas à imagem.

Salvamento da Imagem Editada
Após a edição, a imagem modificada é salva no diretório static/images/ com um novo nome (prefixado com edited_).

Executando o Projeto
Requisitos
Python 3.x

Bibliotecas: Flask, Pillow

Instalação das Dependências
Crie um ambiente virtual (opcional, mas recomendado) e instale as dependências com o seguinte comando:

```bash
pip install Flask Pillow
```
Rodando a Aplicação
Execute o comando abaixo para rodar o servidor Flask:

```bash
python app.py
```
Agora, abra o navegador e acesse http://127.0.0.1:5000/ para usar o editor de imagens.

## Conclusão
Este é um editor simples de imagens com funcionalidade básica de edição. Ele pode ser expandido para incluir mais efeitos e funcionalidades, como upload de múltiplas imagens, mais opções de filtros e integração com banco de dados para salvar históricos de edições.







