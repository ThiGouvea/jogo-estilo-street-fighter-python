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

# carregar uma imagem de fundo
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

# função para desenhar a imagem de fundo
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))


# cria duas instancias de lutadores
fighter_1 = Fighter(200, 310)
fighter_2 = Fighter(700, 310)

# loop do jogo
run = True
while run:

    clock.tick(FPS)

    # desenhar o fundo
    draw_bg()

    # movimenta lutadores
    fighter_1.move(SCREEN_WIDTH)

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
