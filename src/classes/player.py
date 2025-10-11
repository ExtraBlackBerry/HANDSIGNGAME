from .player_controller import PlayerController
from .gui.components.sprite import AnimatedSprite
import os
class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.health = 100
        self.mana = 10
        self.mana_regeneration = 1 # per second
        self.controller = PlayerController()
        self.controller.player = self
        
        self.size = (60, 60)  # Default size for animations
        self.animations = {
            'attack': AnimatedSprite(self.get_animation_paths('attack'), position=(100,100), fps=15, size=self.size),
            'charge': AnimatedSprite(self.get_animation_paths('charge'), position=(100,100), fps=10, size=self.size, loop=True),
            'dead': AnimatedSprite(self.get_animation_paths('dead'), position=(100,100), fps=5, size=self.size, loop=True),
            'decomposing': AnimatedSprite(self.get_animation_paths('decomposing'), position=(100,100), fps=5, size=self.size),
            'dying': AnimatedSprite(self.get_animation_paths('dying'), position=(100,100), fps=10, size=self.size),
            'hit': AnimatedSprite(self.get_animation_paths('hit'), position=(100,100), fps=15, size=self.size),
            'idle': AnimatedSprite(self.get_animation_paths('idle'), position=(100,100), fps=10, size=self.size, loop=True),
        }
        self.current_animation = self.animations['idle']
                
    def get_animation_paths(self, action: str) -> list[str]:
        base_path = f'assets/player character/{action}'
        if not os.path.isdir(base_path):
            raise FileNotFoundError(f"Animation folder not found: {base_path}")
        return [os.path.join(base_path, img) for img in os.listdir(base_path) if img.endswith('.png')]
    
    def set_animation(self, action: str):
        if action in self.animations:
            self.current_animation = self.animations[action]
            self.current_animation.current_frame_index = 0  # Reset to first frame
        else:
            raise ValueError(f"Animation '{action}' not found for player '{self.name}'")