import sys, pygame
size = width, height = 500, 500
pygame.init()
Surface = pygame.display.set_mode(size)
pygame.display.init
#Draw a green square the size of the window on to Surface.                                           
pygame.draw.rect(Surface, (0, 255, 0), (0, 0, width, height))
#Update only the top left quarter of the window
pygame.display.update(pygame.Rect(0, 0, width/2, height/2))
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        continue
