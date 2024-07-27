import os
import requests
import re
from bs4 import BeautifulSoup 
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from threading import Thread
import webbrowser
from concurrent.futures import ThreadPoolExecutor

# Função para abrir o diretório de salvamento
def open_directory(event):
    webbrowser.open(f'file://{os.path.abspath(save_folder)}')

# Função para baixar uma única imagem
def download_image(img_url, save_folder, log_text, subfolder_name):
    def clean_filename(filename):
        return re.sub(r'[\\/:*?"<>|]', "_", filename)

    img_name = img_url.split("/")[-1]
    img_name = clean_filename(img_name)  # Limpa o nome do arquivo
    img_path = os.path.join(save_folder, img_name)

    try:
        # Faz o download da imagem
        img_data = requests.get(img_url).content
        with open(img_path, "wb") as img_file:
            img_file.write(img_data)
        log_text.config(state=tk.NORMAL)
        log_text.insert(tk.END, f"Imagem {img_name} salva em {subfolder_name}.\n")
        log_text.config(state=tk.DISABLED)
    except requests.RequestException as e:
        log_text.config(state=tk.NORMAL)
        log_text.insert(tk.END, f"Erro ao baixar {img_name}: {e}\n")
        log_text.config(state=tk.DISABLED)

# Função para baixar imagens em segundo plano
def download_images():
    global save_folder
    url = url_entry.get()

    if not url:
        messagebox.showerror("Erro", "Por favor, insira a URL do jogo.")
        return

    # Extraindo APPID da URL
    appid_match = re.search(r'/app/(\d+)/', url)
    if not appid_match:
        messagebox.showerror("Erro", "APPID não encontrado na URL.")
        return
    appid = appid_match.group(1)

    # URLs das quatro imagens adicionais
    additional_images = [
        f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/library_hero.jpg",
        f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/library_600x900.jpg",
        f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/header.jpg",
        f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/capsule_616x353.jpg"
    ]

    # Faz o download da página
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se há erros na resposta
    except requests.RequestException as e:
        messagebox.showerror("Erro", f"Erro ao acessar a URL: {e}")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")

    # Encontra o nome do jogo
    game_name_element = soup.find("div", class_="apphub_AppName")
    if game_name_element:
        game_name = game_name_element.get_text()
    else:
        messagebox.showerror("Erro", "Nome do jogo não encontrado na página.")
        return

    # Remove caracteres inválidos do nome do jogo
    subfolder_name = re.sub(r'[\\/:*?"<>|]', "_", game_name)

    save_folder = os.path.join("screenshots", subfolder_name)
    try:
        os.makedirs(save_folder, exist_ok=True)
    except OSError as e:
        messagebox.showerror("Erro", f"Erro ao criar diretório de salvamento: {e}")
        return

    log_text.config(state=tk.NORMAL)  # Habilita a edição do widget de texto
    log_text.delete("1.0", tk.END)  # Limpa o conteúdo do widget de texto
    log_text.insert(tk.END, f"Iniciando download das imagens para '{subfolder_name}'...\n")
    log_text.insert(tk.END, "Imagens serão salvas em: ")
    log_text.insert(tk.END, os.path.abspath(save_folder) + "\n", "link")
    log_text.config(state=tk.DISABLED)  # Desabilita a edição do widget de texto

    # Procura por URLs de imagens que contêm "1920x1080"
    image_urls = re.findall(r'https://.*?1920x1080.*?\.jpg', response.text)

    if not image_urls:
        messagebox.showerror("Erro", "Nenhuma imagem encontrada na página.")
        return

    # Inclui as URLs das imagens adicionais na lista de download
    image_urls.extend(additional_images)

    def download_thread():
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(download_image, img_url, save_folder, log_text, subfolder_name) for img_url in image_urls]
            for future in futures:
                future.result()
        
        log_text.config(state=tk.NORMAL)
        log_text.insert(tk.END, "Download das imagens concluído.\n")
        log_text.config(state=tk.DISABLED)
        messagebox.showinfo("Sucesso", "Download das imagens concluído.")

    thread = Thread(target=download_thread)
    thread.start()

# Criação da janela
window = tk.Tk()
window.title("Downloader de Imagens")
window.geometry("900x450")  # Define a resolução inicial

# Entrada da URL
url_label = tk.Label(window, text="URL do Jogo:")
url_label.pack()
url_entry = tk.Entry(window, width=100)
url_entry.pack()

# Botão para iniciar o download
download_button = tk.Button(window, text="Baixar Imagens", command=download_images)
download_button.pack()

# Log de download das imagens
log_label = tk.Label(window, text="Log de Download:")
log_label.pack()
log_text = scrolledtext.ScrolledText(window, state=tk.DISABLED, wrap=tk.WORD, height=20, width=100)
log_text.pack()

# Configuração do estilo de link
log_text.tag_config("link", foreground="blue", underline=True)
log_text.tag_bind("link", "<Button-1>", open_directory)

# Executa a interface
window.mainloop()
