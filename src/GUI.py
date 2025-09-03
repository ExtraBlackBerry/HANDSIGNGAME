import pygame # type: ignore

class GUI:
    def __init__(self):
        # Setup
        pygame.init()
        self._SCREEN_WIDTH = 800
        self._SCREEN_HEIGHT = 600
        self._screen = pygame.display.set_mode((self._SCREEN_WIDTH, self._SCREEN_HEIGHT))
        pygame.display.set_caption("Seal Strike - Main Menu")
        self._player_name = "None"
        self._host_screen_open = False

        # Colours
        self._COLOR_BACKGROUND = (34,30,32,255)
        self._COLOR_BUTTON = (58, 51, 120)
        self._COLOR_TEXT = (255, 255, 255)
        self._COLOR_PLAYER_BOX = (0, 255, 0)
        self._COLOR_ENEMY_BOX = (255, 0, 0)
        self._COLOR_HEALTH_BAR= (255, 0, 0)

        # Fonts TODO: Get ttf file for fonts
        self._button_font = pygame.font.SysFont('Arial', 30)
        
        self._host_popup_open = False
        
    def draw_button(self, surface, text, pos, width, height, colour, text_colour, font, border_radius=15):
        # Button Rectangle
        rect = pygame.Rect(0, 0, width, height)
        rect.center = pos
        pygame.draw.rect(surface, colour, rect, border_radius=border_radius)
        
        # Button Text
        text = font.render(text, True, text_colour)
        text_rect = text.get_rect(center=rect.center)
        surface.blit(text, text_rect)
        
    def draw_player_box(self, surface, text, pos, width, height, box_colour, text_colour, font, border_radius=15):
        # Player Box Rectangle
        rect = pygame.Rect(0, 0, width, height)
        rect.center = pos
        pygame.draw.rect(surface, box_colour, rect, border_radius=border_radius)
        
        # Player Box Text
        text = font.render(text, True, text_colour)
        text_rect = text.get_rect(center=rect.center)
        surface.blit(text, text_rect)
        
    def name_input_screen(self):
        # Input Box Setup
        input_box = pygame.Rect(300, 250, 200, 50)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        text = ''
        font = pygame.font.Font(None, 36)
        
        active = False
        done = False
        
        # Subtitle Setup
        subtitle_text = font.render("Set Name", True, self._COLOR_TEXT)
        subtitle_rect = subtitle_text.get_rect(center=(input_box.centerx, input_box.top - 25))
        
        # Logo Setup
        logo_image = pygame.image.load('assets/logo.png')
        orig_width, orig_height = logo_image.get_size()
        logo_image = pygame.transform.scale(logo_image, (167, 114))
        logo_rect = logo_image.get_rect(center=(self._SCREEN_WIDTH//2, 130))
        
        
        # Input Loop
        while not done:
            for event in pygame.event.get():
                # quit event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                # Click on input box
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else: # If click outside box, deactivate
                        active = False
                    color = color_active if active else color_inactive # Color based on state
                # Backspace and Enter
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
                            
            self._screen.fill(self._COLOR_BACKGROUND) # Clear frame
            
            # Rendering
            # Input box
            max_width = input_box.width - 10             # Dont let text exceed box width
            txt_surface = font.render(text, True, color) # Update input text each loop
            
            pygame.draw.rect(self._screen, color, input_box, 2)
            if txt_surface.get_width() > max_width:
                # Show rightmost part of text if too long
                offset = txt_surface.get_width() - max_width
                cropped_surface = txt_surface.subsurface((offset, 0, max_width, txt_surface.get_height()))
                text_rect = cropped_surface.get_rect(center=input_box.center)
                self._screen.blit(cropped_surface, text_rect)
            else: # Text fits in box
                text_rect = txt_surface.get_rect(center=input_box.center)
                self._screen.blit(txt_surface, text_rect)
            
            # Subtitle
            self._screen.blit(subtitle_text, subtitle_rect)
            
            # Logo
            self._screen.blit(logo_image, logo_rect)
            
            pygame.display.flip() # Update Frame

        return text

    def host_screen(self):
        # Needs to go to play screen after setting up host
        pass

    def join_screen(self):
        # Needs to go to play screen after joining host
        pass

    def play_screen(self):
        pass
        
    def main_menu(self, player_name="None"):
        # init pygame if not already done
        # IDK if neeeded, but just in case this gets called
        # outside of this file, it might need to be initialized
        if not pygame.get_init():
            pygame.init()
            
        clock = pygame.time.Clock()
        delta_time = 0
        running = True
        
        # Logo
        logo_image = pygame.image.load('assets/logo.png')
        logo_rect = logo_image.get_rect(center=(self._SCREEN_WIDTH//2, 130))
        
        # Button setup
        button_width = 250
        button_height = 70
        button_y_start = 300 # Y coord of center of first button
        button_spacing = 90
        
        host_button_rect = pygame.Rect(0, 0, button_width, button_height)
        host_button_rect.center = (self._SCREEN_WIDTH//2, button_y_start)
        join_button_rect = pygame.Rect(0, 0, button_width, button_height)
        join_button_rect.center = (self._SCREEN_WIDTH//2, button_y_start + button_spacing)
        exit_button_rect = pygame.Rect(0, 0, button_width, button_height)
        exit_button_rect.center = (self._SCREEN_WIDTH//2, button_y_start + button_spacing * 2)
        
        # Name display Setup
        name_box_width = 200
        name_box_height = 50
        name_box_x = self._SCREEN_WIDTH - name_box_width
        name_box_y = self._SCREEN_HEIGHT - name_box_height - 20
        name_box_rect = pygame.Rect(name_box_x, name_box_y, name_box_width, name_box_height)

        while running:
            
            # === Poll for events ===
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Button Events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    # Check if mouse is over any buttons
                    if host_button_rect.collidepoint(mouse_pos):
                        # TODO: Link host screen
                        print("Link host screen here")
                        host_screen_open = True
                    if join_button_rect.collidepoint(mouse_pos):
                        # TODO: Link join screen
                        print("Link join screen here")
                    if exit_button_rect.collidepoint(mouse_pos):
                        running = False
                    
            self._screen.fill(self._COLOR_BACKGROUND) # Clear frame
            
            # === Rendering ===
            # Logo
            self._screen.blit(logo_image, logo_rect)
            
            # Buttons
            self.draw_button(self._screen, "HOST", host_button_rect.center, button_width, button_height, self._COLOR_BUTTON, self._COLOR_TEXT, self._button_font)
            self.draw_button(self._screen, "JOIN", join_button_rect.center, button_width, button_height, self._COLOR_BUTTON, self._COLOR_TEXT, self._button_font)
            self.draw_button(self._screen, "EXIT", exit_button_rect.center, button_width, button_height, self._COLOR_BUTTON, self._COLOR_TEXT, self._button_font)
            
            # Name display box
            pygame.draw.rect(self._screen, (112,240,245,255), name_box_rect)
            max_name_width = name_box_width - 10
            name_text_surface = self._button_font.render(player_name, True, self._COLOR_TEXT)
            if name_text_surface.get_width() > max_name_width: # Crop if too long
                # Cropped to leftmost part
                cropped_surface = name_text_surface.subsurface((0, 0, max_name_width, name_text_surface.get_height()))
                name_text_rect = cropped_surface.get_rect(center=name_box_rect.center)
                self._screen.blit(cropped_surface, name_text_rect)
            else: # Text fits
                name_text_rect = name_text_surface.get_rect(center=name_box_rect.center)
                self._screen.blit(name_text_surface, name_text_rect)
                
            # If host popup is open grey out menu
            # semi transparent overlay
            if self._host_screen_open:
                overlay = pygame.Surface((self._SCREEN_WIDTH, self._SCREEN_HEIGHT))
                overlay.set_alpha(128)
                overlay.fill((50, 50, 50))
                self._screen.blit(overlay, (0, 0))
                self.host_screen()
            
            # === Controls ===
            keys = pygame.key.get_pressed()
            # if keys[pygame.K_w]: # Example w key
            
            pygame.display.flip() # Update Frame
            delta_time = clock.tick(60) / 1000

        pygame.quit()
    

if __name__ == "__main__":
    gui = GUI()
    player_name = gui.name_input_screen()
    # Annoying check
    if player_name is None:
        player_name = ""
        
    gui.main_menu(player_name)