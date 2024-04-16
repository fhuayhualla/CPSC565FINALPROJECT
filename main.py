import pygame
import sys
import random


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
BUTTON_COLOR = (100, 200, 255)
BUTTON_HOVER_COLOR = (100, 100, 255)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 20
CAR_COLORS = ['red', 'green', 'blue', 'yellow', 'purple']
CAR_WIDTH = 40
CAR_HEIGHT = 20
ROAD_COLOR = (50, 50, 50)
DASH_COLOR = (255, 255, 255)
DASH_LENGTH = 20
DASH_SPACE = 20


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, FONT_SIZE)


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.clicked = False

    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
            elif pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        color = BUTTON_HOVER_COLOR if self.rect.collidepoint(pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect)
        text_img = font.render(self.text, True, TEXT_COLOR)
        screen.blit(text_img, (self.rect.x + 20, self.rect.y + 10))
        return action


running = True
simulation_active = False
num_lanes = 3
cars = []

setup_button = Button(50, 50, 100, 50, 'Setup')
go_button = Button(200, 50, 100, 50, 'Go')
lane_buttons = [Button(400 + i * 110, 50, 100, 50, f'{n} Lanes') for i, n in enumerate([3, 5, 7])]


def create_cars():
    global cars, num_lanes
    cars.clear()
    road_top = 150
    lane_height = (SCREEN_HEIGHT - road_top) / num_lanes
    for lane in range(num_lanes):
        y = road_top + (lane + 0.5) * lane_height
        for _ in range(5):
            x = random.randint(50, SCREEN_WIDTH - 50)
            speed = random.randint(1, 5)
            color = random.choice(CAR_COLORS)
            cars.append((x, y, speed, color))


def move_cars():
    for idx, (x, y, speed, color) in enumerate(cars):
        x += speed
        if x > SCREEN_WIDTH:
            x = -CAR_WIDTH
        cars[idx] = (x, y, speed, color)


def draw_cars():
    for x, y, speed, color in cars:
        pygame.draw.rect(screen, pygame.Color(color), (x, y - CAR_HEIGHT // 2, CAR_WIDTH, CAR_HEIGHT))


def draw_road():
    road_top = 150
    pygame.draw.rect(screen, ROAD_COLOR, (0, road_top, SCREEN_WIDTH, SCREEN_HEIGHT - road_top))
    lane_height = (SCREEN_HEIGHT - road_top) / num_lanes
    for lane in range(1, num_lanes):
        y = road_top + lane * lane_height
        for x in range(0, SCREEN_WIDTH, DASH_LENGTH + DASH_SPACE):
            pygame.draw.rect(screen, DASH_COLOR, (x, y - 2, DASH_LENGTH, 4))


while running:
    screen.fill((30, 30, 30))
    draw_road()

    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            running = False

    if setup_button.draw():
        create_cars()
        simulation_active = False

    if go_button.draw():
        simulation_active = not simulation_active

    for button in lane_buttons:
        if button.draw():
            num_lanes = int(button.text.split()[0])
            create_cars()
            simulation_active = False

    if simulation_active:
        move_cars()

    draw_cars()
    pygame.display.flip()
    clock.tick(60)
#test for pycharm
pygame.quit()
sys.exit()
