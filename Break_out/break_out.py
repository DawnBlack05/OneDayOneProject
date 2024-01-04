# Module
import pygame as pg
from random import uniform

# Constants
SCREEN = (800, 800)
GRAY       = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY  = ( 30,  30,  30)
BLACK      = (  0,   0,   0)
RED        = (255,   0,   0)
COF = 0.02  # Coefficent of Friction. 마찰계수
R = 7

# Bricks
class Brick:
    def __init__(self, pos):
        self.pos = pg.Vector2(pos)
        self.rect = pg.Rect(pos[0] + 1, pos[1] + 1, 38, 18)
        self.destroyed = False
    def draw(self):
        pg.draw.rect(screen, GRAY, self.rect, 0, 2)

brick_positions = [(40 * x, 20 * y) for x in range(20) for y in range(20)]
bricks = [Brick(pos) for pos in brick_positions]

# Ball
class Ball:
    def __init__(self, pos=(250, 600), vel=(0.2, 0.2)):
        self.pos = pg.Vector2(*pos)
        self.rect = pg.Rect(self.pos[0] - R, self.pos[1] - R, 1 + 2 * R, 1 + 2 * R)
        self.vel = pg.Vector2(*vel)

    def draw(self):
        pg.draw.circle(screen, LIGHT_GRAY, self.pos, R)

    def update(self, dt):
        self.pos += dt * self.vel
        self.rect = pg.Rect(self.pos[0] - R, self.pos[1] - R, 1 + 2 * R, 1 + 2 * R)

#ball = Ball()
balls = [Ball()]

# Board
class Board:
    def __init__(self):
        self.pos = pg.Vector2(400, 750)
        self.rect = pg.Rect(self.pos[0] - 40, self.pos[1] - 2, 81, 5)
        self.vel = pg.Vector2(0, 0)
    
    def draw(self):
        pg.draw.rect(screen, GRAY, self.rect)
    
    def update(self, dt):
        self.pos += dt * self.vel
        self.rect = pg.Rect(self.pos[0] - 40, self.pos[1] - 2, 81, 5)

board = Board()

# Settings
pg.init()
running = True
screen = pg.display.set_mode(SCREEN)
time_past = pg.time.get_ticks()
destroyed_block_count = 0

# Main
while running:
    # init
    screen.fill(BLACK)

    # event process
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                board.vel = pg.Vector2(-0.6, 0)
            elif event.key == pg.K_RIGHT:
                board.vel = pg.Vector2(0.6, 0)
        elif event.type == pg.KEYUP:
            if event.key in [pg.K_LEFT, pg.K_RIGHT]:
                board.vel = pg.Vector2(0, 0)

    # time_checker
    time_now = pg.time.get_ticks()
    dt = time_now - time_past
    time_past = time_now
    
    # board
    if board.pos[0] < 51:
        board.vel = pg.Vector2(0, 0)
        board.pos[0] = 51
    elif board.pos[0] > 749:
        board.vel = pg.Vector2(0, 0)
        board.pos[0] = 749
    board.update(dt)
    board.draw()

    # ball
    for ball in balls:
        ball.update(dt)
        ball.draw()
        if ball.rect.colliderect(board.rect):
            ball.vel[0] += dt * board.vel[0] * COF
            ball.vel[1] += dt * ball.vel.dot(board.vel) * 0.1
            ball.vel[1] *= -1
            ball.pos += pg.Vector2(0, -1)
        elif ball.pos[0] < R:
            ball.pos[0] = R
            ball.vel[0] *= -1
        elif ball.pos[0] > 800 - R:
            ball.pos[0] = 800 - R
            ball.vel[0] *= -1
        elif ball.pos[1] > 800:
            balls.remove(ball)
        elif ball.pos[1] < R:
            ball.pos[1] = R
            ball.vel[1] *= -1
        if ball.vel.length() > 0.7:
            ball.vel = ball.vel.normalize() * 0.7
    
    # bricks
    for ball in balls:
        for brick in bricks:
            if not brick.destroyed:
                brick.draw()
                if brick.rect.colliderect(ball.rect):
                    x_diff = ball.pos[0]-brick.pos[0]
                    y_diff = ball.pos[1]-brick.pos[1]
                    if y_diff >= 20:
                        ball.vel[1] *= -1
                        ball.pos[1] += 1
                    elif y_diff <= -20:
                        ball.vel[1] *= -1
                        ball.pos[1] -= 1
                    elif x_diff >= 40:
                        ball.vel[0] *= -1
                        ball.pos[0] += 1
                    elif x_diff <= -40:
                        ball.vel[0] *= -1
                        ball.pos[0] -= 1
                    brick.destroyed = True
                    destroyed_block_count += 1
                    x_speed = uniform(-0.1, 0.1)
                    y_speed = uniform(0.1, 0.3)
                    balls.append(Ball((brick.pos[0]+20, brick.pos[1]+10), (x_speed, y_speed)))
                    break
        

    # game over
    if len(balls) == 0:
        print("Game Over!")
        running = False

    # success
    if destroyed_block_count == len(bricks):
        print("Succeed!")
        screen.fill(BLACK)
        pg.time.wait(1500)
        running = False
    

    pg.display.update()
