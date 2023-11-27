import pygame
import time 
import numpy as np
import random

pygame.init()
WIDTH, HEIGHT = 500, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
ALIVE_COLOR = (255, 255, 255)
DEATH_COLOR = (0,0,0)
pygame.display.set_caption('Conway\'s Game Of Life')
TILE_SIZE = 20
WIDTH_GRID = WIDTH // TILE_SIZE
HEIGHT_GRID = HEIGHT // TILE_SIZE
BROWN   = (160, 82, 45)
FPS = 60
keys = pygame.key.get_pressed()
clock = pygame.time.Clock()

def adjust_grid(positions):
    all_neighbors = set()
    new_positions = set()

    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) in [2, 3]:
            new_positions.add(position)
    
    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) == 3:
            new_positions.add(position)
    
    return new_positions

def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx > WIDTH_GRID:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy > HEIGHT_GRID:
                continue
            if dx == 0 and dy == 0:
                continue

            neighbors.append((x + dx, y + dy))
    
    return neighbors
def grid(positions):
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(WIN, ALIVE_COLOR, (*top_left, TILE_SIZE, TILE_SIZE))
        
    for row in range(HEIGHT_GRID):
        pygame.draw.line(WIN, BROWN, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))
        
    for col in range(WIDTH_GRID):
        pygame.draw.line(WIN, BROWN, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))

def gen(num):
    return set([(random.randrange(0, HEIGHT_GRID), random.randrange(0, WIDTH_GRID)) for _ in range(num)])

def draw_window():
    WIN.fill(DEATH_COLOR)
def main():
    positions = set()
    playing = False

    run = True
    count = 0
    update_freq = 120

    positions = set()
    while run:
        clock.tick(FPS)

        if playing:
            count += 1
        
        if count >= update_freq:
            count = 0
            positions = adjust_grid(positions)

        pygame.display.set_caption("Playing" if playing else "Paused")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)
            elif event.type == pygame.MOUSEBUTTONUP:
                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing
                
                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0
                
                if event.key == pygame.K_g:
                    positions = gen(random.randrange(2, 5) * WIDTH_GRID)



        

                    
                    
        draw_window()
        grid(positions)
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    main()
    
    
    
