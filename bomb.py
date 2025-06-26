import pygame
from game_map import MAP

class Bomb:
    def __init__(self, x, y, bomb_id, explosion_range, owner):
        self.x = int(x)
        self.y = int(y)
        self.bomb_id = bomb_id
        self.timer = 3
        self.explosion_duration = 0.5
        self.exploded = False
        self.explosion_time = 0
        self.explosion_range = explosion_range
        self.owner = owner

    def update(self, dt):
        if not self.exploded:
            self.timer -= dt
            if self.timer <= 0:
                self.explode()
                self.exploded = True
                self.explosion_time = self.explosion_duration
        else:
            self.explosion_time -= dt

    def explode(self):
        affected_grids = []
        for dx in range(0, self.explosion_range + 1):
            nx, ny = self.x + dx, self.y
            if 0 <= nx < len(MAP[0]) and 0 <= ny < len(MAP):
                if MAP[ny][nx] == 1:
                    break
                affected_grids.append((nx, ny))
            else:
                break
        for dx in range(-1, -self.explosion_range - 1, -1):
            nx, ny = self.x + dx, self.y
            if 0 <= nx < len(MAP[0]) and 0 <= ny < len(MAP):
                if MAP[ny][nx] == 1:
                    break
                affected_grids.append((nx, ny))
            else:
                break
        for dy in range(0, self.explosion_range + 1):
            nx, ny = self.x, self.y + dy
            if 0 <= nx < len(MAP[0]) and 0 <= ny < len(MAP):
                if MAP[ny][nx] == 1:
                    break
                affected_grids.append((nx, ny))
            else:
                break
        for dy in range(-1, -self.explosion_range - 1, -1):
            nx, ny = self.x, self.y + dy
            if 0 <= nx < len(MAP[0]) and 0 <= ny < len(MAP):
                if MAP[ny][nx] == 1:
                    break
                affected_grids.append((nx, ny))
            else:
                break
        for nx, ny in affected_grids:
            if MAP[ny][nx] == 2:
                MAP[ny][nx] = 0
                print(f"Bom meledak dan menghancurkan kotak merah di ({nx}, {ny})")
            else:
                print(f"Bom meledak di ({nx}, {ny}), tidak ada kotak merah.")

    def draw(self, screen):
        GRID_SIZE = 40
        if not self.exploded:
            pygame.draw.circle(screen, (255, 0, 0), (self.x * GRID_SIZE + GRID_SIZE // 2, self.y * GRID_SIZE + GRID_SIZE // 2), 10)
        else:
            from game_map import get_explosion_grids
            affected_grids = get_explosion_grids(self)
            for nx, ny in affected_grids:
                pygame.draw.rect(screen, (255, 255, 0), (nx * GRID_SIZE, ny * GRID_SIZE, GRID_SIZE, GRID_SIZE))