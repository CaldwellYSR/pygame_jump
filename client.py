#!env/bin/python

import pygame, sys, random

BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()

        # Set X and Y deltas to calculate how far to move during update
        self.dx = 0
        self.dy = 0

        # List of colliders
        self.level = None

    def update(self):
        self.calc_gravity()

        self.rect.x += self.dx
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            if self.rect.top < block.rect.bottom - 4 and self.rect.bottom > block.rect.top + 4:
                if self.dx > 0:
                    self.rect.right = block.rect.left
                elif self.dx < 0:
                    self.rect.left = block.rect.right

        self.rect.y += self.dy
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            above = abs(self.rect.bottom - block.rect.top) < 10
            if above:
                self.rect.bottom = block.rect.top 
                self.dy = 0
            else:
                self.rect.top = block.rect.bottom
                self.dy = 0

    def calc_gravity(self):
        if self.dy == 0:
            self.dy = 1
        else: 
            self.dy += 0.35

    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0: 
            self.dy = -10

    def go_left(self):
        self.dx = -6

    def go_right(self):
        self.dx = 6

    def stop(self):
        self.dx = 0

class Platform(pygame.sprite.Sprite):

    def __init__(self, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 1

class Level(object):
    
    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

        self.background = None

    def update(self):
        self.platform_list.update()
        for platform in self.platform_list.sprites():
            if platform.rect.bottom > SCREEN_HEIGHT:
                platform.kill()
                last = len(self.platform_list.sprites()) - 1
                block = Platform(210, 20)
                left = random.randint(0, 1)
                if left:
                    block.rect.x = self.platform_list.sprites()[last].rect.x - 210 - random.randint(-100, 400)
                else:
                    block.rect.x = self.platform_list.sprites()[last].rect.right - random.randint(-100, 400)
                block.rect.y = 0
                self.platform_list.add(block)

        self.enemy_list.update()

    def draw(self, screen):
        screen.fill(BLACK)
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

class Level_01(Level):
    
    def __init__(self, player):
        Level.__init__(self, player) 

        level = [
            [210, 20, 300, 600],
            [210, 20, 500, 500],
            [210, 20, 200, 400],
            [210, 20, 600, 300],
            [210, 20, 500, 300],
            [210, 20, 200, 200],
            [210, 20, 400, 100]
        ]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

def main():
    pygame.init()
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("PyGame Doodle Jump")
    player = Player()
    clock = pygame.time.Clock()
    done = False

    level_list = []
    level_list.append(Level_01(player))

    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    player.rect.x = 130
    player.rect.y = 100 - player.rect.height
    active_sprite_list.add(player)

    while not done:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                break

        # Key presses
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] or pressed[pygame.K_w]: player.jump()
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]: player.go_right()
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]: player.go_left()
        if not (pressed[pygame.K_RIGHT] or pressed[pygame.K_d])  and not (pressed[pygame.K_LEFT] or pressed[pygame.K_a]): player.stop()

        active_sprite_list.update()
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH
 
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left < 0:
            player.rect.left = 0

        # If you fall off the world
        if player.rect.top > SCREEN_HEIGHT:
            done = True

        # --- All drawing code below here ---
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # --- All drawing code above here ---

        clock.tick(60)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
