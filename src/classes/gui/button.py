import pygame

class Button:
    def __init__(self, button_name , pos, width, height, display_text, font, base_colour, hover_colour):
        """ Create a button. Able to change colour on hover and check for clicks.  
        Handle click logic in class that creates the button.

        Args:
            button_name (str): Identifier for the button
            pos (tuple): (x,y) position of top left corner of button
            width (int): Width of button
            height (int): Height of button
            display_text (str): Text to display on button
            font (pygame.font.Font): Font object for rendering text
            base_colour (tuple): Colour of button when not hovered
            hover_colour (tuple): Colour of button when hovered
        """
        # Button setup (pos is top left corner)
        self._button_name = button_name # Need an identifier for the button
        self._x_pos = pos[0]
        self._y_pos = pos[1]
        self._width = width
        self._height = height
        self._base_colour, self._hover_colour, self._current_colour = base_colour, hover_colour, base_colour
        # Text
        self._font = font
        self._text = display_text
        self._text_surface = self._font.render(self._text, True, 'white')
        # Rectangles
        self._button_rect = pygame.Rect(self._x_pos, self._y_pos, width, height)
    
    def show(self, screen):
        # Draw button rectangle
        pygame.draw.rect(screen, self._current_colour, self._button_rect, border_radius=8)
        # Draw text
        text_rect = self._text_surface.get_rect(center=self._button_rect.center)
        screen.blit(self._text_surface, text_rect)
        
    def is_hovered(self, mouse_pos):
        self._mouse_pos_x, self._mouse_pos_y = mouse_pos
        # Change button rect colour if hovered
        if self._button_rect.collidepoint(self._mouse_pos_x, self._mouse_pos_y):
            self._current_colour = self._hover_colour
            return True
        else:
            self._current_colour = self._base_colour
            return False
        
    def is_clicked(self, event):
        # Can just check position of event against button rect
        # handling logic in class that calls this method
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._button_rect.collidepoint(event.pos):
                return True
        return False