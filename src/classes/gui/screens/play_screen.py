import pygame
from ..components.stat_bar import StatBar

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
        
        # Character display area
        self.character_display_rect = pygame.Rect(0, 0, sw, sh/3 * 2)
        self.character_display_surface = pygame.Surface((sw, sh/3 * 2))
        
        # Player 1 Stats display area
        self.player1_health_bar = StatBar(self.display, (sw/10, sh/100), sw/10 * 2, sh/40, 100, 100, (255,0,0))
        self.player1_mana_bar = StatBar(self.display, (sw/10, sh/100 * 4), sw/10 * 1.7, sh/40, 10, 2, (0,0,255))
        # self.player1_stats_rect = pygame.Rect(sw/10, sh/100, sw/10 * 2, sh/20)
        # self.player1_stats_surface = pygame.Surface((sw/10 * 2, sh/20))
        # Player 2 Stats display area
        self.player2_health_bar = StatBar(self.display, (sw/10 * 7, sh/100), sw/10 * 2, sh/40, 100, 40, (255,0,0), 'right')
        self.player2_mana_bar = StatBar(self.display, (sw/10 * 7 + sw/10 * 0.3, sh/100 * 4), sw/10 * 1.7, sh/40, 10, 9, (0,0,255), 'right')
        # self.player2_stats_rect = pygame.Rect(sw/10 * 7, sh/100, sw/10 * 2, sh/20)
        # self.player2_stats_surface = pygame.Surface((sw/10 * 2, sh/20))
        
        # Start player camera capture
        self.player1.controller.start_capture()
        
    def show(self):
        
        self.display.fill((34,30,32))
        pygame.display.set_caption("Play Screen")

        self.update_camera_display()
        self.update_spell_display()
        self.update_character_display()
        
    def update_camera_display(self):
        # Get current frame from player1's controller
        frame = self.player1.controller.get_current_frame()
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
        # Fill dark gray for now
        self.spell_display_surface.fill((37,38,43))
        self.display.blit(self.spell_display_surface, self.spell_display_rect)
        
    def update_character_display(self):
        # Fill green for now
        self.character_display_surface.fill((0,255,0))
        self.display.blit(self.character_display_surface, self.character_display_rect)
        
        self.update_player_stat_display()
        
    def update_player_stat_display(self):
        # Fill pink for now
        # self.player1_stats_surface.fill((255,0,255))
        # self.display.blit(self.player1_stats_surface, self.player1_stats_rect)
        # self.player2_stats_surface.fill((255,0,255))
        # self.display.blit(self.player2_stats_surface, self.player2_stats_rect)
        
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