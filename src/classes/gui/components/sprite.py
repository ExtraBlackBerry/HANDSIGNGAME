import pygame
import os

class StaticSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, position=(0, 0)):
        super().__init__()
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=position)

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, image_paths: list[str], position: tuple[int, int] = (0, 0), fps: int = 30):
        super().__init__()
        # Get frames from list of image paths
        self.frames = []
        for path in image_paths:
            if not os.path.isfile(path):
                raise FileNotFoundError(f"Image file not found: {path}")
            self.frames.append(pygame.image.load(path))
        
        # Rectangle
        self.rect = self.frames[0].get_rect(topleft=position)
        
        # Animation Control
        self.frame_rate =  fps
        self.current_frame_index = 0
        self.image = self.frames[self.current_frame_index]

    def update(self):
        # Update frame based on frame rate
        now = pygame.time.get_ticks() # Gets time since pygame.init() in ms
        if now - self.last_update > 1000 // self.frame_rate:
            self.last_update = now
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
            self.image = self.frames[self.current_frame_index]