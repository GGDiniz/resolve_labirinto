import numpy as np
import cv2
import random

def gerar_labirinto(largura=31, altura=31, nome_arquivo="labirinto.png"):
    # Forçar dimensões ímpares
    if largura % 2 == 0:
        largura += 1
    if altura % 2 == 0:
        altura += 1

    # Definir cores
    cor_parede = (0, 0, 0)
    cor_caminho = (255, 255, 255)
    cor_inicio = (0, 255, 0)
    cor_fim = (0, 0, 255)

    # Criar matriz cheia de paredes
    labirinto = np.zeros((altura, largura, 3), dtype=np.uint8)
    labirinto[:, :] = cor_parede

    # Função para pegar vizinhos
    def vizinhos(y, x):
        direcoes = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        random.shuffle(direcoes)
        for dy, dx in direcoes:
            ny, nx = y + dy, x + dx
            if 0 <= ny < altura and 0 <= nx < largura:
                yield ny, nx, dy, dx

    # Começar no canto superior esquerdo
    stack = [(0, 0)]
    labirinto[0, 0] = cor_caminho

    while stack:
        y, x = stack[-1]
        encontrado = False
        for ny, nx, dy, dx in vizinhos(y, x):
            if (labirinto[ny, nx] == cor_parede).all():
                labirinto[ny, nx] = cor_caminho
                labirinto[y + dy // 2, x + dx // 2] = cor_caminho
                stack.append((ny, nx))
                encontrado = True
                break
        if not encontrado:
            stack.pop()

    # Definir início
    labirinto[0, 0] = cor_inicio

    # Definir fim no caminho mais próximo do canto inferior direito
    for y in reversed(range(altura)):
        for x in reversed(range(largura)):
            if (labirinto[y, x] == cor_caminho).all():
                labirinto[y, x] = cor_fim
                break
        else:
            continue
        break

    # Ampliar imagem
    escala = 30
    labirinto_ampliado = cv2.resize(
        labirinto, (largura * escala, altura * escala), interpolation=cv2.INTER_NEAREST
    )

    # Salvar
    cv2.imwrite(nome_arquivo, labirinto_ampliado)
    print(f"💾 Labirinto salvo como {nome_arquivo}")


# Gerar labirinto
if __name__ == "__main__":
    gerar_labirinto(largura=31, altura=31, nome_arquivo="labirinto.png")
