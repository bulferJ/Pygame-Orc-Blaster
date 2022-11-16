import pygame
from sys import exit
from pygame import mixer
import os

#basic setup for any game
pygame.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode((800,500)) #Sets window
pygame.display.set_caption('Orc Blaster')#Text/Title is displayed at top of window


game_active = False
start = True
game_over = False #press g for game_over, for toubleshooting
vic_screen = False #victory


#start screen text
start_font = pygame.font.Font('space_game_graphics/Audiowide-Regular.ttf',30)
start_text = start_font.render('Orc Blaster',False,'Cyan')
#Player selects these for control preference
mouse_and_touch_text = start_font.render('Mouse and Touch Pad',False,'Cyan')
arrows_and_space_text = start_font.render('Arrows and Space',False,'Cyan') 
#rectangles are placed around text for a 'hitbox', or collide point with the mouse
mouse_and_touch_rect = mouse_and_touch_text.get_rect(center = (220,300))
arrows_and_space_rect = arrows_and_space_text.get_rect(center = (620,300))
#player mouse button input at start screen to change controls
mouse_and_touch = False
arrows_and_space = False
#game over screen, press g to get to this screen
game_over_text = start_font.render('Game Over',False,'Cyan')
you_suck_text = start_font.render('You Suck',False,'Cyan')

bg = pygame.image.load('space_game_graphics/space_bg.jpg') #background

sp_img = pygame.image.load(os.path.join('space_game_graphics','spaceship.png'))#sp = spaceship
sp = pygame.transform.scale(sp_img,(100,100))
sp_rect = sp.get_rect( center = (400,420))

orc_img = pygame.image.load(os.path.join('space_game_graphics','orc.xcf')) #displays when orc_health = 0
orc_dead = pygame.image.load(os.path.join('space_game_graphics','orc_dead.xcf'))
orc_dead = pygame.transform.scale(orc_dead,(130,110))

orc = pygame.transform.scale(orc_img,(150,120))
#either pygame.Rect(left,top,width,height), or pygame.get_rect(center = (x,y)) for drawing rect directly over image
#rectangles are useful for moving the image, and for collision. Sprite class combines image and rect, for less code
orc_rect = pygame.Rect(100,50,130,50)


#simply played every time laser collides with orc_rect, in game loop
laser_sound = pygame.mixer.Sound('space_game_graphics/laser1.wav')
#main music simply plays before game loop, and stops when game_over = True
main_music = pygame.mixer.Sound('space_game_graphics/Techno_5.mp3')
#sounds played in game loop, sometimes play/loop over and over, with every frame
#this is solved with a boolean has_played_x_music variable, playing the music once. See game over funtion in game loop
#These two sounds require these boolean variables (there may be an easier way to do this, idk)
game_over_music = pygame.mixer.Sound('space_game_graphics/game_over.mp3')
death_sound = pygame.mixer.Sound('space_game_graphics/death_1.mp3')

left = False
right = False #sp/spaceship movement and attack
firing = False

#the width of sp and orc health bars are equal to the health variables, causing the health bars to shrink, each time sp and orc are attacked
sp_health = 100
orc_health = 100 

#sp movement, attack, and health bar all in one funtion
def sp_display():
    global orc_health, sp_health, game_over, arrows_and_space, mouse_and_touch, keys

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
    #sp movement controls are chosen by player on start screen
    if arrows_and_space == True:
        if left and sp_rect.x >= 0:
            sp_rect.x -= 5
        
        if right and sp_rect.x <= 700:
            sp_rect.x += 5
    #the sp horizontal position follows the mouse
    if mouse_and_touch == True:
        sp_rect.x = pygame.mouse.get_pos()[0]

    win.blit(sp,sp_rect) 

    #health bar

    #first rect is a red overlay, size doesn't change
    sp_health_rect_red = pygame.Rect(sp_rect.x ,480,100,10)
    pygame.draw.rect(win,(255,0,0),sp_health_rect_red)

    #each rects x position is based on sp

    #this rect shrinks with decreasing health
    sp_health_rect_green = pygame.Rect(sp_rect.x ,480,sp_health,10)
    pygame.draw.rect(win,(50,180,0),sp_health_rect_green)

    #attack

    #control 1
    if mouse_and_touch == True:
        arrows_and_space = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            firing = True
        else:
            firing = False
    #control 2
    if arrows_and_space == True:
        mouse_and_touch = False
        if keys[pygame.K_SPACE]:
            firing = True
        else:
            firing = False

    if firing:
        laser_sound.play()
        laser = pygame.Rect(sp_rect.x+49,0, 3,380)
        laser_ball =  pygame.Rect(sp_rect.x+43.5,371, 15,15)
        laser_rect = pygame.draw.rect(win,(255,0,0),laser)
        pygame.draw.ellipse(win,(200,0,0),laser_ball)
        if laser_rect.colliderect(orc_rect) and orc_health >= 0:
            print(orc_health)
            orc_health -= 1   
    #death   
    if sp_health <= 0: #player dies
        game_over = True
    

orc_vel = 1 #velocity, or speed orc is moving left to right

# if the orc is moving left or right, projectile moves in that direction, for better physics
orc_left = True 
orc_right = False

def orc_display():
    global orc_vel, vic_screen, game_active, orc_left, orc_right, vic_timer
    if orc_health >= 0:
        if orc_rect.x <= -20:
            orc_vel *= -1
            orc_right = True
            orc_left = False
        if orc_rect.x >= 680:
            orc_vel *= -1
            orc_left = True
            orc_right = False
        orc_rect.x  -= orc_vel
        win.blit(orc, orc_rect)
        orc_health_rect_green = pygame.Rect(orc_rect.x + 25,23,orc_health,10)
        orc_health_rect_red = pygame.Rect(orc_rect.x + 25,23,100,10)
        pygame.draw.rect(win,(255,0,0),orc_health_rect_red)
        pygame.draw.rect(win,(50,180,0),orc_health_rect_green)
        orc_attack()

    else:
        orc_death()
    

barf_y_vel = 3 #barf is orc projectile
barf_x_vel = -1

barf = pygame.Rect(orc_rect.x,80,15,15)   

def orc_attack():
    global barf_x_vel, sp_health
    pygame.draw.ellipse(win, (0,50,0), barf)
    barf.x += barf_x_vel
    barf.y += barf_y_vel
    if barf.y >= 500:
        barf.y = 80
        barf.x = orc_rect.x + 50
    if orc_left:
        barf_x_vel = -1
    if orc_right:
        barf_x_vel = 1
    if barf.colliderect(sp_rect) and sp_health >= 0:
            sp_health -= 5 

has_played_orc_death_sound = False

def orc_death():
        global has_played_orc_death_sound
        win.blit(orc_dead, orc_rect)
        
        #so orc death sound does not loop/repeat
        if has_played_orc_death_sound == False:
            laser_sound.stop()
            death_sound.play()
            has_played_orc_death_sound = True

# to make sure game music only plays once in game loop
has_played_game_over_music = False 

# main music only excecutes once because it is before game loop
# thus does not require has_played boolean
main_music.play(5)

while True:
    for event in pygame.event.get(): #basic game setup
        if event.type == pygame.QUIT: #gives window 'X' button to quit
            pygame.quit()
            exit()
    if game_active == True:

        pygame.mouse.set_visible(False) #mouse is invisible
        win.blit(bg, (0,0))
        sp_display()
        orc_display()
        
        #screen shortcuts for troubleshooting
        if keys[pygame.K_g]: #to get to game_over screen
            game_over = True
            run = False
        if keys[pygame.K_v]: #to get to victory screen
            vic_screen = True
            run = False

    #start menu/screen
    if start == True:
        win.blit(bg, (0,0)) # space background
        win.blit(start_text,(320,100)) # Orc Blaster Title Text
        win.blit(mouse_and_touch_text,mouse_and_touch_rect) # 1st control option
        win.blit(arrows_and_space_text,arrows_and_space_rect) # 2nd control option

        if event.type == pygame.MOUSEBUTTONDOWN: # if player clicks
            if (mouse_and_touch_rect.collidepoint(event.pos)):
                mouse_and_touch = True # activates player controls
                game_active = True #starts game
                start = False 
            if (arrows_and_space_rect.collidepoint(event.pos)):
                arrows_and_space = True  # activates player controls
                game_active = True #starts game
                start = False

    #game_over screen
    if game_over == True:
        game_active = False
        main_music.stop()
        if has_played_game_over_music == False:
            game_over_music.play(0)
            has_played_game_over_music = True

        win.blit(bg, (0,0)) #space background
        win.blit(game_over_text,(310,100))
        win.blit(you_suck_text,(320,300))
        
    if vic_screen == True:
        win.blit(bg, (0,0))



    #updates at 60 fps, required for every game
    clock.tick(60)
    pygame.time.delay(2)
    pygame.display.update()
