# Module
import pygame as pg
from random import choice

# Constants
SCREEN_SHAPE = (800, 800) # => 20 * 20
GREEN        = (  0, 102,   0)
LIGHT_GREEN  = ( 51, 153,  51)
BLACK        = (  0,   0,   0)
LIGHT_BLACK  = ( 30,  30,  30)
RED          = (230,  51,  51)
UP           = (  0, -40)
DOWN         = (  0,  40)
LEFT         = (-40,   0)
RIGHT        = ( 40,   0)

# Settings
running = True
pg.init()
screen = pg.display.set_mode(SCREEN_SHAPE)
pg.display.set_caption("Snake Game!")
snake_img = pg.image.load("snake.png")
pg.display.set_icon(snake_img)
positions = [(i*40, j*40) for i in range(20) for j in range(20)]
map_info = {position : () for position in positions}
snake_positions = [(400, 600), (400, 640)]
moving_direction = UP
clock = pg.time.Clock()
moved_time = pg.time.get_ticks()
inputed_directions = []
reserved_direction = None
apple_pos = (400, 200)
score = 0 

# Utils
opposite = {
    UP : DOWN,
    DOWN : UP,
    RIGHT : LEFT,
    LEFT : RIGHT
}


# Map Drawer
def draw(pos, color):
    pg.draw.rect(screen, color, [*pos, 40, 40])

# Main
while running:
    # get banned direction
    h_x, h_y = snake_positions[0]
    b1_x, b1_y = snake_positions[1]
    banned_direction = (b1_x - h_x, b1_y - h_y)

    # event process
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                inputed_directions.append(UP)
            elif event.key == pg.K_LEFT:
                inputed_directions.append(LEFT)
            elif event.key == pg.K_DOWN:
                inputed_directions.append(DOWN)
            elif event.key == pg.K_RIGHT:
                inputed_directions.append(RIGHT)
    
    # moving direction process
    while inputed_directions != []:
        if inputed_directions[0] in (banned_direction, moving_direction):
            del inputed_directions[0]
        elif len(inputed_directions) >= 2:
            if inputed_directions[1] in (inputed_directions[0], opposite[inputed_directions[0]]):
                del inputed_directions[1]
            else:
                reserved_direction = inputed_directions[1]
                break
        else:
            break
    

    # move
    now_time = pg.time.get_ticks()
    if now_time - moved_time >= 80:
        # moving direction process2
        if inputed_directions != []:
            moving_direction = inputed_directions[0]
        elif reserved_direction != None:
            moving_direction = reserved_direction
            reserved_direction = None
        

        v_x, v_y = moving_direction
        # h_x, h_y = snake_positions[0] 위에 있어서 생략

        h_after_x, h_after_y = h_x + v_x, h_y + v_y
        if (h_after_x, h_after_y) in snake_positions or h_after_x > 760 or h_after_x < 0 or h_after_y > 760 or h_after_y < 0 :
            # dead
            print('Game Over!')
            print(f"score : {score}")
            running = False
        elif (h_after_x, h_after_y) == apple_pos:
            # scored
            snake_positions.insert(0, (h_after_x, h_after_y))
            score += 1
            posible_apple_positions = [pos for pos in positions if pos not in snake_positions]
            apple_pos = choice(posible_apple_positions)
        else:
            # nothing
            snake_positions.insert(0, (h_after_x, h_after_y))
            del snake_positions[-1]

        # init
        moved_time = pg.time.get_ticks()
        inputed_directions = []


    

    # map setting
    for position in positions:
        if position in snake_positions:
            if snake_positions[0] == position:
                map_info[position] = BLACK
            else:
                map_info[position] = LIGHT_BLACK
        elif position == apple_pos:
            map_info[position] = RED
        elif (sum(position) / 40) % 2 == 0:
            map_info[position] = GREEN
        else :
            map_info[position] = LIGHT_GREEN

    # draw
    for position in map_info:
        color = map_info[position]
        draw(position, color)

    # end
    clock.tick(60)
    pg.display.update()