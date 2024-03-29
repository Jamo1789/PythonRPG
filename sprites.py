import pygame
from config import *

import math
import random

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])  # Corrected the method name to 'Surface'
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

    
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1
       

        self.image = self.game.character_spritesheet.get_sprite(3,2,self.width,self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.down_animations = [self.game.character_spritesheet.get_sprite(3, 1, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(32, 1, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(65, 1, self.width, self.height)]

        self.up_animations = [self.game.character_spritesheet.get_sprite(225, 1, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(257, 1, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(289, 1, self.width, self.height)]

        self.left_animations = [self.game.character_spritesheet.get_sprite(96, 1, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(128, 1, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(127, 1, self.width, self.height)
                           ]

        self.right_animations = [self.game.character_spritesheet.get_sprite(161, 1, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(192, 1, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(192, 1, self.width, self.height)]
    def animate(self):
        
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3,2,self.width,self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(32, 5,self.width,self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(96, 1,self.width,self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(161, 1,self.width,self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self,self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False         
            

    def update(self):  # Added 'self' parameter to the update method
        self.movement()
        self.animate()
        self.collide_enemy()
        

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.x_change = 0
        self.y_change = 0
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
           for sprite in self.game.all_sprites:
               sprite.rect.x += PLAYER_SPEED
               
           self.x_change -= PLAYER_SPEED
           self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
               sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
               sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
               sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:        
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED         
            
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:        
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height   
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED
   
         


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7,30)

        self.image = self.game.enemy_spritesheet.get_sprite(3,2,self.width,self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()  # Use get_rect() to create the rectangle
        self.rect.x = self.x
        self.rect.y = self.y
        self.left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height)]

        self.right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)]
    def update(self):
        self.movement()
        #self.move_towards_player()
        self.animate()
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.x_change = 0
        self.y_change = 0
        
    def movement(self):
     if self.facing == 'left':
         self.x_change -= ENEMY_SPEED
         self.movement_loop -= 1
         if self.movement_loop <= -self.max_travel:
             self.facing = 'right'
             self.movement_loop = 0
     elif self.facing == 'right':
         self.x_change += ENEMY_SPEED
         self.movement_loop += 1
         if self.movement_loop >= self.max_travel:
             self.facing = 'left'
             self.movement_loop = 0
#   def move_towards_player(self, player):
#        player = self.game.player
        # Find direction vector (dx, dy) between enemy and player.
#        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
#        dist = math.hypot(dx, dy)
#        dx, dy = dx / dist, dy / dist  # Normalize.
        # Move along this normalized vector towards the player at current speed.
#        self.rect.x += dx * ENEMY_SPEED
#        self.rect.y += dy * ENEMY_SPEED

    def animate(self):
        
        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3,98,self.width,self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3,66,self.width,self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(960,448,self.width,self.height)
        
        self.rect = self.image.get_rect()  # Use get_rect() to create the rectangle
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64,352,self.width,self.height)
        self.rect = self.image.get_rect()  # Use get_rect() to create the rectangle
        self.rect.x = self.x
        self.rect.y = self.y
class Button():
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('NanumGothic-Bold.ttf', fontsize)
        self.content = content
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fg = fg
        self.bg = bg
        self.content = content
        self.fontsize = fontsize
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        return self.rect.collidepoint(pos) and pressed[0]






        

