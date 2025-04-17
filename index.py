import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bricks Breaker")

# Clock object to control the frame rate
clock = pygame.time.Clock()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
colors = [red, green, blue, yellow]

# Paddle
paddle_width = 100
paddle_height = 10
paddle_speed = 6
paddle1 = pygame.Rect(screen_width // 2 - paddle_width // 2, screen_height - 40, paddle_width, paddle_height)
paddle2 = pygame.Rect(screen_width // 2 - paddle_width // 2, 30, paddle_width, paddle_height)

# Ball
ball_radius = 10
ball_speed = 5
ball = pygame.Rect(screen_width // 2 - ball_radius // 2, screen_height // 2 - ball_radius // 2, ball_radius * 2, ball_radius * 2)
ball_speed_x = ball_speed * random.choice((1, -1))
ball_speed_y = ball_speed * random.choice((1, -1))

# Bricks
brick_rows = 5
brick_cols = 9
brick_width = 75
brick_height = 30

def create_bricks():
    bricks = [pygame.Rect(i * (brick_width + 10) + 35, j * (brick_height + 10) + 50, brick_width, brick_height) for i in range(brick_cols) for j in range(brick_rows)]
    brick_colors = [random.choice(colors) for _ in range(len(bricks))]
    return bricks, brick_colors

bricks, brick_colors = create_bricks()

# Score
score = 0

# Level
level = 1

# Difficulty
difficulty = 1

# Game mode (1 for single player, 2 for two players)
game_mode = 1

def move_paddle(paddle, left_key, right_key):
    keys = pygame.key.get_pressed()
    if keys[left_key] and paddle.left > 0:
        paddle.left -= paddle_speed
    if keys[right_key] and paddle.right < screen_width:
        paddle.right += paddle_speed

def move_ball():
    global ball_speed_x, ball_speed_y, score, level

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x = -ball_speed_x
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y = -ball_speed_y
    if ball.colliderect(paddle1):
        ball_speed_y = -ball_speed
        ball_speed_x += (ball.centerx - paddle1.centerx) // 10
    if game_mode == 2 and ball.colliderect(paddle2):
        ball_speed_y = ball_speed
        ball_speed_x += (ball.centerx - paddle2.centerx) // 10

    for i, brick in enumerate(bricks[:]):
        if ball.colliderect(brick):
            bricks.remove(brick)
            brick_colors.pop(i)
            ball_speed_y = -ball_speed_y
            score += 1
            if not bricks:
                level += 1
                load_level(level)
            break

def load_level(level):
    global bricks, brick_colors, ball_speed_x, ball_speed_y, ball
    bricks, brick_colors = create_bricks()
    ball.x, ball.y = screen_width // 2 - ball_radius // 2, screen_height // 2 - ball_radius // 2
    ball_speed_x = ball_speed * random.choice((1, -1))
    ball_speed_y = ball_speed * random.choice((1, -1))

def draw_elements():
    screen.fill(black)
    pygame.draw.rect(screen, white, paddle1)
    if game_mode == 2:
        pygame.draw.rect(screen, white, paddle2)
    pygame.draw.ellipse(screen, white, ball)
    for brick, color in zip(bricks, brick_colors):
        pygame.draw.rect(screen, color, brick)
    draw_score()
    pygame.display.flip()

def draw_score():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}  Level: {level}", True, white)
    screen.blit(text, (20, 10))

def check_game_over():
    if ball.bottom >= screen_height or ball.top <= 0:
        return True
    return False

def start_menu():
    global game_mode, level, difficulty
    font = pygame.font.Font(None, 36)

    menu_running = True
    while menu_running:
        screen.fill(black)
        title = font.render("Bricks Breaker", True, white)
        screen.blit(title, (screen_width // 2 - title.get_width() // 2, 100))

        single_player = font.render("1. Single Player", True, white)
        two_players = font.render("2. Two Players", True, white)
        screen.blit(single_player, (screen_width // 2 - single_player.get_width() // 2, 200))
        screen.blit(two_players, (screen_width // 2 - two_players.get_width() // 2, 250))

        level_text = font.render(f"Level: {level}", True, white)
        difficulty_text = font.render(f"Difficulty: {difficulty}", True, white)
        screen.blit(level_text, (screen_width // 2 - level_text.get_width() // 2, 300))
        screen.blit(difficulty_text, (screen_width // 2 - difficulty_text.get_width() // 2, 350))

        instruction = font.render("Press Enter to Start", True, white)
        screen.blit(instruction, (screen_width // 2 - instruction.get_width() // 2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_mode = 1
                elif event.key == pygame.K_2:
                    game_mode = 2
                elif event.key == pygame.K_UP:
                    level += 1
                elif event.key == pygame.K_DOWN:
                    level = max(1, level - 1)
                elif event.key == pygame.K_LEFT:
                    difficulty = max(1, difficulty - 1)
                elif event.key == pygame.K_RIGHT:
                    difficulty += 1
                elif event.key == pygame.K_RETURN:
                    menu_running = False

# Game loop
start_menu()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    move_paddle(paddle1, pygame.K_LEFT, pygame.K_RIGHT)
    if game_mode == 2:
        move_paddle(paddle2, pygame.K_a, pygame.K_d)
    move_ball()

    if check_game_over():
        running = False

    draw_elements()
    clock.tick(60)

pygame.quit()
sys.exit()