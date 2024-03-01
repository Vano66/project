import pygame
import os
import sys


def load_image(name, color_key=None):
    fullname = os.path.join('sprite', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


pygame.init()
size = width, height = 700, 700
screen = pygame.display.set_mode(size)
sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
car_group = pygame.sprite.Group()

tile_image = {'wall': load_image('desert.png'),
              'empty': load_image('road.png'),
              "car_1": load_image("car_1.png"),
              "car_2": load_image("car_2.png")}

player_image = load_image('car4.1.png')

tile_width = tile_height = 100


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Машинки", '',
                  "Движение на левую и правую кнопку мыши"]
    fon = pygame.transform.scale(load_image('fon.jpg'), size)
    screen.blit((fon), (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 500, 500)


class SpriteGroup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for inet in self:
            inet.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_image[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 5, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0], tile_height * self.pos[1] + 5)


class Car(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(car_group)
        self.image = tile_image["car_1"]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 5, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0], tile_height * self.pos[1] + 5)


def move(hero, movement):
    x, y = hero.pos
    if movement == 'up':
        if y > 0 and level_map[y - 1][x] == '.':
            hero.move(x, y - 1)
    elif movement == 'down':
        if y < max_y - 1 and level_map[y + 1][x] == '.':
            hero.move(x, y + 1)
    elif movement == 'left':
        if x > 0 and level_map[y][x - 1] == '.':
            hero.move(x - 1, y)
    elif movement == 'right':
        if x < max_x - 1 and level_map[y][x + 1] == '.':
            hero.move(x + 1, y)


def move_car(car, movement):
    x, y = car.pos
    if movement == 'up':
        if y > 0 and level_map[y - 1][x] == '.':
            car.move(x, y - 1)
    elif movement == 'down':
        if y < max_y - 1 and level_map[y + 1][x] == '.':
            car.move(x, y + 1)
    elif movement == 'left':
        if x > 0 and level_map[y][x - 1] == '.':
            car.move(x - 1, y)
    elif movement == 'right':
        if x < max_x - 1 and level_map[y][x + 1] == '.':
            car.move(x + 1, y)


def load_level(filename):
    filename = 'data/' + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def generate_level(level):
    new_player, x, y, new_car = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '$' and new_car is None:
                new_car = Car(x, y)
                level[y][x] = '.'
    return new_player, x, y, new_car


if __name__ == '__main__':
    player = None
    ranning = True
    start_screen()
    level_map = load_level('field.txt')
    hero, max_x, max_y, car = generate_level(level_map)

    while ranning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ranning = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if hero.rect.collidepoint(pygame.mouse.get_pos()):
                    if event.button == 3:
                        move(hero, 'right')
                    if event.button == 1:
                        move(hero, 'left')
                elif car.rect.collidepoint(pygame.mouse.get_pos()):
                    if event.button == 3:
                        move_car(car, 'up')
                    if event.button == 1:
                        move_car(car, 'down')

        screen.fill(pygame.Color('black'))
        sprite_group.draw(screen)
        hero_group.draw(screen)
        car_group.draw(screen)
        pygame.display.flip()
    pygame.quit()
