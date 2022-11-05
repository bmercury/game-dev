from cgi import test
import pygame as pg
import os

from colors import *
from ship import Ship

pg.font.init()
pg.mixer.init()

TITLE = "Demo 1"
WIDTH, HEIGHT = 900, 500
FPS = 60

SHIP_WIDTH, SHIP_HEIGHT = 55, 40
SHIP_SPEED = 5

BULLET_SPEED = 10
HEALTH_FONT = pg.font.SysFont('sans-serif', 40)
WIN_FONT = pg.font.SysFont('sans-serif', 80)

WIN = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption(TITLE)
ship_yellow_img = pg.image.load(os.path.join('Assets','player_yellow.png'))
ship_yellow_img = pg.transform.scale(ship_yellow_img, (SHIP_WIDTH, SHIP_HEIGHT))
ship_yellow_img = pg.transform.rotate(ship_yellow_img, 90)
ship_red_img = pg.image.load(os.path.join('Assets','player_red.png'))
ship_red_img = pg.transform.scale(ship_red_img, (SHIP_WIDTH, SHIP_HEIGHT))
ship_red_img = pg.transform.rotate(ship_red_img, -90)
bg_img = pg.image.load(os.path.join('Assets','bg.png'))
bg_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))
BORDER = pg.Rect(WIDTH/2-1, 0, 2, HEIGHT)
YELLOW_HURT = pg.USEREVENT + 1
RED_HURT = pg.USEREVENT + 2
BULLET_DMG = 5
BULLET_HIT_SOUND = pg.mixer.Sound(os.path.join('Assets','grenade.mp3'))
BULLET_FIRE_SOUND = pg.mixer.Sound(os.path.join('Assets','gun.mp3'))

def render(bg_img, yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    WIN.fill(PURPLE)
    WIN.blit(ship_yellow_img, (yellow.x, yellow.y))
    WIN.blit(ship_red_img, (red.x, red.y))
    pg.draw.rect(WIN, (255,255,255), BORDER)

    yellow_health_text = HEALTH_FONT.render("HP: " + str(yellow_health), 1, WHITE)
    red_health_text = HEALTH_FONT.render("HP: " + str(red_health), 1, WHITE)

    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    for bullet in yellow_bullets :
        pg.draw.rect(WIN, YELLOW, bullet)

    for bullet in red_bullets :
        pg.draw.rect(WIN, RED, bullet)

    pg.display.update()

def show_winner(text):
    draw_text = WIN_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2-draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pg.display.update()
    pg.time.delay(2000)

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_SPEED
        if red.colliderect(bullet):
            pg.event.post(pg.event.Event(RED_HURT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_SPEED
        if yellow.colliderect(bullet):
            pg.event.post(pg.event.Event(YELLOW_HURT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def handle_player_movement(keys_pressed, yellow, red):
    #MOVE YELLOW
    if keys_pressed[pg.K_a] and yellow.x - SHIP_SPEED > 0: #left
        yellow.x -= SHIP_SPEED
    if keys_pressed[pg.K_d] and yellow.x + SHIP_SPEED < WIDTH//2 - SHIP_WIDTH: #right
        yellow.x += SHIP_SPEED
    if keys_pressed[pg.K_w] and yellow.y - SHIP_SPEED > 0: #up
        yellow.y -= SHIP_SPEED
    if keys_pressed[pg.K_s] and yellow.y + SHIP_SPEED < HEIGHT - SHIP_HEIGHT: #down
        yellow.y += SHIP_SPEED

    #MOVE RED
    if keys_pressed[pg.K_LEFT] and red.x - SHIP_SPEED > WIDTH//2: #left
        red.x -= SHIP_SPEED
    if keys_pressed[pg.K_RIGHT] and red.x + SHIP_SPEED < WIDTH - SHIP_WIDTH: #right
        red.x += SHIP_SPEED
    if keys_pressed[pg.K_UP] and red.y - SHIP_SPEED > 0: #up
        red.y -= SHIP_SPEED
    if keys_pressed[pg.K_DOWN] and red.y + SHIP_SPEED < HEIGHT - SHIP_HEIGHT: #down
        red.y += SHIP_SPEED

def main():

    yellow = pg.Rect(100, 300, SHIP_WIDTH, SHIP_HEIGHT)
    red = pg.Rect(700, 300, SHIP_WIDTH, SHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []

    yellow_health = 10
    red_health = 10

    winner_txt = ""

    clock = pg.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    bullet = pg.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pg.K_RCTRL:
                    bullet = pg.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HURT:
                red_health -= BULLET_DMG
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HURT:
                yellow_health -= BULLET_DMG
                BULLET_HIT_SOUND.play()

        if red_health <= 0:
            winner_txt = "Yellow wins!"
        
        if yellow_health <= 0:
            winner_txt = "Red wins!"

        if winner_txt != "":
            show_winner(winner_txt)
            break

        keys_pressed = pg.key.get_pressed()
        handle_player_movement(keys_pressed, yellow, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        render(bg_img, yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)

    main()

if __name__ == "__main__":
    main()