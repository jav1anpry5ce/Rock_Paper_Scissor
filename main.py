import pygame
import random

class Object(pygame.sprite.Sprite):
    def __init__(self, object, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.object = object
        self.x = x 
        self.y = y 
        self.speed = 2
        self.image = self.load_image()
        self.direction = [self.speed, -self.speed]
        self.xmove = random.choice(self.direction)
        self.ymove = random.choice(self.direction)
        self.rect = pygame.Rect(round(self.x), round(self.y), 64, 64)

    def load_image(self):
        if self.object == 'ROCK':
            return pygame.image.load('rock.png')
        elif self.object == 'PAPER':
            return pygame.image.load('paper.png')
        elif self.object == 'SCISSOR':
            return pygame.image.load('scissor.png')

    def movement(self):
        self.x += self.xmove
        self.y += self.ymove
        self.rect = pygame.Rect(round(self.x), round(self.y), 64, 64)
        if self.x <= 0:
            self.xmove = self.speed
        elif self.x >= 736:
            self.xmove = -self.speed
        if self.y <= 0:
            self.ymove = self.speed
        elif self.y >= 536:
            self.ymove = -self.speed
    
    def object_change(self, new_object):
        self.object = new_object
        self.image = self.load_image()

    def collide(self, spriteGroup):
        if pygame.sprite.spritecollide(self, spriteGroup, False):
            self.xmove = abs(self.xmove)
            self.ymove = abs(self.ymove)

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = pygame.image.load('background.jpg')
        self.FPS = 120
        self.clock = pygame.time.Clock()
        self.rockgroup = pygame.sprite.Group()
        self.papergroup = pygame.sprite.Group()
        self.scissorgroup = pygame.sprite.Group()
        self.num = 2
        for i in range(self.num):
            self.rockgroup.add(Object('ROCK', random.randint(50, 650), random.randint(50, 500)))
            self.scissorgroup.add(Object('SCISSOR', random.randint(50, 650), random.randint(50, 500)))
            self.papergroup.add(Object('PAPER', random.randint(50, 650), random.randint(50, 500)))
    
    def display(self):
        self.screen.blit(self.background, (0,0))
        for rock in self.rockgroup:
            rock.movement()
            self.screen.blit(rock.image, (rock.x, rock.y))
        for paper in self.papergroup:
            paper.movement()
            self.screen.blit(paper.image, (paper.x, paper.y))
        for scissor in self.scissorgroup:
            scissor.movement()
            self.screen.blit(scissor.image, (scissor.x, scissor.y))

    def collisison(self):
        for paper in self.papergroup:
            if pygame.sprite.spritecollide(paper, self.rockgroup, True):
                self.papergroup.add(Object('PAPER', paper.x+25, paper.y+25))
            self.papergroup.remove(paper)
            paper.collide(self.rockgroup)
            self.papergroup.add(paper)
        self.papergroup.update()

        for rock in self.rockgroup:
            if pygame.sprite.spritecollide(rock, self.scissorgroup, True):
                self.rockgroup.add(Object('ROCK', rock.x+25, rock.y+25))
            self.rockgroup.remove(rock)
            rock.collide(self.scissorgroup)
            self.rockgroup.add(rock)
        self.rockgroup.update()

        for scissor in self.scissorgroup:
            if pygame.sprite.spritecollide(scissor, self.papergroup, True):
                self.scissorgroup.add(Object('SCISSOR', scissor.x+25, scissor.y+25))
            self.scissorgroup.remove(scissor)
            scissor.collide(self.papergroup)
            self.scissorgroup.add(scissor)
        self.scissorgroup.update()
   

    def play(self):
        self.display()
        self.collisison()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
               
game = Game()

while True:
    game.play()
    pygame.display.update()
    game.clock.tick(game.FPS)