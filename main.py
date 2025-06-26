import asyncio
import platform
import pygame
from player import Player
from bomb import Bomb
from game_map import MAP, draw_map, get_explosion_grids
from ui import draw_hud, draw_game_over

pygame.init()
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 40
FPS = 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def get_num_players():
    while True:
        try:
            num = int(input("Masukkan jumlah pemain (2-4): "))
            if 2 <= num <= 4:
                return num
            print("Harus antara 2 dan 4 pemain!")
        except ValueError:
            print("Masukkan angka yang valid!")

num_players = get_num_players()
spawn_points = [(1, 1), (13, 1), (1, 13), (13, 13)]
controls = [
    {"up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d, "bomb": pygame.K_SPACE},
    {"up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "bomb": pygame.K_RETURN},
    {"up": pygame.K_i, "down": pygame.K_k, "left": pygame.K_j, "right": pygame.K_l, "bomb": pygame.K_o},
    {"up": pygame.K_t, "down": pygame.K_g, "left": pygame.K_f, "right": pygame.K_h, "bomb": pygame.K_y}
]
players = [Player(spawn_points[i][0], spawn_points[i][1], i, controls[i]) for i in range(num_players)]
bombs = []
game_over = False
bomb_counter = 0
game_timer = 0
last_updated_minute = -1
current_explosion_range = 1

def setup():
    pygame.display.set_caption("Bomb It PvP")

def update_loop():
    global game_over, bomb_counter, game_timer, last_updated_minute, current_explosion_range
    if game_over:
        return
    
    dt = clock.tick(FPS) / 1000.0
    game_timer += dt
    minutes = int(game_timer // 60)

    if minutes != last_updated_minute:
        last_updated_minute = minutes
        if minutes % 2 == 1:  # Menit ganjil
            for player in players:
                player.max_bombs = int((minutes + 1) // 2) + 1
                print(f"Menit {minutes}: Max bombs for Player {player.player_id + 1} increased to {player.max_bombs}")
        else:  # Menit genap
            current_explosion_range = max(1, int(minutes // 2) + 1)
            for bomb in bombs:
                if not bomb.exploded:
                    bomb.explosion_range = current_explosion_range
            print(f"Menit {minutes}: Explosion range increased to {current_explosion_range}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        if event.type == pygame.KEYDOWN:
            for player in players:
                if player.alive and event.key == player.controls["bomb"]:
                    active_bombs = [bomb for bomb in bombs if not bomb.exploded and bomb.owner == player]
                    if player.can_place_bomb(active_bombs):
                        bombs.append(Bomb(player.x, player.y, bomb_counter, current_explosion_range, player))
                        bomb_counter += 1
                    if len(active_bombs) + 1 >= player.max_bombs:
                        player.bomb_cooldown = player.bomb_cooldown_duration

    keys = pygame.key.get_pressed()
    for player in players:
        if player.alive:
            dx, dy = 0, 0
            if keys[player.controls["left"]]:
                dx = -1
            elif keys[player.controls["right"]]:
                dx = 1
            elif keys[player.controls["up"]]:
                dy = -1
            elif keys[player.controls["down"]]:
                dy = 1
            player.move(dx, dy, bombs)
    
    for player in players:
        if player.bomb_cooldown > 0:
            player.bomb_cooldown -= dt
        active_bombs = [bomb for bomb in bombs if not bomb.exploded and bomb.owner == player]
        if len(active_bombs) < player.max_bombs:
            player.bomb_cooldown = 0

    for bomb in bombs[:]:
        bomb.update(dt)
        if bomb.exploded and bomb.explosion_time <= 0:
            bombs.remove(bomb)
        if bomb.exploded and bomb.explosion_time >= bomb.explosion_duration - dt:
            affected_grids = get_explosion_grids(bomb)
            for player in players:
                if player.alive:
                    for nx, ny in affected_grids:
                        if nx == player.x and ny == player.y:
                            player.take_damage(20, bomb.bomb_id)
                            break
    
    alive_players = sum(1 for player in players if player.alive)
    if alive_players <= 1:
        game_over = True
        print("Game Over! Pemenang ditentukan!")

    screen.fill((0, 0, 0))
    draw_map(screen)
    for player in players:
        player.draw(screen)
    draw_hud(screen, game_timer, bombs, players, game_over, current_explosion_range)
    for bomb in bombs:
        bomb.draw(screen)
    if game_over:
        draw_game_over(screen, players)
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