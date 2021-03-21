import pygame,sys,random,time,os,math
import data.engine as e
import data.cursor as cursor
import data.sword as sword
from pygame.locals import *
#-----tons of variables---------------------------------------------------------------------------------
# pygame initialization etc.----------------------------------------------------------------------------
pygame.init()
clock = pygame.time.Clock()
screen_size = (700,500)
screen = pygame.display.set_mode(screen_size,0,32)
pygame.display.set_caption('weapon master')
display = pygame.Surface((263,188))
e.set_global_colorkey((0,0,0))
#------ loading images, camera etc.---------------------------------------------------------------------
e.load_animations('data/images/entities/')
player = e.entity(256,128,16,16,'player')
player.moving_left = False
player.moving_right = False
true_scroll = [0,0]
game_map = e.load_map('data/images/tile_maps/map')
player.vertical_momentum = 0
player.air_timer = 0
last_time = time.time()
blue_tile = {1: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_0.png'),
             2: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_1.png'),
             3: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_2.png'),
             4: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_3.png'),
             5: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_4.png'),
             6: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_5.png'),
             7: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_6.png'),
             8: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_7.png'),
             9: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_8.png'),
             10: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_9.png'), 
             11: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_a.png'),
             12: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_b.png'),
             13: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_c.png'),
             14: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_d.png'),
             15: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_e.png'),
             16: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_f.png')}
#----- sounds-------------------------------------------------------------------------------------------
jump_sound = pygame.mixer.Sound('data/sounds/jump_sound.wav')
pygame.mixer.music.load('data/sounds/music.wav')
pygame.mixer.music.play(-1)
errors = 0
# ---- chunk generation---------------------------------------------------------------------------------
CHUNK_SIZE = 8
particles = []
def generate_chunk(x,y):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0 
            if target_y > 10:
                tile_type = 5 
            elif target_y == 10:
                tile_type = 2 
            if tile_type != 0:
                chunk_data.append([[target_x,target_y],tile_type])
    return chunk_data
chunk_map = {}
#-----cursor--------------------------------------------------------------------------------------------
mx, my = pygame.mouse.get_pos()
cursor = cursor.cursor([my, my], 'data/images/cursor/default.png')
pygame.mouse.set_visible(False)
# --- mainloop------------------------------------------------------------------------------------------
start_time = time.time()
values = []
#-----angle stuff---------------------------------------------------------------------------------------
def meassure_angle(dis_x, dis_y):
    try:
        angle = math.atan(dis_x / dis_y)
        if dis_x < 0:
            dis_x += math.pi
        angle = math.degrees(angle)
        return angle
    except ZeroDivisionError:
        angle = 10

#-----sword---------------------------------------------------------------------------------------------
sword_img = pygame.image.load('data/images/sword/sword.png')
class Sword():
    def __init__(self, pos,img):
        self.pos = pos
        self.img = img
        self.img.set_colorkey((0,0,0))
        self.width, self.height = self.img.get_width(), self.img.get_height()
        self.angle = 0
sword = Sword([player.x, player.y], sword_img)
while True:
#-------scroll-------------------------------------------------------------
    true_scroll[0] += (player.x - true_scroll[0] - 154)
    true_scroll[1] += (player.y - true_scroll[1] - 98)
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    end_time = time.time() - start_time
    display.fill((52, 235, 155))
        #-------mouse handling stuff------------------------------------------------------------------------
    mx, my = pygame.mouse.get_pos()
    game_mx = int(mx/3)
    game_my = int(my/3)
    #------- tile rendering ----------------------------------------------------------------------------
    tile_rects = []
    for y in range(3):
        for x in range(4):
            target_x = x - 1 + int(round(scroll[0]/(CHUNK_SIZE*16)))
            target_y = y - 1 + int(round(scroll[1]/(CHUNK_SIZE*16)))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in game_map:
                chunk_map[target_chunk] = generate_chunk(target_x,target_y)
            for tile in chunk_map[target_chunk]:
                display.blit(blue_tile[tile[1]],(tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1]+64))
                if tile[1] in [1,2]:
                    tile_rects.append(pygame.Rect(tile[0][0]*16,tile[0][1]*16+64,16,16))
    #------- movement stuff-----------------------------------------------------------------------------
    player_movement = [0,0]
    if player.moving_right == True:
        player_movement[0] += 4
    if player.moving_left == True:
        player_movement[0] -= 4
    player_movement[1] += player.vertical_momentum
    player.vertical_momentum += 0.5
    if player.vertical_momentum > 4:
        player.vertical_momentum = 4

    if player_movement[0] == 0:
        player.set_action('idle')
    if player_movement[0] > 0:
        player.set_flip(False)
        player.set_action('run')
    if player_movement[0] < 0:
        player.set_flip(True)
        player.set_action('run')
    # ----- colisions-----------------------------------------------------------------------------------
    collision_types = player.move(player_movement, tile_rects)

    if collision_types['bottom'] == True:
        player.air_timer = 0
        player.vertical_momentum = 0
        vertical_momentum_mode = 3
    else:
        player.air_timer += 1
    
    #------sword handling-------------------------------------------------------------------------------
    sword.pos[0] = player.x - scroll[0]
    sword.pos[1] = player.y - scroll[1]
    #----- pygame events--------------------------------------------------------------------------------    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                player.moving_left = True
            if event.key == K_RIGHT:
                player.moving_right = True
            if event.key == K_UP:
                if player.air_timer < 12:
                    player.vertical_momentum = -10
                    jump_sound.play()
        if event.type == KEYUP:
            if event.key == K_LEFT:
                player.moving_left = False
            if event.key == K_RIGHT:
                player.moving_right = False

    #----display rendering stuff------------------------------------------------------------------------

    player.display(display,scroll)
    player.change_frame(1)
    cursor.render(display, [mx, my])
    try:
        display.blit(pygame.transform.rotate(sword.img, meassure_angle(sword.pos[0]-mx, sword.pos[1]-my)), (sword.pos[0], sword.pos[1]))
    except TypeError:
        print(errors)
        errors += 1
    screen.blit(pygame.transform.scale(display,screen_size),(0,0))
    clock.tick(60)  
    pygame.display.update()