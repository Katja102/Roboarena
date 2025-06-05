import pygame
import sys

# Initialisierung
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)

# Konstanten
WIDTH, HEIGHT = 800, 600
FPS = 30
STRAHL_SPEED = 4
FARBE_HINTERGRUND = (0, 0, 0)
FARBE_WAND = (200, 0, 0)
FARBE_STRAHL = (0, 255, 255)
FARBE_SPUR = (100, 200, 200)
FARBE_SPUR_SLOW = (250, 255, 0)
FARBE_SPUR_WIN = (0, 255, 0)
FARBE_SPUR_GAMEOVER = (180, 180, 180)
FARBE_SLOW = (250, 255, 0)
MOVING_WALL_SPEED = 1

# Spiel-Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hack Minigame")
font = pygame.font.SysFont(None, 48)
clock = pygame.time.Clock()

# Spielzustand (Anfangswerte)
game_state = "levels"
trail = []
leben = 3


class Level:
    def __init__(
        self,
        start_pos,
        start_dir,
        ziel_pos,
        ziel_dir,
        direction,
        strahl_speed,
        walls,
        slow_buttons,
        moving_walls,
    ):
        start_area = start_dir.copy()
        start_area = [(element * 5) + 35 for element in start_dir.copy()]
        self.start_chip = pygame.Rect(*start_pos, *start_area)
        self.start_dir = start_dir
        ziel_area = [(abs(element) * 10) + 40 for element in ziel_dir]
        self.ziel_chip = pygame.Rect(*ziel_pos, *ziel_area)
        self.ziel_dir = ziel_dir
        up = self.start_dir[1] == 1
        strahl = [
            self.start_chip.x + 12.5 if up else self.start_chip.x,
            self.start_chip.y + 12.5 if not up else self.start_chip.y,
            10,
            10,
        ]
        self.strahl = pygame.Rect(*strahl)
        self.direction = direction
        self.strahl_speed = strahl_speed
        self.is_slowed = False
        self.slow_timer = 0
        self.walls = walls
        self.slow_buttons = slow_buttons
        self.moving_walls = moving_walls

    def start_chip_box(self):
        if self.start_dir[0] == 1:
            x = self.start_chip.x + 10
        else:
            x = self.start_chip.x
        if self.start_dir[1] == 1:
            y = self.start_chip.y + 10
        else:
            y = self.start_chip.y
        box = (
            x,
            y,
            30 if self.start_dir[0] != 0 else self.start_chip.w,
            30 if self.start_dir[1] != 0 else self.start_chip.h,
        )
        return pygame.Rect(box)

    def ziel_chip_box(self):
        x = self.ziel_chip.x + 6 if self.ziel_dir[0] == 1 else self.ziel_chip.x
        y = self.ziel_chip.y + 6 if self.ziel_dir[1] == 1 else self.ziel_chip.y
        box = (
            x,
            y,
            44 if self.ziel_dir[0] != 0 else self.ziel_chip.w,
            44 if self.ziel_dir[1] != 0 else self.ziel_chip.h,
        )
        return pygame.Rect(box)

    def zeichne_welt(self):
        screen.fill(FARBE_HINTERGRUND)
        for wall in self.walls:
            pygame.draw.rect(screen, FARBE_WAND, wall)
        for button in self.slow_buttons:
            pygame.draw.rect(screen, FARBE_SLOW, button)
        for m_wall in self.moving_walls:
            pygame.draw.rect(screen, FARBE_WAND, m_wall)
        pygame.draw.rect(screen, (255, 255, 255), self.ziel_chip)
        pygame.draw.rect(screen, (180, 180, 180), self.ziel_chip_box())
        pygame.draw.rect(screen, (255, 255, 255), self.start_chip)
        pygame.draw.rect(screen, (180, 180, 180), self.start_chip_box())

    def reset_strahl(self):
        self.strahl.x = self.start_chip.x
        if self.start_dir[1] == 1:
            self.strahl.x += 12.5
        self.strahl.y = self.start_chip.y
        if self.start_dir[0] == 1:
            self.strahl.y += 12.5
        self.direction = [0, -1]
        self.strahl_speed = STRAHL_SPEED


# Wände für Levels
walls1 = [
    pygame.Rect(0, 70, 800, 20),
    pygame.Rect(0, 510, 700, 20),
    pygame.Rect(0, 70, 20, 460),
    pygame.Rect(600, 598, 200, 10),
    pygame.Rect(795, 200, 20, 460),
    pygame.Rect(780, 70, 20, 460),
    pygame.Rect(500, 150, 160, 200),
    pygame.Rect(300, 102, 3, 13),
    pygame.Rect(300, 124, 3, 15),
    pygame.Rect(540, 88, 3, 15),
    pygame.Rect(540, 137, 3, 15),
    pygame.Rect(259, 116, 400, 7),
    pygame.Rect(50, 150, 600, 70),
    pygame.Rect(50, 150, 20, 120),
    pygame.Rect(70, 200, 150, 20),
    pygame.Rect(380, 250, 100, 160),
    pygame.Rect(85, 250, 100, 160),
    pygame.Rect(0, 300, 100, 160),
    pygame.Rect(0, 500, 700, 100),
    pygame.Rect(200, 220, 160, 100),
    pygame.Rect(220, 300, 120, 20),
    pygame.Rect(320, 200, 20, 120),
    pygame.Rect(340, 200, 180, 20),
    pygame.Rect(500, 220, 20, 140),
    pygame.Rect(520, 340, 140, 20),
    pygame.Rect(620, 240, 20, 100),
    pygame.Rect(640, 240, 115, 20),
    pygame.Rect(766, 240, 20, 200),
    pygame.Rect(85, 237, 100, 100),
    pygame.Rect(100, 350, 300, 60),
    pygame.Rect(100, 400, 580, 20),
    pygame.Rect(100, 400, 20, 70),
    pygame.Rect(300, 420, 20, 90),
    pygame.Rect(0, 400, 700, 120),
    pygame.Rect(680, 420, 20, 90),
]

slow_buttons1 = [pygame.Rect(680, 280, 20, 20)]

moving_wall1 = [pygame.Rect(500, 300, 50, 20)]

walls2 = [
    pygame.Rect(0, 500, 300, 100),
    pygame.Rect(500, 500, 300, 100),
    pygame.Rect(0, 0, 300, 100),
    pygame.Rect(500, 0, 300, 100),
    pygame.Rect(0, 0, 100, 600),
    pygame.Rect(700, 0, 100, 600),
    pygame.Rect(250, 150, 430, 270),
    pygame.Rect(150, 180, 100, 10),
    pygame.Rect(100, 210, 100, 10),
    pygame.Rect(150, 260, 100, 10),
    pygame.Rect(100, 330, 100, 10),
    pygame.Rect(150, 410, 100, 10),
]

slow_buttons2 = [pygame.Rect(170, 420, 20, 20)]

moving_wall2 = [pygame.Rect(500, 300, 50, 20)]

# Level Setup
level1 = Level(
    (736, HEIGHT - 44),
    [0, 1],
    (730, 107),
    [-1, 0],
    [0, -1],
    STRAHL_SPEED,
    walls1,
    slow_buttons1,
    moving_wall1,
)
level2 = Level(
    (380, HEIGHT - 50),
    [0, 1],
    (382.5, 0),
    [0, 1],
    [0, -1],
    STRAHL_SPEED,
    walls2,
    slow_buttons2,
    moving_wall2,
)


# Hilfsfunktionen
def zeichne_text(text_str, farbe, y_offset=0, shadow=True):
    text = font.render(text_str, True, farbe)
    if shadow:
        shadow_txt = font.render(text_str, True, (0, 0, 0))
        screen.blit(
            shadow_txt,
            (
                WIDTH // 2 - text.get_width() // 2 + 2,
                HEIGHT // 2 + 2 + y_offset,
            ),
        )
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + y_offset))


def zeichne_spur(farbe):
    for segment in trail:
        pygame.draw.rect(screen, farbe, segment)


chosen_level = level1

# Spiel-Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game_state == "start":
                    game_state = "playing"
                elif game_state == "gameover":
                    leben = 3
                    trail.clear()
                    chosen_level.reset_strahl()
                    game_state = "playing"
                elif game_state == "win":
                    leben = 3
                    trail.clear()
                    chosen_level.reset_strahl()
                    game_state = "playing"
            elif event.key == pygame.K_LSHIFT:
                if game_state == "gameover":
                    game_state = "levels"
                elif game_state == "win":
                    game_state = "levels"
            elif game_state == "levels":
                if event.key == pygame.K_1:
                    chosen_level = level1
                if event.key == pygame.K_2:
                    chosen_level = level2
                game_state = "playing"
            elif event.key == pygame.K_l:
                if game_state == "gameover":
                    leben = 3
                    trail.clear()
                    chosen_level.reset_strahl()
                    game_state = "levels"
                elif game_state == "win":
                    leben = 3
                    trail.clear()
                    chosen_level.reset_strahl()
                    game_state = "levels"
            elif event.key == pygame.K_ESCAPE:
                running = False
            elif game_state == "playing":
                if event.key == pygame.K_UP:
                    chosen_level.direction = [0, -1]
                elif event.key == pygame.K_DOWN:
                    chosen_level.direction = [0, 1]
                elif event.key == pygame.K_LEFT:
                    chosen_level.direction = [-1, 0]
                elif event.key == pygame.K_RIGHT:
                    chosen_level.direction = [1, 0]

    if game_state == "levels":
        screen.fill(FARBE_HINTERGRUND)
        zeichne_text("Drücke 1 für Level 1", (0, 255, 0), -25)
        zeichne_text("Drücke 2 für Level 2", (0, 255, 0), 25)

    if game_state == "start":
        zeichne_text("Drücke ENTER zum Starten", (0, 255, 0))

    elif game_state == "playing":
        chosen_level.zeichne_welt()
        chosen_level.strahl.x += chosen_level.direction[0] * chosen_level.strahl_speed
        chosen_level.strahl.y += chosen_level.direction[1] * chosen_level.strahl_speed

        trail.append(
            pygame.Rect(chosen_level.strahl.x + 2, chosen_level.strahl.y + 2, 6, 6)
        )
        if not chosen_level.is_slowed:
            zeichne_spur(FARBE_SPUR)
        else:
            zeichne_spur(FARBE_SPUR_SLOW)

        pygame.draw.rect(screen, FARBE_STRAHL, chosen_level.strahl)

        for m_wall in chosen_level.moving_walls:
            m_wall.x += MOVING_WALL_SPEED
            if m_wall.left <= WIDTH / 2 or m_wall.right >= WIDTH:
                MOVING_WALL_SPEED *= -1

        if chosen_level.is_slowed:
            chosen_level.slow_timer -= clock.get_time()
        if chosen_level.slow_timer <= 0:
            chosen_level.strahl_speed = STRAHL_SPEED
            chosen_level.is_slowed = False

        for wall in chosen_level.walls:
            if chosen_level.strahl.colliderect(wall):
                leben -= 1
                if leben <= 0:
                    game_state = "gameover"
                else:
                    trail.clear()
                    chosen_level.reset_strahl()
                break

        for m_wall in chosen_level.moving_walls:
            if chosen_level.strahl.colliderect(m_wall):
                leben -= 1
                if leben <= 0:
                    game_state = "gameover"
                else:
                    trail.clear()
                    chosen_level.reset_strahl()
                break

        for button in chosen_level.slow_buttons:
            if chosen_level.strahl.colliderect(button):
                if not chosen_level.is_slowed:
                    chosen_level.strahl_speed = 1
                    chosen_level.is_slowed = True
                    chosen_level.slow_timer = 3000

        if chosen_level.strahl.colliderect(chosen_level.ziel_chip):
            game_state = "win"

        screen.blit(font.render(f"Leben: {leben}", True, (255, 255, 255)), (20, 20))

    elif game_state == "gameover":
        zeichne_spur(FARBE_SPUR_GAMEOVER)
        zeichne_text("Game Over!", (255, 0, 0))
        zeichne_text("Drücke ENTER für Neustart", (255, 255, 255), 60)
        zeichne_text("oder L für Levelauswahl", (255, 255, 255), 95)

    elif game_state == "win":
        zeichne_spur(FARBE_SPUR_WIN)
        zeichne_text("Erfolg! Ziel erreicht!", (255, 255, 255))
        zeichne_text("Drücke ENTER für Neustart ", (255, 255, 255), 60)
        zeichne_text("oder L für Levelauswahl", (255, 255, 255), 95)

    pygame.display.flip()
    clock.tick(FPS)

# Aufräumen
pygame.quit()
sys.exit()
