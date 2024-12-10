from random import randint

import pygame

# РљРѕРЅСЃС‚Р°РЅС‚С‹ РґР»СЏ СЂР°Р·РјРµСЂРѕРІ РїРѕР»СЏ Рё СЃРµС‚РєРё:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# РќР°РїСЂР°РІР»РµРЅРёСЏ РґРІРёР¶РµРЅРёСЏ:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Р¦РІРµС‚ С„РѕРЅР° - С‡РµСЂРЅС‹Р№:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Р¦РІРµС‚ РіСЂР°РЅРёС†С‹ СЏС‡РµР№РєРё
BORDER_COLOR = (93, 216, 228)

# Р¦РІРµС‚ СЏР±Р»РѕРєР°
APPLE_COLOR = (255, 0, 0)

# Р¦РІРµС‚ Р·РјРµР№РєРё
SNAKE_COLOR = (0, 255, 0)

# РЎРєРѕСЂРѕСЃС‚СЊ РґРІРёР¶РµРЅРёСЏ Р·РјРµР№РєРё:
SPEED = 20

# РќР°СЃС‚СЂРѕР№РєР° РёРіСЂРѕРІРѕРіРѕ РѕРєРЅР°:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Р—Р°РіРѕР»РѕРІРѕРє РѕРєРЅР° РёРіСЂРѕРІРѕРіРѕ РїРѕР»СЏ:
pygame.display.set_caption('Р—РјРµР№РєР°')

# РќР°СЃС‚СЂРѕР№РєР° РІСЂРµРјРµРЅРё:
clock = pygame.time.Clock()


class GameObject():
    """Р‘Р°Р·РѕРІС‹Р№ РєР»Р°СЃСЃ."""

    def __init__(
            self,
            position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            body_color=BOARD_BACKGROUND_COLOR
    ):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """РњРµС‚РѕРґ, РѕРїСЂРµРґРµР»СЏСЋС‰РёР№, РєР°Рє РѕР±СЉРµРєС‚ Р±СѓРґРµС‚ РѕС‚СЂРёСЃРѕРІС‹РІР°С‚СЊСЃСЏ РЅР° СЌРєСЂР°РЅРµ."""
        pass


class Snake(GameObject):
    """РљР»Р°СЃСЃ РѕРїРёСЃС‹РІР°СЋС‰РёР№ Р·РјРµР№РєСѓ Рё РµС‘ РїРѕРІРµРґРµРЅРёРµ."""

    def __init__(
            self,
            positions=None,
            length=1,
            body_color=SNAKE_COLOR,
            direction=RIGHT,
            next_direction=None
    ):
        if positions is None:
            positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        super().__init__(body_color=body_color)
        self.positions = positions
        self.length = length
        self.direction = direction
        self.next_direction = next_direction

    def update_direction(self):
        """РњРµС‚РѕРґ, РѕР±РЅРѕРІР»СЏСЋС‰РёР№ РЅР°РїСЂР°РІР»РµРЅРёРµ РґРІРёР¶РµРЅРёСЏ Р·РјРµР№РєРё."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """РњРµС‚РѕРґ, РѕР±РЅРѕРІР»СЏСЋС‰РёР№ РїРѕР·РёС†РёСЋ Р·РјРµР№РєРё."""
        head_x, head_y = self.get_head_position()
        new_head = (head_x + self.direction[0] * GRID_SIZE,
                    head_y + self.direction[1] * GRID_SIZE)
        if new_head[0] < 0:
            new_head = (SCREEN_WIDTH - GRID_SIZE, new_head[1])
        elif new_head[0] >= SCREEN_WIDTH:
            new_head = (0, new_head[1])
        elif new_head[1] < 0:
            new_head = (new_head[0], SCREEN_HEIGHT - GRID_SIZE)
        elif new_head[1] >= SCREEN_HEIGHT:
            new_head = (new_head[0], 0)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """РњРµС‚РѕРґ, РѕС‚СЂРёСЃРѕРІС‹РІР°СЋС‰РёР№ Р·РјРµР№РєСѓ РЅР° СЌРєСЂР°РЅРµ."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """РњРµС‚РѕРґ, РІРѕР·РІСЂР°С‰Р°СЋС‰РёР№ РїРѕР·РёС†РёСЋ РіРѕР»РѕРІС‹ Р·РјРµР№РєРё."""
        return self.positions[0]

    def reset(self):
        """РњРµС‚РѕРґ, СЃР±СЂР°СЃС‹РІР°СЋС‰РёР№ Р·РјРµР№РєСѓ РІ РЅР°С‡Р°Р»СЊРЅРѕРµ СЃРѕСЃС‚РѕСЏРЅРёРµ."""
        self.length = 1
        self.direction = RIGHT
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.next_direction = None


class Apple(GameObject):
    """РљР»Р°СЃСЃ, РѕРїРёСЃС‹РІР°СЋС‰РёР№ СЏР±Р»РѕРєРѕ Рё РґРµР№СЃС‚РІРёСЏ СЃ РЅРёРј."""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color=body_color)
        self.position = self.randomize_position()

    def randomize_position(self):
        """РњРµС‚РѕРґ, СѓСЃС‚Р°РЅР°РІР»РёРІР°СЋС‰РёР№ СЃР»СѓС‡Р°Р№РЅРѕРµ РїРѕР»РѕР¶РµРЅРёРµ СЏР±Р»РѕРєР° РЅР° РїРѕР»Рµ."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)
        return self.position

    def draw(self):
        """РњРµС‚РѕРґ, РѕС‚СЂРёСЃРѕРІС‹РІР°СЋС‰РёР№ СЏР±Р»РѕРєРѕ РЅР° РёРіСЂРѕРІРѕР№ РїРѕРІРµСЂС…РЅРѕСЃС‚Рё."""
        rect = (pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Р¤СѓРЅРєС†РёСЏ, РѕР±СЂР°Р±Р°С‚С‹РІР°СЋС‰Р°СЏ РЅР°Р¶Р°С‚РёСЏ РєР»Р°РІРёС€."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """РћСЃРЅРѕРІРЅРѕР№ С†РёРєР» РёРіСЂС‹."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            apple.randomize_position()
            snake.length += 1
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
