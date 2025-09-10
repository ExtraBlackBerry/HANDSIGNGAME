import pygame

from .button import Button
from .input_box import InputBox

class JoinScreen:
    def __init__(self, screen, join_function, player_name):
        self._screen = screen
        self._font = pygame.font.Font(None, 30)
        self._host_ip = None
        self._player_name = player_name
        
        self._join_function = join_function
        
        # Logo
        self._logo_image = pygame.image.load('assets/logo.png')
        self._logo_rect = self._logo_image.get_rect(center=(self._screen.get_width()//2, 130))
        
        # Popup
        self._popup_width, self._popup_height = 400, 250
        self._popup_x = (self._screen.get_width() - self._popup_width) // 2
        self._popup_y = (self._screen.get_height() - self._popup_height) // 2
        self._popup_rect = pygame.Rect(self._popup_x, self._popup_y, self._popup_width, self._popup_height)
        
        self.buttons = [
            # Join Game button
            Button(
                button_name="Join",
                pos=(self._popup_x + (self._popup_width - 120)//2, self._popup_y + self._popup_height - 50),
                width=120, height=40,
                display_text="Join Game",
                font=self._font,
                base_colour=(150, 150, 150), hover_colour=(100, 100, 100)
            ),
            # Close button (small x top right of popup)
            Button(
                button_name="Close",
                pos=(self._popup_x + self._popup_width - 40, self._popup_y + 10),
                width=30, height=30,
                display_text="X",
                font=self._font,
                base_colour='red', hover_colour=(200, 0, 0)
            )
        ]
        
        # Input box for IP
        self._ip_input_box = InputBox(
            pos=(self._popup_x + (self._popup_width - 200)//2, self._popup_y + 100),
            width=200,
            height=50,
            label_text="Host IP",
            font=pygame.font.Font(None, 30),
            base_colour=(150, 150, 150),
            active_colour=(50, 50, 50),
            label_colour='black'
        )

    def show(self):
        self._screen.fill((34,30,32))
        pygame.display.set_caption("Join Game")
        
        # Draw logo
        self._screen.blit(self._logo_image, self._logo_rect)
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self._screen.get_width(), self._screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        self._screen.blit(overlay, (0, 0))
        # Draw popup
        pygame.draw.rect(self._screen, 'grey', self._popup_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.show(self._screen)
            button.is_hovered(pygame.mouse.get_pos())
            
        # Draw input box
        self._ip_input_box.show(self._screen)

    def handle_event(self, event):
        # Handle input box
        self._ip_input_box.handle_event(event)
        self._host_ip = self._ip_input_box._text.strip() # Just update host IP as text changes
        
        # Handle buttons
        for button in self.buttons:
            if button.is_clicked(event):
                # Try to join with current text in IP box
                if button._button_name == "Join":
                    if self._host_ip:
                        try:
                            self._join_function(self._host_ip)
                            # If successful, return 'Joined' to switch screen
                            # to waiting screen
                            return 'Joined'
                        except Exception as e:
                            print(f"Error joining host: {e}")
                            return 'JoinFailed'
                            
                return button._button_name
            

        
        return None