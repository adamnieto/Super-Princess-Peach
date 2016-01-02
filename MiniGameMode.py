import pygame
import BrickBreaker
import Simon
import Snake


class MiniGameMode:
    def __init__(self):
        pygame.init()
        self.__screenSize = (640, 480)
        self.__screen = pygame.display.set_mode(self.__screenSize)
        pygame.display.set_caption("Mini Game Mode")
        self.__clock = pygame.time.Clock()
        # FPS = Frames per second
        self.__FPS = 20
        self.__font = pygame.font.SysFont("Helvetica", 18, bold=False,
                                          italic=False)
        self.__completed = False
        self.__mode = "Mini Game"

    def displayMessage(self):
        # creates an image (or surface) with text
        # font.render("text", anti alias, color)
        # anti alias is a boolean and if true has smooth edges on text
        # can have optional background color argument
        welcomeMsg = self.__font.render("Welcome!",
                                        True, (0, 0, 0))
        # this draws a source surface onto another surface (screen)
        # surface.blit(source surface, (top-left corner coordinates of source))
        self.__screen.blit(welcomeMsg, (280, 20))

        selectionMsg = self.__font.render("Please select a mini game:",
                                          True, (0, 0, 0))
        self.__screen.blit(selectionMsg, (220, 40))
        brickBreakerChoiceMsg = self.__font.render("Press 1 for Brick Breaker",
                                                   True, (0, 0, 0))
        simonChoiceMsg = self.__font.render("Press 2 for Simon",
                                            True, (0, 0, 0))
        snakeChoiceMsg = self.__font.render("Press 3 for Snake",
                                            True, (0, 0, 0))
        quitChoiceMsg = self.__font.render("Press Q to Quit",
                                           True, (0, 0, 0))
        self.__screen.blit(brickBreakerChoiceMsg, (40, 115))
        self.__screen.blit(simonChoiceMsg, (435, 115))
        self.__screen.blit(snakeChoiceMsg, (70, 215))
        self.__screen.blit(quitChoiceMsg, (435, 215))

    def drawRects(self):
        # pygame.draw.rect(surface, color, Rect area)
        # Rect stores rectangular coordinates/areas = (x, y, width, height)

        # draws rect for brick breaker
        pygame.draw.rect(self.__screen, (255, 130, 180), (35, 100, 210, 50))
        # draws rect for snake
        pygame.draw.rect(self.__screen, (255, 130, 180), (35, 200, 210, 50))
        # draws rect for simon
        pygame.draw.rect(self.__screen, (255, 130, 180), (400, 100, 210, 50))
        # draws rect for quit
        pygame.draw.rect(self.__screen, (255, 130, 180), (400, 200, 210, 50))

    def runBrickBreaker(self):
        brickBreakerGame = BrickBreaker.BrickBreaker()
        brickBreakerGame.runBrickBreaker(self.__mode)

    def runSimon(self):
        simon = Simon.Simon()
        simon.runSimon(self.__mode)

    def runSnake(self):
        snake = Snake.Snake()
        snake.runSnake(self.__mode)

    def runMiniGameMenu(self):
        while not self.__completed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__completed = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.runBrickBreaker()
                    if event.key == pygame.K_2:
                        self.runSimon()
                    if event.key == pygame.K_3:
                        self.runSnake()
                    if event.key == pygame.K_q:
                        self.__completed = True

            try:
                background = pygame.image.load("PeachesCastle.png")
                self.__screen.blit(background, (0, -2))
            except pygame.error as err:
                print(err)

            self.drawRects()

            self.displayMessage()
            pygame.display.update()
