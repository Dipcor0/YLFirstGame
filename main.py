import pygame
from math import ceil

SIZE_SCREEN = 500, 500
SIZE_PLAYER = 20, 20
SIZE_PLATFORM = 50, 10
SIZE_LADDER = 10, 50
COLOR_PLAYER = pygame.Color('Blue')
COLOR_SCREEN = pygame.Color('Black')
COLOR_PLATFORM = pygame.Color('Grey')
COLOR_LADDER = pygame.Color('Red')
SPEED_FALL = 3
STEP_PLAYER = 10


class Platform(pygame.sprite.Sprite):
    def __init__(self, *args, created_pos: tuple):
        super().__init__(*args)
        self.image = pygame.Surface(SIZE_PLATFORM)
        pygame.draw.rect(self.image, COLOR_PLATFORM, ((0, 0), SIZE_PLATFORM), width=0)
        self.rect = pygame.Rect(created_pos, SIZE_PLATFORM)
        self.rect.x = created_pos[0]
        self.rect.y = created_pos[1]


class Ladder(pygame.sprite.Sprite):
    def __init__(self, *args, created_pos: tuple):
        super().__init__(*args)
        self.image = pygame.Surface(SIZE_LADDER)
        pygame.draw.rect(self.image, COLOR_LADDER, ((0, 0), SIZE_LADDER), width=0)
        self.rect = pygame.Rect(created_pos, SIZE_LADDER)
        self.rect.x = created_pos[0]
        self.rect.y = created_pos[1]


class Player(pygame.sprite.Sprite):
    def __init__(self, *args, created_pos: tuple, platforms, ladders):
        super().__init__(*args)
        self.clock = pygame.time.Clock()
        self.group_platforms = platforms
        self.group_ladders = ladders
        self.up = False

        self.image = pygame.Surface(SIZE_PLAYER)
        pygame.draw.rect(self.image, COLOR_PLAYER, ((0, 0), SIZE_PLAYER), width=0)
        self.rect = pygame.Rect(created_pos, SIZE_PLAYER)
        self.rect.x = created_pos[0]
        self.rect.y = created_pos[1]

    def update(self, *args):
        if pygame.sprite.spritecollideany(self, self.group_ladders):
            self.up = True
        else:
            self.up = False
        if not pygame.sprite.spritecollideany(self, self.group_platforms) and not self.up:
            self.rect = self.rect.move(0, ceil(self.clock.tick() * SPEED_FALL / 1000))

        if args:
            event = args[0]
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.rect.x = event.pos[0]
                self.rect.y = event.pos[1]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.rect.x -= STEP_PLAYER
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.rect.x += STEP_PLAYER
                elif (event.key == pygame.K_w or event.key == pygame.K_UP) and self.up:
                    self.rect.y -= STEP_PLAYER
                elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and self.up:
                    self.rect.y += STEP_PLAYER


class Controller:
    def __enter__(self):
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode(SIZE_SCREEN)
        self.player = None
        self.ctrl_down = False

        self.group_platform = pygame.sprite.Group()
        self.group_ladder = pygame.sprite.Group()
        self.group_player = pygame.sprite.Group()
        return self

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if not self.player:
                            self.player = Player(self.group_player, created_pos=event.pos,
                                                 platforms=self.group_platform, ladders=self.group_ladder)
                        else:
                            self.group_player.update(event)
                    elif event.button == 3:
                        if self.ctrl_down:
                            Ladder(self.group_ladder, created_pos=event.pos)
                        else:
                            Platform(self.group_platform, created_pos=event.pos)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL:
                        self.ctrl_down = True
                    if self.player:
                        self.group_player.update(event)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LCTRL:
                        self.ctrl_down = False
            self.screen.fill(COLOR_SCREEN)

            self.group_player.update()
            self.group_player.draw(self.screen)
            self.group_ladder.draw(self.screen)
            self.group_platform.draw(self.screen)

            pygame.display.flip()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pygame.quit()


with Controller() as game:
    game.run()
