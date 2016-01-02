import pygame
from pygame.locals import *
import random


class Simon:
    def __init__(self):
        # pygame.init() initializes pygame
        pygame.init()
        # Format of .ogg: Ogg is an open and standardized bitstream container
        # format designed for streaming and manipulation.
        try:
            pygame.mixer.music.load('Overworld.ogg')
            pygame.mixer.music.set_volume(.5)
            pygame.mixer.music.play(-1)
        except pygame.error as err:
                print(err)
        self.__completed = False
        self.__gameOver = False
        pygame.display.set_caption("Simon Mini-Game")
        self.__screen = pygame.display.set_mode((640, 480))
        # sets up the font
        self.__font = pygame.font.SysFont("Helvetica", 20, bold=True,
                                          italic=False)
        # keep the time of the game
        self.__clock = pygame.time.Clock()
        # self.__sequence is the list that holds the patterns of pygame
        self.__sequence = []
        self.__numList = []
        self.__pressList = []
        # keyFlag are flags that indicate if a key is pressed
        self.__keyFlag = False
        # pygame.draw.rect(surface, color, (x, y, width, height)
        self.makeYellowRect()
        self.makeRedRect()
        self.makeBlueRect()
        self.makeGreenRect()
        self.__score = 0
        self.__state = 0
        self.__mode = "Mini Game"
        self.__waitForInput = False

    def makeYellowRect(self):
        yellowRect = pygame.draw.rect(self.__screen, (155, 155, 0),
                                      (60, 65, 150, 150))
        return yellowRect

    def makeRedRect(self):
        redRect = pygame.draw.rect(self.__screen, (155, 0, 0),
                                   (60, 250, 150, 150))
        return redRect

    def makeBlueRect(self):
        blueRect = pygame.draw.rect(self.__screen, (0, 0, 155),
                                    (250, 65, 150, 150))
        return blueRect

    def makeGreenRect(self):
        greenRect = pygame.draw.rect(self.__screen, (0, 155, 0),
                                     (250, 250, 150, 150))
        return greenRect

    def makeBrightYellowRect(self):
        brightYellowRect = pygame.draw.rect(self.__screen, (255, 255, 0),
                                            (60, 65, 150, 150))
        return brightYellowRect

    def makeBrightRedRect(self):
        brightRedRect = pygame.draw.rect(self.__screen, (255, 0, 0),
                                         (60, 250, 150, 150))
        return brightRedRect

    def makeBrightBlueRect(self):
        brightBlueRect = pygame.draw.rect(self.__screen, (0, 0, 255),
                                          (250, 65, 150, 150))
        return brightBlueRect

    def makeBrightGreenRect(self):
        brightGreenRect = pygame.draw.rect(self.__screen, (0, 255, 0),
                                           (250, 250, 150, 150))
        return brightGreenRect

    def findInput(self):
        # defines keys
        keys = pygame.key.get_pressed()
        if self.__state != 1:
            # space key starts the game
            if keys[pygame.K_SPACE] and self.__state == 0:
                self.__state = 1
            # If player loses (what 3 stands for), player
            # presses "enter" and
            # player should get choice to restart this mini game or
            # quit entirely.
            if keys[pygame.K_RETURN] and self.__mode == "Mini Game":
                # this just restarts the mini game from the beginning
                self.__init__()
            if keys[pygame.K_RETURN] and self.__mode == "Story" and \
                    self.__state == 3:
                # this just restarts the mini game from the beginning
                self.__init__()

            # Allows player to quit game if not playing and press Q
            if keys[pygame.K_q]:
                self.__state = 3
                try:
                    pygame.mixer.music.stop()
                    gameOver = pygame.mixer.Sound('game over.ogg')
                    gameOver.set_volume(.5)
                    gameOver.play(0)
                except pygame.error as err:
                    print(err)
                self.__gameOver = True

    # Narrative: Creates a random color Sequence.
    def createSequence(self):
        for x in range(5):
            # picks a random number between 1 through 4
            # 1 equals Yellow, 2 equals Red, 3 equals Blue
            # 4 equals Green
            randomNum = random.randint(1, 4)
            # RandomNum is put into another list
            # Therefore, a two dimensional list is created
            self.__sequence.append([randomNum])

    # Narrative: Determines if the keys have been pressed and RETURNS
    # it to the corresponding number (which corresponds to specific color)
    def pressKey(self, event):
        if self.__state == 1:
            try:
                for event in pygame.event.get():
                    # If the user wants to exit out of the program pygame.QUIT
                    # will stop the game/end the while loop
                    if event.type == pygame.QUIT:
                        self.__state = 3
                        self.__gameOver = True
                if event.key == K_t:
                    # calls makes the sound and flash when user presses keys
                    return [1]
                if event.key == K_g:
                    return [2]
                if event.key == K_y:
                    return [3]
                if event.key == K_h:
                    return [4]
                if event.key == K_q:
                    self.__state = 3
                    self.__gameOver = True
            except AttributeError:
                print("Sorry Something went wrong try again!")
                self.__state = 3
                self.__gameOver = True

            except pygame.error as err:
                print(err)
                self.__state = 3
                self.__gameOver = True

    def gameFlashBrightRect(self):
        # self.__sequence holds all of the random elements generated by computer
        # self.__numList is made in order to do a comparison with the user input
        for num in self.__sequence:
            self.__numList.append(num)
            for item in self.__numList:
                # Time so game is not immediate
                pygame.time.delay(200)
                if item == [1]:
                    self.makeBrightYellowRect()
                    try:
                        simonSound1 = pygame.mixer.Sound("simonSound1.ogg")
                        simonSound1.play(0)
                    except pygame.error as err:
                        print(err)
                    # first wait time is wait until it goes to a new color
                    pygame.display.update()
                    # the second wait time is how long the color is bright
                    pygame.time.delay(300)
                    self.makeYellowRect()
                elif item == [2]:
                    self.makeBrightRedRect()
                    try:
                        simonSound2 = pygame.mixer.Sound("simonSound2.ogg")
                        simonSound2.play(0)
                    except pygame.error as err:
                        print(err)
                    pygame.display.update()
                    pygame.time.delay(300)
                    self.makeRedRect()
                elif item == [3]:
                    self.makeBrightBlueRect()
                    try:
                        simonSound3 = pygame.mixer.Sound("simonSound3.ogg")
                        simonSound3.play(0)
                    except pygame.error as err:
                        print(err)
                    pygame.display.update()
                    pygame.time.delay(300)
                    self.makeBlueRect()
                else:
                    self.makeBrightGreenRect()
                    try:
                        simonSound4 = pygame.mixer.Sound("simonSound4.ogg")
                        simonSound4.play(0)
                    except pygame.error as err:
                        print(err)
                    pygame.time.wait(250)
                    pygame.display.update()
                    pygame.time.delay(300)
                    self.makeGreenRect()
                pygame.display.update()

            # Must have following if statement for a non-empty
            # numList because if the empty list past through
            # the code an error would occur
            # If the numberList not empty:
            # give the wait times
            if not self.__numList == []:
                numListLength = len(self.__numList)
                if numListLength == 1:
                    pygame.time.delay(2000)
                elif 1 < numListLength <= 3:
                    pygame.time.delay(4000)
                else:
                    pygame.time.delay(7000)
            # Determines if a key. was pressed
            # Sets the self.__keyFlag to True if button is pressed
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.__keyFlag = True
            # If the key was pressed:
            if self.__keyFlag:
                # Calls the pressKey function that returns
                # the number associated with the color
                # pressed by the user
                # That number is appended to the empty list (pressList).
                try:
                    self.__pressList.append(self.pressKey(event))
                except AttributeError:
                    print("Sorry Something went wrong try again!")
                    self.__state = 3
                    self.__gameOver = True
                except pygame.error as err:
                    print(err)
                    self.__state = 3
                    self.__gameOver = True

            # Compares the user input to the actual sequence
            if self.__pressList == self.__numList:
                self.__score += 1
                self.displayScore()
                try:
                    # plays sounds indicating user inputted correctly
                    pygame.mixer.music.stop()
                    oneUp = pygame.mixer.Sound("smw_1-up.wav")
                    oneUp.play(0)
                except pygame.error as err:
                    print(err)
                # Screen is updated for the score to show
                pygame.display.update()
            else:
                # state 3 = game over
                self.__state = 3
                try:
                    pygame.mixer.music.stop()
                    gameOver = pygame.mixer.Sound('game over.ogg')
                    gameOver.set_volume(.5)
                    gameOver.play(0)
                except pygame.error as err:
                    print(err)
                self.__gameOver = True
                # loop will end with this keyword break because
                # the game was over
                break

    def displayScore(self):
        # stops scores/lives from overlaying on top of each other
        pygame.draw.rect(self.__screen, (0, 0, 0), (0, 0, 640, 30))
        # creates an image (or surface) with text
        # font.render("text", anti alias, color)
        # anti alias is a boolean and if true has smooth edges on text
        # can have optional background color argument
        fontSurface = self.__font.render("SCORE: " + str(self.__score), True,
                                         (255, 255, 255))
        # this draws a source surface onto another surface (screen)
        # surface.blit(source surface, (top-left corner coordinates of source))
        self.__screen.blit(fontSurface, (180, 10))

    def message(self):
        # stops messages from overlaying on top of each other
        pygame.draw.rect(self.__screen, (0, 0, 0), (0, 430, 640, 30))
        if self.__state == 0:
            message = "Press SPACE to start or Q to quit."
        elif self.__state == 2:
            if self.__mode == "Story":
                message = "You won! Press Q to continue story mode"
            else:
                message = "You won! Press ENTER to play again or Q to quit"
        else:
            message = "Game over. Press ENTER to play again or Q to quit"
        # creates an image (or surface) with text
        # font.render("text", anti alias, color)
        # anti alias is a boolean and if true has smooth edges on text
        # can have optional background color argument
        fontSurface = self.__font.render(message, True, (255, 255, 255))
        # this draws a source surface onto another surface (screen)
        # surface.blit(source surface, (top-left corner coordinates of source))
        self.__screen.blit(fontSurface, (30, 430))

    def displayInstructions(self):
        # displays the instructions :)
        pygame.draw.rect(self.__screen, (0, 0, 0), (400, 30, 250, 200))

        instructionsLabel = self.__font.render("Instructions:",
                                               True, (255, 255, 255))
        instructions = self.__font.render("Match the pattern 5x", True,
                                          (255, 255, 255))
        instructionsYB = self.__font.render("T = Yellow   Y = Blue",
                                            True, (255, 255, 255))
        instructionsRG = self.__font.render("G = Red   H = Green",
                                            True, (255, 255, 255))
        # puts the text on the window
        self.__screen.blit(instructionsLabel, (460, 30))
        self.__screen.blit(instructions, (420, 60))
        self.__screen.blit(instructionsYB, (420, 90))
        self.__screen.blit(instructionsRG, (420, 120))

    def runSimon(self, mode):
        while not self.__completed:
            # while game is over but still running, displays a message
            # to start over or totally quit
            while self.__gameOver:
                self.displayScore()
                if self.__state != 1:
                    self.message()
                pygame.display.update()

                # determines if user wants to quit or continue
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.__gameOver = False
                        self.__completed = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.__gameOver = False
                            self.__completed = True
                        if event.key == pygame.K_RETURN and \
                                self.__mode == "Mini Game":
                            # starts game over from beginning
                            self.__init__()
                        if event.key == pygame.K_RETURN and \
                                self.__state == 3 and self.__mode == "Story":
                            # starts game over from beginning
                            self.__init__()

            # pygame.event.get() gets input from computer
            for event in pygame.event.get():
                # If the user wants to exit out of the program pygame.QUIT
                # will stop the game/end the while loop
                if event.type == pygame.QUIT:
                    self.__state = 3
                    try:
                        pygame.mixer.music.stop()
                        gameOver = pygame.mixer.Sound('game over.ogg')
                        gameOver.set_volume(.5)
                        gameOver.play(0)
                    except pygame.error as err:
                        print(err)
                    self.__gameOver = True

            # sets frame rate to no more than 50 frames per second
            self.__clock.tick(50)
            self.findInput()
            self.__mode = mode
            # state 1 = play mode
            if self.__state == 1:
                # stops messages from showing up during play
                pygame.draw.rect(self.__screen, (0, 0, 0), (0, 430, 640, 50))
                self.createSequence()
                self.gameFlashBrightRect()
            if self.__score == 5:
                # state 2 = game won
                self.__state = 2
                try:
                    pygame.mixer.music.stop()
                    win = pygame.mixer.Sound("World Clear.ogg")
                    win.play(0)
                except pygame.error as err:
                        print(err)
                self.__gameOver = True
            self.displayScore()
            self.message()
            self.displayInstructions()
            pygame.display.update()

        # stops all sounds from playing
        pygame.mixer.stop()

        if self.__mode == "Story":
            # returns the game state (not playing, playing, win, or game over)
            # back to story mode
            return self.__state
