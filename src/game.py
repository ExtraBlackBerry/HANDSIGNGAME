import pygame
from classes.network import NetPeer
from classes.screen_manager import ScreenManager
from classes.player import Player
from classes.gui.screens.play_screen import PlayScreen

TEST_NUMBER = 2

if TEST_NUMBER == 1:
    # Test full program with networking
    network = NetPeer()
    manager = ScreenManager()
    network.scr_mgr_start_game = manager.start_game
    manager._network = network # type: ignore
    manager._network
    manager._network_close_function = network.close
    manager._network_host_function = network.host
    manager._network_join_function = network.join
    manager._network_send_function = network.send
    manager._network_receive_player2 = network.get_player_join_event
    manager.run()
    
if TEST_NUMBER == 2:
    # Test only PlayScreen display
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    player1 = Player("Player1")
    player2 = Player("Player2")
    play_screen = PlayScreen(screen, player1, player2)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            play_screen.handle_event(event)
        play_screen.show()
        pygame.display.flip()
    pygame.quit()