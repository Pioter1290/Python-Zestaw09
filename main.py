import sys
import pygame
import tkinter as tk
from tkinter import messagebox
import random
import time

pygame.init()

screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("Snake")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)

clock = pygame.time.Clock()
snake_pos = [100, 50]
snake_body = [[100, 50]]
snake_direction = ''
change_dir = snake_direction
speed = 20
game_over = False
score = 0

apple_pos = [random.randrange(1, 30) * speed, random.randrange(1, 25) * speed]
apple_spawn_time = time.time()

poison_pos = [random.randrange(1, 30) * speed, random.randrange(1, 25) * speed]
poison_apple_active = False
poison_apple_spawn_time = 0
poison_apple_interval = 30

pygame.font.init()
font = pygame.font.SysFont('arial', 35, bold=True)

def game_over_message(score):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("GAME OVER", f"Your Score: {score}")
    root.destroy()

def change_direction():
    global snake_direction, change_dir, game_over
    if change_dir == 'UP' and snake_direction == 'DOWN':
        game_over = True
    elif change_dir == 'DOWN' and snake_direction == 'UP':
        game_over = True
    elif change_dir == 'LEFT' and snake_direction == 'RIGHT':
        game_over = True
    elif change_dir == 'RIGHT' and snake_direction == 'LEFT':
        game_over = True
    else:
        snake_direction = change_dir

def draw_score(score):
    score_surface = font.render(f'Score: {score}', True, WHITE)
    score_rect = score_surface.get_rect(center=(520, 30))
    screen.blit(score_surface, score_rect)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_dir = 'UP'
            elif event.key == pygame.K_DOWN:
                change_dir = 'DOWN'
            elif event.key == pygame.K_LEFT:
                change_dir = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                change_dir = 'RIGHT'

    change_direction()

    if snake_direction == 'UP':
        snake_pos[1] -= speed
    if snake_direction == 'DOWN':
        snake_pos[1] += speed
    if snake_direction == 'LEFT':
        snake_pos[0] -= speed
    if snake_direction == 'RIGHT':
        snake_pos[0] += speed

    snake_body.insert(0, list(snake_pos))

    # Sprawdzenie czy wąż zjadł jablko
    if pygame.Rect(snake_pos[0], snake_pos[1], speed, speed).colliderect(pygame.Rect(apple_pos[0], apple_pos[1], speed, speed)):
        score += 1
        apple_pos = [random.randrange(1, 30) * speed, random.randrange(1, 25) * speed]
        apple_spawn_time = time.time()

    else:
        snake_body.pop()

    # Sprawdzenie czy wąż zjadl zatrute jablko
    if poison_apple_active and pygame.Rect(snake_pos[0], snake_pos[1], speed, speed).colliderect(pygame.Rect(poison_pos[0], poison_pos[1], speed, speed)):
        game_over = True

    # Generowanie jabłka
    if time.time() - apple_spawn_time > 10:
        apple_pos = [random.randrange(1, 30) * speed, random.randrange(1, 25) * speed]
        apple_spawn_time = time.time()


    if not poison_apple_active and time.time() - poison_apple_spawn_time > poison_apple_interval:
        poison_pos = [random.randrange(1, 30) * speed, random.randrange(1, 25) * speed]
        poison_apple_active = True
        poison_apple_spawn_time = time.time()

    if poison_apple_active and time.time() - poison_apple_spawn_time > 10:
        poison_apple_active = False

    if snake_pos[0] <= 0:
        snake_pos[0] = snake_pos[0] + 600
    if snake_pos[0] >= 600:
        snake_pos[0] = snake_pos[0] - 600
    if snake_pos[1] <= 0:
        snake_pos[1] = snake_pos[1] + 500
    if snake_pos[1] >= 500:
        snake_pos[1] = snake_pos[1] - 500

    screen.fill(BLACK)
    for pos in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], speed, speed))

    pygame.draw.rect(screen, RED, pygame.Rect(apple_pos[0], apple_pos[1], speed, speed))

    if poison_apple_active:
        pygame.draw.rect(screen, PURPLE, pygame.Rect(poison_pos[0], poison_pos[1], speed, speed))

    draw_score(score)

    if game_over:
        game_over_message(score)
        break

    pygame.display.update()

    clock.tick(15)

pygame.quit()
sys.exit()
