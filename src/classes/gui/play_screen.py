import pygame

class PlayScreen:
    def __init__(self, screen, player1, player2):
        self.display = screen
        self.player1 = player1
        self.player2 = player2
        self._font = pygame.font.Font(None,40)
        self._button_font = pygame.font.Font(None,60)
        
    def show(self):
        
        self.display.fill((34,30,32))
        pygame.display.set_caption("Play Screen")

    def handle_event(self, event):
        return None