from .player_controller import PlayerController
from .gui.components.sprite import AnimatedSprite
import os
class Player:
    def __init__(self, name, network) -> None:
        self.name = name
        self.max_health = 100
        self.max_mana = 10
        self.current_health = self.max_health
        self.current_mana = self.max_mana
        self.mana_regeneration = 1 # per second
        self.controller = PlayerController(network)
        self.controller.player = self
        self.dead = False
        
        self.size = (60, 60)  # Default size for animations
        self.animations = {
            'attack': AnimatedSprite(self.get_animation_paths('attack'), position=(100,100), fps=15, size=(120,120)),
            'charge': AnimatedSprite(self.get_animation_paths('charge'), position=(100,100), fps=10, size=self.size, loop=True),
            'dead': AnimatedSprite(self.get_animation_paths('dead'), position=(100,100), fps=5, size=self.size, loop=True),
            'dying': AnimatedSprite(self.get_animation_paths('dying'), position=(100,100), fps=10, size=self.size),
            'hit': AnimatedSprite(self.get_animation_paths('hit'), position=(100,100), fps=15, size=self.size),
            'idle': AnimatedSprite(self.get_animation_paths('idle'), position=(100,100), fps=10, size=self.size, loop=True),
            'stomping': AnimatedSprite(self.get_animation_paths('stomping'), position=(100,100), fps=10, size=self.size),
        }
        self.current_animation = self.animations['idle']
        
    # GAMEPLAY MANAGEMENT
    
    def take_damage(self, amount: int):
        self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0
            self.dead = True
            self.play_animation('dying')
        else:
            self.play_animation('hit')
            
    def spend_mana(self, amount: int) -> bool:
        if self.current_mana < amount:
            return False
        self.current_mana = max(0, self.current_mana - amount)
        return True
        
    # ANIMATION MANAGEMENT
                
    def get_animation_paths(self, action: str) -> list[str]:
        base_path = f'assets/player character/{action}'
        if not os.path.isdir(base_path):
            raise FileNotFoundError(f"Animation folder not found: {base_path}")
        return [os.path.join(base_path, img) for img in os.listdir(base_path) if img.endswith('.png')]
    
    def set_animation(self, action: str):
        # Set current animation and reset it
        if action in self.animations:
            print(f"Setting animation for {self.name} to {action}")
            self.current_animation = self.animations[action]
            self.current_animation.reset()
        else:
            print(f"Animation '{action}' not found for {self.name}.")

    def play_animation(self, action: str):
        self.set_animation(action)
        if not self.current_animation.loop:
            self.current_animation.reset()
            
    def update_animation(self):
        self.current_animation.update()
        if self.current_animation.finished:
            if self.current_animation == self.animations['dying']:
                self.set_animation('dead')
            # Go to idle when finished
            else:
                self.set_animation('idle')