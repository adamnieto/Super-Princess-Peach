import pygame


class GameOver:
    def __init__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Story Mode")
        self.__font = pygame.font.SysFont("Helvetica", 22, bold=True,
                                          italic=False)
        self.__completed = False
        self.__mode = "Story"
        try:
            gameOver = pygame.mixer.Sound('game over.ogg')
            gameOver.set_volume(.5)
            gameOver.play(0)
        except pygame.error as err:
            print(err)

    def displayMessage(self):
        gameOverMsg = "Sorry! Game over. Please try again."
        gameOverSurface = self.__font.render(gameOverMsg, True, (255, 105, 180))
        self.__screen.blit(gameOverSurface, (143, 350))

        continueMsg = "Press Q to continue to the main menu"
        continueSurface = self.__font.render(continueMsg, True, (255, 255, 255))
        self.__screen.blit(continueSurface, (130, 380))

    def runGameOver(self):
        while not self.__completed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__completed = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.__completed = True
            self.__screen.fill((0, 0, 0))
            try:
                background = pygame.image.load("gameover.jpeg")
                self.__screen.blit(background, (0, -41))
            except pygame.error as err:
                print(err)

            self.displayMessage()

            pygame.display.update()

        # stops all sounds from playing
        pygame.mixer.stop()
