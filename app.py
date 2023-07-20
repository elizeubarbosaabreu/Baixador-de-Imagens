import os
import requests
import PySimpleGUI as sg
from bs4 import BeautifulSoup
from urllib.parse import urlparse

"""  _           _               _                  _      
| |__   __ _(_)_  ____ _  __| | ___  _ __    __| | ___ 
| '_ \ / _` | \ \/ / _` |/ _` |/ _ \| '__|  / _` |/ _ \
| |_) | (_| | |>  < (_| | (_| | (_) | |    | (_| |  __/
|_.__/ \__,_|_/_/\_\__,_|\__,_|\___/|_|     \__,_|\___|
                                                       
 _                                      
(_)_ __ ___   __ _  __ _  ___ _ __ ___  
| | '_ ` _ \ / _` |/ _` |/ _ \ '_ ` _ \ 
| | | | | | | (_| | (_| |  __/ | | | | |
|_|_| |_| |_|\__,_|\__, |\___|_| |_| |_|
                   |___/                
Criado por Elizeu Barbosa Abreu
"""
# Função para fazer o download das imagens
def fazer_download_imagens(url, diretorio_destino):
    # Faz o download do conteúdo HTML
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontra todas as tags <img> no HTML
    tags_img = soup.find_all('img')

    # Calcula o total de imagens para a barra de loading
    total_imagens = len(tags_img)
    progresso = 0

    # Percorre as tags <img> encontradas
    for img in tags_img:
        # Obtém a URL da imagem
        img_url = img['src']

        # Ignora URLs que não começam com 'http://' ou 'https://'
        if not img_url.startswith(('http://', 'https://')):
            continue

        # Faz o download da imagem
        response = requests.get(img_url)

        # Extrai o nome do arquivo da URL da imagem
        nome_arquivo = os.path.basename(urlparse(img_url).path)

        # Define o caminho completo para salvar a imagem
        caminho_arquivo = os.path.join(diretorio_destino, nome_arquivo)

        # Salva a imagem no diretório de destino
        with open(caminho_arquivo, 'wb') as arquivo:
            arquivo.write(response.content)

        progresso += 1
        # Atualiza a barra de loading com o progresso atual
        janela['-PROGRESS-'].update_bar(progresso, total_imagens)
        janela.read(timeout=0)

    print('Download concluído.')

# Layout da interface gráfica
sg.theme('reddit')
layout = [
    [sg.Text('Digite a URL do site com as imagens:')],
    [sg.Input(key='-URL-', size=(50, 1))],
    [sg.Text('Selecione o diretório de destino:')],
    [sg.Input(key='-DIR-', size=(40, 1)), sg.FolderBrowse(button_text='Diretório', auto_size_button=True)],
    [sg.Text('Status'), sg.ProgressBar(1, orientation='h', size=(25, 10), key='-PROGRESS-')],
    [sg.Button('Baixar imagens')],
]

# Cria a janela
janela = sg.Window('Download de Imagens', layout)

while True:
    evento, valores = janela.read()
    if evento == sg.WINDOW_CLOSED:
        break
    if evento == 'Baixar imagens':
        url = valores['-URL-']
        diretorio_destino = valores['-DIR-']

        if not url or not diretorio_destino:
            sg.popup('Por favor, preencha a URL do site e selecione o diretório de destino.')
            continue

        # Verifica se o diretório de destino existe e cria um novo se necessário
        if not os.path.exists(diretorio_destino):
            try:
                os.makedirs(diretorio_destino)
            except Exception as e:
                sg.popup(f'Erro ao criar o diretório de destino:\n{e}')
                continue

        try:
            fazer_download_imagens(url, diretorio_destino)
            sg.popup('Download concluído!')
            
        except Exception as e:
            sg.popup(f'Ocorreu um erro ao fazer o download das imagens:\n{e}')

        janela['-URL-'].update('')

janela.close()
