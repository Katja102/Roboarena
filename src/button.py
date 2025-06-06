import pygame


class Button:
    def __init__(self, rect, text, font, bg_color, text_color, hover_color=None):
        """
        rect: pygame.Rect oder Tupel (x, y, width, height)
        text: Button-Beschriftung
        font: pygame.font.Font-Objekt
        bg_color: Hintergrundfarbe (Tuple)
        text_color: Textfarbe (Tuple)
        hover_color: Hintergrundfarbe bei Hover (optional)
        """
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color if hover_color else bg_color

        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            color = self.hover_color
        else:
            color = self.bg_color
        pygame.draw.rect(screen, color, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, event):
        """
        Prüft, ob der Button per Maus geklickt wurde.
        event: pygame.event.Event-Objekt
        Rückgabe: True, wenn geklickt, sonst False
        """
        if (
            event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
        ):  # Linke Maustaste
            if self.rect.collidepoint(event.pos):
                return True
        return False
