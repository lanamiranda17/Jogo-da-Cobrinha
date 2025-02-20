import pygame
import random
pygame.init()

largura_tela = 700
altura_tela = 500
tela = pygame.display.set_mode((largura_tela, altura_tela))

pygame.display.set_caption("Snake Game")

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERDE_ESCURO = (0, 150, 0)  # Cor mais escura para a sombra
VERMELHO = (255, 0, 0)
CINZA = (211, 211, 211)

cobra = [(200, 200), (220, 200), (240, 200)]  # Posição inicial da cobra

# Atualizações de posição
novo_x = 20
novo_y = 0

def nova_bolinha(obstaculos):

    comida_ocupada = False
    comida = (random.randrange(40, largura_tela, 20), random.randrange(40, altura_tela, 20)) # COmeça a paritr do 40,40 pra não sobressair o placar
        
    for obstaculo in obstaculos:
       for bloco in obstaculo:
            if comida == bloco:
                comida_ocupada = True
        
    if comida_ocupada:
        return nova_bolinha (obstaculos)
    else:
        return comida


def novo_obstaculo():
    
    x = random.randrange(0, largura_tela, 20)
    y = random.randrange(0, altura_tela, 20)

    forma = random.choice([0,1,2])

    if forma == 0:
        obstaculos = [(x,y), (x+20,y), (x+40, y)]
    elif forma == 1:
        obstaculos = [(x,y), (x, y+20), (x, y+40)]
    else: 
        obstaculos = [(x,y), (x+20, y), (x, y+20)]

    return obstaculos

obstaculos = [novo_obstaculo(), novo_obstaculo(), novo_obstaculo()]

bolinha = nova_bolinha(obstaculos)

placar = 0

clock = pygame.time.Clock()

def mostrar_game_over():
    fonte = pygame.font.SysFont(None, 40)
    texto = fonte.render("GAME OVER!", True, VERMELHO)
    tela.blit(texto, [largura_tela // 3, altura_tela // 2])
    pygame.display.update()

def mostrar_placar(placar):
    fonte = pygame.font.SysFont(None, 25)
    texto = fonte.render("Pontos: "+ str(placar), True, BRANCO)
    tela.blit(texto, [0, 0])

# Função para desenhar a cobra com afinamento
def desenhar_cobra(cobra):
    for i, bloco in enumerate(cobra):
        tamanho = 20 - i  # O tamanho vai diminuindo com o aumento do índice (afunilamento)
        if tamanho < 5:  # Largura e altura mínima para evitar que a cobra desapareça
            tamanho = 5

        # Desenha a borda escura mais espessa
        borda_espessura = 4  # Aumentando a espessura da borda
        pygame.draw.rect(tela, VERDE_ESCURO, pygame.Rect(bloco[0], bloco[1], tamanho, tamanho))
        pygame.draw.rect(tela, VERDE, pygame.Rect(bloco[0] + borda_espessura, bloco[1] + borda_espessura, tamanho - 2 * borda_espessura, tamanho - 2 * borda_espessura))

# Loop principal
rodando = True
primeiro_movimento = True  # Flag para garantir que o "Game Over" só apareça após o primeiro movimento
while rodando:
    # Verificar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Fechar o jogo
            rodando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and novo_x == 0:
                novo_x = -20
                novo_y = 0
            elif event.key == pygame.K_RIGHT and novo_x == 0:
                novo_x = +20
                novo_y = 0
            elif event.key == pygame.K_UP and novo_y == 0:
                novo_y = -20
                novo_x = 0
            elif event.key == pygame.K_DOWN and novo_y == 0:
                novo_y = +20
                novo_x = 0

    # Atualização do movimento
    nova_cabeca = (cobra[0][0] + novo_x, cobra[0][1] + novo_y)
    cobra.insert(0, nova_cabeca)

    cabeca_x, cabeca_y = cobra[0]

    if cabeca_x >= largura_tela:
        cabeca_x = 0
    elif cabeca_x < 0:
        cabeca_x = largura_tela - 20

    if cabeca_y >= altura_tela:
        cabeca_y = 0
    elif cabeca_y < 0:
        cabeca_y = altura_tela - 20

    cobra[0] = (cabeca_x, cabeca_y)
    
    # Verificar colisão com o corpo (após o primeiro movimento)
    if not primeiro_movimento and cobra[0] in cobra[1:]:
        mostrar_game_over()
        pygame.time.wait(2000)  # Esperar 2 segundos antes de sair
        rodando = False

    if cobra[0] == bolinha:
        bolinha = nova_bolinha(obstaculos)
        placar += 1
        obstaculos.append (novo_obstaculo())
    else:
        cobra.pop()

    

    for obstaculo in obstaculos:
        for bloco in obstaculo:
            if cobra[0] == bloco:
                mostrar_game_over()
                pygame.time.wait(2000)  # Esperar 2 segundos antes de sair
                rodando = False
    

    # Marcar que o primeiro movimento aconteceu
    primeiro_movimento = False

    # Preencher a tela com uma cor
    tela.fill(PRETO)

    # Desenhar a cobra
    desenhar_cobra(cobra)
    mostrar_placar(placar)

    # Desenhar a bolinha
    pygame.draw.rect(tela, VERMELHO, pygame.Rect(bolinha[0], bolinha[1], 20, 20))


    for obstaculo in obstaculos:  
        for bloco in obstaculo:  
            pygame.draw.rect(tela, CINZA, pygame.Rect(*bloco, 20, 20)) # BORDA MAIS ESCURA
    for obstaculo in obstaculos:  # Itera pelos grupos de obstáculos
        for bloco in obstaculo:  # Itera pelos blocos de cada obstáculo
            pygame.draw.rect(tela, BRANCO, pygame.Rect(bloco[0]+4, bloco[1]+4, 12, 12))


    # Atualizar a tela
    pygame.display.update()
    clock.tick(10)  # Número de quadros por segundo (FPS)

# Sair do pygame
pygame.quit()
