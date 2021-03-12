import pygame,sys,random,time,os
import data.engine as e
#-----tons of variables
#pygame initialization etc.
pygame.init()
clock = pygame.time.Clock()
screen_size = (700,500)
screen = pygame.display.set_mode(screen_size,0,32)
display = pygame.Surface((250,183))
#------ loading images, camera etc.
e.load_animations('data/images/entities/')
player = e.entity(256,196,16,16,'player')
# skurboll = e.entity(128,196,16,16,'skurboll')
player.moving_left = False
player.moving_right = False
true_scroll = [0,0]
scroll_strength = 20
camera_x = 100
camera_x_modify = 100
camera_y = 90
vertical_momentum_mode = 3
powerup_object = e.entity(128,184,8,8,'powerup_object')

game_map = e.load_map('data/images/tile_maps/map')
player.vertical_momentum = 0
player.air_timer = 0
# ---- tile indeses etc.
Gras_tile = {1: pygame.image.load('data/images/tile_maps/Gras_tiles/Gras_tiles_0.png'),
             2: pygame.image.load('data/images/tile_maps/Gras_tiles/Gras_tiles_1.png'),
             3: pygame.image.load('data/images/tile_maps/Gras_tiles/Gras_tiles_2.png'),
             4: pygame.image.load('data/images/tile_maps/Gras_tiles/Gras_tiles_3.png'),
             5: pygame.image.load('data/images/tile_maps/Gras_tiles/Gras_tiles_4.png'),
             6: pygame.image.load('data/images/tile_maps/Gras_tiles/Gras_tiles_5.png'),
             7: pygame.image.load('data/images/tile_maps/Gras_tiles/Gras_tiles_6.png'),
             8: pygame.image.load('data/images/tile_maps/Gras_tiles/Gras_tiles_7.png'),
             9: pygame.image.load('data/images/tile_maps/Gras_tiles/Gras_tiles_8.png')}
blue_tile = {1: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_0.png'),
             2: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_1.png'),
             3: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_2.png'),
             4: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_3.png'),
             5: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_4.png'),
             6: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_5.png'),
             7: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_6.png'),
             8: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_7.png'),
             9: pygame.image.load('data/images/tile_maps/blue_tiles/blue_tile_8.png')}
#----- sounds
jump_sound = pygame.mixer.Sound('data/sounds/jump_sound.wav')
pygame.mixer.music.load('data/sounds/music.wav')
pygame.mixer.music.play(-1)
# ---- chunk generation
CHUNK_SIZE = 8

def generate_chunk(x,y):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0 # nothing
            if target_y > 10:
                tile_type = 5 # dirt
            elif target_y == 10:
                tile_type = 2 # grass
            if tile_type != 0:
                chunk_data.append([[target_x,target_y],tile_type])
    return chunk_data
chunk_map = {}
# --- mainloop
while True:
    display.fill((52, 235, 155))
    # ----- scrolling
    true_scroll[0] += (player.x - true_scroll[0] - camera_x) / scroll_strength
    true_scroll[1] += (player.y - true_scroll[1] - camera_y) / scroll_strength
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    #------- tile rendering
    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile =='1':
                display.blit(blue_tile[1], (x*16-scroll[0],y*16-scroll[1]))
            if tile =='2':
                display.blit(blue_tile[2], (x*16-scroll[0],y*16-scroll[1]))
            if tile =='3':
                display.blit(blue_tile[3], (x*16-scroll[0],y*16-scroll[1]))
            if tile =='4':
                display.blit(blue_tile[4], (x*16-scroll[0],y*16-scroll[1]))
            if tile =='5':
                display.blit(blue_tile[5], (x*16-scroll[0],y*16-scroll[1]))
            if tile =='6':
                display.blit(blue_tile[6], (x*16-scroll[0],y*16-scroll[1]))
            if tile =='7':
                display.blit(blue_tile[7], (x*16-scroll[0],y*16-scroll[1]))
            if tile =='8':
                display.blit(blue_tile[8], (x*16-scroll[0],y*16-scroll[1]))
            if tile =='9':
                display.blit(blue_tile[9], (x*16-scroll[0],y*16-scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x*16,y*16,16,16))
            x += 1
        y += 1
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
    #------- movement stuff
    player_movement = [0,0]
    if player.moving_right == True:
        player_movement[0] += 2
        player.x += 2
    if player.moving_left == True:
        player_movement[0] -= 2
        player.x -= 2
    player_movement[1] += player.vertical_momentum
    player.vertical_momentum += 0.5
    if player.vertical_momentum > vertical_momentum_mode:
        player.vertical_momentum = vertical_momentum_mode

    if player_movement[0] == 0:
        player.set_action('idle')
    if player_movement[0] > 0:
        player.set_flip(False)
        player.set_action('run')
    if player_movement[0] < 0:
        player.set_flip(True)
        player.set_action('run')

    collision_types = player.move(player_movement, tile_rects)
    if player.obj.rect.colliderect(powerup_object.obj.rect):
    	player.vertical_momentum = -10
    	vertical_momentum_mode = 0.2
    	jump_sound.play()

    if collision_types['bottom'] == True:
        player.air_timer = 0
        player.vertical_momentum = 0
        vertical_momentum_mode = 3
    else:
        player.air_timer += 1
    #----- pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.moving_left = True
            if event.key == pygame.K_RIGHT:
                player.moving_right = True
            if event.key == pygame.K_UP:
                if player.air_timer < 12:
                    player.vertical_momentum = -10
                    jump_sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.moving_left = False
            if event.key == pygame.K_RIGHT:
                player.moving_right = False
    #----display rendering stuff
    if player.y == 224 or player.y == 224.5:
        camera_y = 150
    else:
        camera_y = 90 
    if player.x < camera_x_modify:
    	camera_x = 0
    	scroll_strength = 8
    else:
    	camera_x = camera_x_modify
    	scroll_strength = 20
    player.display(display,scroll)
    powerup_object.display(display,scroll)
    powerup_object.change_frame(1)
    player.change_frame(1)
    screen.blit(pygame.transform.scale(display,screen_size),(0,0))
    clock.tick(60)  
    pygame.display.update()
