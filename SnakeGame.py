import pygame
import random

# Inicializa o Pygame
pygame.init()

# Dimensões da tela
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20  # Tamanho de cada "célula" do jogo

# Define as cores em RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Cria a janela do jogo
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Controla a taxa de atualização do jogo
clock = pygame.time.Clock()

# Função para desenhar a cobra e a comida
def draw_snake(snake_body):
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

def draw_food(x, y):
    pygame.draw.rect(screen, RED, (x, y, CELL_SIZE, CELL_SIZE))

def main():
    # Posição inicial da cobra (centro da tela)
    snake_x = WIDTH // 2
    snake_y = HEIGHT // 2
    
    # Velocidade inicial (cobra parada)
    snake_dx = 0
    snake_dy = 0
    
    # Corpo da cobra (lista de coordenadas)
    snake_body = [(snake_x, snake_y)]
    snake_length = 1
    
    # Gera posição inicial da comida em coordenadas múltiplas de CELL_SIZE
    food_x = random.randrange(0, WIDTH, CELL_SIZE)
    food_y = random.randrange(0, HEIGHT, CELL_SIZE)
    
    # Loop principal do jogo
    running = True
    while running:
        clock.tick(10)  # A cobra se move ~10 vezes por segundo
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Controle da cobra pelas setas do teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_dy == 0:
                    snake_dx = 0
                    snake_dy = -CELL_SIZE
                elif event.key == pygame.K_DOWN and snake_dy == 0:
                    snake_dx = 0
                    snake_dy = CELL_SIZE
                elif event.key == pygame.K_LEFT and snake_dx == 0:
                    snake_dx = -CELL_SIZE
                    snake_dy = 0
                elif event.key == pygame.K_RIGHT and snake_dx == 0:
                    snake_dx = CELL_SIZE
                    snake_dy = 0
        
        # Atualiza a posição da cobra
        snake_x += snake_dx
        snake_y += snake_dy
        
        # Verifica se a cobra bateu nas paredes (Game Over)
        if snake_x < 0 or snake_x >= WIDTH or snake_y < 0 or snake_y >= HEIGHT:
            running = False
        
        # Adiciona a nova posição da cabeça da cobra
        snake_body.insert(0, (snake_x, snake_y))
        
        # Verifica se a cobra comeu a comida
        if snake_x == food_x and snake_y == food_y:
            # Gera nova comida
            food_x = random.randrange(0, WIDTH, CELL_SIZE)
            food_y = random.randrange(0, HEIGHT, CELL_SIZE)
            snake_length += 1
        else:
            # Remove o último segmento se não comer
            snake_body.pop()
        
        # Verifica colisão com o próprio corpo (Game Over)
        if len(snake_body) != len(set(snake_body)):
            # Se houver posições duplicadas no corpo, houve colisão
            running = False
        
        # Desenha o fundo
        screen.fill(BLACK)
        
        # Desenha a comida
        draw_food(food_x, food_y)
        
        # Desenha a cobra
        draw_snake(snake_body)
        
        # Atualiza a tela
        pygame.display.update()
    
    # Finaliza o jogo
    pygame.quit()

# Executa o jogo
if __name__ == "__main__":
    main()
