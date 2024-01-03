# Module
import pygame as pg
from random import sample

# Constants
SCREEN = (900, 900)
WHITE = (255, 255, 255)
GRAY = (153, 153, 153)
LIGHT_GRAY = (204, 204, 204)
DARK_GRAY = (102, 102, 102)
COLOR1 = ( 51,  51, 153)
COLOR2 = ( 51, 153,  51)
COLOR3 = (204, 000,  51)
COLOR4 = (255, 204, 000)
COLOR5 = (204,  51, 204)
COLOR6 = (102, 204,  51)
COLOR7 = (  0,  51, 153)
COLOR8 = (204,   0, 255)
LEFT_CLICK = 1
RIGHT_CLICK = 3


# Utils
def near(pos):
    x, y = pos
    if x == 0:
        if y == 0:
            near_list = [
                        (  x, y+1),
            (x+1,   y), (x+1, y+1), 
            ]
        elif y == 17:
            near_list = [
            (  x, y-1),           
            (x+1, y-1), (x+1,   y) 
            ]
        else:
            near_list = [
            (  x, y-1),             (  x, y+1),
            (x+1, y-1), (x+1,   y), (x+1, y+1), 
            ]
    elif x == 17:
        if y == 0:
            near_list = [
            (x-1,   y), (x-1, y+1),
                        (  x, y+1),
            ]
        elif y == 17:
            near_list = [
            (x-1, y-1), (x-1,   y),
            (  x, y-1),            
            ]
        else:
            near_list = [
            (x-1, y-1), (x-1,   y), (x-1, y+1),
            (  x, y-1),             (  x, y+1),
            ]
    else:
        if y == 0:
            near_list = [
            (x-1,   y), (x-1, y+1),
                        (  x, y+1),
            (x+1,   y), (x+1, y+1), 
            ]
        elif y == 17:
            near_list = [
            (x-1, y-1), (x-1,   y),
            (  x, y-1),            
            (x+1, y-1), (x+1,   y), 
            ]
        else:
            near_list = [
            (x-1, y-1), (x-1,   y), (x-1, y+1),
            (  x, y-1),             (  x, y+1),
            (x+1, y-1), (x+1,   y), (x+1, y+1), 
            ]
    
    return near_list
def text_drawer(num, i, j):
    util_dict = {
        1 : text_1,
        2 : text_2,
        3 : text_3,
        4 : text_4,
        5 : text_5,
        6 : text_6,
        7 : text_7,
        8 : text_8,
    }
    text = util_dict[num]
    text_rect = text.get_rect(center = (i * 50 + 25, j * 50 + 25))
    screen.blit(text, text_rect)
# Settings
map_positions = [(x, y) for x in range(18) for y in range(18)]
map_data = {
    pos : {
        'hidden' : 0,
        'opened' : False,
        'flagged' : False
    } for pos in map_positions
} 
mine_positions = sample(map_positions, 40)
for pos in mine_positions:
    map_data[pos]['hidden'] = '*'
    for pos_near_mine in near(pos):
        if pos_near_mine not in mine_positions:
            map_data[pos_near_mine]['hidden'] += 1
running = True
pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode(SCREEN)
pg.display.set_caption("Mine Sweeper!")
mine_icon = pg.image.load("mine.png")
pg.display.set_icon(mine_icon)
mine_image = pg.transform.scale(mine_icon, (45, 45))
mine_rect = mine_image.get_rect(center=(450, 450))
flag_img = pg.transform.scale(pg.image.load('flag.png'), (40, 40))
flag_left = 40
font = pg.font.Font('font.ttf', 30)
text_1 = font.render('1', True, COLOR1)
text_2 = font.render('2', True, COLOR2)
text_3 = font.render('3', True, COLOR3)
text_4 = font.render('4', True, COLOR4)
text_5 = font.render('5', True, COLOR5)
text_6 = font.render('6', True, COLOR6)
text_7 = font.render('7', True, COLOR7)
text_8 = font.render('8', True, COLOR8)
gameover = False


# Main
while running:
    screen.fill(LIGHT_GRAY)
    
    # event process
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == LEFT_CLICK:
                mouse_pos_raw = pg.mouse.get_pos()
                x, y = mouse_pos_raw
                mouse_pos = (x // 50), (y // 50)
                if not map_data[mouse_pos]['opened'] and not map_data[mouse_pos]['flagged']:
                    map_data[mouse_pos]['opened'] = True
            elif event.button == RIGHT_CLICK:
                mouse_pos_raw = pg.mouse.get_pos()
                x, y = mouse_pos_raw
                mouse_pos = (x // 50), (y // 50)
                if not map_data[mouse_pos]['opened']:
                    if map_data[mouse_pos]['flagged']:
                        flag_left += 1
                        map_data[mouse_pos]['flagged'] = False  
                    elif flag_left != 0:
                        flag_left -= 1
                        map_data[mouse_pos]['flagged'] = True
                    
    # map draw & emptys_open
    for i, j in map_positions:
        if map_data[(i, j)]['opened']:
            if map_data[(i, j)]['hidden'] != '*':
                if map_data[(i, j)]['hidden'] != 0:
                   text_drawer(map_data[(i, j)]['hidden'], i, j)
                else:
                    for near_position in near((i, j)):
                        map_data[near_position]['opened'] = True
            else:
                print('Game Over!')
                pg.draw.rect(screen, GRAY, [i * 50, j * 50, 50, 50])
                gameover = True
                running = False
        else:
            pg.draw.rect(screen, GRAY, [i * 50, j * 50, 50, 50])
            if map_data[(i, j)]['flagged']:
                flag_rect = flag_img.get_rect(center = (i * 50 + 25, j * 50 + 25))
                screen.blit(flag_img, flag_rect)
        pg.draw.rect(screen, DARK_GRAY, [i * 50, j * 50, 50, 50], 1)
    
    # game over
    if gameover:
        for i, j in mine_positions:
            mine_rect = mine_image.get_rect(center = (i * 50 + 25, j * 50 + 25))
            screen.blit(mine_image, mine_rect)
            pg.display.update()
            pg.time.wait(10)
        pg.time.wait(800)
    
    # success
    count = 0
    for i, j in map_positions:
        if map_data[(i, j)]['opened'] == flag_left:
            pg.display.update()
            pg.time.wait(1000)
            running = False
            print('succeed!!')
            print(f'time : {clock.get_time()}')


    # end
    clock.tick(60)
    pg.display.update()