import pygame
import os
import math


#Klasse Settings mit Globalen Variabeln und Einstellungen
class Settings(object):
    window_width = 800
    window_height = 500
    fps = 60
    file_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(file_path, "images")
    caption = "Space Ship"
    rotate = 0
    life = 3
    countspeed = 0


#Klasse Background hier wird ein passendes bitmap als Hintergrund hinzugefügt. wird von run aufgerufen
class Background(object):
    def __init__(self, filename="background.png"):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.image_path, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))


#Player Klasse hier sind wird der Spieler abgelegt tranformiert und skaliert
class Player(pygame.sprite.Sprite):
    def __init__(self, picturefile):
        super().__init__()
        self.image_orig = pygame.image.load(os.path.join(Settings.image_path, picturefile)).convert_alpha()
        self.image_orig = pygame.transform.scale(self.image_orig, (40, 35))
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 2
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = 10
        self.rect.centery = 10
        self.speed_v = 0
        self.speed_h = 0
        self.rect.centerx = Settings.window_width / 2
        self.rect.bottom = Settings.window_height / 2

#update updatet die rotate, wall collison und die bewegung
    def update(self):
        self.rotate()
        self.wall_collision()
        self.rect.move_ip((self.speed_h, self.speed_v))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

#Überprüft ob sich der Spieler am rand in richtung rand bewegt und setzt die neu Position fest
    def wall_collision(self):
        if self.rect.top + self.speed_v < 0:
            self.rect.centery = Settings.window_height - 25
        if self.rect.bottom + self.speed_v > Settings.window_height:
            self.rect.centery = 25
        if self.rect.left + self.speed_h < 0:
            self.rect.centerx = Settings.window_width -25
        if self.rect.right + self.speed_h > Settings.window_width:
            self.rect.centerx = 25
 
 #Rotate lässte den spieler sich drehen und sorgt dafür das das alte center auch das neue center ist. wird von Watch for events aufgerufen
    def rotate(self):
        c = self.rect.center
        self.image = pygame.transform.rotate(self.image_orig, Settings.rotate)
        self.rect = self.image.get_rect()
        self.rect.center = c        

#Up Rechnet die geschwindigkeit aus mit dem Winkel und dem speed und setzt eine Obergrenze von 10 für alle Richtungen fest
    def up(self):
        self.speed_h = self.speed_h - math.sin(math.radians(Settings.rotate))
        self.speed_v = self.speed_v - math.cos(math.radians(Settings.rotate))
        if self.speed_h <= -10:
            self.speed_h = -10
        if self.speed_h >= 10:
            self.speed_h = 10
        if self.speed_v <= -10:
            self.speed_v = -10
        if self.speed_v >= 10:
            self.speed_v = 10


#Klasse Game hier wird der spieler in eine Gruppe abgelegt und fügt ihn hinzu 
class Game(object):
    def __init__(self) -> None:
        super().__init__()
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.display.set_caption(Settings.caption)

        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player("ship.png"))

        self.running = False

#Run startet die wichtigsten Funktionen und lässt sie wiederholen
    def run(self):
        self.start()
        self.running = True
        while self.running:
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()
        pygame.quit()

#Watch for events überprüft ob events in form von tastendruck vorliegt. wird von run aufgerufen
    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP:
                    self.player.sprite.up()
                elif event.key == pygame.K_RIGHT:
                    if Settings.rotate == 0:
                        Settings.rotate = 337.5
                    elif Settings.rotate == 22.5:
                        Settings.rotate = 0
                    else:
                        Settings.rotate -= 22.5
                elif event.key == pygame.K_LEFT:
                    if Settings.rotate >= 337.5:
                        Settings.rotate = 0
                    else:
                        Settings.rotate += 22.5

#Start startet den Background und lässt den spieler Spawnen. wird von run aufgerufen
    def start(self):
        self.background = Background()
        self.spawn()

    def spawn(self):
        self.player.add(Player("ship.png"))

    def update(self):
        self.player.update()

    def draw(self):
        self.background.draw(self.screen)
        self.player.draw(self.screen)

        pygame.display.flip()


if __name__ == '__main__':

    game = Game()
    game.run()