# Module
import pygame as pg
from random import choice, randint

# Constants
SCREEN_SHAPE = (1200, 600)
G = 1.8
BLACK = (0, 0, 0)

# Obstacle
obstacles = {
    'high'          : pg.image.load("obstacle_high.png"),
    'high_double'   : pg.image.load("obstacle_double.png"),
    'low'           : pg.image.load("obstacle.png"),
    'low_double'    : pg.image.load("obstacle_double.png"),
    'low_triple'    : pg.image.load("obstacle_triple.png"),
    
}

pterodactyl_up = pg.image.load("pterodactyl_up.png")
pterodactyl_down = pg.image.load("pterodactyl_down.png")

class Obstacle:
    def __init__(self, kind):
        self.pterodactyl = True if kind == "pterodactyl" else False
        self.summoned = False
        if 'high' in kind:
            self.inflate_x = -30
        else:
            self.inflate_x = -10
        if 'double' in kind:
            self.inflate_x -= 10
        if 'triple' in kind:
            self.inflate_x -= 20
        img = obstacles[kind].copy()
        self.x = 1400
        self.y = 500
        if self.pterodactyl:
            self.y = randint(200, 500)
        self.v_x = obstacle_vel
        self.img = img
        self.rect = img.get_rect(bottomleft = (1400, 500))
        self.summon_position = summon_position - randint(0, 30)
    
    def draw(self):
        self.rect = self.img.get_rect(bottomleft = (self.x, self.y))
        self.hitbox = self.rect.inflate(self.inflate_x, -15)
        if self.pterodactyl:
            self.hitbox = self.hitbox.inflate(-10, -40)
        screen.blit(self.img, self.rect)


# Dino
class Dino:
    def __init__(self):
        self.y = 450
        self.v_y = 0
        self.img = dino_standing_img
        self.rect = self.img.get_rect(center = (150, 450))
        self.hitbox = self.rect.inflate(-140, -100)

    def draw(self):
        self.rect = self.img.get_rect(center = (150, self.y))
        self.hitbox = self.rect.inflate(-140, -100)
        screen.blit(self.img, self.rect)

# Settings
obstacle_vel = 11
summon_position = 100
running = True
pg.init()
screen = pg.display.set_mode(SCREEN_SHAPE)
pg.display.set_caption("Dino Game!")
dino_back_foot_step_img = pg.image.load("Dino_back_foot_step.png")
dino_front_foot_step_img = pg.image.load("Dino_front_foot_step.png")
dino_standing_img = pg.image.load("Dino_standing.png")
pg.display.set_icon(dino_standing_img)
dino_back_foot_step_img = pg.transform.scale(dino_back_foot_step_img, (200, 200))
dino_front_foot_step_img = pg.transform.scale(dino_front_foot_step_img, (200, 200))
dino_standing_img = pg.transform.scale(dino_standing_img, (200, 200))
dino_died_img = pg.image.load("Dino_died.png")
waiting = True
clock = pg.time.Clock()
dino = Dino()
jumping = False
stepped = True
jumped = False
walk_tick = 10
jump_time_limit = 3
time_passed_from_jump_started = 0
obstacle_list = [
    Obstacle('high')
]
tick = 0
score = 0
font = pg.font.SysFont('Candara', 30, True, False)
text = font.render(f"score : {score}", True, BLACK)
text2 = font.render("Press Any Key to Start!", True, BLACK)
    
# Main
while running:
    screen.fill((230, 230, 230))
    pg.draw.line(screen, BLACK, (0, 480), (1200, 480), 3)
    tick += 1

    # event process
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if waiting:
                waiting = False
            if event.key == pg.K_SPACE:
                jumping = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                jumping = False

    if dino.y == 450:
        stepped = True
        if jumping:
            jumped = True
            time_passed_from_jump_started = 0

    # jump optimization
    if jumped or (not jumped and time_passed_from_jump_started != 0 and jump_time_limit > time_passed_from_jump_started):
        time_passed_from_jump_started += 1
        if time_passed_from_jump_started > 6:
            dino.v_y -= time_passed_from_jump_started
            if dino.v_y <= -25:
                dino.v_y = -24
        else : 
            dino.v_y -= 6
        if dino.v_y < -25:
            jumped = False

    # obstacle
    if not waiting:
        for obs in obstacle_list:
            # draw
            obs.draw()
            if obs.pterodactyl and tick % 10 == 0:
                obs.img = pterodactyl_down if obs.img == pterodactyl_up else pterodactyl_up
            # moving
            obs.x -= obs.v_x

            # summoning
            if obs.x < obs.summon_position and not obs.summoned:
                obstacle_list.append(Obstacle(choice(list(obstacles.keys()))))
                obs.summoned = True

            if obs.x < -200:
                del obstacle_list[0]
    
    # walking
    if not waiting and tick % walk_tick == 0:
        if dino.y < 450:
            dino.img = dino_standing_img
        elif dino.img == dino_back_foot_step_img:
            dino.img = dino_front_foot_step_img
        else:
            dino.img = dino_back_foot_step_img

    if not waiting and tick % 5 == 0:
        score += 1
        text = font.render(f"score : {score}", True, BLACK)
    
    if score == 150:
        obstacles['pterodactyl'] = pg.image.load("pterodactyl_up.png")

    if score > 0 and tick % 500 == 0 and obstacle_vel < 26:
        obstacle_vel += 3
        summon_position -= 10
        walk_tick -= 1
    # crushing
    for obs in obstacle_list:
        if dino.hitbox.colliderect(obs):
            running = False
            dino.img = dino_died_img
            print("Game Over!")
            print(f"Score : {score}")

    if waiting:
        screen.blit(text2, (200, 200))

    dino.draw() 
    dino.y += dino.v_y
    if dino.y >= 450:
        dino.y = 450
        dino.v_y = 0
    else: 
        dino.v_y += G

    screen.blit(text, [1000, 20])

    # end
    clock.tick(60)
    pg.display.update()