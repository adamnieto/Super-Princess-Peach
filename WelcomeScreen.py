import pygame
import MiniGameMode
import StoryMode


class WelcomeScreen:
    def __init__(self):
        # initializes pygame
        pygame.init()
        # loads music to play infinitely (until stop)
        try:
            pygame.mixer.music.load('Overworld.ogg')
            pygame.mixer.music.set_volume(.5)
            pygame.mixer.music.play(-1)
        except pygame.error as err:
            print(err)
        # Screen size (x, y)
        self.__screenSize = (640, 480)
        # displays the screen of the screen size
        self.__screen = pygame.display.set_mode(self.__screenSize)
        # initializes the font type
        self.__font = pygame.font.SysFont("Helvetica", 18, bold=False,
                                          italic=False)
        # Sets window title
        pygame.display.set_caption("Welcome To Super Princess Peach!")
        # Variable the continues or stops game loop
        self.__completed = False

    def runStoryMode(self):
        # makes an instance of the sprite class, peach
        #  sets initial coordinates at (20, 355)
        storyMode = StoryMode.StoryMode(20, 355)
        # allows loop to run with peach sprite
        storyMode.runStoryMode(storyMode)

    def runMiniGameMode(self):
        miniGameMenu = MiniGameMode.MiniGameMode()
        miniGameMenu.runMiniGameMenu()

    def displayMessage(self):
        # draws rect for "Press S for story mode"
        # (where to put rectangle, (color), (width, height, x, y)
        pygame.draw.rect(self.__screen, (255, 130, 180), (410, 70, 195, 30))
        # draws rect for M for mini game mode
        pygame.draw.rect(self.__screen, (255, 130, 180), (390, 120, 245, 30))

        # Writes message onto rectangle
        storyMsg = "Press S for Story Mode"
        # (text, makes letter smoother (anti alias), color)
        storyMsgSurface = self.__font.render(storyMsg, True, (0, 0, 0))
        # Puts message onto screen at the points (x, y)
        # (starting at top left corner)
        self.__screen.blit(storyMsgSurface, (415, 75))

        miniMsg = "Press M for Mini Game Mode"
        miniMsgSurface = self.__font.render(miniMsg, True, (0, 0, 0))
        # this draws a source surface onto another surface (screen)
        # surface.blit(source surface, (top-left corner coordinates of source))
        self.__screen.blit(miniMsgSurface, (395, 125))

        quitMsg = "Press Q to quit program"
        quitMsgSurface = self.__font.render(quitMsg, True, (0, 0, 0))
        self.__screen.blit(quitMsgSurface, (5, 5))

    def renderHomeScreen(self):
        try:
            # Loads the castle background
            homeScreen = pygame.image.load("PeachCastle2.png")
            # Scales it to size of screen ((width, height)
            homeScreen = pygame.transform.scale(homeScreen, (640, 480))
            # Puts it onto screen, top left corner is at the points (0, 0)
            self.__screen.blit(homeScreen, (0, 0))
        except pygame.error as err:
            print(err)

        try:
            # loads the peach logo and scales it down to correct size
            peachSign = pygame.image.load("super_princess_peach_logo.gif")
            peachSign = pygame.transform.scale(peachSign, (290, 100))
            self.__screen.blit(peachSign, (5, 50))
        except pygame.error as err:
            print(err)

        try:
            # loads the peach image and scales it down to correct size
            peachImg = pygame.image.load("peach.png")
            peachImg = pygame.transform.scale(peachImg, (120, 200))
            self.__screen.blit(peachImg, (50, 280))
        except pygame.error as err:
            print(err)

        try:
            # loads the mario image and scales it down to correct size
            marioImg = pygame.image.load("mario2.png")
            marioImg = pygame.transform.scale(marioImg, (120, 200))
            self.__screen.blit(marioImg, (500, 280))
        except pygame.error as err:
            print(err)

    def runWelcomeScreen(self):
        # Game loop
        # While self.__completed == False
        while not self.__completed:
            # Gets the user input because it is an event driven GUI
            for event in pygame.event.get():
                # If the user quits game by clicking
                # the 'X' in the corner of screen
                if event.type == pygame.QUIT:
                    # reassigns self.__completed and terminates loop
                    self.__completed = True
                # If a key is pressed
                if event.type == pygame.KEYDOWN:
                    # If the m is pressed "Mini Game" function is called
                    if event.key == pygame.K_m:
                        self.runMiniGameMode()
                    # If the s is pressed "Story Mode" function is called
                    if event.key == pygame.K_s:
                        self.runStoryMode()
                    # If q is pressed, program is exited by reassigning
                    # self.__completed to True and terminating loop
                    if event.key == pygame.K_q:
                        self.__completed = True

            # Calls each function
            self.renderHomeScreen()
            self.displayMessage()

            # Updates screen with each iteration in the while loop
            pygame.display.update()
