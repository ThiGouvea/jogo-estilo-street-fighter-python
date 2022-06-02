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

# define as variaveis do lutador
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# carregar uma imagem de fundo
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

# carrega as imagens para animação dos personagens
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# define o numero de passos em cada animação
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

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
fighter_1 = Fighter(200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS)
fighter_2 = Fighter(700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)

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

    # faz update da animação dos lutadores
    fighter_1.update()
    fighter_2.update()

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
