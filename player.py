import pygame

class Player:
    def __init__(self, x, y, player_id, controls):
        self.x = int(x)
        self.y = int(y)
        self.player_id = player_id
        self.controls = controls
        self.speed = 1
        self.hp = 100
        self.alive = True
        self.damaged_bombs = set()
        self.max_bombs = 1
        self.bomb_cooldown = 0
        self.bomb_cooldown_duration = 2
        self.color = [(255, 255, 255), (255, 100, 100), (100, 255, 100), (100, 100, 255)][player_id]

    def move(self, dx, dy, bombs):
        new_x = self.x + dx
        new_y = self.y + dy
        from game_map import MAP
        if (0 <= new_x < len(MAP[0]) and 0 <= new_y < len(MAP) and 
            MAP[new_y][new_x] == 0 and 
            not any(bomb.x == new_x and bomb.y == new_y and not bomb.exploded for bomb in bombs)):
            self.x = new_x
            self.y = new_y

    def take_damage(self, damage, bomb_id):
        if bomb_id not in self.damaged_bombs:
            self.hp -= damage
            self.damaged_bombs.add(bomb_id)
            print(f"Pemain {self.player_id + 1} terkena damage {damage}, HP tersisa: {self.hp}")
            if self.hp <= 0:
                self.alive = False
                print(f"Pemain {self.player_id + 1} mati!")

    def can_place_bomb(self, active_bombs):
        return len(active_bombs) < self.max_bombs

    def draw(self, screen):
        GRID_SIZE = 40
        if self.alive:
            pygame.draw.rect(screen, self.color, (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, (255, 0, 0), (self.x * GRID_SIZE, self.y * GRID_SIZE - 10, GRID_SIZE, 5))
            pygame.draw.rect(screen, (0, 255, 0), (self.x * GRID_SIZE, self.y * GRID_SIZE - 10, GRID_SIZE * (self.hp / 100), 5))
        else:
            pygame.draw.rect(screen, (100, 100, 100), (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))