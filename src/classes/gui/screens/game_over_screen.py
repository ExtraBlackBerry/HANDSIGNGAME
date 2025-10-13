import pygame
from ..components.button import Button

class GameOverScreen:
    def __init__(self, screen, is_winner, player1, player2):
        self._screen = screen
        self._is_winner = is_winner
        self._font = pygame.font.Font(None, 30)
        self._player1 = player1
        self._player2 = player2
        
        # Logo (Making it look like host screen for now)
        self._logo_image = pygame.image.load('assets/logo.png')
        self._logo_rect = self._logo_image.get_rect(center=(self._screen.get_width()//2, 130))
        
        
        # Popup
        self._popup_width, self._popup_height = 400, 250
        self._popup_x = (self._screen.get_width() - self._popup_width) // 2
        self._popup_y = (self._screen.get_height() - self._popup_height) // 2
        self._popup_rect = pygame.Rect(self._popup_x, self._popup_y, self._popup_width, self._popup_height)
        
        
        self.buttons = [
            Button(
                button_name="restart",
                pos=(self._popup_x + (self._popup_width - 120)//2, self._popup_y + self._popup_height - 50),
                width=120, height=40,
                display_text="Start Game",
                font=self._font,
                base_colour=(150, 150, 150), hover_colour=(100, 100, 100)
            ),
            Button(
                button_name="menu",
                pos=(self._popup_x + (self._popup_width - 120)//2, self._popup_y + self._popup_height - 100),
                width=120, height=40,
                display_text="Main Menu",
                font=self._font,
                base_colour=(150, 150, 150), hover_colour=(100, 100, 100)
            )
        ]
        
        # Winner or loser text
        if self._is_winner:
            self._result_text = self._font.render("You Win!", True, 'black')
        else:
            self._result_text = self._font.render("You Lose!", True, 'black')

    def show(self):
        # Draw background
        self._screen.fill((34, 30, 32))
        self._screen.blit(self._logo_image, self._logo_rect)
        
        # Darken background
        overlay = pygame.Surface(self._screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        self._screen.blit(overlay, (0, 0))
        
        # Draw popup
        pygame.draw.rect(self._screen, 'grey', self._popup_rect)
        
        # Draw result text
        text_rect = self._result_text.get_rect(center=(self._popup_x + self._popup_width//2, self._popup_y + 70))
        self._screen.blit(self._result_text, text_rect)
        
        # Draw buttons, both get quit, host gets restart as well
        for button in self.buttons:
            if self._player1.is_hosting or button._button_name != "restart":
                button.show(self._screen)

    def handle_event(self, event):
        # Buttons
        for button in self.buttons:
            if button.is_clicked(event):
                return button._button_name