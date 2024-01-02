# Module
import pygame as pg
from random import choice

# Constants
SCREEN_SHAPE = (800, 800)
WHITE  = (255, 255, 255)
BLACK  = (  0,   0,   0)
GRAY   = (120, 120, 120)
YELLOW = (255, 204,  51)
GREEN  = (  0, 204,   0)

# Settings
pg.init()
running = True
screen = pg.display.set_mode(SCREEN_SHAPE)
pg.display.set_caption("Wordle!")
wordle_icon_img = pg.image.load("word.png")
pg.display.set_icon(wordle_icon_img)
clock = pg.time.Clock()
font_big = pg.font.Font("NotoSansMono-Light.ttf", 100)
font_small = pg.font.Font("NotoSansMono-Light.ttf", 60)
font_tiny = pg.font.Font("NotoSansMono-Light.ttf", 20)
score = 0

# Vocab
f = open("vocab.txt", "r")
vocab = [line.strip().upper() for line in f.readlines()]
answer = choice(vocab)
vocab.remove(answer)
f.close()

# Word
word = ''
word_processed = ''
words_commited = []

print(answer)
# Main
while running:
    screen.fill(WHITE)

    # word process
    if len(word) < 5:
        word_processed = word + '_'*(5-len(word))
    else:
        word_processed = word

    # event process
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key in range(pg.K_a, pg.K_z + 1):
                if len(word) < 5:
                    word += chr(event.key).upper()
            elif event.key == pg.K_BACKSPACE:
                word = word[:-1]
            elif event.key == pg.K_RETURN and len(word) == 5:
                words_commited.append(word)
                word = ''
    
    # score
    score_text = font_tiny.render(f"score : {score}", True, BLACK)
    score_text_rect = score_text.get_rect(center = (700, 150))
    screen.blit(score_text, score_text_rect)

    # blit texts            
    current_word = font_big.render(f"{' '.join(word_processed)}", True, BLACK)
    current_word_rect = current_word.get_rect(center = (400, 50))
    screen.blit(current_word, current_word_rect)
    for idx, commited_word in enumerate(words_commited):
        for pos, alphabet in enumerate(commited_word):
            if alphabet in answer:
                if answer[pos] == alphabet:
                    pg.draw.rect(screen, GREEN, (130 + pos*36 + idx//5 * 360, 200 + idx%5 * 100, 36, 72))
                else:
                    pg.draw.rect(screen, YELLOW, (130 + pos*36 + idx//5 * 360, 200 + idx%5 * 100, 36, 72))
            else:
                pg.draw.rect(screen, GRAY, (130 + pos*36 + idx//5 * 360, 200 + idx%5 * 100, 36, 72))
        commited_text = font_small.render(f'{commited_word}', True, BLACK)
        commited_text_rect = commited_text.get_rect(center = (220 + idx//5 * 360, 230 + idx%5 * 100))
        screen.blit(commited_text, commited_text_rect)
    
    # succeed
    if answer in words_commited:
        celebrating_text = font_tiny.render('Correct!', True, BLACK)
        celebrating_text_rect = celebrating_text.get_rect(center = (650, 120))
        screen.blit(celebrating_text, celebrating_text_rect)
        score += 1
        pg.display.update()
        pg.time.wait(1000)
        words_commited = []
        answer = choice(vocab)
        vocab.remove(answer)
    
    # game over
    if len(words_commited) == 10:
        if answer not in words_commited:
            print('Game Over!')
            print(f'score : {score}')
            running = False

    # end
    clock.tick(60)
    pg.display.update()
