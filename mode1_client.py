import pygame
from socket import *


FILL_COLOR = (255, 255, 255)    # white


def setting():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('192.168.137.57', 1972))

    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    return sock, screen, clock


def main():
    sock, screen, clock = setting()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sock.send("exit".encode('utf-8'))
                pygame.quit()
                exit()

            screen.fill(FILL_COLOR)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    sock.send('up'.encode('utf-8'))
                elif event.key == pygame.K_DOWN:
                    sock.send('down'.encode('utf-8'))
                elif event.key == pygame.K_LEFT:
                    sock.send('left'.encode('utf-8'))
                elif event.key == pygame.K_RIGHT:
                    sock.send('right'.encode('utf-8'))
                elif event.key == pygame.K_1:
                    sock.send('one'.encode('utf-8'))
                elif event.key == pygame.K_2:
                    sock.send('two'.encode('utf-8'))
                elif event.key == pygame.K_3:
                    sock.send('thr'.encode('utf-8'))
                elif event.key == pygame.K_4:
                    sock.send('for'.encode('utf-8'))
                elif event.key == pygame.K_5:
                    sock.send('fiv'.encode('utf-8'))

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    sock.send('keyupbldc'.encode('utf-8'))
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    sock.send('keyupservo'.encode('utf-8'))

        pygame.display.update()
        clock.tick(20)


if __name__ == "__main__":
    main()
