import pygame
from pygame.locals import *


pygame.init()


clock = pygame.time.Clock()
fps = 60

screen_width = 1080
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Super Mining")

#define game variables
tile_size = 40 
main_menu = True

pygame.mixer.init()
background_music = pygame.mixer.Sound('audio/114 Surat An-Nas.mp3')
background_music.play(-1)

icon = pygame.image.load("img/logogame.png")
pygame.display.set_icon(icon)

menu_bg_img = pygame.image.load('img/menu_background.png')
bg_img = pygame.image.load('img/background.png')

in_menu = True

start_img = pygame.image.load('img/start.png')
setting_img = pygame.image.load('img/setting.png')

exit_img = pygame.image.load('img/exit.png')


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = None
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked :
                self.clicked = True
                action = "click"
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        screen.blit(self.image, self.rect)

        return action



class Player():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.score = 0
        self.gravity = 0.8
        self.jump_velocity = -18
        

        for num in range(1, 4):
            img_right = pygame.image.load(f"img/char{num}.png")
            img_right = pygame.transform.scale(img_right, (30, 50))
            img_left  = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.jump_count = 0
        self.on_ground = True
        

    def handle_collision(self, tile_type):
        if tile_type == 1:
            self.score += 10

    def update(self):
        dx = 0
        dy = 0
        walk_cooldown = 5
        
    
        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE] and self.jump_count < 2 and self.on_ground:
            self.vel_y = self.jump_velocity
            self.jumped = True
            self.jump_count += 1
            self.on_ground = False

        if not key[pygame.K_SPACE]:
            self.jumped = False

        if key[pygame.K_SPACE] == False:
            self.jumped = False

        if key[pygame.K_LEFT]:
            dx -= 3
            self.counter += 1
            self.direction = -1

        if key[pygame.K_RIGHT]:
            dx += 3
            self.counter += 1
            self.direction = 1
        if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False :
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]



        self.counter += 1
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]



        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y


        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0



            if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):
                tile_type = world.get_tile_type(tile)
                self.handle_collision(tile_type)
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                    self.jump_count = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.jump_count = 0
                    self.on_ground = True



        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.vel_y = 0
            self.jump_count = 0
            self.on_ground =True


        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 1) 



class World():
    def __init__(self, data):
        self.tile_list = []

    

        grass_img = pygame.image.load('img/13.png')
        guitar_img = pygame.image.load('img/12.png')
        laptop_img = pygame.image.load('img/10.png')
        alarm_img = pygame.image.load('img/7.png')
        tas_img = pygame.image.load('img/5.png')
        buku_img = pygame.image.load('img/3.png')
        hp_img = pygame.image.load('img/1.png')
        
    

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 0:
                    pass
                if tile == 1:
                    img = pygame.transform.scale(guitar_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    img = pygame.transform.scale(laptop_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 4:
                    img = pygame.transform.scale(alarm_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 5:
                    img = pygame.transform.scale(tas_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 6:
                    img = pygame.transform.scale(buku_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 7:
                    img = pygame.transform.scale(hp_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    
    def get_tile_type(self, tile):
        x = tile[1].x // tile_size 
        y = tile[1].y // tile_size 
        return world_data[y][x]

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 1)

world_data = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 3, 4, 5, 6, 7, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 2, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0],
        
    ]

level_2_data = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 3, 4, 5, 6, 7, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 2, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0],
        
]

player = Player(50, screen_height - 100)

world = World(world_data)

world_2 = World(level_2_data)

center_x = screen_width // 2.5
button_y = screen_height // 2.5 - 120

start_button = Button(center_x, button_y, start_img)
setting_button = Button(center_x, button_y + 100, setting_img)

exit_button = Button(center_x, button_y + 200, exit_img)

door_img = pygame.image.load('img/pintu.png')
door_rect = door_img.get_rect()
door_rect.x = 1040  # Ganti dengan posisi pintu di layar
door_rect.y = 70   # Ganti dengan posisi pintu di layar

game_started = False
game_over = False
start_time = 0

game_duration = 30



run = True

while run:
    clock.tick(fps)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill((0, 0, 0))

    if in_menu:
        screen.blit(menu_bg_img, (0, 0))
        if exit_button.draw():
            run = False

        if setting_button.draw():
            run = False

        if start_button.draw():
            in_menu = False
            game_started = True
            start_time = current_time
    elif game_over:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        score_text = font.render(f"Your Score: {player.score}", True, (255, 255, 255))
        restart_text = font.render("Click START to play again", True, (255, 255, 255))
        screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2 - 100))
        screen.blit(score_text, (screen_width // 2 - 100, screen_height // 2 - 50))
        screen.blit(restart_text, (screen_width // 2 - 150, screen_height // 2))
        

        if start_button.draw():
            game_over = False
            in_menu = True
            player.score = 0
    else:
        screen.blit(bg_img, (0, 0))
        if game_started:
            # Hitung sisa waktu
            elapsed_time = (current_time - start_time) // 1000  # dalam detik
            remaining_time = game_duration - elapsed_time

            if remaining_time <= 0:
                game_started = False
                in_menu = True
                  
        world.draw() 
        screen.blit(door_img, door_rect)
        player.update()

        font = pygame.font.Font(None, 36)
        text = font.render(f"Time Left: {remaining_time} seconds | Score: {player.score}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

    pygame.display.update()

pygame.quit()