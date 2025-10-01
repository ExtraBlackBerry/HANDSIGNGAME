import pygame
from .button import Button

class MainMenu:
    def __init__(self, screen, player):
        self._screen = screen
        self._player = player
        self._font = pygame.font.Font(None,40)
        self._button_font = pygame.font.Font(None,60)
        self._button_spacing = 120
        self._button_width, self._button_height = 300, 80
        
        self._buttons = [
            # Host button
            Button(
                button_name="Host",
                pos=(self._screen.get_width()//2 - self._button_width //2, self._screen.get_height()//2 - 85),
                width=self._button_width, height=self._button_height,
                display_text="Host",
                font=self._button_font,
                base_colour=(58, 51, 120), hover_colour=(38, 31, 100)
            ),
            # Join button
            Button(
                button_name="Join",
                pos=(self._screen.get_width()//2 - self._button_width //2, self._screen.get_height()//2 - 85 + self._button_spacing),
                width=self._button_width, height=self._button_height,
                display_text="Join",
                font=self._button_font,
                base_colour=(58, 51, 120), hover_colour=(38, 31, 100)
            ),
            # Exit button
            Button(
                button_name="Exit",
                pos=(self._screen.get_width()//2 - self._button_width //2, self._screen.get_height()//2 - 85 + (self._button_spacing * 2)),
                width=self._button_width, height=self._button_height,
                display_text="Exit",
                font=self._button_font,
                base_colour=(58, 51, 120), hover_colour=(38, 31, 100)
            )
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
        self._name_box_text_surface = self._font.render(self._player.name, True, 'white')
        self._name_box_rect = pygame.Rect(self._name_box_x, self._name_box_y, self._name_box_width, self._name_box_height)
        self._name_box_text_rect = self._name_box_text_surface.get_rect(center=self._name_box_rect.center)

    def show(self):
        
        self._screen.fill((34,30,32))
        pygame.display.set_caption("Main Menu")
                
        # Update buttons
        for button in self._buttons:
            button.show(self._screen)
            button.is_hovered(pygame.mouse.get_pos())
            
        # Draw logo
        self._screen.blit(self._logo_image, self._logo_rect)
        
        # Draw name box
        pygame.draw.rect(self._screen, self._name_box_colour, self._name_box_rect)
        # Crop name text to left most part if too wide for box
        if self._name_box_text_surface.get_width() > self._name_box_width - 10:
            cropped_surface = self._name_box_text_surface.subsurface((0, 0, self._name_box_width - 10, self._name_box_text_surface.get_height()))
            self._name_box_text_rect = cropped_surface.get_rect(center=self._name_box_text_rect.center)
            self._screen.blit(cropped_surface, self._name_box_text_rect)
        else:
            self._screen.blit(self._name_box_text_surface, self._name_box_text_rect)

            
        
    def handle_event(self, event):
        # Handle button logic
        for button in self._buttons:
            # Just returning a string to indicate which button was pressed
            # to be handled in ScreenManager
            if button.is_clicked(event):
                return button._button_name
        return None