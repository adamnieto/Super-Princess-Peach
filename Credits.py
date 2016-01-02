import pygame


class Credits:
    def __init__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Credits")
        self.__completed = False
        self.__clock = pygame.time.Clock()
        # FPS = Frames per second
        self.__FPS = 20
        # retrieves a font from system.
        # pygame.font.SysFont(name, size, bold=boolean, italic=boolean)
        self.__font = pygame.font.SysFont("Helvetica", 22, bold=True,
                                          italic=False)
        try:
            gameWon = pygame.mixer.Sound('World Clear.ogg')
            gameWon.play(0)
        except pygame.error as err:
                print(err)

    def displayCredits(self):
        # writes messages in the credits and blits them onto screen
        congratsMsg = "Congratulations! You Won!"
        congratsSurface = self.__font.render(congratsMsg, True,
                                             (255, 105, 180))
        self.__screen.blit(congratsSurface, (185, 20))

        creditsMsg = "Game Created By:"
        creditsSurface = self.__font.render(creditsMsg, True, (20, 170, 50))
        self.__screen.blit(creditsSurface, (225, 50))

        thanksMsg = "Special thanks to all the players!"
        thanksSurface = self.__font.render(thanksMsg, True, (255, 30, 0))
        self.__screen.blit(thanksSurface, (160, 210))

        continueMsg = "Press Q to continue to the main menu"
        continueSurface = self.__font.render(continueMsg, True,
                                             (255, 255, 255))
        self.__screen.blit(continueSurface, (130, 240))

    def writeNames(self):
        # writes group names in the credits and blits them onto screen
        amyMsg = "Amy Chen"
        samMsg = "Sam Kustin"
        adamMsg = "Adam Nieto"
        melissaMsg = "Melissa Wolff"

        amyCredit = self.__font.render(amyMsg, True, (0, 191, 255))
        self.__screen.blit(amyCredit, (255, 80))

        samCredit = self.__font.render(samMsg, True, (0, 191, 255))
        self.__screen.blit(samCredit, (250, 110))

        adamCredit = self.__font.render(adamMsg, True, (0, 191, 255))
        self.__screen.blit(adamCredit, (250, 140))

        melissaCredit = self.__font.render(melissaMsg, True, (0, 191, 255))
        self.__screen.blit(melissaCredit, (245, 170))

    def runCredits(self):
        while not self.__completed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__completed = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.__completed = True
            self.__screen.fill((0, 0, 0))
            try:
                # loads picture of mario, peach, and rest of group
                groupPic = pygame.image.load("peachAndFriends.png")
                groupPic = pygame.transform.scale(groupPic, (300, 200))
                self.__screen.blit(groupPic, (180, 280))
            except pygame.error as err:
                print(err)

            self.displayCredits()
            self.writeNames()

            pygame.display.update()

        # stops all sounds from playing
        pygame.mixer.stop()
