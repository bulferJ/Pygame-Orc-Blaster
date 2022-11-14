
import pygame
from sys import exit
from pygame import mixer
import os


pygame.init()
clock = pygame.time.Clock()

win = pygame.display.set_mode((800,500))
pygame.display.set_caption('Orc Blaster')


game_active = False
start = True
game_over = False
vic_screen = False

start_font = pygame.font.Font('space_game_graphics/Audiowide-Regular.ttf',30)
start_text = start_font.render('Orc Blaster',False,'Cyan')

game_over_text = start_font.render('Game Over',False,'Cyan')
you_suck_text = start_font.render('You Suck',False,'Cyan')

mouse_and_touch_text = start_font.render('Mouse and Touch Pad',False,'Cyan')
arrows_and_space_text = start_font.render('Arrows and Space',False,'Cyan')

mouse_and_touch_rect = mouse_and_touch_text.get_rect(center = (220,300))
arrows_and_space_rect = arrows_and_space_text.get_rect(center = (620,300))


bg = pygame.image.load('space_game_graphics/space_bg.jpg')

sp_img = pygame.image.load(os.path.join('space_game_graphics','spaceship.png'))
sp = pygame.transform.scale(sp_img,(100,100))
sp_rect = sp.get_rect( center = (400,420))

orc_img = pygame.image.load(os.path.join('space_game_graphics','orc.xcf'))
orc_dead = pygame.image.load(os.path.join('space_game_graphics','orc_dead.xcf'))
orc_dead = pygame.transform.scale(orc_dead,(130,110))

orc = pygame.transform.scale(orc_img,(150,120))
orc_rect = orc.get_rect( center = (400,70))

orc_health = 100


laser_sound = pygame.mixer.Sound('space_game_graphics/laser1.wav')

left = False
right = False
firing = False

def sp_display():
    if arrows_and_space == True:
        if left and sp_rect.x >= 0:
            sp_rect.x -= 5
        
        if right and sp_rect.x <= 700:
            sp_rect.x += 5
    if mouse_and_touch == True:
        sp_rect.x = pygame.mouse.get_pos()[0]

    win.blit(sp,sp_rect)
    global orc_health
    if firing:
        laser = pygame.Rect(sp_rect.x+49,0, 3,380)
        laser_ball =  pygame.Rect(sp_rect.x+43.5,371, 15,15)
        laser_rect = pygame.draw.rect(win,(255,0,0),laser)
        pygame.draw.ellipse(win,(200,0,0),laser_ball)
        if laser_rect.colliderect(orc_rect) and orc_health >= 0:
            print(orc_health)
            orc_health -= 1    
            laser_sound.play()
            
orc_vel = 1

def orc_display():
    global orc_vel, vic_screen, game_active, vic_timer
    if orc_health >= 0:
        if orc_rect.x <= -20:
            orc_vel *= -1
        if orc_rect.x >= 680:
            orc_vel *= -1
        orc_rect.x  -= orc_vel
        win.blit(orc, orc_rect)
    else:
        win.blit(orc_dead, orc_rect)
        vic_timer = pygame.time.get_ticks() + 3000
        
        if pygame.time.get_ticks() > vic_timer:
            vic_screen = True
            game_active = False
   

    orc_health_rect = pygame.Rect(orc_rect.x + 20,23,orc_health,10)
    orc_health_draw = pygame.draw.rect(win,(255,0,0),orc_health_rect)



mouse_and_touch = False
arrows_and_space = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if game_active == True:
        pygame.mouse.set_visible(False)
        win.blit(bg, (0,0))
        sp_display()
        orc_display()
        # print(int(orc_dead_blit))
        keys = pygame.key.get_pressed()
        #key statements must be if,elif and else
        if keys[pygame.K_LEFT]:
            left = True
            right = False

        elif keys[pygame.K_RIGHT]:
            right = True
            left = False
        else:
            right = False
            left = False

        #checks which laser firing controls are active, should be in funtion for cleaner code
        if mouse_and_touch == True:
            arrows_and_space = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                firing = True
            else:
                firing = False
        if arrows_and_space == True:
            mouse_and_touch = False
            if keys[pygame.K_SPACE]:
                firing = True
            else:
                firing = False
        
        #game over test
        if keys[pygame.K_g]:
            game_over = True
            run = False


    if start == True:
        win.blit(bg, (0,0))
        win.blit(start_text,(320,100))
        win.blit(mouse_and_touch_text,mouse_and_touch_rect)
        win.blit(arrows_and_space_text,arrows_and_space_rect)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if (mouse_and_touch_rect.collidepoint(event.pos)):
                mouse_and_touch = True
                game_active = True
                start = False
            if (arrows_and_space_rect.collidepoint(event.pos)):
                arrows_and_space = True
                game_active = True
                start = False
    if game_over == True:
        win.blit(bg, (0,0))
        win.blit(game_over_text,(310,100))
        win.blit(you_suck_text,(320,300))
            
    if vic_screen == True:
        win.blit(bg, (0,0))




    clock.tick(60)
    pygame.time.delay(2)
    pygame.display.update()