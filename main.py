import pygame
from sprites import *
from config import *
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = True  # Add this line to initialize the 'playing' attribute
          # Add the following line to initialize the 'all_sprites' attribute
        #self.player = Player(self, 30, 40)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates() 
        self.character_spritesheet = Spritesheet('img/spritesheet.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')
        self.enemy_spritesheet = Spritesheet('img/enemy.png')
        self.font = pygame.font.Font('NanumGothic-Bold.ttf', 32)
        self.intro_background = pygame.image.load('./img/bg.webp')
        self.go_background = pygame.image.load('./img/gameover.png')

    def createTilemap(self):
     for i, row in enumerate(tilemap):
        for j, column in enumerate(row):
            Ground(self, j,i)
            if column == 'B':
                Block(self, j, i)
            if column == 'E':
                Enemy(self, j, i)
            if column == 'P':
                Player(self, j,i)
        
        
    def new(self):
        # a new game starts
        self.createTilemap()
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.createTilemap()

        #self.player = Player(self,1,2)
    def events(self):
        #game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False


    def update(self):
        # game loop updates
        self.all_sprites.update()
    def draw(self):
        #game loop draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()
    def main(self):
        # game loop
        self.new()  # Call new to initialize game-specific attributes
        while self.playing:
            self.events()
            self.update()
            self.draw()
        #self.running = False

    def game_over(self):
        text = self.font.render('Game over', True, BLACK)
        text_rect = text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))
        restart_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, 'Restart', 32)  # Pass 'self' as the first argument
        for sprite in self.all_sprites:
            sprite.kill()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False  # Fix the variable name here
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()
            self.screen.blit(self.go_background, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)  # Use restart_button.image and restart_button.rect
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True
        title = self.font.render('Awesome_game', True, BLACK)
        title_rect = title.get_rect(x=10, y=10)
        play_button = Button(10, 50, 100, 50, WHITE, BLACK, 'Play', fontsize=32)
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Fix the typo here
                    intro = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
g = Game()
g.intro_screen()
while g.running:
    g.main()
    g.game_over()
pygame.quit()
sys.exit()
