import pygame
from fighter import Fighter

pygame.init()

# cria a tela do jogo
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

# define a atualização da tela do jogo (FPS)
clock = pygame.time.Clock()
FPS = 60

# define as cores
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# carregar uma imagem de fundo
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

# função para desenhar a imagem de fundo
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

    # função que desenha o HP dos lutadores na tela
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


# cria duas instancias de lutadores
fighter_1 = Fighter(200, 310)
fighter_2 = Fighter(700, 310)

# loop do jogo
run = True
while run:

    clock.tick(FPS)

    # desenhar o fundo
    draw_bg()

    # mostra os status do lutador
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)

    # movimenta lutadores
    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)

    # desenha os lutadores na tela
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # lidar com os eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # faz update da tela
    pygame.display.update()
# sair do jogo
pygame.quit()
