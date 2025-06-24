import pygame
import sys
import config
from map import Map
from map_renderer import MapRenderer
from robot import Robot
from bullet import Bullet
from button import Button
from sounds import Sounds

# Initialisation
pygame.init()

# Get current screen resolution
info = pygame.display.Info()
max_width: int = info.current_w
max_height: int = info.current_h

# Calculate TILE_SIZE to fit the fixed grid into the screen
config.TILE_SIZE = min(max_width // config.COLUMNS, max_height // config.ROWS)

# set window size
window_width: int = config.TILE_SIZE * config.COLUMNS
window_height: int = config.TILE_SIZE * config.ROWS

# Create window (not fullscreen)
screen: pygame.Surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Roboarena")
clock = pygame.time.Clock()

# Debug info
print(f"Monitor: {max_width}x{max_height}")
print(f"Fenster: {window_width}x{window_height}")
print(f"TILE_SIZE: {config.TILE_SIZE}")


def draw_text(
    surface, text, x, y, font_size, color=(255, 255, 255), font_name=None, center=False
):
    font = pygame.font.SysFont(font_name, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, y))
    if center:
        surface.blit(text_surface, text_rect)
    else:
        surface.blit(text_surface, (x, y))


def main_menu():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)

    start_button = Button(
        rect=(screen.get_width() // 2 - 100, 300, 200, 50),
        text="Start Game",
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    options_button = Button(
        rect=(screen.get_width() // 2 - 100, 370, 200, 50),
        text="Options",
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    instructions_button = Button(
        rect=(screen.get_width() // 2 - 100, 440, 200, 50),
        text="How to play",
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    level_button = Button(
        rect=(screen.get_width() // 2 - 100, 510, 200, 50),
        text="Level selection",
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    quit_button = Button(
        rect=(screen.get_width() // 2 - 100, 580, 200, 50),
        text="Exit Game",
        font=font,
        bg_color=(200, 50, 50),
        text_color=(255, 255, 255),
        hover_color=(255, 80, 80),
    )

    running = True
    while running:
        screen.fill((30, 30, 30))

        title_font = pygame.font.SysFont(None, 80)
        title_surf = title_font.render("Main Menu", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(title_surf, title_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if start_button.is_clicked(event):
                game_loop()
            if options_button.is_clicked(event):
                options()
            if instructions_button.is_clicked(event):
                instructions_menu()
            if level_button.is_clicked(event):
                level_selection()
            if quit_button.is_clicked(event):
                pygame.quit()
                sys.exit()

        start_button.draw(screen)
        options_button.draw(screen)
        instructions_button.draw(screen)
        level_button.draw(screen)
        quit_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def pause_menu():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)

    continue_button = Button(
        rect=(screen.get_width() // 2 - 100, 230, 200, 50),
        text="Continue",
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    menu_button = Button(
        rect=(screen.get_width() // 2 - 100, 300, 200, 50),
        text="Main Menu",
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    options_button = Button(
        rect=(screen.get_width() // 2 - 100, 370, 200, 50),
        text="Options",
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    instructions_button = Button(
        rect=(screen.get_width() // 2 - 100, 440, 200, 50),
        text="How to play",
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    quit_button = Button(
        rect=(screen.get_width() // 2 - 100, 510, 200, 50),
        text="Exit Game",
        font=font,
        bg_color=(200, 50, 50),
        text_color=(255, 255, 255),
        hover_color=(255, 80, 80),
    )

    paused = True
    while paused:

        sounds = Sounds()
        sounds.stop_all_sounds()
        screen.fill((30, 30, 30))

        title_font = pygame.font.SysFont(None, 80)  # große Schrift
        title_surf = title_font.render("Paused", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(title_surf, title_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if continue_button.is_clicked(event):
                paused = False
            if menu_button.is_clicked(event):
                main_menu()
            if options_button.is_clicked(event):
                options()
            if instructions_button.is_clicked(event):
                instructions_menu()
            if quit_button.is_clicked(event):
                pygame.quit()
                sys.exit()

        continue_button.draw(screen)
        menu_button.draw(screen)
        options_button.draw(screen)
        instructions_button.draw(screen)
        quit_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def options():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)

    easy_button = Button(
        rect=(screen.get_width() // 2 - 350, 300, 200, 50),
        text="Easy",
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    medium_button = Button(
        rect=(screen.get_width() // 2 - 100, 300, 200, 50),
        text="Medium",
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    hard_button = Button(
        rect=(screen.get_width() // 2 + 150, 300, 200, 50),
        text="Hard",
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    back_button = Button(
        rect=(screen.get_width() // 2 - 100, 510, 200, 50),
        text="Back",
        font=font,
        bg_color=(200, 50, 50),
        text_color=(255, 255, 255),
        hover_color=(255, 80, 80),
    )

    running = True
    while running:
        screen.fill((30, 30, 30))

        draw_text(screen, "Options", 0, 150, 80, center=True)

        draw_text(screen, "Difficulty", 0, 250, 50, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if easy_button.is_clicked(event):
                pass
            if medium_button.is_clicked(event):
                pass
            if hard_button.is_clicked(event):
                pass
            if back_button.is_clicked(event):
                return

        easy_button.draw(screen)
        medium_button.draw(screen)
        hard_button.draw(screen)
        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def level_selection():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)

    start_button = Button(
        rect=(screen.get_width() // 2 - 100, 400, 200, 50),
        text="Start Game",
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    level1_button = Button(
        rect=(screen.get_width() // 2 - 250, 300, 200, 50),
        text="Level 1",
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    level2_button = Button(
        rect=(screen.get_width() // 2 + 50, 300, 200, 50),
        text="Level 2",
        font=font,
        bg_color=(20, 130, 200),
        text_color=(255, 255, 255),
        hover_color=(40, 160, 255),
    )

    back_button = Button(
        rect=(screen.get_width() // 2 - 100, 570, 200, 50),
        text="Back",
        font=font,
        bg_color=(200, 50, 50),
        text_color=(255, 255, 255),
        hover_color=(255, 80, 80),
    )

    running = True
    while running:
        screen.fill((30, 30, 30))

        draw_text(screen, "Level Selection", 0, 150, 80, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if start_button.is_clicked(event):
                game_loop()
            if level1_button.is_clicked(event):
                game_loop("test-level.txt")
            if level2_button.is_clicked(event):
                game_loop("test-level2.txt")
            if back_button.is_clicked(event):
                return

        start_button.draw(screen)
        level1_button.draw(screen)
        level2_button.draw(screen)
        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def instructions_menu():
    font = pygame.font.SysFont(None, 40)

    back_button = Button(
        rect=(screen.get_width() // 2 - 100, 500, 200, 50),
        text="Back",
        font=font,
        bg_color=(200, 50, 50),
        text_color=(255, 255, 255),
        hover_color=(255, 80, 80),
    )

    instructions = ["Game instructions here..."]

    running = True
    while running:
        screen.fill((30, 30, 30))
        draw_text(screen, "How to play", 0, 150, 80, center=True)

        for i, line in enumerate(instructions):
            draw_text(screen, line, 50, 200 + i * 35, 30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if back_button.is_clicked(event):
                return

        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def game_loop(map_file: str | None = None):
    if map_file is None:
        map_file = "test-level.txt"

    # Load map data and prepare rendering
    game_map = Map(map_file)
    map_renderer = MapRenderer(screen, config.TEXTURES)
    map_renderer.draw_map_picture(game_map.get_map_data())
    walls: list[pygame.Rect] = game_map.walls()

    # Create robots using spawn positions
    spawn_positions = game_map.generate_spawn_positions()
    player = Robot(
        screen, *spawn_positions[0], config.TILE_SIZE // 2, 180, (255, 255, 255), 1, 2, True
    )
    enemy1 = Robot(
        screen, *spawn_positions[1], config.TILE_SIZE // 2, 0, (0, 100, 190), 1, 2, False
    )
    enemy2 = Robot(
        screen, *spawn_positions[2], config.TILE_SIZE // 2, 50, (255, 50, 120), 1, 2, False
    )
    enemy3 = Robot(
        screen, *spawn_positions[3], config.TILE_SIZE // 2, 50, (0, 250, 0), 1, 2, False
    )
    robots: list[Robot] = [player, enemy1, enemy2, enemy3]

    # Setup for bullets and movement
    bullets: list[Bullet] = []
    circle_tick: int = 100
    enemy_behaviour_tick: int = 0
    angle: int = 180

    running = True

    # run game
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sounds = Sounds()
                sounds.stop_all_sounds()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu()

        screen.fill((220, 220, 220))  # light gray background
        map_renderer.draw_map()
        ticks = pygame.time.get_ticks()
        if ticks > circle_tick:
            circle_tick += 50
            angle = (angle + 3) % 360
        if ticks > enemy_behaviour_tick:
            enemy_behaviour_tick += 3000  # 3 sec
            goals: list[Robot | None] = []
            for robot in robots:
                if robot is player:
                    continue
                goals.append(robot.get_robot_with_distance_prob(game_map, robots))
        for robot in robots:
            if robot is player:  # player
                player.update_player(robots, game_map, walls, bullets)
                if player.lives == 0:
                    gameover()
            else:  # enemies
                robot.update_enemy(
                    goals[robots.index(robot) - 1], robots, game_map, walls, bullets
                )
                if robot.lives == 0:
                    robots.remove(robot)
                    if len(robots) <= 1:
                        victory()
        for bullet in bullets:
            bullet.update_bullet(game_map)
            if not bullet.alive:
                bullets.remove(bullet)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


def gameover():

    sounds = Sounds()
    sounds.stop_all_sounds()
    running = True
    while running:
        screen.fill((30, 30, 30))

        draw_text(screen, "GAME OVER", 0, 200, 100, center=True)

        draw_text(
            screen,
            "Press ESC to return to Main Menu or press ENTER to restart",
            0,
            250,
            50,
            center=True,
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                elif event.key == pygame.K_RETURN:
                    game_loop()

        pygame.display.flip()
        clock.tick(60)


def victory():

    sounds = Sounds()
    sounds.stop_all_sounds()
    running = True
    while running:
        screen.fill((30, 30, 30))

        draw_text(screen, "VICTORY", 0, 200, 100, center=True)

        draw_text(
            screen,
            "Press ESC to return to Main Menu or press ENTER to restart",
            0,
            250,
            50,
            center=True,
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                elif event.key == pygame.K_RETURN:
                    game_loop()

        pygame.display.flip()
        clock.tick(60)


main_menu()
