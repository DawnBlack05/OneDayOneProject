# Module
import pygame as pg
from random import randint

# Constants
SCREEN_SHAPE = (800, 800)
OBSTACLE_VELOCITY = 5
G = 1

# bird
class flappy_bird:
    def __init__(self):
        self.pos = pg.Vector2(100, 400)
        self.img = pg.transform.scale(bird_icon, (70, 70))
        self.rect = self.img.get_rect(topleft = self.pos)
        self.y_v = 0

    def draw(self):
        self.rect = self.img.get_rect(topleft = self.pos)
        screen.blit(self.img, self.rect)
    
    def jump(self):
        self.y_v = 14

# obstacle
class block:
    def __init__(self, pos:tuple, image:pg.Surface, rect:pg.Rect):
        self.pos = pg.Vector2(pos)
        self.img = image
        self.rect = rect
        self.hitbox = self.rect.inflate(-10, -10)
    
    def draw(self):
        screen.blit(self.img, self.rect)

class obstacle:
    def __init__(self, x):
        y = randint(100, 500) # 위에 거 y좌표
        self.x = x
        image = pg.image.load("obstacle.png")
        image_upside_down = pg.transform.rotate(image, 180)
        self.blocks = [block((x, y), image_upside_down, image_upside_down.get_rect(bottomleft=(x, y))), block((x, y+200), image, image_upside_down.get_rect(bottomleft=(x, y)))]
        self.y = y
        self.point = 1

    def draw(self):
        self.blocks[0].rect = self.blocks[0].img.get_rect(bottomleft=(self.blocks[0].pos))
        self.blocks[1].rect = self.blocks[1].img.get_rect(topleft=(self.blocks[1].pos))
        self.blocks[0].hitbox = self.blocks[0].rect.inflate(-20, -20)
        self.blocks[1].hitbox = self.blocks[1].rect.inflate(-20, -20)
        self.blocks[0].draw()
        self.blocks[1].draw()
    
    def move(self):
        self.x -= OBSTACLE_VELOCITY
        self.blocks[0].pos = (self.x, self.y)
        self.blocks[1].pos = (self.x, self.y+200)

# Settings
running = True
pg.init()
screen = pg.display.set_mode(SCREEN_SHAPE)
pg.display.set_caption("Flappy Bird!")
bird_icon = pg.image.load("bird.png")
pg.display.set_icon(bird_icon)
clock = pg.time.Clock()
score = 0
background_img = pg.image.load("background.jpg")
camera_position = pg.Vector2(0, 0)
bird = flappy_bird()
moved_time = pg.time.get_ticks()
obstacles = [obstacle(800), obstacle(1200), obstacle(1600)]
font = pg.font.SysFont("Corbel", 30, True, False)
BLACK = (0, 0, 0)
text = font.render(f"score : {score}", True, BLACK)

# Main
while running:
    # background
    screen.blit(background_img, (0, 0))

    # event process
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                bird.jump()

    bird.draw()

    # bird move
    now_time = pg.time.get_ticks()
    if now_time - moved_time >= 20:
        bird.y_v -= G
        bird.pos -= (0, bird.y_v)

        # init
        moved_time = pg.time.get_ticks()
    
    # obstacle
    for blocks in obstacles:
        blocks.draw()
        blocks.move()
        if blocks.x <= -150:
            blocks.x = 1050
            blocks.point = 1
        
        #score
        if blocks.x <= -40 and blocks.point == 1:
            score += 1
            blocks.point = 0
            text = font.render(f"score : {score}", True, BLACK)
        
        # game over
        for fence in blocks.blocks:
            if bird.rect.colliderect(fence.hitbox):
                print("Game Over!")
                print(f"Score : {score}")
                running = False
    

    # game over
    if bird.pos[1] < -70 or bird.pos[1] > 870:
        print("Game Over!")
        print(f"Score : {score}")
        running = False

    #score
    screen.blit(text, [650, 20])
    # end
    clock.tick(60)
    pg.display.update()