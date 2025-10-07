import pygame
from ..components.input_box import InputBox

class LoginScreen:
    def __init__(self, screen):
        self._screen = screen
        self._font = pygame.font.Font(None, 40)
        
        # Input box for name
        self._name_input_box = InputBox(
            pos=(self._screen.get_width()//2 - 100, self._screen.get_height()//2),
            width=200,
            height=50,
            label_text="Enter Name",
            font=self._font,
            base_colour='lightskyblue3',
            active_colour='dodgerblue2',
            label_colour='white'
        )
        
        # Logo
        self._logo_image = pygame.image.load('assets/logo.png')
        self._logo_image = pygame.transform.scale(self._logo_image, (167, 114))
        self._logo_rect = self._logo_image.get_rect(center=(self._screen.get_width()//2, 130))
        

    def show(self):
        self._screen.fill((34,30,32))
        pygame.display.set_caption("Login")
        
        # Draw input box
        self._name_input_box.show(self._screen)
        
        # Draw logo
        self._screen.blit(self._logo_image, self._logo_rect)
        

    def handle_event(self, event):
        name_result = self._name_input_box.handle_event(event)
        if name_result is not None:
            return name_result
        return None