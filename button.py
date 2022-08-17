import pygame

#button class
class Button:
    def __init__(self, x, y, image, scale):
		
        width = image.get_width()
		
        height = image.get_height()
		
        self.img = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		
        self.rect = self.img.get_rect()
		
        self.rect.topleft = (x, y)
		
        self.clicked = False
    
    def hover(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def get_clicked(self):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not (self.clicked):
                self.clicked = True
                action = True
            
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        return action

    def draw(self, surface):
        surface.blit(self.img, (self.rect.x, self.rect.y))
        

    
