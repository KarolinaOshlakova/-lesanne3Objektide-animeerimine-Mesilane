import pygame
import sys
import random

pygame.init()


light_blue = (173, 216, 230)
gray = (128, 128, 128)
yellow = (255, 255, 0)
brown = (139, 69, 19)
red = (255, 0, 0)
dark_red = (200, 0, 0)

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Autod ja takistused")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)


REDcar_img = pygame.image.load("ppp.png")
REDcar_img = pygame.transform.scale(REDcar_img, (160, 130))
BLcar_img = pygame.image.load("mmm.png")
BLcar_img = pygame.transform.scale(BLcar_img, (160, 130))

def drawRoad():
    pygame.draw.rect(screen, gray, (0, 0, screen_width, screen_height))

    dash_height = 40
    dash_width = 12
    dash_gap = 20
    dash_y = 0
    center_x = screen_width // 2 - dash_width // 2
    while dash_y < screen_height:
        pygame.draw.rect(screen, yellow, (center_x, dash_y, dash_width, dash_height))
        dash_y += dash_height + dash_gap

def show_game_over():
    text = font.render("GAME OVER", True, red)
    screen.blit(text, (screen_width//2 - text.get_width()//2, screen_height//2 - text.get_height()//2))
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()

car_width = 160
car_height = 130
half = screen_width // 2

red_car_x = half // 2 - car_width // 2
blue_car_x = half + half // 2 - car_width // 2
red_car_y = screen_height - car_height - 20
blue_car_y = screen_height - car_height - 160


red_speed_normal = -3
red_speed_slow = -1
red_speed_fast = -5
red_car_speed_y = red_speed_normal

blue_speed_normal = -2
blue_speed_slow = -0.8
blue_speed_fast = -3.5
blue_car_speed_y = blue_speed_normal


red_slowdown_time = 0
red_speedup_time = 0
blue_slowdown_time = 0
blue_speedup_time = 0

obstacle_width = 50
obstacle_height = 25
boost_width = 50
boost_height = 25

obstacles = []
red_boosts = []
blue_boosts = []

def spawn_obstacle(for_red):
    if for_red:
        x = random.randint(10, half - obstacle_width - 10)
    else:
        x = random.randint(half + 10, screen_width - obstacle_width - 10)
    y = random.randint(-600, -100)
    return pygame.Rect(x, y, obstacle_width, obstacle_height)

def spawn_boost(for_red):
    if for_red:
        x = random.randint(10, half - boost_width - 10)
    else:
        x = random.randint(half + 10, screen_width - boost_width - 10)
    y = random.randint(-1000, -300)
    return pygame.Rect(x, y, boost_width, boost_height)

obstacles.append(spawn_obstacle(for_red=True))
obstacles.append(spawn_obstacle(for_red=False))
red_boosts.append(spawn_boost(for_red=True))
blue_boosts.append(spawn_boost(for_red=False))

game_over = False

while not game_over:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and blue_car_x > half:
        blue_car_x -= 5
    if keys[pygame.K_RIGHT] and blue_car_x + car_width < screen_width:
        blue_car_x += 5

    red_car_y += red_car_speed_y
    blue_car_y += blue_car_speed_y


    if red_car_y < -car_height:
        red_car_y = screen_height
    if blue_car_y < -car_height:
        blue_car_y = screen_height

 
    for i in range(len(obstacles)):
        obstacles[i].y += 2
        if obstacles[i].y > screen_height:
            obstacles[i] = spawn_obstacle(for_red=(i == 0))


    for i in range(len(red_boosts)):
        red_boosts[i].y += 2
        if red_boosts[i].y > screen_height:
            red_boosts[i] = spawn_boost(for_red=True)

    for i in range(len(blue_boosts)):
        blue_boosts[i].y += 2
        if blue_boosts[i].y > screen_height:
            blue_boosts[i] = spawn_boost(for_red=False)


    red_rect = pygame.Rect(red_car_x, red_car_y, car_width, car_height)
    blue_rect = pygame.Rect(blue_car_x, blue_car_y, car_width, car_height)

    red_in_obstacle = False
    blue_in_obstacle = False

    for obstacle in obstacles:
        if red_rect.colliderect(obstacle):
            red_car_speed_y = red_speed_slow
            red_slowdown_time = pygame.time.get_ticks()
            red_in_obstacle = True
        if blue_rect.colliderect(obstacle):
            blue_car_speed_y = blue_speed_slow
            blue_slowdown_time = pygame.time.get_ticks()
            blue_in_obstacle = True

    for boost in red_boosts:
        if red_rect.colliderect(boost):
            red_car_speed_y = red_speed_fast
            red_speedup_time = pygame.time.get_ticks()

    for boost in blue_boosts:
        if blue_rect.colliderect(boost):
            blue_car_speed_y = blue_speed_fast
            blue_speedup_time = pygame.time.get_ticks()


    now = pygame.time.get_ticks()
    if not red_in_obstacle and now - red_slowdown_time > 2000 and now - red_speedup_time > 2000:
        red_car_speed_y = red_speed_normal
    if not blue_in_obstacle and now - blue_slowdown_time > 2000 and now - blue_speedup_time > 2000:
        blue_car_speed_y = blue_speed_normal


    if red_rect.colliderect(blue_rect):
        show_game_over()

    screen.fill(light_blue)
    drawRoad()

    for obstacle in obstacles:
        pygame.draw.rect(screen, brown, obstacle)

    for boost in red_boosts + blue_boosts:
        pygame.draw.rect(screen, dark_red, boost)

    screen.blit(REDcar_img, (red_car_x, red_car_y))
    screen.blit(BLcar_img, (blue_car_x, blue_car_y))

    pygame.display.flip()
