import pygame
from classes.network import NetPeer
from classes.player import Player
from classes.gui.play_screen import PlayScreen

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