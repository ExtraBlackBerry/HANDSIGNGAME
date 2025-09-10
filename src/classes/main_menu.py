import pygame

class MainMenu:
    def __init__(self, screen):
        self._screen = screen
        
    def show(self):
        self._screen.fill('black')
        
    def handle_event(self, event):
        pass