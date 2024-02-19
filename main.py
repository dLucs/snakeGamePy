import pygame
import settings
import random

clock = pygame.time.Clock()
screen = pygame.display.set_mode((settings.SCREEN_SIZE, settings.SCREEN_SIZE))


init_game = True
playing = True
food = True

time = None

snake_rect = None
snake_length = None
snake_parts = None
snake_direction = None

food_rect = None


while playing:
    # Generate snake when game starts
    if init_game:
        init_game = False
        time = 0
        # Randomize the starting location of the snake
        snake_rect = pygame.rect.Rect(
            [
                random.randrange(0, settings.SCREEN_SIZE, settings.GRID_SIZE),
                random.randrange(0, settings.SCREEN_SIZE, settings.GRID_SIZE),
                settings.SNAKE_PART,
                settings.SNAKE_PART,
            ]
        )
        snake_length = 1
        snake_parts = []
        snake_direction = pygame.math.Vector2(0, 0)

    # Randomly generate food
    if food:
        food = False
        food_rect = pygame.rect.Rect(
            [
                random.randrange(0, settings.SCREEN_SIZE, settings.GRID_SIZE),
                random.randrange(0, settings.SCREEN_SIZE, settings.GRID_SIZE),
                settings.FOOD_SIZE,
                settings.FOOD_SIZE,
            ]
        )

    # Event listeners
    for event in pygame.event.get():
        # Quitting the game
        if (
            event.type == pygame.QUIT
            or event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            playing = False
        # Controlling the snake
        if event.type == pygame.KEYDOWN:
            if (
                event.key == pygame.K_UP
                or event.key == pygame.K_w
                and not snake_direction[1] > 0
            ):
                snake_direction = pygame.Vector2(0, -settings.SNAKE_MOVE_LENGTH)
            if (
                event.key == pygame.K_DOWN
                or event.key == pygame.K_s
                and not snake_direction[1] < 0
            ):
                snake_direction = pygame.Vector2(0, settings.SNAKE_MOVE_LENGTH)
            if (
                event.key == pygame.K_RIGHT
                or event.key == pygame.K_d
                and not snake_direction[0] < 0
            ):
                snake_direction = pygame.Vector2(settings.SNAKE_MOVE_LENGTH, 0)
            if (
                event.key == pygame.K_LEFT
                or event.key == pygame.K_a
                and not snake_direction[0] > 0
            ):
                snake_direction = pygame.Vector2(-settings.SNAKE_MOVE_LENGTH, 0)
    actual_time = pygame.time.get_ticks()

    # Background and grid creation
    screen.fill(settings.BG_COLOR)

    for i in range(0, settings.SCREEN_SIZE, settings.GRID_SIZE):
        pygame.draw.line(
            screen,
            settings.GRID_COLOR,
            start_pos=(i, 0),
            end_pos=(i, settings.SCREEN_SIZE),
        )
        pygame.draw.line(
            screen,
            settings.GRID_COLOR,
            start_pos=(0, i),
            end_pos=(settings.SCREEN_SIZE, i),
        )

    # Update the snake's position, record the updated position in a list,
    # and manage the length of the snake based on a time condition.
    # The time condition ensures that the snake's position is updated at a certain interval
    if actual_time - time > settings.SPEED:
        time = actual_time
        snake_rect.move_ip(snake_direction)
        snake_parts.append(snake_rect.copy())

        # Simulate the snake's movement and the removal of its tail as it moves forward
        snake_parts = snake_parts[-snake_length:]

    pygame.draw.rect(screen, settings.FOOD_COLOR, food_rect, 0, 10)

    [
        pygame.draw.rect(screen, settings.SNAKE_COLOR, snake_part, 8, 4)
        for snake_part in snake_parts
    ]

    # Game Over
    if (
        # Wall Game Over
        snake_rect.left < 0
        or snake_rect.right > settings.SCREEN_SIZE
        or snake_rect.top < 0
        or snake_rect.bottom > settings.SCREEN_SIZE
        # Snake Game Over, checks whether there are any duplicate centers among the snake parts
        or len(snake_parts) != len(set(snake_part.center for snake_part in snake_parts))
    ):
        init_game = True
        food = True

    # Eating food and growing
    if snake_rect.center == food_rect.center:
        snake_length += 1
        food = True

    pygame.display.flip()

    clock.tick(settings.FPS)


pygame.quit()
