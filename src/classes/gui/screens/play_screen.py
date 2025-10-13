import pygame
from ..components.stat_bar import StatBar
from ..components.sprite import StaticSprite, AnimatedSprite
import os

class PlayScreen:
    def __init__(self, screen, player1, player2):
        self.display = screen
        self.player1 = player1
        self.player2 = player2
        self._font = pygame.font.Font(None,40)
        self._button_font = pygame.font.Font(None,60)
        
        # Camera display area
        sw, sh = self.display.get_size()
        self.camera_display_rect = pygame.Rect(sw/4 * 3, sh/3 * 2, sw/4, sh/3)
        self.camera_display_surface = pygame.Surface((sw/4, sh/3))
        
        # Spell display area
        self.spell_display_rect = pygame.Rect(0, sh/3 * 2, sw/4 * 3, sh/3)
        self.spell_display_surface = pygame.Surface((sw/4 * 3, sh/3))
        self.skill_text = None
        
        # Character display area
        self.character_display_rect = pygame.Rect(0, 0, sw, sh/3 * 2)
        self.character_display_surface = pygame.Surface((sw, sh/3 * 2))
        
        # Player 1 Stats display area
        self.player1_health_bar = StatBar(self.display, (sw/10, sh/100), sw/10 * 2, sh/40, self.player1.max_health, self.player1.current_health, (255,0,0))
        self.player1_mana_bar = StatBar(self.display, (sw/10, sh/100 * 4), sw/10 * 1.7, sh/40, self.player1.max_mana, self.player1.current_mana, (0,0,255))
        # Player 2 Stats display area
        self.player2_health_bar = StatBar(self.display, (sw/10 * 7, sh/100), sw/10 * 2, sh/40, self.player2.max_health, self.player2.current_health, (255,0,0), 'right')
        self.player2_mana_bar = StatBar(self.display, (sw/10 * 7 + sw/10 * 0.3, sh/100 * 4), sw/10 * 1.7, sh/40, self.player2.max_mana, self.player2.current_mana, (0,0,255), 'right')
        self.name_display_font = pygame.font.Font(os.path.join('assets', 'fonts', 'BebasNeue-Regular.ttf'), 30)
        
        # Sprites
        self.background_sprites = []
        # Iterate folder and load all images as StaticSprites
        bg_folder = os.path.join('assets', 'background layers')
        # Sort images by number prefix to ensure correct layering
        bg_images = sorted(
            [img for img in os.listdir(bg_folder) if img.endswith('.png')],
            key=lambda x: int(os.path.splitext(x)[0])
        )
        for img in bg_images:
            sprite = StaticSprite(os.path.join(bg_folder, img), position=(0,-300))
            # Resize sprite to fit character display area width
            sprite.image = pygame.transform.scale(sprite.image, (self.character_display_rect.w, sprite.image.get_height()))
            self.background_sprites.append(sprite)
            
        # Flip player2 animations horizontally
        for anim in self.player2.animations.values():
            anim.mirror(horizontal=True)
            
        # Assign player1 controller and start camera
        self.player1.assign_controller()
        self.player1.controller.on_skill = self.on_skill # Set callback for when skill is recognized
        self.player1.controller.start_capture()

        
    def show(self):
        
        self.display.fill((34,30,32))
        pygame.display.set_caption("Play Screen")

        self.update_camera_display()
        self.update_spell_display()
        self.update_character_display()
        
    def update_camera_display(self):
        # Get current frame from player1's controller
        #frame = self.player1.controller.get_current_frame()
        frame = self.player1.controller.control_loop()
        # If no frame, fill black
        if frame is None:
            self.camera_display_surface.fill((0,0,0))
            self.display.blit(self.camera_display_surface, self.camera_display_rect)
            return
        
        # Convert frame from numpy array to pygame surface
        h,w = frame.shape[:2]
        surface = pygame.image.frombuffer(frame.tobytes(), (w,h), 'RGB')
        # Scale to fit camera_display_surface and blit
        cam_sized = pygame.transform.scale(surface, (self.camera_display_rect.w, self.camera_display_rect.h))
        self.camera_display_surface.fill((0,0,0)) # Clear last frame
        self.camera_display_surface.blit(cam_sized, (0, 0))
        self.display.blit(self.camera_display_surface, self.camera_display_rect)
    
    def update_spell_display(self):
        last_skill = self.player1.controller.skill_used_name
        self.spell_display_surface.fill((37, 37, 38))
        signs = self.player1.controller.sign_collection
        display_text = ", ".join(signs) if signs else (last_skill if last_skill else "Empty")
        text_surf = self.name_display_font.render(display_text, True, (255,255,255))
        text_rect = text_surf.get_rect(center=(self.spell_display_rect.w/2, self.spell_display_rect.h/2))
        self.spell_display_surface.blit(text_surf, text_rect)
        self.display.blit(self.spell_display_surface, self.spell_display_rect)
            
        
    def update_character_display(self):
        # Draw background sprites
        self.character_display_surface.fill((0,0,0))
        for sprite in self.background_sprites:
            self.character_display_surface.blit(sprite.image, sprite.rect)
        self.display.blit(self.character_display_surface, self.character_display_rect)
        
        # Draw shadows below player characters
        shadow_color = (23, 30, 50, 180)
        shadow_surface = pygame.Surface((120, 40), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, shadow_color, (0, 0, 50, 20))
        # Player 1 shadow
        self.character_display_surface.blit(shadow_surface, (295, 420))
        # Player 2 shadow
        self.character_display_surface.blit(shadow_surface, (1006, 420))
        
        # Draw player characters
        self.player1.update_animation()
        self.player2.update_animation()
        # Scuffed size fix: Get anchor at center bottom of idle animation, so all animations align properly
        p1_base_topleft = (290, 372)
        p2_base_topleft = (1000, 372)
        p1_idle = self.player1.animations['idle'].image
        p2_idle = self.player2.animations['idle'].image
        p1_anchor = (p1_base_topleft[0] + p1_idle.get_width() // 2,
                     p1_base_topleft[1] + p1_idle.get_height())
        p2_anchor = (p2_base_topleft[0] + p2_idle.get_width() // 2,
                     p2_base_topleft[1] + p2_idle.get_height())
        p1_rect = self.player1.current_animation.image.get_rect(midbottom=p1_anchor)
        p2_rect = self.player2.current_animation.image.get_rect(midbottom=p2_anchor)
        self.character_display_surface.blit(self.player1.current_animation.image, p1_rect)
        self.character_display_surface.blit(self.player2.current_animation.image, p2_rect)
        self.display.blit(self.character_display_surface, self.character_display_rect)
        
        # Draw player names below where stats will be
        p1_name_surf = self.name_display_font.render(self.player1.name, True, (255,255,255))
        p2_name_surf = self.name_display_font.render(self.player2.name, True, (255,255,255))
        self.display.blit(p1_name_surf, (self.player1_mana_bar._pos[0], self.player1_mana_bar._pos[1] + 30))
        self.display.blit(p2_name_surf, (self.player2_mana_bar._pos[0] + self.player2_mana_bar._width - p2_name_surf.get_width(), self.player2_mana_bar._pos[1] + 30))
        
        # Draw player stats
        self.update_player_stat_display()
        
    def update_player_stat_display(self):
        # Update stat bars to current player stats
        self.player1_health_bar.set_current_value(self.player1.current_health)
        self.player1_mana_bar.set_current_value(self.player1.current_mana)
        self.player2_health_bar.set_current_value(self.player2.current_health)
        self.player2_mana_bar.set_current_value(self.player2.current_mana)
        
        # Draw the stat bars
        self.player1_mana_bar.show()
        self.player2_mana_bar.show()
        self.player1_health_bar.show()
        self.player2_health_bar.show()
        
    
    def handle_event(self, event):
        return None
    
    def start_game(self):
        pass
    
    def quit_game(self):
        self.player1.controller.stop_capture()
    
    def on_skill(self, skill, player = "default"):
        if player == "default":
            player = self.player2
        target = self.player2 if player == self.player1 else self.player1 # Make sure target is the other player
        mana_cost = skill['mana_cost']
        damage = skill['damage']
        
        # Mana already checked in controller before sending skill, just apply damage
        target.take_damage(damage)