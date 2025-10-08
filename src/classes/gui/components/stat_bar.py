import pygame

class StatBar:
    def __init__(self, screen, pos, width, height, max_value, current_value, bar_colour, orientation = 'left'):
        self._screen = screen
        self._pos = int(pos[0]), int(pos[1])
        self._width = int(width)
        self._height = int(height)
        self._max_value = max_value
        self._current_value = current_value
        self._bar_colour = bar_colour
        self._bg_colour = bar_colour[0]//3, bar_colour[1]//3, bar_colour[2]//3 # Darker bg
        self._border_colour = (255, 255, 255)
        self._border_width = 2
        self._orientation = orientation # 'left', 'right' which way the bar fills toward

    def apply_value(self, value_change):
        # Takes pos or neg value as input
        # Use for applying damage or healing
        self._current_value += value_change
        self._current_value = self.clamp(self._current_value)
            
    def set_current_value(self, new_value):
        # Directly set current value
        self._current_value = new_value
        self._current_value = self.clamp(self._current_value)
        
    def set_max_value(self, new_max):
        self._max_value = new_max
            
    def clamp(self, value):
        if value < 0:
            return 0
        elif value > self._max_value:
            return self._max_value
        return value

    def show(self):
        # Draw bg
        pygame.draw.rect(self._screen, self._bg_colour, (*self._pos, self._width, self._height))
        
        # Draw fill bar based on current value
        fill_width = int((self._current_value / self._max_value) * self._width)
        # choose fill direction based on orientation given
        x,y= self._pos
        if self._orientation == 'right':
            fill_x = x + (self._width - fill_width)
        else: # left
            fill_x = x
        pygame.draw.rect(self._screen, self._bar_colour, (fill_x, y, fill_width, self._height))
        
        # Draw border
        pygame.draw.rect(self._screen, self._border_colour, (*self._pos, self._width, self._height), self._border_width)