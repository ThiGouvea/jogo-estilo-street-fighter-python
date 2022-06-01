import pygame


class Fighter():
    def __init__(self, x, y):
        self.flip = False
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.health = 100

    def move(self, screen_width, screen_height, surface, target):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0

        # aceita o pressionamento de teclas
        key = pygame.key.get_pressed()

        # só se pode fazer outras ações se não estiver atacando no momento
        if self.attacking ==False:
            # movimento
            if key[pygame.K_a]:
                dx = -SPEED
            if key[pygame.K_d]:
                dx = SPEED
            # pulo
            if key[pygame.K_w] and self.jump == False:
                self.vel_y = -30
                self.jump = True
            # ataque
            if key[pygame.K_r] or key[pygame.K_t]:
                self.attack(surface, target)
                # determina qual tipo de ataque foi usado
                if key[pygame.K_r]:
                    self.attack_type = 1
                if key[pygame.K_t]:
                    self.attack_type = 2

        # aplica a força da gravidade
        self.vel_y += GRAVITY
        dy += self.vel_y

        # faz com que os lutadores fiquem no limite da tela
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        # certifica que os jogadores estão de frente um pro outro
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # atualiza a posição do jogador na tela
        self.rect.x += dx
        self.rect.y += dy


    def attack(self, surface, target):
        self.attacking = True
        attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            target.health -= 10

        pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
