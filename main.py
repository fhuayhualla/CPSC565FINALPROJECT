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
lane_reservations = {}
aggressive_car_count = 0
normal_car_count = 0
passive_car_count = 0

preferred_color = 'balanced'
car_preference_active = False
schelling_active = False


class Car:
    def __init__(self, x, y, speed, color):
        self.x = x
        self.y = y
        self.base_speed = speed
        self.current_speed = speed
        self.color = color
        self.target_y = y
        self.is_changing_lanes = False
        if color == 'red':
            self.lane_change_cooldown_max = 120
        elif color == 'yellow':
            self.lane_change_cooldown_max = 180
        else:
            self.lane_change_cooldown_max = 240
        self.lane_change_cooldown = 0
        self.car_surface = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
        self.draw_car_details()


    def draw_car_details(self):
        pygame.draw.rect(self.car_surface, pygame.Color(self.color), (0, 0, CAR_WIDTH, CAR_HEIGHT))
        wheel_color = (0, 0, 0)
        pygame.draw.circle(self.car_surface, wheel_color, (10, 5), 5)
        pygame.draw.circle(self.car_surface, wheel_color, (CAR_WIDTH - 10, 5), 5)
        pygame.draw.circle(self.car_surface, wheel_color, (10, CAR_HEIGHT - 5), 5)
        pygame.draw.circle(self.car_surface, wheel_color, (CAR_WIDTH - 10, CAR_HEIGHT - 5), 5)
        window_color = (200, 200, 255)
        pygame.draw.rect(self.car_surface, window_color, (5, 3, CAR_WIDTH - 10, CAR_HEIGHT / 3))

    def draw(self):
        screen.blit(self.car_surface, (self.x, self.y - CAR_HEIGHT // 2))

    def adjust_speed(self, other_cars):
        safe_distance = 150 if self.color == 'green' else 120 if self.color == 'yellow' else 100
        buffer_distance = 10
        min_distance = float('inf')
        for other in other_cars:
            if self.y == other.y and other.x > self.x:
                distance = other.x - self.x
                if distance < min_distance:
                    min_distance = distance
        if min_distance < safe_distance + buffer_distance:
            self.current_speed = max(1, self.current_speed - 2)
        else:
            self.current_speed = self.base_speed

    def move(self):
        global aggressive_car_count, normal_car_count, passive_car_count

        self.x += self.current_speed
        if self.x > SCREEN_WIDTH:
            self.x = -CAR_WIDTH
            if self.color == 'red':
                aggressive_car_count += 1
            elif self.color == 'yellow':
                normal_car_count += 1
            elif self.color == 'green':
                passive_car_count += 1
        if self.x > SCREEN_WIDTH:
            self.x = -CAR_WIDTH
        if self.y != self.target_y:
            vertical_step = 2 if self.target_y > self.y else -2
            self.y += vertical_step
            if abs(self.target_y - self.y) < 2:
                self.y = self.target_y
                self.is_changing_lanes = False
        if self.lane_change_cooldown > 0:
            self.lane_change_cooldown -= 1


class Button:
    def __init__(self, x, y, width, height, text, action=None, dropdown_items=None, active_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.active_color = active_color if active_color else BUTTON_COLOR
        self.clicked = False
        self.dropdown = dropdown_items is not None
        self.dropdown_items = dropdown_items if dropdown_items else []
        self.show_dropdown = False

    def draw(self, active=False):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
                if self.dropdown:
                    self.show_dropdown = not self.show_dropdown
            elif pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        if active:
            color = self.active_color if self.active_color else BUTTON_HOVER_COLOR
        else:
            color = BUTTON_HOVER_COLOR if self.rect.collidepoint(pos) else BUTTON_COLOR

        pygame.draw.rect(screen, color, self.rect)
        text_img = font.render(self.text, True, TEXT_COLOR)
        screen.blit(text_img, (self.rect.x + 20, self.rect.y + 10))

        if self.show_dropdown:
            for item in self.dropdown_items:
                item.draw()

        return action


setup_button = Button(50, 50, 100, 50, 'Setup')


go_button = Button(200, 50, 100, 50, 'Go')
lane_buttons = [Button(400 + i * 110, 20, 100, 30, f'{n} Lanes') for i, n in enumerate([3, 5, 7])]

def set_preference(color):
    global preferred_color
    preferred_color = color
    create_cars()
    car_pref_button.show_dropdown = False

car_pref_button = Button(800, 80, 150, 50, 'Car Preferences', dropdown_items=[
    Button(800, 130, 150, 50, 'More Red Cars', action=lambda: set_preference('More Red Cars')),
    Button(800, 180, 150, 50, 'More Yellow Cars', action=lambda: set_preference('More Yellow Cars')),
    Button(800, 230, 150, 50, 'More Green Cars', action=lambda: set_preference('More Green Cars'))
])

def toggle_schelling_mode():
    global schelling_active
    schelling_active = not schelling_active
schelling_button = Button(510, 70, 100, 30, 'Schelling', action=toggle_schelling_mode,active_color=(0, 255, 0))




running = True
simulation_active = False
num_lanes = 3
cars = []


def create_cars():
    global cars, num_lanes, preferred_color
    cars.clear()
    lane_height = (SCREEN_HEIGHT - ROAD_TOP) / num_lanes
    color_choices = {
        'More Red Cars': ['red'] * 5 + ['yellow'] + ['green'],
        'More Yellow Cars': ['yellow'] * 5 + ['red'] + ['green'],
        'More Green Cars': ['green'] * 5 + ['red'] + ['yellow'],
        'balanced': ['red', 'yellow', 'green']
    }
    selected_colors = color_choices.get(preferred_color, ['red', 'yellow', 'green'])

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
            color = random.choice(selected_colors)
            speed = 4 if color == 'red' else (3 if color == 'yellow' else 2)
            car = Car(x, y, speed, color)
            cars.append(car)
            last_x = x

def create_balanced_cars():
    global cars, num_lanes
    cars.clear()
    lane_height = (SCREEN_HEIGHT - ROAD_TOP) / num_lanes

    color_choices = ['red', 'yellow', 'green']
    num_colors = len(color_choices)
    color_index = 0

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
            color = color_choices[color_index]
            color_index = (color_index + 1) % num_colors
            speed = 4 if color == 'red' else (3 if color == 'yellow' else 2)
            car = Car(x, y, speed, color)
            cars.append(car)
            last_x = x

setup_button.action = create_balanced_cars

def apply_schelling_sort():
    global cars, num_lanes
    if not schelling_active:
        return

    sorted_cars = sorted(cars, key=lambda x: -x.base_speed)
    cars_per_lane = len(sorted_cars) // num_lanes

    for i, car in enumerate(sorted_cars):
        lane_index = i // cars_per_lane
        lane_index = min(lane_index, num_lanes - 1)
        lane_height = (SCREEN_HEIGHT - ROAD_TOP) / num_lanes
        car.target_y = ROAD_TOP + (lane_index + 0.5) * lane_height


def move_cars():
    global cars, num_lanes, lane_reservations
    lane_height = (SCREEN_HEIGHT - ROAD_TOP) / num_lanes
    sorted_cars = sorted(cars, key=lambda c: (c.y, c.x))

    apply_schelling_sort()

    for lane in list(lane_reservations.keys()):
        lane_reservations[lane] -= 1
        if lane_reservations[lane] <= 0:
            del lane_reservations[lane]

    for car in sorted_cars:
        car.adjust_speed(sorted_cars)
        if not car.is_changing_lanes and car.lane_change_cooldown == 0:
            current_lane_index = int((car.y - ROAD_TOP) / lane_height)
            possible_lanes = []
            if current_lane_index > 0:
                possible_lanes.append(current_lane_index - 1)
            if current_lane_index < num_lanes - 1:
                possible_lanes.append(current_lane_index + 1)

            min_distance_current_lane = float('inf')
            for other in sorted_cars:
                if other.y == car.y and other.x > car.x:
                    distance = other.x - car.x
                    if distance < min_distance_current_lane:
                        min_distance_current_lane = distance

            for new_lane in possible_lanes:
                new_y = ROAD_TOP + (new_lane + 0.5) * lane_height
                projected_safe = True
                min_distance_new_lane = float('inf')
                for other in sorted_cars:
                    if other != car and abs(other.y - new_y) < 5:
                        projected_other_x = other.x + other.current_speed
                        projected_car_x = car.x + car.current_speed
                        distance = abs(projected_other_x - projected_car_x)
                        if distance < 100:
                            projected_safe = False
                            break
                        if distance < min_distance_new_lane:
                            min_distance_new_lane = distance

                if new_lane not in lane_reservations and projected_safe and min_distance_new_lane > min_distance_current_lane:
                    car.target_y = new_y
                    car.is_changing_lanes = True
                    car.lane_change_cooldown = car.lane_change_cooldown_max
                    lane_reservations[new_lane] = 60
                    break

        car.move()

def draw_car_counts():
    aggressive_text = font.render(f'Aggressive: {aggressive_car_count}', True, TEXT_COLOR)
    normal_text = font.render(f'Normal: {normal_car_count}', True, TEXT_COLOR)
    passive_text = font.render(f'Passive: {passive_car_count}', True, TEXT_COLOR)
    screen.blit(aggressive_text, (800, 10))
    screen.blit(normal_text, (800, 30))
    screen.blit(passive_text, (800, 50))


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
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if car_pref_button.rect.collidepoint(event.pos):
                car_pref_button.clicked = True
                car_pref_button.show_dropdown = not car_pref_button.show_dropdown
            elif car_pref_button.show_dropdown:
                for item in car_pref_button.dropdown_items:
                    if item.rect.collidepoint(event.pos):
                        item.action()

    if car_pref_button.draw():
        if not car_pref_button.show_dropdown:
            create_cars()

    if setup_button.draw():
        setup_button.action()
        simulation_active = False
        aggressive_car_count = 0
        normal_car_count = 0
        passive_car_count = 0

    if go_button.draw():
        simulation_active = not simulation_active

    if schelling_button.draw(active=schelling_active):
        schelling_button.action()

    for button in lane_buttons:
        if button.draw():
            num_lanes = int(button.text.split()[0])
            create_cars()
            simulation_active = False

    if simulation_active:
        move_cars()

    draw_cars()
    draw_car_counts()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()