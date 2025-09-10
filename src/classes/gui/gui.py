import pygame # type: ignore

class GUI:
    def __init__(self):
        # Setup
        pygame.init()
        self._SCREEN_WIDTH = 1280
        self._SCREEN_HEIGHT = 780
        self._screen = pygame.display.set_mode((self._SCREEN_WIDTH, self._SCREEN_HEIGHT))
        pygame.display.set_caption("Seal Strike")
        self._player_name = "None"
        
        # Host screen
        self._currently_hosting = False
        self._host_screen_open = False
        self._network_host_function = lambda: None
        self._network_close_function = lambda: None

        # Colours
        self._COLOR_BACKGROUND = (34,30,32,255)
        self._COLOR_BUTTON = (58, 51, 120)
        self._COLOR_TEXT = (255, 255, 255)
        self._COLOR_PLAYER_BOX = (0, 255, 0)
        self._COLOR_ENEMY_BOX = (255, 0, 0)
        self._COLOR_HEALTH_BAR= (255, 0, 0)

        # Fonts TODO: Get ttf file for fonts
        self._font = pygame.font.SysFont('Arial', 30)
        
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
            
    def draw_input_box(self, rect, colour, font, text, active):
        # Input Box Setup
        max_width = rect.width - 10
        txt_surface = font.render(text, True, colour)
        pygame.draw.rect(self._screen, colour, rect, 2)
        
        if txt_surface.get_width() > max_width: # Text too long, crop to rightmost part
            offset = txt_surface.get_width() - max_width
            cropped_surface = txt_surface.subsurface((offset, 0, max_width, txt_surface.get_height()))
            text_rect = cropped_surface.get_rect(center=rect.center)
            self._screen.blit(cropped_surface, text_rect)
        else: # Text fits, draw normally
            text_rect = txt_surface.get_rect(center=rect.center)
            self._screen.blit(txt_surface, text_rect)

    def name_input_screen(self):
        # Input box setup
        box_x = (self._SCREEN_WIDTH - 200) // 2
        box_y = int(self._SCREEN_HEIGHT * 0.5) - (50 // 2)
        
        input_box = pygame.Rect(box_x, box_y, 200, 50)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        name = ''
        font = pygame.font.Font(None, 36)
        
        # Logo setup
        logo_image = pygame.image.load('assets/logo.png')
        logo_image = pygame.transform.scale(logo_image, (167, 114))
        logo_rect = logo_image.get_rect(center=(self._SCREEN_WIDTH//2, 130))
        
        # Subtitle setup
        subtitle_text = font.render("Set Name", True, self._COLOR_TEXT)
        subtitle_rect = subtitle_text.get_rect(center=(input_box.centerx, input_box.top - 25))
        
        # Input loop
        active = False
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos): # Toggle active if clicked in box
                        active = not active
                    else: # Deactivate if clicked outside box
                        active = False
                    color = color_active if active else color_inactive
                    
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:      # Enter Text
                            done = True
                        elif event.key == pygame.K_BACKSPACE: # Delete last char
                            name = name[:-1]
                        else:                                 # Add char to text
                            name += event.unicode

            self._screen.fill(self._COLOR_BACKGROUND) # Clear frame
            
            # Rendering
            self._screen.blit(logo_image, logo_rect)
            self._screen.blit(subtitle_text, subtitle_rect)
            self.draw_input_box(input_box, color, font, name, active)
            
            pygame.display.flip() # Update Frame

        return name

    def host_screen(self):
        # Popup setup
        popup_width, popup_height = 400, 250
        popup_x = (self._SCREEN_WIDTH - popup_width) // 2
        popup_y = (self._SCREEN_HEIGHT - popup_height) // 2
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        
        pygame.draw.rect(self._screen, (220, 220, 220), popup_rect) # Draw bg

        # Exit button setup
        x_size = 30
        x_center = popup_rect.right - x_size // 2 - 10
        y_center = popup_rect.top + x_size // 2 + 10
        
        # Draw X button
        self.draw_button(self._screen,"X",(x_center, y_center),x_size,x_size,(180, 50, 50),'white',pygame.font.SysFont('Arial', 24),border_radius=8)
        x_rect = pygame.Rect(0, 0, x_size, x_size)
        x_rect.center = (x_center, y_center)

        # Title
        popup_font = pygame.font.SysFont('Arial', 32)
        popup_text = popup_font.render("Host Game", True, 'black')
        popup_text_rect = popup_text.get_rect(center=(popup_rect.centerx, popup_rect.top + 40))
        self._screen.blit(popup_text, popup_text_rect)

        # TODO: Player List
        # TODO: Start game button

        return x_rect # Passing out to handle click in main menu event loop
    
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
            
        running = True
        host_x_button = None
        
        # Logo
        logo_image = pygame.image.load('assets/logo.png')
        logo_rect = logo_image.get_rect(center=(self._SCREEN_WIDTH//2, 130))
        
        # Button setup
        button_width = 250
        button_height = 70
        button_y_start = self._SCREEN_HEIGHT // 2 # Y coord of center of first button
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
                    if not self._host_screen_open: # Only check buttons if host popup not open
                        # Check if mouse is over any buttons
                        if host_button_rect.collidepoint(mouse_pos):
                            # TODO: Link host screen
                            if not self._currently_hosting:
                                self._network_host_function()
                                self._currently_hosting = True
                                self._host_screen_open = True
                            else:
                                print("Already hosting a game") # TODO: Make this a popup
                        if join_button_rect.collidepoint(mouse_pos):
                            # TODO: Link join screen
                            print("Link join screen here")
                        if exit_button_rect.collidepoint(mouse_pos):
                            running = False
                    else:
                        if host_x_button and host_x_button.collidepoint(mouse_pos): # Host Popup X Button
                            self._network_close_function()
                            self._host_screen_open = False
                            self._currently_hosting = False

            self._screen.fill(self._COLOR_BACKGROUND) # Clear frame
            
            # === Rendering ===
            # Logo
            self._screen.blit(logo_image, logo_rect)
            
            # Buttons
            self.draw_button(self._screen, "HOST", host_button_rect.center, button_width, button_height, self._COLOR_BUTTON, self._COLOR_TEXT, self._font)
            self.draw_button(self._screen, "JOIN", join_button_rect.center, button_width, button_height, self._COLOR_BUTTON, self._COLOR_TEXT, self._font)
            self.draw_button(self._screen, "EXIT", exit_button_rect.center, button_width, button_height, self._COLOR_BUTTON, self._COLOR_TEXT, self._font)
            
            # Name display box
            pygame.draw.rect(self._screen, (112,240,245,255), name_box_rect)
            max_name_width = name_box_width - 10
            name_text_surface = self._font.render(player_name, True, self._COLOR_TEXT)
            if name_text_surface.get_width() > max_name_width: # Crop if too long
                # Cropped to leftmost part
                cropped_surface = name_text_surface.subsurface((0, 0, max_name_width, name_text_surface.get_height()))
                name_text_rect = cropped_surface.get_rect(center=name_box_rect.center)
                self._screen.blit(cropped_surface, name_text_rect)
            else: # Text fits
                name_text_rect = name_text_surface.get_rect(center=name_box_rect.center)
                self._screen.blit(name_text_surface, name_text_rect)
                
            # Host popup
            if self._host_screen_open:
                overlay = pygame.Surface((self._SCREEN_WIDTH, self._SCREEN_HEIGHT))
                overlay.set_alpha(128)
                overlay.fill((50, 50, 50))
                self._screen.blit(overlay, (0, 0))
                host_x_button = self.host_screen() # Draw host screen and get X button rect
            
            # === Controls ===
            keys = pygame.key.get_pressed()
            # if keys[pygame.K_w]: # Example w key
            
            pygame.display.flip() # Update Frame

        pygame.quit()
    

if __name__ == "__main__":
    from network import NetPeer
    network = NetPeer()
    gui = GUI()
    gui._network_host_function = network.host
    gui._network_close_function = network.close
    
    player_name = gui.name_input_screen()
    # Annoying check
    if player_name is None:
        player_name = ""
        
    gui.main_menu(player_name)