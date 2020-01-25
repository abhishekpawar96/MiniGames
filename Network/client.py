import sys

import pygame

from Network import colors
from Network.network import Network
from Network.player import Player

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redraw_window(w, p1, p2):
    w.fill(colors.WHITE)
    p1.draw(w)
    p2.draw(w)
    pygame.display.update()


def main():
    run = True
    n = Network()
    p1 = n.getP()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2 = n.send(p1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                # sys.exit()exit

        p1.move()
        redraw_window(win, p1, p2)


main()
