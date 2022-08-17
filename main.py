import pygame
from pygame import mixer
import os
import time
import random
from win32api import GetSystemMetrics
from menu import pause

os.chdir("C:/Users/William/Documents/Clement/Python/Space_Invaders")
pygame.init()
pygame.font.init()

screen_width = GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)

WIDTH, HEIGHT = screen_width - 300, screen_height - 80
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("images", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("images", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("images", "pixel_ship_blue_small.png"))

# Load player spaceship
YELLOW_SHIP = pygame.image.load(os.path.join("images", "pixel_ship_yellow.png"))


# Load laser images
RED_LASER = pygame.image.load(os.path.join("images", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("images", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("images", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("images", "pixel_laser_yellow.png"))

# Load background
background = pygame.transform.scale(pygame.image.load(os.path.join("images", "background-black.png")), (WIDTH, HEIGHT))


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.hit = False
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    COOLDOWN = 30
    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cooldown_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1

    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x,self.y, self.laser_img)
            self.lasers.append(laser)
            self.cooldown_counter = 1

    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x,y,health)
        self.ship_img = YELLOW_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def shoot(self):
        laser_sound = pygame.mixer.Sound('laser.wav')
        laser_sound.play()
        if self.cooldown_counter == 0:
            laser = Laser(self.x,self.y, self.laser_img)
            self.lasers.append(laser)
            self.cooldown_counter = 1

    def move_lasers(self, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(-7)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj) and not laser.hit:
                        obj.health -= 10
                        laser.hit = True
                        if obj.health <= 0:
                            objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)    
        self.healthbar(window)                

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))



class Enemy(Ship):
    COLOR_MAP = {"red":(RED_SPACE_SHIP, RED_LASER), "green": (GREEN_SPACE_SHIP, GREEN_LASER), "blue": (BLUE_SPACE_SHIP, BLUE_LASER)}

    def __init__(self, x, y, color, health):
        super().__init__(x,y,health)
        self.max_health = health
        self.color = color
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y - self.ship_img.get_height(), self.ship_img.get_width(), 10))
        if self.health > 0:
            pygame.draw.rect(window, (0,255,0), (self.x, self.y - self.ship_img.get_height(), self.ship_img.get_width() * (self.health/self.max_health), 10))
        

    def shoot(self):
        if self.cooldown_counter == 0:
            if self.color == "red":
                laser = Laser(self.x -15,self.y, self.laser_img)
            elif self.color == "green":
                laser = Laser(self.x-15, self.y, self.laser_img)
            else:
                laser = Laser(self.x-24, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cooldown_counter = 1



def collide(obj_1, obj_2):
    offset_x = obj_2.x - obj_1.x
    offset_y = obj_2.y - obj_1.y
    return obj_1.mask.overlap(obj_2.mask, (offset_x, offset_y)) != None


def main():
    play = True
    FPS = 60
    level = 0
    count_lives = 5
    main_font = pygame.font.SysFont("comicsans", 40)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    num_enemies = 5
    enemy_vel = 1

    player_velocity = 8
    laser_vel = 5

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw():
        WIN.blit(background, (0,0))

        # put text
        lives_label = main_font.render(f"Lives: {count_lives}", 1, (0,255,0))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WIN.blit(lives_label, (10,10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        
        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You lost!", 1, (255, 255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2 - lost_label.get_height()/2))

        pygame.display.update()

    player = Player(WIDTH / 2 - 50, HEIGHT - 110)

    while play:
        clock.tick(FPS)
        redraw()
        if play:
            if count_lives <= 0 or player.health <= 0:
                lost = True
                lost_count += 1

            if lost:
                if lost_count > FPS * 3:
                    play = False
                else:
                    continue

            if len(enemies) == 0:
                level += 1
                num_enemies += 1
                for i in range(num_enemies):
                    color = random.choice(["red", "blue", "green"])
                    if color == "red":
                        enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), color, 30)
                    elif color == "blue":
                        enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), color, 10)
                    else:
                        enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), color, 20)
                    enemies.append(enemy)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
        
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player.x - player_velocity > 0:
                player.x -= player_velocity
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player.x + player_velocity + player.get_width() < WIDTH:
                player.x += player_velocity
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and player.y - player_velocity > 0:
                player.y -= player_velocity
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and player.y + player_velocity + player.get_height() + 20 < HEIGHT:
                player.y += player_velocity
            if keys[pygame.K_SPACE]:
                player.shoot()
            if keys[pygame.K_p]:
                play = pause(WIN, background)

            for enemy in enemies[:]:
                enemy.move(enemy_vel)
                enemy.move_lasers(laser_vel, player)
                if random.randrange(0, 3 * FPS) == 1:
                    enemy.shoot()
            
                if collide(enemy, player):
                    player.health -= 10
                    enemies.remove(enemy)
                elif enemy.y + enemy.get_height() > HEIGHT:
                    count_lives -= 1
                    enemies.remove(enemy)
        
            player.move_lasers(enemies)
        else:
            quit()



def main_menu():
    title_font = pygame.font.SysFont("comicsans", 60)
    run = True
    while run:
        WIN.blit(background, (0,0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT/2 - title_label.get_height()/2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

if __name__ == "__main__":
    main_menu()