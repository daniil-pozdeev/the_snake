from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject():
    """Базовый класс."""

    def __init__(
            self,
            position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            body_color=BOARD_BACKGROUND_COLOR
    ):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод, определяющий, как объект будет отрисовываться на экране."""
        pass


class Snake(GameObject):
    """Класс описывающий змейку и её поведение."""

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
        """Метод, обновляющий направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, обновляющий позицию змейки."""
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
        """Метод, отрисовывающий змейку на экране."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Метод, возвращающий позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод, сбрасывающий змейку в начальное состояние."""
        self.length = 1
        self.direction = RIGHT
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.next_direction = None


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним."""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color=body_color)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Метод, устанавливающий случайное положение яблока на поле."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)
        return self.position

    def draw(self):
        """Метод, отрисовывающий яблоко на игровой поверхности."""
        rect = (pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Функция, обрабатывающая нажатия клавиш."""
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
    """Основной цикл игры."""
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

