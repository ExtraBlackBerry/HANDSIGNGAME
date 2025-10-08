import pygame

class InputBox:
    def __init__(self, pos, width, height, label_text, font, base_colour, active_colour, label_colour) -> None:
        # Input box
        self._x_pos = pos[0]
        self._y_pos = pos[1]
        self._width = width
        self._height = height
        self._base_colour, self._active_colour, self._current_colour = base_colour, active_colour, base_colour
        self._label_colour = label_colour
        # Text
        self._font = font
        self._text = " "
        self._text_surface = self._font.render(self._text, True, self._current_colour)
        # label
        self._label_text = label_text
        self._label_surface = self._font.render(self._label_text, True, self._label_colour)
        self._label_rect = self._label_surface.get_rect(center=(self._x_pos + self._width//2, self._y_pos - 30))
        
        # Rectangle
        self._input_rect = pygame.Rect(self._x_pos, self._y_pos, width, height)
        self._active = False
        
    def show(self, screen):
        # Draw input box rectangle
        pygame.draw.rect(screen, self._current_colour, self._input_rect, width=2)
        
        # Draw text
        self._text_surface = self._font.render(self._text, True, self._current_colour) # Update text colour
        text_rect = self._text_surface.get_rect(center=self._input_rect.center)
        # Crop displayed text if too wide for box
        if self._text_surface.get_width() > self._width - 10:
            cropped_surface = self._text_surface.subsurface((self._text_surface.get_width() - (self._width - 10), 0, self._width - 10, self._text_surface.get_height()))
            text_rect = cropped_surface.get_rect(center=self._input_rect.center) # Re-center cropped text
            screen.blit(cropped_surface, text_rect)
        else:
            screen.blit(self._text_surface, text_rect)
            
        # Draw label
        screen.blit(self._label_surface, self._label_rect)
    
    def handle_event(self, event):
        # Activate/deactivate input box on click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._input_rect.collidepoint(event.pos): # Set active if clicked
                self._active = True
            else: # Clicked outside box, deactivate
                self._active = False
            # Change colour
            self._current_colour = self._active_colour if self._active else self._base_colour
        
        # Key input
        if event.type == pygame.KEYDOWN and self._active:
            if event.key == pygame.K_RETURN: # Return name on enter key
                return self._text
            elif event.key == pygame.K_BACKSPACE:
                self._text = self._text[:-1]
            else:
                self._text += event.unicode
            # Update text surface
            self._text_surface = self._font.render(self._text, True, self._current_colour)
        return None
    
    