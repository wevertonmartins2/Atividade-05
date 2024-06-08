import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from queue import Queue
import random

def criar_labirinto(tamanho, num_obstaculos, seed=None):
    """
    Cria um labirinto com o tamanho fornecido e número de obstáculos. Usa seed para reprodutibilidade.
    """
    if seed:
        random.seed(seed)
        
    labirinto = np.zeros(tamanho, dtype=int)
    caminho = [(random.choice(range(1, tamanho[0]-1)), y) for y in range(1, tamanho[1] - 1)]
    
    for x, y in caminho:
        labirinto[x, y] = 0
    
    for _ in range(num_obstaculos):
        x, y = random.randint(0, tamanho[0] - 1), random.randint(0, tamanho[1] - 1)
        if (x, y) not in caminho:
            labirinto[x, y] = 1
    
    return labirinto

def busca_em_largura(labirinto, inicio, fim):
    """
    Realiza uma busca em largura para encontrar o caminho de início a fim no labirinto.
    """
    fila = Queue()
    fila.put(inicio)
    caminhos = {inicio: []}

    while not fila.empty():
        ponto = fila.get()
        if ponto == fim:
            return caminhos[ponto] + [fim]
        for vizinho in [(0,1), (1,0), (0,-1), (-1,0)]:
            x, y = ponto[0] + vizinho[0], ponto[1] + vizinho[1]
            if 0 <= x < len(labirinto) and 0 <= y < len(labirinto[0]) and labirinto[x][y] == 0 and (x, y) not in caminhos:
                fila.put((x, y))
                caminhos[(x, y)] = caminhos[ponto] + [ponto]

    return None

def imprimir_labirinto(labirinto, caminho):
    """
    Imprime um labirinto com o caminho encontrado.
    """
    cor_labirinto = (255, 255, 255)  # branco
    cor_caminho = (0, 200, 0)  # verde
    cor_obstaculo = (0, 0, 0)  # preto
    cor_texto = (255, 255, 255)  # branco

    tamanho_imagem = (labirinto.shape[1] * 30, labirinto.shape[0] * 30)
    img = Image.new("RGB", tamanho_imagem, color=cor_labirinto)
    draw = ImageDraw.Draw(img)

    for i in range(labirinto.shape[0]):
        for j in range(labirinto.shape[1]):
            x1, y1 = j * 30, i * 30
            x2, y2 = x1 + 30, y1 + 30
            if labirinto[i][j] == 1:
                draw.rectangle([x1, y1, x2, y2], fill=cor_obstaculo)
            elif (i, j) in caminho:
                draw.rectangle([x1, y1, x2, y2], fill=cor_caminho)
                try:
                    font = ImageFont.truetype("arial.ttf", 12)
                except IOError:
                    font = ImageFont.load_default()
                draw.text((x1 + 5, y1 + 5), str(caminho.index((i, j)) + 1), fill=cor_texto, font=font)

    st.image(img, caption='Labirinto com Caminho', use_column_width=True)

def app():
    st.title("Busca em Largura em Labirintos")
    st.markdown("### Seleção de Parâmetros do Labirinto")

    tamanhos_labirinto = {
        "7x7": (7, 7, 8),
        "9x11": (9, 11, 15),
        "7x15": (7, 15, 10)
    }
    tamanho_selecionado = st.selectbox("Selecione um tamanho de labirinto:", list(tamanhos_labirinto.keys()))
    seed = st.number_input("Insira uma semente para gerar o labirinto (opcional):", value=0, step=1)

    if seed != 0:
        seed = int(seed)
    else:
        seed = None

    labirinto_tamanho, labirinto_largura, num_obstaculos = tamanhos_labirinto[tamanho_selecionado]
    
    labirinto = criar_labirinto((labirinto_tamanho, labirinto_largura), num_obstaculos, seed)
    inicio = (0, 0)
    fim = (labirinto_tamanho - 1, labirinto_largura - 1)

    st.subheader("Labirinto Original")
    imprimir_labirinto(labirinto, [])

    st.markdown("### Resultado da Busca")
    caminho = busca_em_largura(labirinto, inicio, fim)

    if caminho is None:
        st.error("Não há caminho para o fim!")
    else:
        st.success("Caminho encontrado!")
        imprimir_labirinto(labirinto, caminho)

    if st.button("Gerar Novo Caminho"):
        caminho = busca_em_largura(labirinto, inicio, fim)
        if caminho is None:
            st.error("Não há caminho para o fim!")
        else:
            st.success("Novo caminho gerado!")
            imprimir_labirinto(labirinto, caminho)

if __name__ == "__main__":
    app()
