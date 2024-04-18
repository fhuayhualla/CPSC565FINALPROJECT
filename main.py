import pygame
import sys
import random


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
BUTTON_COLOR = (100, 200, 255)
BUTTON_HOVER_COLOR = (100, 100, 255)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 20
CAR_COLORS = ['red', 'yellow', 'green']
CAR_WIDTH = 40
CAR_HEIGHT = 20
ROAD_COLOR = (50, 50, 50)
DASH_COLOR = (255, 255, 255)
DASH_LENGTH = 20
DASH_SPACE = 20
ROAD_TOP = 150


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, FONT_SIZE)


class Car:
    def __init__(self, x, y, speed, color):
        self.x = x
        self.y = y
        self.base_speed = speed
        self.current_speed = speed
        self.color = color
        self.target_y = y
        self.is_changing_lanes = False
        self.lane_change_cooldown = 0

    def adjust_speed(self, other_cars):
        min_distance = float('inf')
        for other in other_cars:
            if self.y == other.y and other.x > self.x:
                distance = other.x - self.x
                if distance < min_distance:
                    min_distance = distance
        if min_distance < 100:
            self.current_speed = max(1, min(self.current_speed, other.current_speed - 1))
        else:
            self.current_speed = self.base_speed

    def move(self):
        self.x += self.current_speed
        if self.x > SCREEN_WIDTH:
            self.x = -CAR_WIDTH
        if self.y != self.target_y:
            vertical_step = 2 if self.target_y > self.y else -2
            self.y += vertical_step
            if abs(self.target_y - self.y) < 2:
                self.y = self.target_y
                self.is_changing_lanes = False
                if self.lane_change_cooldown == 0:
                    self.lane_change_cooldown = 60
        if self.lane_change_cooldown > 0:
            self.lane_change_cooldown -= 1

    def draw(self):
        pygame.draw.rect(screen, pygame.Color(self.color), (self.x, self.y - CAR_HEIGHT // 2, CAR_WIDTH, CAR_HEIGHT))

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



setup_button = Button(50, 50, 100, 50, 'Setup')
go_button = Button(200, 50, 100, 50, 'Go')
lane_buttons = [Button(400 + i * 110, 50, 100, 50, f'{n} Lanes') for i, n in enumerate([3, 5, 7])]


running = True
simulation_active = False
num_lanes = 3
cars = []


def create_cars():
    global cars, num_lanes
    cars.clear()
    lane_height = (SCREEN_HEIGHT - ROAD_TOP) / num_lanes

    for lane in range(num_lanes):
        y = ROAD_TOP + (lane + 0.5) * lane_height
        last_x = 50
        while True:
            next_min_x = last_x + 100
            next_max_x = min(SCREEN_WIDTH - 50, next_min_x + 200)
            if next_min_x >= SCREEN_WIDTH - 50:
                break
            if next_min_x > next_max_x:
                break
            x = random.randint(next_min_x, next_max_x)
            color = random.choice(CAR_COLORS)
            speed = 4 if color == 'red' else (3 if color == 'yellow' else 2)
            car = Car(x, y, speed, color)
            cars.append(car)
            last_x = x





def move_cars():
    global cars, num_lanes
    lane_height = (SCREEN_HEIGHT - ROAD_TOP) / num_lanes
    sorted_cars = sorted(cars, key=lambda c: (c.y, c.x))

    for i, car in enumerate(sorted_cars):
        car.adjust_speed(sorted_cars)
        if not car.is_changing_lanes and car.lane_change_cooldown == 0:
            for other in sorted_cars:
                if other.y == car.y and 0 < other.x - car.x < 80 and other.current_speed < car.base_speed:
                    possible_lanes = [l for l in range(num_lanes) if l != int((car.y - ROAD_TOP) / lane_height)]
                    for new_lane in possible_lanes:
                        new_y = ROAD_TOP + (new_lane + 0.5) * lane_height
                        if all(not (abs(other.y - new_y) < 5 and abs(other.x - car.x) < CAR_WIDTH + 50) for other in sorted_cars):
                            car.target_y = new_y
                            break

        car.move()



def draw_cars():
    for car in cars:
        car.draw()


def draw_road():
    pygame.draw.rect(screen, ROAD_COLOR, (0, ROAD_TOP, SCREEN_WIDTH, SCREEN_HEIGHT - ROAD_TOP))

    lane_height = (SCREEN_HEIGHT - ROAD_TOP) / num_lanes

    for lane in range(1, num_lanes):
        y = ROAD_TOP + lane * lane_height
        for x in range(0, SCREEN_WIDTH, DASH_LENGTH + DASH_SPACE):
            pygame.draw.rect(screen, DASH_COLOR, (x, y - 2, DASH_LENGTH, 4))


while running:
    screen.fill((30, 30, 30))

    draw_road()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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

pygame.quit()
sys.exit()

