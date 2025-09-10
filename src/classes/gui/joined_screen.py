import pygame
from .button import Button

class JoinedScreen:
    def __init__(self, screen, player_name):
        self._screen = screen
        self._font = pygame.font.Font(None, 30)
        self._host_name = 'HOST' # TODO: Get from networking class
        self._joined_name = player_name
        
        # Logo
        self._logo_image = pygame.image.load('assets/logo.png')
        self._logo_rect = self._logo_image.get_rect(center=(self._screen.get_width()//2, 130))
        
        # Popup
        self._popup_width, self._popup_height = 400, 250
        self._popup_x = (self._screen.get_width() - self._popup_width) // 2
        self._popup_y = (self._screen.get_height() - self._popup_height) // 2
        self._popup_rect = pygame.Rect(self._popup_x, self._popup_y, self._popup_width, self._popup_height)
        
        self.buttons = [
            # Leave button
            Button(
                button_name="Leave",
                pos=(self._popup_x + (self._popup_width - 120)//2, self._popup_y + self._popup_height - 50),
                width=120, height=40,
                display_text="Leave",
                font=self._font,
                base_colour=(150, 150, 150), hover_colour=(100, 100, 100)
            ),
            # Close button (small x top right of popup)
            Button(
                button_name="Close",
                pos=(self._popup_x + self._popup_width - 40, self._popup_y + 10),
                width=30, height=30,
                display_text="X",
                font=self._font,
                base_colour='red', hover_colour=(200, 0, 0)
            )
        ]
        
        # Host name display box
        self._host_box_width, self._host_box_height = 300, 50
        self._host_box_x = self._popup_x + (self._popup_width - self._host_box_width) // 2
        self._host_box_y = self._popup_y + 70
        self._host_box_rect = pygame.Rect(self._host_box_x, self._host_box_y, self._host_box_width, self._host_box_height)
        self._host_box_text_surface = self._font.render(self._host_name, True, 'black')
        # Joined player display box
        self._joined_box_width, self._joined_box_height = 300, 50
        self._joined_box_x = self._popup_x + (self._popup_width - self._joined_box_width) // 2
        self._joined_box_y = self._popup_y + 130
        self._joined_box_rect = pygame.Rect(self._joined_box_x, self._joined_box_y, self._joined_box_width, self._joined_box_height)
        self._joined_box_text_surface = self._font.render(self._joined_name if self._joined_name else "OPEN SLOT", True, 'black')
        
        
        
    def show(self):
        # Screen setup
        self._screen.fill((34,30,32))
        pygame.display.set_caption("Joined Game")
        
        # Draw logo
        self._screen.blit(self._logo_image, self._logo_rect)
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self._screen.get_width(), self._screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        self._screen.blit(overlay, (0, 0))
        
        # Draw popup
        pygame.draw.rect(self._screen, 'grey', self._popup_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.show(self._screen)
            button.is_hovered(pygame.mouse.get_pos())
            
        # display host
        pygame.draw.rect(self._screen, 'white', self._host_box_rect, border_radius=5)
        host_text_rect = self._host_box_text_surface.get_rect(center=self._host_box_rect.center)
        self._screen.blit(self._host_box_text_surface, host_text_rect)
        # display joined player
        pygame.draw.rect(self._screen, 'white', self._joined_box_rect, border_radius=5)
        joined_text_rect = self._joined_box_text_surface.get_rect(center=self._joined_box_rect.center)
        self._screen.blit(self._joined_box_text_surface, joined_text_rect)
        
        # Status
        status_text = self._font.render("Waiting for host...", True, 'black')
        status_rect = status_text.get_rect(center=(self._popup_x + self._popup_width//2, self._popup_y + 30))
        self._screen.blit(status_text, status_rect)
        
    def handle_event(self, event):
        for button in self.buttons:
            if button.is_clicked(event):
                return button._button_name
        return None