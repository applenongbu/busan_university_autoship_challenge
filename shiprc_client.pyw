import pygame
from socket import *
clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('192.168.137.57', 1972))

white = (255,255,255)
pygame.init()
screen = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()
speed = 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            clientSock.send("exit".encode('utf-8'))
            pygame.quit()
            exit()
            
        screen.fill(white)
        if (event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_UP):
                clientSock.send('up'.encode('utf-8'))    
            elif(event.key == pygame.K_DOWN):
                clientSock.send('down'.encode('utf-8'))    
            elif(event.key == pygame.K_LEFT):
                clientSock.send('left'.encode('utf-8'))    
            elif(event.key == pygame.K_RIGHT):
                clientSock.send('right'.encode('utf-8'))
            elif(event.key == pygame.K_1):
                clientSock.send('one'.encode('utf-8'))
            elif(event.key == pygame.K_2):
                clientSock.send('two'.encode('utf-8'))
            elif(event.key == pygame.K_3):
                clientSock.send('thr'.encode('utf-8'))
            elif(event.key == pygame.K_4):
                clientSock.send('for'.encode('utf-8'))
            elif(event.key == pygame.K_5):
                clientSock.send('fiv'.encode('utf-8'))
        elif (event.type == pygame.KEYUP):
            
            if(event.key == pygame.K_UP or event.key == pygame.K_DOWN):
                clientSock.send('keyupbldc'.encode('utf-8'))
            elif(event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                clientSock.send('keyupservo'.encode('utf-8'))    
        
    
    pygame.display.update()
    clock.tick(20)
