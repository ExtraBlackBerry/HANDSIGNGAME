import pygame
from .button import Button

class MainMenu:
    def __init__(self, screen, player_name):
        self._screen = screen
        self._font = pygame.font.Font(None,40)
        self._button_spacing = 70
        self._buttons = [
            # 0: Host button
            Button("Host", (self._screen.get_width()//2 - 100, self._screen.get_height()//2), 
                200, 50, "Host Game", pygame.font.Font(None, 36), 'gray', (100, 100, 100))
            # 1: Join button
            ,Button("Join", (self._screen.get_width()//2 - 100, self._screen.get_height()//2 + self._button_spacing),
                200, 50, "Join Game", pygame.font.Font(None, 36), 'gray', (100, 100, 100))
            # 2: Exit button
            ,Button("Exit", (self._screen.get_width()//2 - 100, self._screen.get_height()//2 + 2*self._button_spacing),
                200, 50, "Exit", pygame.font.Font(None, 36), 'gray', (100, 100, 100))
        ]
        # Logo
        self._logo_image = pygame.image.load('assets/logo.png')
        self._logo_rect = self._logo_image.get_rect(center=(self._screen.get_width()//2, 130))
        
        # Name display
        self._name_box_colour = 'gray'
        self._name_box_width = 200
        self._name_box_height = 50
        self._name_box_x = self._screen.get_width() - self._name_box_width
        self._name_box_y = self._screen.get_height() - self._name_box_height - 20
        self._name_box_rect = pygame.Rect(self._name_box_x, self._name_box_y, self._name_box_width, self._name_box_height)
        self._name_max_width = self._name_box_width - 10
        self._name_box_text_surface = self._font.render(player_name, True, 'white')
        self._name_box_rect = pygame.Rect(self._name_box_x, self._name_box_y, self._name_box_width, self._name_box_height)
        self._name_box_text_rect = self._name_box_text_surface.get_rect(center=self._name_box_rect.center)

    def show(self):
        
        self._screen.fill((34,30,32))
                
        # Update buttons
        for button in self._buttons:
            button.show(self._screen)
            button.is_hovered(pygame.mouse.get_pos())
            
        # Draw logo
        self._screen.blit(self._logo_image, self._logo_rect)
        
        # Draw name box
        pygame.draw.rect(self._screen, self._name_box_colour, self._name_box_rect)
        # Crop name text to left most part if too wide for box
        if self._name_box_text_surface.get_width() > self._name_max_width:
            cropped_surface = self._name_box_text_surface.subsurface((0, 0, self._name_max_width, self._name_box_text_surface.get_height()))
            self._name_box_text_rect = cropped_surface.get_rect(center=self._name_box_text_rect.center)
        self._screen.blit(self._name_box_text_surface, self._name_box_text_rect)

            
        
    def handle_event(self, event):
        # Handle button logic
        for button in self._buttons:
            # Just returning a string to indicate which button was pressed
            # to be handled in ScreenManager
            if button.is_clicked(event):
                if button._button_name == "Host":
                    return "host"
                if button._button_name == "Join":
                    return "join"
                if button._button_name == "Exit":
                    return "exit"
        return None