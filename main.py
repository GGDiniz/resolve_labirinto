import cv2
import numpy as np
from collections import deque
import matplotlib.pyplot as plt
import imageio


def resolver_labirinto(nome_arquivo):
    # 📂 Carregar imagem e redimensionar
    imagem = cv2.imread(nome_arquivo)

    if imagem is None:
        print("❌ Imagem não encontrada. Verifique o nome do arquivo e tente novamente.")
        return

    # Reduzir para 300x300 (ajuste se quiser outro tamanho)
    tamanho_alvo = (300, 300)
    imagem = cv2.resize(imagem, tamanho_alvo, interpolation=cv2.INTER_AREA)

    # 🧠 Definir cores (em BGR)
    cor_parede = (0, 0, 0)
    cor_caminho = (255, 255, 255)
    cor_inicio = (0, 255, 0)
    cor_fim = (0, 0, 255)

    # 🔍 Encontrar início e fim
    inicio = None
    fim = None

    for y in range(imagem.shape[0]):
        for x in range(imagem.shape[1]):
            pixel = tuple(imagem[y, x])
            if pixel == cor_inicio:
                inicio = (y, x)
            elif pixel == cor_fim:
                fim = (y, x)

    if inicio is None or fim is None:
        print("❌ Início ou fim não encontrados na imagem.")
        return

    print(f"✅ Início encontrado em {inicio}")
    print(f"✅ Fim encontrado em {fim}")

    # 🗺️ Criar mapa binário (1 = caminho, 0 = parede)
    mapa = np.zeros((imagem.shape[0], imagem.shape[1]), dtype=np.uint8)

    for y in range(imagem.shape[0]):
        for x in range(imagem.shape[1]):
            pixel = tuple(imagem[y, x])
            if pixel == cor_parede:
                mapa[y, x] = 0
            else:
                mapa[y, x] = 1

    # 🔍 BFS
    def bfs(mapa, inicio, fim):
        filas = deque([inicio])
        visitado = set()
        came_from = {}
        visitado.add(inicio)

        while filas:
            atual = filas.popleft()

            if atual == fim:
                break

            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = atual[0] + dy, atual[1] + dx

                if 0 <= ny < mapa.shape[0] and 0 <= nx < mapa.shape[1]:
                    if mapa[ny, nx] == 1 and (ny, nx) not in visitado:
                        filas.append((ny, nx))
                        visitado.add((ny, nx))
                        came_from[(ny, nx)] = atual

        caminho = []
        atual = fim
        while atual != inicio:
            caminho.append(atual)
            atual = came_from.get(atual)
            if atual is None:
                print("❌ Caminho não encontrado.")
                return []

        caminho.append(inicio)
        caminho.reverse()
        return caminho

    caminho = bfs(mapa, inicio, fim)

    if not caminho:
        print("⚠️ Não foi possível encontrar um caminho.")
        return

    print(f"🚩 Caminho encontrado com {len(caminho)} passos.")

    # 🎨 Criar frames para GIF desenhando linha roxa contínua no caminho
    frames = []
    imagem_caminho = imagem.copy()

    # Para controlar a linha progressiva até o passo i
    for i in range(len(caminho)):
        # Copia a imagem base para desenhar o caminho até o passo i
        img_temp = imagem_caminho.copy()

        # Desenha linhas entre pontos consecutivos até o passo i
        for j in range(i):
            y1, x1 = caminho[j]
            y2, x2 = caminho[j + 1]
            pt1 = (x1, y1)  # Note que OpenCV usa (x, y)
            pt2 = (x2, y2)

            # Desenha linha roxa com espessura 2
            cv2.line(img_temp, pt1, pt2, (255, 0, 255), thickness=2)

        # A cada 10 passos, salva um frame
        if i % 10 == 0 or i == len(caminho) - 1:
            frame_rgb = cv2.cvtColor(img_temp, cv2.COLOR_BGR2RGB)
            frames.append(frame_rgb.copy())

    # Mostrar último frame
    plt.imshow(frames[-1])
    plt.title('Caminho encontrado')
    plt.axis('off')
    plt.show()

    # Salvar GIF
    resultado_nome_gif = 'resultado_' + nome_arquivo.rsplit('.', 1)[0] + '.gif'
    imageio.mimsave(resultado_nome_gif, frames, duration=0.05)
    print(f"💾 Resultado salvo como {resultado_nome_gif}")


if __name__ == "__main__":
    nome_arquivo = input("🖼️ Digite o nome da imagem do labirinto (incluindo .png ou .jpg): ")
    resolver_labirinto(nome_arquivo)
