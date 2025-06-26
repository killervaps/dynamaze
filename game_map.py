import pygame

MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,2,0,0,2,0,2,0,0,2,0,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
    [1,2,0,2,0,2,0,2,0,2,0,2,0,2,1],
    [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
    [1,0,0,2,0,0,2,0,2,0,0,2,0,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
    [1,2,0,2,0,2,0,2,0,2,0,2,0,2,1],
    [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
    [1,0,0,2,0,0,2,0,2,0,0,2,0,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
    [1,2,0,2,0,2,0,2,0,2,0,2,0,2,1],
    [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
    [1,0,0,2,0,0,2,0,2,0,0,2,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

def draw_map(screen):
    GRID_SIZE = 40
    for y, row in enumerate(MAP):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, (128, 128, 128), (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif cell == 2:
                pygame.draw.rect(screen, (255, 0, 0), (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def get_explosion_grids(bomb):
    affected_grids = []
    for dx in range(0, bomb.explosion_range + 1):
        nx, ny = bomb.x + dx, bomb.y
        if 0 <= nx < len(MAP[0]) and 0 <= ny < len(MAP):
            if MAP[ny][nx] == 1:
                break
            affected_grids.append((nx, ny))
        else:
            break
    for dx in range(-1, -bomb.explosion_range - 1, -1):
        nx, ny = bomb.x + dx, bomb.y
        if 0 <= nx < len(MAP[0]) and 0 <= ny < len(MAP):
            if MAP[ny][nx] == 1:
                break
            affected_grids.append((nx, ny))
        else:
            break
    for dy in range(0, bomb.explosion_range + 1):
        nx, ny = bomb.x, bomb.y + dy
        if 0 <= nx < len(MAP[0]) and 0 <= ny < len(MAP):
            if MAP[ny][nx] == 1:
                break
            affected_grids.append((nx, ny))
        else:
            break
    for dy in range(-1, -bomb.explosion_range - 1, -1):
        nx, ny = bomb.x, bomb.y + dy
        if 0 <= nx < len(MAP[0]) and 0 <= ny < len(MAP):
            if MAP[ny][nx] == 1:
                break
            affected_grids.append((nx, ny))
        else:
            break
    return affected_grids