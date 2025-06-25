import asyncio
import platform
import pygame

pygame.init()
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 40
FPS = 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

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

class Player:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.speed = 1
        self.hp = 100
        self.alive = True
        self.damaged_bombs = set()
        self.max_bombs = 1  
        self.bomb_cooldown = 0
        self.bomb_cooldown_duration = 2

    def move(self, dx, dy, bombs):
        new_x = self.x + dx
        new_y = self.y + dy
        if (0 <= new_x < len(MAP[0]) and 0 <= new_y < len(MAP) and 
            MAP[new_y][new_x] == 0 and 
            not any(bomb.x == new_x and bomb.y == new_y and not bomb.exploded for bomb in bombs)):
            self.x = new_x
            self.y = new_y

    def take_damage(self, damage, bomb_id):
        if bomb_id not in self.damaged_bombs:
            self.hp -= damage
            self.damaged_bombs.add(bomb_id)
            print(f"Pemain terkena damage {damage}, HP tersisa: {self.hp}")
            if self.hp <= 0:
                self.alive = False
                print("Pemain mati!")

    def can_place_bomb(self, active_bombs):
        return len(active_bombs) < self.max_bombs

class Bomb:
    def __init__(self, x, y, bomb_id, explosion_range=1):
        self.x = int(x)
        self.y = int(y)
        self.bomb_id = bomb_id
        self.timer = 3
        self.explosion_duration = 0.5
        self.exploded = False
        self.explosion_time = 0
        self.explosion_range = explosion_range

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

player = Player(1, 1)
bombs = []
game_over = False
bomb_counter = 0
game_timer = 0
last_updated_minute = -1
current_explosion_range = 1  

def setup():
    pygame.display.set_caption("Bomb It")

def draw_map():
    for y, row in enumerate(MAP):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, GRAY, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif cell == 2:
                pygame.draw.rect(screen, RED, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_player():
    if player.alive:
        pygame.draw.rect(screen, WHITE, (player.x * GRID_SIZE, player.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, RED, (player.x * GRID_SIZE, player.y * GRID_SIZE - 10, GRID_SIZE, 5))
        pygame.draw.rect(screen, (0, 255, 0), (player.x * GRID_SIZE, player.y * GRID_SIZE - 10, GRID_SIZE * (player.hp / 100), 5))

def draw_hud(game_timer, bombs):
    font = pygame.font.Font(None, 36)
    minutes = int(game_timer // 60)
    seconds = int(game_timer % 60)
    timer_text = font.render(f"Time: {minutes:02d}:{seconds:02d}", True, WHITE)
    screen.blit(timer_text, (10, 10))
    active_bombs = sum(1 for bomb in bombs if not bomb.exploded)
    bomb_text = font.render(f"Bombs: {player.max_bombs - active_bombs}/{player.max_bombs}", True, WHITE)
    screen.blit(bomb_text, (10, 40))
    cooldown_text = font.render(f"Bomb Cooldown: {max(0, player.bomb_cooldown):.1f}s", True, WHITE)
    screen.blit(cooldown_text, (10, 70))
    range_text = font.render(f"Explosion Range: {current_explosion_range}", True, WHITE)
    screen.blit(range_text, (10, 100))

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

def update_loop():
    global game_over, bomb_counter, game_timer, last_updated_minute, current_explosion_range
    if game_over:
        return
    
    dt = clock.tick(FPS) / 1000.0
    game_timer += dt
    minutes = int(game_timer // 60)

    
    if minutes != last_updated_minute:
        last_updated_minute = minutes
        if minutes % 2 == 1:  
            player.max_bombs = int((minutes + 1) // 2) + 1
            print(f"Menit {minutes}: Max bombs increased to {player.max_bombs}")
        else:  
            current_explosion_range = max(1, int(minutes // 2) + 1)
            for bomb in bombs:
                if not bomb.exploded:
                    bomb.explosion_range = current_explosion_range
            print(f"Menit {minutes}: Explosion range increased to {current_explosion_range}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player.alive:
            active_bombs = [bomb for bomb in bombs if not bomb.exploded]
            if player.can_place_bomb(active_bombs):
                bombs.append(Bomb(player.x, player.y, bomb_counter, current_explosion_range))
                bomb_counter += 1
            if len(active_bombs) + 1 >= player.max_bombs:
                player.bomb_cooldown = player.bomb_cooldown_duration

    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT]:
        dx = -1
    elif keys[pygame.K_RIGHT]:
        dx = 1
    elif keys[pygame.K_UP]:
        dy = -1
    elif keys[pygame.K_DOWN]:
        dy = 1
    if player.alive:
        player.move(dx, dy, bombs)
    
    if player.bomb_cooldown > 0:
        player.bomb_cooldown -= dt
    
    
    active_bombs = [bomb for bomb in bombs if not bomb.exploded]
    if len(active_bombs) < player.max_bombs:
        player.bomb_cooldown = 0

    for bomb in bombs[:]:
        bomb.update(dt)
        if bomb.exploded and bomb.explosion_time <= 0:
            bombs.remove(bomb)
        if bomb.exploded and bomb.explosion_time >= bomb.explosion_duration - dt:
            affected_grids = get_explosion_grids(bomb)
            for nx, ny in affected_grids:
                if nx == player.x and ny == player.y and player.alive:
                    player.take_damage(20, bomb.bomb_id)
                    break
    
    if not player.alive:
        game_over = True
        print("Game Over!")
    
    screen.fill(BLACK)
    draw_map()
    draw_player()
    draw_hud(game_timer, bombs)
    for bomb in bombs:
        if not bomb.exploded:
            pygame.draw.circle(screen, RED, (bomb.x * GRID_SIZE + GRID_SIZE // 2, bomb.y * GRID_SIZE + GRID_SIZE // 2), 10)
        else:
            affected_grids = get_explosion_grids(bomb)
            for nx, ny in affected_grids:
                pygame.draw.rect(screen, YELLOW, (nx * GRID_SIZE, ny * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    if game_over:
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, WHITE)
        screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2))
    pygame.display.flip()

async def main():
    setup()
    while True:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
