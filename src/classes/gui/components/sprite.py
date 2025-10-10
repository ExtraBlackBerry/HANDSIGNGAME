import pygame
import os

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, folder_path: str, pos=(0,0), layer: int=0):
        super().__init__() # Inherit from pygame Sprite class, has draw and update methods
        self._layer = layer
        self._frames = self.load_frames(folder_path)
        self._num_frames = len(self._frames)
        self._current_frame = 0
        self._fps = 10
        self._rect = self._frames[0].get_rect(topleft=pos)
        
    def load_frames(self, folder_path: str):
        # Load all images in folder
        frames = []
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith('.png'):
                img_path = os.path.join(folder_path, filename)
                image = pygame.image.load(img_path).convert_alpha()
                frames.append(image)
        return frames # List of pygame surfaces
    
    def update(self, dt):
        # Update animation frame based on fps and dt
        self._current_frame += self._fps * dt
        if self._current_frame >= self._num_frames:
            self._current_frame = 0
            
class CharacterSprite(GameSprite):
    def __init__(self, folder_path: str, pos=(0,0), layer: int=0):
        super().__init__(folder_path, pos, layer)
        
    def update(self, dt):
        super().update(dt)
        
    def take_damage(self, amount):
        # Placeholder for taking damage logic
        pass
    
    def cast_spell(self, spell_name):
        # Placeholder for casting spell logic
        pass
    
    def die(self):
        # Placeholder for death logic
        pass