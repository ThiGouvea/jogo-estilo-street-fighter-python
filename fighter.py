import pygame


class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 # 0:parado, 1:correr, 2:pular, 3:ataque1, 4:ataque2, 5:acert0, 6:morte
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.health = 100
        self.alive = True


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

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # aceita o pressionamento de teclas
        key = pygame.key.get_pressed()

        # só se pode fazer outras ações se não estiver atacando no momento
        if self.attacking == False and self.alive == True and round_over == False:
            # checa se é os controles do jogador 1
            if self.player == 1:
                # movimento
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
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

            # checa se é os controles do jogador 1
            if self.player == 2:
                # movimento
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                # pulo
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                # ataque
                if key[pygame.K_o] or key[pygame.K_p]:
                    self.attack(surface, target)
                    # determina qual tipo de ataque foi usado
                    if key[pygame.K_o]:
                        self.attack_type = 1
                    if key[pygame.K_p]:
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

        # aplica cooldown de ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # atualiza a posição do jogador na tela
        self.rect.x += dx
        self.rect.y += dy


    # lida com updates de animação
    def update(self):
        # checa qual ação o jogador esta fazendo
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6) # 6:morreu
        elif self.hit == True:
            self.update_action(5) # 5:acerto
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3) # 3:ataque1
            elif self.attack_type == 2:
                self.update_action(4) # 4:ataque2
        elif self.jump == True:
            self.update_action(2) # 2:pulando
        elif self.running == True:
            self.update_action(1) # 1:correndo
        else:
            self.update_action(0) # 0:parado

        animation_cooldown = 50
        # faz update da imagem
        self.image = self.animation_list[self.action][self.frame_index]
        # checa se tempo o suficiente passou desde o ultimo update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # checa pra ver se a animação terminou
        if self.frame_index >= len(self.animation_list[self.action]):
            # se o jogador esta morto então termina a animação
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # checa se um ataque foi executado
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                # checa se tomou dano
                if self.action == 5:
                    self.hit = False
                    # se o jogador estava no meio de um ataque, então o ataque para
                    self.attacking = False
                    self.attack_cooldown = 20


    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
            pygame.draw.rect(surface, (0, 255, 0), attacking_rect)


    def update_action(self, new_action):
        # checa se a nova ação é diferente da anterior
        if new_action != self.action:
            self.action = new_action
            # faz update das configurações da animação sendo usada
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
