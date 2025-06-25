import asyncio
import platform
import pygame

pygame.init()
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 40
FPS = 60
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

class Bomb:
    def __init__(self, x, y, bomb_id):
        self.x = int(x)
        self.y = int(y)
        self.bomb_id = bomb_id  
        self.timer = 3  
        self.explosion_duration = 0.5  
        self.exploded = False
        self.explosion_time = 0

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
        directions = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]  
        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < len(MAP[0]) and 0 <= ny < len(MAP):
                if MAP[ny][nx] == 2:
                    MAP[ny][nx] = 0
                    print(f"Bom meledak dan menghancurkan kotak merah di ({nx}, {ny})")
                else:
                    print(f"Bom meledak di ({nx}, {ny}), tidak ada kotak merah.")

player = Player(1, 1)
bombs = []
game_over = False
bomb_counter = 0  

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

def update_loop():
    global game_over, bomb_counter
    if game_over:
        return
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player.alive:
            bombs.append(Bomb(player.x, player.y, bomb_counter))
            bomb_counter += 1

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
    
    dt = clock.tick(FPS) / 1000.0
    for bomb in bombs[:]:
        bomb.update(dt)
        if bomb.exploded and bomb.explosion_time <= 0:
            bombs.remove(bomb)
        
        if bomb.exploded and bomb.explosion_time >= bomb.explosion_duration - dt:  
            directions = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]
            for dx, dy in directions:
                nx, ny = bomb.x + dx, bomb.y + dy
                if nx == player.x and ny == player.y and player.alive:
                    player.take_damage(20, bomb.bomb_id)
                    break
    
    if not player.alive:
        game_over = True
        print("Game Over!")
    
    screen.fill(BLACK)
    draw_map()
    draw_player()
    for bomb in bombs:
        if not bomb.exploded:
            pygame.draw.circle(screen, RED, (bomb.x * GRID_SIZE + GRID_SIZE // 2, bomb.y * GRID_SIZE + GRID_SIZE // 2), 10)
        else:         
            directions = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]
            for dx, dy in directions:
                nx, ny = bomb.x + dx, bomb.y + dy
                if 0 <= nx < len(MAP[0]) and 0 <= ny < len(MAP):
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
