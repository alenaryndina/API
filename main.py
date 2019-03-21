import pygame
import requests
import sys
import os


def ll(x, y):
    return "{0},{1}".format(x, y)


class MapParams(object):
    # Параметры по умолчанию.
    def __init__(self):
        self.lat = 52.718552  # Координаты центра карты на старте.
        self.lon = 41.426697
        self.zoom = 10  # Масштаб карты на старте.
        self.type = "map"  # Тип карты на старте.

    def ll(self):
        return ll(self.lon, self.lat)

    def update(self, event):
        if event.key == 280 and self.zoom < 19:  # PG_UP
            self.zoom += 1
        elif event.key == 281 and self.zoom > 2:  # PG_DOWN
            self.zoom -= 1
        elif event.key == 276:  # LEFT
            self.lon -= 0.01 * 2 ** (10 - self.zoom)
        elif event.key == 275:  # RIGHT
            self.lon += 0.01 * 2 ** (10 - self.zoom)
        elif event.key == 273 and self.lat < 85:  # UP
            self.lat += 0.01 * 2 ** (10 - self.zoom)
        elif event.key == 274 and self.lat > -85:  # DOWN
            self.lat -= 0.01 * 2 ** (10 - self.zoom)
        elif event.key == 49:  # map key1
            self.type = "map"
        elif event.key == 50:  # sat key2
            self.type = "sat"
        elif event.key == 51:  # sat,skl key3
            self.type = "sat,skl"
        if self.lon > 180:
            self.lon -= 360
        if self.lon < -180:
            self.lon += 360


def load_map(mp):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=mp.ll(), z=mp.zoom, type=mp.type)

    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return None

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)

    return map_file


def render_text(text):
    font = pygame.font.Font(None, 30)
    return font.render(text, 1, (100, 0, 100))


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))

    mp = MapParams()
    running = True
    map_file = load_map(mp)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                mp.update(event)
                map_file = load_map(mp)
        if map_file:
            screen.blit(pygame.image.load(map_file), (0, 0))

        pygame.display.flip()

    pygame.quit()
    os.remove(map_file)


if __name__ == "__main__":
    main()
