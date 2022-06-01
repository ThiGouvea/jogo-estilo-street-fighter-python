import pygame


class Fighter():
    def __init__(self, x, y, data, sprite_sheet, animation_steps):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = False
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0:parado, 1:correr, 2:pular, 3:ataque1, 4:ataque2, 5:acert0, 6:morte
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.health = 100

    def load_images(self, sprite_sheet, animation_steps):
        # extrai as imagens da lista de animação
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

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
        surface.blit(self.image, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
