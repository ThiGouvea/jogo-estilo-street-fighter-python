import pygame


class Fighter():
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0

    def move(self, screen_width):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0

        # aceita o pressionamento de teclas
        key = pygame.key.get_pressed()

        # movimento
        if key[pygame.K_a]:
            dx = -SPEED
        if key[pygame.K_d]:
            dx = SPEED
        # pulo
        if key[pygame.K_w]:
            self.vel_y = -30

        # aplica a força da gravidade
        self.vel_y += GRAVITY
        dy += self.vel_y

        # faz com que os lutadores fiquem no limite da tela
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom

        # atualiza a posição do jogador na tela
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
