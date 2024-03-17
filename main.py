import random
import pygame
from screeninfo import get_monitors

pygame.init()
pygame.font.init()
pygame.mixer.init()


run = True
game = True
FPS = 60
keys = pygame.key.get_pressed()
f_medium = pygame.font.Font(None,70)
f_small = pygame.font.Font(None,50)

clock = pygame.time.Clock()
time_now = pygame.time.get_ticks()
last_menu_sound_time = pygame.time.get_ticks()

score = 0
score_checked = False

fall_speed = 0.9
game_speed = 8
start_game = False
start_press = False
game_false = False
menu = False
start_logo = True
logo_anim = True

check_collide = False
clicked = False

# экран
for monitor in get_monitors():
    screen_w = monitor.width
    screen_h = monitor.height - 60
screen = pygame.display.set_mode((screen_w,screen_h))
screen.fill((0,0,0))
pygame.display.set_caption("Flappy Bird 2.0")
icon = pygame.image.load("pic/icon.png")
pygame.display.set_icon(icon)

# фон
fon = pygame.image.load("pic/fon.png")
bottom_fon = pygame.image.load("pic/bottom_fon.png")
new_fon = pygame.transform.scale(fon,(screen_w,screen_h + 180))
new_bottom_fon = pygame.transform.scale(bottom_fon,(screen_w,130))
bottom_fon_x = 0

# музыка
fon_sound = pygame.mixer.Sound("sounds/fon_sound.mp3")
menu_sound = pygame.mixer.Sound("sounds/menu_sound.mp3")
fon_sound_status = 1
menu_sound_status = 1
wing_effect = pygame.mixer.Sound("sounds/wing.mp3")
score_effect = pygame.mixer.Sound("sounds/point.mp3")
press_effect = pygame.mixer.Sound("sounds/press.mp3")

menu_sound.set_volume(0.2)
fon_sound.set_volume(0.4)
wing_effect.set_volume(0.8)

# конфиг трубы
pipe_image = pygame.image.load("pic/pipe.png")
new_pipe_image = pygame.transform.scale(pipe_image,(100,510))
pipe_gap = 300
pipe_hight = random.randint(-130,130)


# время
milsec = 0
sec = 0

score_text = f_small.render(f"Score: {score}",True,(224, 219, 56))
game_false_score_text = f_small.render(f"Your score: {score}",True,(224,219,56))

start_button_pic = pygame.image.load("pic/start.png")
start_button_rect = start_button_pic.get_rect(topleft=((700,420)))

restart_button_pic = pygame.image.load("pic/restart.png")
restart_button_rect = restart_button_pic.get_rect(topleft=((700,600)))

close_button_pic = pygame.image.load("pic/close_button.png")
close_button_rect = close_button_pic.get_rect(topleft=((20,20)))

settings_button_pic = pygame.image.load("pic/settings.png")
settings_button_rect = settings_button_pic.get_rect(topleft=((1030,660)))

skins_button_pic = pygame.image.load("pic/skins.png")
skins_button_rect = skins_button_pic.get_rect(topleft=((780,650)))

menu_status = "main"

logotype = pygame.image.load("pic/LOGO.png").convert()
logotype = pygame.transform.scale(logotype,(screen_w,screen_h)).convert()
logo_alpha = 0
logo_skip_text = f_medium.render("CLICK TO SKIP",True,(255,255,255))
logo_fon = pygame.mixer.Sound("sounds/logo_sound.mp3")
logo_fon.play()
logo_volume = 1

bird_x = 300
bird_y = 350

# ПТИЧКА
class Bird(pygame.sprite.Sprite):
    def __init__(self,keys,speed,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 0
        self.image = pygame.image.load("pic/flapp.png")
        self.rect = self.image.get_rect()
        self.keys = keys
        self.x = x
        self.y = y
        self.speed = speed
        self.jump = False
        self.rect.center = (self.x, self.y)
        self.clicked = False
    
    def update(self):
        global start_game,start_press,game_false,btm_pipe,top_pipe,check_collide,game,menu
        if start_game == True and start_press == True and menu == False and start_logo == False:
            # скорость падения

            if self.speed < 8:
                self.speed += 0.5
                self.rect.y += self.speed

            # падение
            if self.y < 950:
                self.rect.y += self.speed

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            if self.rect.bottom >= 930 and start_press == True:
                start_game = False
                game_false = True

            self.collide = pygame.sprite.spritecollide(bird1,Pipes,False)
            if start_game == True:
                if self.collide:
                    start_game = False
                    game_false = True
                    check_collide = False
            
        # прыжок
        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False and game_false == False and menu == False and start_logo == False:
            start_press = True
            self.clicked = True
            game = True
            if self.rect.y > 40:
                wing_effect.play()
                self.speed = -8
                

# ТРУБА
class Pipe(pygame.sprite.Sprite):
    def __init__(self,image,position,x,y):
        global pipe_gap
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [self.x,self.y - (pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [self.x,self.y + (pipe_gap / 2)]
    
    def update(self):
        global bird_x,score,score_checked,pipe_hight,btm_pipe,top_pipe

        # движение
        if start_game == True and start_press == True:
            self.rect.x -= game_speed
            if self.rect.right < 0:
                self.rect.x = 1920
        
        # счет
        if self.rect.x > 300 and self.rect.x < 309 and score_checked == False:
            score_effect.play()
            score += 1
            score_checked = True
        else:
            score_checked = False

class Switch(pygame.sprite.Sprite):
    def __init__(self,x,y,font,size,value,textvar=''):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("pic/ON.png")
        self.offimage = pygame.image.load("pic/OFF.png")
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.textvar = textvar
        self.rect.topleft = (self.x,self.y)
        self.value = value
        self.size = size
        self.font = pygame.font.Font(font,size)

    def draw(self):
        if self.value == 'on':
            screen.blit(self.image,(self.x,self.y))
        if self.value == 'off':
            screen.blit(self.offimage,(self.x,self.y))
        self.text = self.font.render(self.textvar,True,(255,255,255))
        screen.blit(self.text,(self.x-65,self.y-60))

def reset_game():
    global game_false,start_game,start_press,milsec,sec,check_collide,clicked,score
    game_false = False
    start_press = False
    start_game = False
    check_collide = False
    clicked = False
    score = 0
    
    milsec = 0
    sec = 0
    if fon_sound_status == 1:
        fon_sound.play()

    # перезапуск птицы
    bird1.rect.x = 300
    bird1.rect.y = 350

    # перезапуск труб
    Pipes.empty()
    for i in range(0,5):
        pipe_hight = random.randint(-130,130)
        btm_pipe = Pipe(new_pipe_image,-1,screen_w + 400 * i,510 + pipe_hight)
        top_pipe = Pipe(new_pipe_image,1,screen_w + 400 * i,510 + pipe_hight)
        Pipes.add(btm_pipe)
        Pipes.add(top_pipe)

def pressed(Rect):
    global clicked
    if Rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1 and clicked == False:
        return True

# группы
Birds = pygame.sprite.Group()
Pipes = pygame.sprite.Group()
bird1 = Bird(keys,fall_speed,bird_x,bird_y)
Birds.add(bird1)

music_switcher = Switch(500,300,None,85,'on','Game music')
music_switcher2 = Switch(500,500,None,85,'on','Menu music')

for i in range(0,5):
    pipe_hight = random.randint(-130,130)
    btm_pipe = Pipe(new_pipe_image,-1,screen_w + 400 * i,510 + pipe_hight)
    top_pipe = Pipe(new_pipe_image,1,screen_w + 400 * i,510 + pipe_hight)
    Pipes.add(btm_pipe)
    Pipes.add(top_pipe)
    check_collide = True

while run == True:

    time_now = pygame.time.get_ticks()


    screen.fill((0,0,0))
    if start_logo == False:
        screen.blit(new_fon,(0,0))

    keys = pygame.key.get_pressed()

    # таймер музыки
    milsec += 1
    if milsec == FPS:
        sec += 1
        milsec = 0
    if sec == 7 and milsec == 48:
        if start_game == True:
            if fon_sound_status == 1:
                fon_sound.play()
            sec = 0
    
    # остановка музыки
    if start_game == False and start_press == True and game_false == True:
        fon_sound.stop()

    # выход
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif start_button_rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
            if menu == True:
                press_effect.play()
                menu_sound.stop()
                clicked = True
                menu = False
                game_false_score_text = f_small.render("Your score: "+str(score),True,(224,219,56))
                reset_game()



    # отрисовка
    if menu == False and game_false == False and start_logo == False:
        Birds.update()
        Birds.draw(screen)

    # анимация логотипа
    if start_logo == True:
        screen.blit(logotype,(0,0))
        if logo_alpha < 256 and logo_anim == True:
            logo_alpha += 2
            if logo_alpha > 254:
                logo_anim = False
        else:
            if logo_alpha > 0 and logo_anim == False:
                logo_alpha -= 2
                logo_skip_text.set_alpha(logo_alpha)
                if logo_alpha < 150 and logo_anim == False:
                    logo_volume -= 0.01
        if logo_alpha < 2 and logo_anim == False:
            start_logo = False
            logo_fon.stop()
            if menu_sound_status == 1:
                menu_sound.play()
            menu = True  
        if pygame.mouse.get_pressed()[0] == 1 and clicked == False:
            start_logo = False
            if menu_sound_status == 1:
                menu_sound.play()
            logo_fon.stop()
            menu = True
            clicked = True
        else:
            clicked = False
        logo_fon.set_volume(logo_volume)
        logotype.set_alpha(logo_alpha)
        screen.blit(logo_skip_text,(700,900))


    # меню игры
    if menu == True and start_game == False and game_false == False and start_logo == False:
        if time_now - last_menu_sound_time >= 42000 and menu_sound_status == 1:
            menu_sound.play()
            last_menu_sound_time = time_now

        # меню...главный экран
        if menu_status == "main" and clicked == False:
            screen.blit(start_button_pic,(700,400))
            screen.blit(settings_button_pic,(1030,660))
            screen.blit(skins_button_pic,(780,650))
            if pressed(settings_button_rect):
                press_effect.play()
                menu_status = "settings"
            if pressed(skins_button_rect):
                menu_status = "skins"

        # меню...настройки
        elif menu_status == "settings":
            screen.blit(close_button_pic,(20,20))
            music_switcher.draw()
            music_switcher2.draw()
            if pressed(close_button_rect):
                press_effect.play()
                menu_status = "main"
            elif pressed(music_switcher.rect) and music_switcher.value == 'on':
                press_effect.play()
                clicked = True
                music_switcher.value = 'off'
                fon_sound_status = 0
            elif pressed(music_switcher.rect) and music_switcher.value == 'off':
                press_effect.play()
                clicked = True
                music_switcher.value = 'on'
                fon_sound_status = 1
            elif pressed(music_switcher2.rect) and music_switcher2.value == 'on':
                menu_sound.stop()
                press_effect.play()
                clicked = True
                music_switcher2.value = 'off'
                fon_sound_status = 0
            elif pressed(music_switcher2.rect) and music_switcher2.value == 'off':
                menu_sound.play()
                press_effect.play()
                clicked = True
                music_switcher2.value = 'on'
                fon_sound_status = 1

        # меню...скины
        elif menu_status == "skins":
            screen.blit(close_button_pic,(20,20))
            if pressed(close_button_rect):
                press_effect.play()
                menu_status = "main"

    if game == True:

        score_text = f_small.render(f"Score: {score}",True,(224, 219, 56))

        if pygame.mouse.get_pressed()[0] == 1 and game_false == False and menu == False and clicked == False and start_logo == False:
            clicked = True
            start_game = True

        Pipes.update()
        Pipes.draw(screen)

        if start_logo == False:
            screen.blit(new_bottom_fon,(bottom_fon_x,920))
            screen.blit(new_bottom_fon,(bottom_fon_x + screen_w,920))
        if bottom_fon_x < -screen_w:
            bottom_fon_x = 0
        
        if start_game == True:
            screen.blit(score_text,(10,10))
            # движение нижнего фона
            bottom_fon_x -= game_speed



        # проигрыш
    if start_game == False and game_false == True and menu == False:
        game = False
        screen.blit(restart_button_pic,(800,650))
        screen.blit(close_button_pic,(20,20))
        screen.blit(game_false_score_text,(500,500))
        if pressed(restart_button_rect):
            press_effect.play()
            clicked = True
            game_false_score_text = f_small.render(str(score),True,(224,219,56))
            reset_game()

        if pressed(close_button_rect):
            press_effect.play()
            if menu_sound_status == 1:
                menu_sound.play()
            menu_status = 'main'
            clicked = True
            start_game = False
            start_press = False
            game_false = False
            menu = True



    if pygame.mouse.get_pressed()[0] == 0:
        clicked = False




        


    clock.tick(FPS)
    pygame.display.update()

pygame.quit()

