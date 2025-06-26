import pygame

def draw_hud(screen, game_timer, bombs, players, game_over, current_explosion_range):
    font = pygame.font.Font(None, 36)
    minutes = int(game_timer // 60)
    seconds = int(game_timer % 60)
    timer_text = font.render(f"Time: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
    screen.blit(timer_text, (10, 10))
    for i, player in enumerate(players):
        active_bombs = sum(1 for bomb in bombs if not bomb.exploded and bomb.owner == player)
        bomb_text = font.render(f"Player {player.player_id + 1} Bombs: {player.max_bombs - active_bombs}/{player.max_bombs}", True, (255, 255, 255))
        screen.blit(bomb_text, (10, 40 + i * 30))
        cooldown_text = font.render(f"Player {player.player_id + 1} Cooldown: {max(0, player.bomb_cooldown):.1f}s", True, (255, 255, 255))
        screen.blit(cooldown_text, (200, 40 + i * 30))
    range_text = font.render(f"Explosion Range: {current_explosion_range}", True, (255, 255, 255))
    screen.blit(range_text, (10, 40 + len(players) * 30))

def draw_game_over(screen, players):
    font = pygame.font.Font(None, 74)
    alive_players = [player for player in players if player.alive]
    if len(alive_players) == 1:
        winner_text = font.render(f"Player {alive_players[0].player_id + 1} Wins!", True, (255, 255, 255))
        screen.blit(winner_text, (600 // 2 - 150, 600 // 2 - 50))
    for player in players:
        if not player.alive:
            game_over_text = font.render(f"Game Over for Player {player.player_id + 1}", True, (255, 255, 255))
            screen.blit(game_over_text, (600 // 2 - 200, 600 // 2 + 50 * (player.player_id + 1)))