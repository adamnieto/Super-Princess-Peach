import SpriteSheet
import pygame
import BrickBreaker
import Simon
import Snake
import Credits
import GameOver


class StoryMode:
    # (x, y) is coordinate where peach starts
    def __init__(self, x, y):
        pygame.init()
        try:
            pygame.mixer.music.load('05-super-mario-64-main-theme.wav')
            pygame.mixer.music.set_volume(.5)
            # -1 means that the music infinitely play while game is playing
            pygame.mixer.music.play(-1)
        except pygame.error as err:
            print(err)
        self.__screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Story Mode")
        self.__black = (0, 0, 0)
        self.__white = (255, 255, 255)
        # refers to starting coordinates
        self.__x = x
        self.__y = y
        # Initially peach does not move anywhere
        self.__moveX = 0
        self.__moveY = 0
        # Initializes the clock
        self.__clock = pygame.time.Clock()
        # Frame rate
        self.__FPS = 50
        self.__completed = False
        self.__mode = "Story"
        # state 1 is the game (story mode) is in play / running
        self.__state = 1
        # state 0 is game (mini game) is not in play
        self.__brickBreakerState = 0
        self.__simonState = 0
        self.__snakeState = 0

        # These are the rectangular areas / coordinates of rects which
        # are behind the castle images so that we can track
        # if peach has collided with a castle
        self.__smallCastle1Rect = pygame.Rect(96, 352, 32, 32)
        self.__smallCastle2Rect = pygame.Rect(256, 352, 32, 32)
        self.__bigCastleRect = pygame.Rect(416, 352, 32, 32)
        self.__peachCastleRect = pygame.Rect(576, 352, 32, 32)

        # this takes the images from sprite sheet
        peachSS = SpriteSheet.SpriteSheet("peach_spritesheet.gif")
        # Sprite 0 is 20x35 pixels at location (445, 69)
        # the first part is the rectangular area
        # the second part makes the image transparent so black doesnt
        # show up around the image
        # (how far the top left corner is from the edge of the left screen,
        # how far the top left corner is from the top of screen,
        # width of image, height of image,
        # makes the background transparent)
        # Transition of her turning to the left
        self.__peachLeft0 = peachSS.image_at((445, 69, 20, 36), (0, 0, 0))
        self.__peachLeft1 = peachSS.image_at((418, 70, 19, 34), (0, 0, 0))
        self.__peachLeft2 = peachSS.image_at((394, 70, 19, 35), (0, 0, 0))
        self.__peachLeft3 = peachSS.image_at((368, 71, 21, 35), (0, 0, 0))
        self.__peachLeft4 = peachSS.image_at((344, 72, 21, 34), (0, 0, 0))
        self.__peachLeft5 = peachSS.image_at((318, 72, 23, 34), (0, 0, 0))
        self.__peachLeft6 = peachSS.image_at((294, 72, 20, 35), (0, 0, 0))
        self.__peachLeft7 = peachSS.image_at((268, 71, 22, 37), (0, 0, 0))

        # makes a list of the images
        self.__peachLeftList = [self.__peachLeft0, self.__peachLeft1,
                                self.__peachLeft2, self.__peachLeft3,
                                self.__peachLeft4, self.__peachLeft5,
                                self.__peachLeft6, self.__peachLeft7]

        # flips all the images in self.__peachLeftList and
        # appends to new list
        # pygame.transform.flip(image surface, flip_x, flip_y)
        # this list makes peach look like she is walking right
        self.__peachRightList = []
        for image in self.__peachLeftList:
            self.__peachRightList.append(
                    pygame.transform.flip(image, True, False))
        # Makes Peach move side to side in forward position
        self.__peachForward0 = peachSS.image_at((271, 33, 19, 34), (0, 0, 0))
        self.__peachForward1 = peachSS.image_at((294, 34, 22, 34), (0, 0, 0))
        self.__peachForward2 = peachSS.image_at((322, 34, 19, 34), (0, 0, 0))
        self.__peachForward3 = peachSS.image_at((344, 33, 21, 34), (0, 0, 0))
        self.__peachForward4 = peachSS.image_at((369, 34, 20, 36), (0, 0, 0))
        self.__peachForward5 = peachSS.image_at((392, 34, 22, 33), (0, 0, 0))
        self.__peachForward6 = peachSS.image_at((417, 34, 20, 34), (0, 0, 0))
        self.__peachForward7 = peachSS.image_at((445, 34, 19, 34), (0, 0, 0))

        self.__peachForwardList = [self.__peachForward0, self.__peachForward1,
                                   self.__peachForward2, self.__peachForward3,
                                   self.__peachForward4, self.__peachForward5,
                                   self.__peachForward6, self.__peachForward7]

        # this allows me to change the image depending on the num
        # self.__imageNum acts as the index
        self.__imageNum = 0
        self.__direction = "Forward"
        # The direction list is equal to the forward list
        self.__directionList = self.__peachForwardList
        # Updates current image by using the imageNum as the index for the
        # Sets current image on screen to the direction list at
        # the specific index
        self.__currentImage = self.__directionList[self.__imageNum]

        # allows image to change only every 5 frames
        self.__timeTarget = 5
        # keeps amount number of times it has
        # gone through the while loop
        self.__timeNum = 0

    # allows sprite to change depending on the current image / image num
    def updateSprite(self, peach):
        self.__timeNum += 1
        if self.__timeNum == self.__timeTarget:
            # allows the image to change depending on current image
            # 8 images of peach, if imageNum (index) less than 7
            # it will count next index
            if self.__imageNum < 7:
                self.__imageNum += 1
                # refers to next image of peach in self.__directionList
                self.__currentImage = self.__directionList[self.__imageNum]
            else:
                # Resets everything at the beginning of the list
                self.__imageNum = 0
                self.__currentImage = self.__directionList[self.__imageNum]
            self.__timeNum = 0

        self.renderPeach(peach)

    # draws/blits the image onto the screen depending on current image
    # peach is equal to her coordinates
    def renderPeach(self, peach):
        # peach.__x gives her x coordinate and peach.__y gives y coordinate
        # +6 and +20 hides the rectangle behind peach
        peachRect = pygame.Rect(peach.__x + 6, peach.__y + 20, 5, 5)
        for image in self.__directionList:
            # if the current image is equal to an image in the direction list
            # a rectangle is drawn behind peach
            if self.__currentImage == image:
                # this creates a rect on peach so that I can track collisions
                # with the castle rects
                peachRect = pygame.draw.rect(self.__screen, (255, 105, 180),
                                             peachRect)
                self.__screen.blit(image, (self.__x, self.__y))

        self.handleCastleCollision(peach, peachRect)

    def renderLogo(self):
        try:
            peachSign = pygame.image.load("super_princess_peach_logo.gif")
            peachSign = pygame.transform.scale(peachSign, (400, 120))
            self.__screen.blit(peachSign, (120, 6))
        except pygame.error as err:
            print(err)

    def renderGround(self):
        landSS = SpriteSheet.SpriteSheet("land_spritesheet.gif")

        grass = landSS.image_at((219, 482, 64, 9), (0, 0, 0))
        # makes grass bigger
        grass = pygame.transform.scale(grass, (650, 40))
        self.__screen.blit(grass, (0, 375))

        ground = landSS.image_at((214, 492, 64, 15), (0, 0, 0))
        # makes ground larger
        ground = pygame.transform.scale(ground, (640, 70))
        self.__screen.blit(ground, (0, 410))

    def renderCastle(self):
        castleSS = SpriteSheet.SpriteSheet("bowserCastle_spritesheet.gif")

        pole = castleSS.image_at((183, 559, 2, 14), (0, 0, 0))
        pole = pygame.transform.scale(pole, (5, 40))
        bowserFlag = castleSS.image_at((179, 521, 17, 16), (0, 0, 0))
        peachFlag = castleSS.image_at((185, 555, 12, 12), (0, 0, 0))

        # green bowser flag if peach hasn't yet won mini game / castle
        # orange flag if peach has won the mini game / castle
        if self.__brickBreakerState != 2:
            self.__screen.blit(pole, (107, 278))
            self.__screen.blit(bowserFlag, (112, 277))
        else:
            self.__screen.blit(pole, (107, 278))
            self.__screen.blit(peachFlag, (112, 277))
        smallCastle1 = castleSS.image_at((6, 485, 96, 81), (0, 0, 0))
        smallCastle1 = pygame.transform.scale(smallCastle1, (80, 80))
        self.__screen.blit(smallCastle1, (70, 310))

        if self.__simonState != 2:
            self.__screen.blit(pole, (267, 278))
            self.__screen.blit(bowserFlag, (272, 277))
        else:
            self.__screen.blit(pole, (267, 278))
            self.__screen.blit(peachFlag, (272, 277))
        smallCastle2 = castleSS.image_at((6, 485, 96, 81), (0, 0, 0))
        smallCastle2 = pygame.transform.scale(smallCastle2, (80, 80))
        self.__screen.blit(smallCastle2, (230, 310))

        if self.__snakeState != 2:
            self.__screen.blit(pole, (417, 258))
            self.__screen.blit(bowserFlag, (422, 257))
        else:
            self.__screen.blit(pole, (417, 258))
            self.__screen.blit(peachFlag, (422, 257))
        bigCastle = castleSS.image_at((236, 452, 160, 177), (0, 0, 0))
        bigCastle = pygame.transform.scale(bigCastle, (100, 100))
        self.__screen.blit(bigCastle, (370, 290))

        peachCastleSS = SpriteSheet.SpriteSheet("peach_castle.png")
        peachCastle = peachCastleSS.image_at((24, 20, 188, 153), (0, 0, 0))
        peachCastle = pygame.transform.scale(peachCastle, (100, 100))
        self.__screen.blit(peachCastle, (520, 290))
        try:
            if self.__state == 2:
                mario = pygame.image.load("marioSprite.png")
                mario = pygame.transform.scale(mario, (45, 45))
                # mario appears near peach's castle if game is won
                self.__screen.blit(mario, (605, 350))
        except pygame.error as err:
            print(err)

    def renderSpeechBubble(self):
        speechBubbleSS = SpriteSheet.SpriteSheet(
                "speech_bubble_large_spritesheet.png")
        speechBubble = speechBubbleSS.image_at((33, 0, 31, 29), (0, 0, 0))
        speechBubble = pygame.transform.scale(speechBubble, (250, 250))
        self.__screen.blit(speechBubble, (12, 90))

    def renderBowser(self):
        try:
            bowser = pygame.image.load("bowser.png")
            bowser = pygame.transform.scale(bowser, (60, 60))
            bowser = pygame.transform.flip(bowser, True, False)
            self.__screen.blit(bowser, (42, 150))
        except pygame.error as err:
            print(err)

    def renderMario(self):
        try:
            mario = pygame.image.load("marioSprite.png")
            mario = pygame.transform.scale(mario, (50, 50))
            self.__screen.blit(mario, (172, 155))
        except pygame.error as err:
            print(err)

    def writeMessage1(self):
        font = pygame.font.SysFont("Calibri", 20, bold=False)
        message1 = font.render("kidnapped", 1, (250, 0, 250))
        self.__screen.blit(message1, (104, 175))

    def writeMessage2(self):
        font2 = pygame.font.SysFont("Calibri", 20, bold=False)
        message2 = font2.render("PLEASE HELP SAVE MARIO!", 1, (250, 0, 250))
        self.__screen.blit(message2, (42, 220))

    def findInput(self):
        keys = pygame.key.get_pressed()

        # if keys[pygame.K_LEFT]:
        #     # causes the x coordinate to change -5 pixels (left)
        #     self.__moveX = -3
        #     # causes the y coordinate to stay constant
        #     self.__moveY = 0
        #     self.__direction = "Left"
        #     self.__directionList = self.__peachLeftList

        # make elif in order to go right
        if keys[pygame.K_RIGHT]:
            self.__moveX = 3
            self.__direction = "Right"
            self.__directionList = self.__peachRightList

        else:
            self.__moveX = 0
            self.__direction = "Forward"
            self.__directionList = self.__peachForwardList

    def renderCastleRects(self):
        # Draws rectangles behind the castle images so that we can track
        # if peach has collided with a castle
        self.__smallCastle1Rect = pygame.draw.rect(self.__screen, (255, 0, 0),
                                                   self.__smallCastle1Rect)
        self.__smallCastle2Rect = pygame.draw.rect(self.__screen, (255, 0, 0),
                                                   self.__smallCastle2Rect)
        self.__bigCastleRect = pygame.draw.rect(self.__screen, (255, 0, 0),
                                                self.__bigCastleRect)
        self.__peachCastleRect = pygame.draw.rect(self.__screen, (255, 0, 0),
                                                  self.__peachCastleRect)

    def handleCastleCollision(self, peach, peachRect):
        # if the rect behind peach collides with the rects behind the castles
        # either a mini game will play or story mode will be completed
        if peachRect.colliderect(self.__smallCastle1Rect):
            self.runBrickBreaker()
            # peach's new coordinates (located after the castle)
            # this is so the mini game won't constantly play
            # because otherwise peach will still be colliding with the castle
            self.__moveX = 50
            peach.__x += self.__moveX
        if peachRect.colliderect(self.__smallCastle2Rect):
            self.runSimon()
            # peach's new coordinates (located after the castle)
            self.__moveX = 50
            peach.__x += self.__moveX
        if peachRect.colliderect(self.__bigCastleRect):
            self.runSnake()
            # peach's new coordinates (located after the castle)
            self.__moveX = 50
            peach.__x += self.__moveX
        if peachRect.colliderect(self.__peachCastleRect):
            # StoryMode is completed
            self.__completed = True

    def runBrickBreaker(self):
        pygame.mixer.music.stop()
        brickBreakerGame = BrickBreaker.BrickBreaker()
        self.__brickBreakerState = brickBreakerGame.runBrickBreaker(self.__mode)
        # if they did not win:
        if self.__brickBreakerState != 2:
            # they lost story mode if 3
            self.__state = 3
            self.__completed = True
        try:
            pygame.mixer.music.load('05-super-mario-64-main-theme.wav')
            pygame.mixer.music.set_volume(.5)
            pygame.mixer.music.play(-1)
        except pygame.error as err:
            print(err)

    def runSimon(self):
        pygame.mixer.music.stop()
        simon = Simon.Simon()
        self.__simonState = simon.runSimon(self.__mode)
        if self.__simonState != 2:
            self.__state = 3
            self.__completed = True
        try:
            pygame.mixer.music.load('05-super-mario-64-main-theme.wav')
            pygame.mixer.music.set_volume(.5)
            pygame.mixer.music.play(-1)
        except pygame.error as err:
            print(err)

    def runSnake(self):
        pygame.mixer.music.stop()
        snake = Snake.Snake()
        self.__snakeState = snake.runSnake(self.__mode)
        if self.__snakeState != 2:
            self.__state = 3
            self.__completed = True
        else:
            # you win!
            self.__state = 2
        try:
            pygame.mixer.music.load('05-super-mario-64-main-theme.wav')
            pygame.mixer.music.set_volume(.5)
            pygame.mixer.music.play(-1)
        except pygame.error as err:
            print(err)

    def runStoryMode(self, peach):
        while not self.__completed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__completed = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.__completed = True

            # fills screen blue only in select rectangular area (sky)
            self.__screen.fill((110, 193, 248), rect=(0, 0, 640, 384))
            # fills screen green only in select rectangular area (grass/ground)
            self.__screen.fill((0, 155, 0), rect=(0, 384, 640, 96))

            self.findInput()

            # Causes the sprite's x coordinate to change accordingly
            peach.__x += self.__moveX

            # if sprite hits edge of screen, it will stop there
            if peach.__x <= 0:
                peach.__x = 0
            if peach.__x >= 620:
                peach.__x = 620

            # writes the super princess peach logo
            self.renderLogo()

            self.renderCastleRects()

            startingPointsX = []
            # while peach is before the first castle the sign will show
            for x in range(100):
                startingPointsX.append(x)
            startingPointsY = [355]
            if peach.__x in startingPointsX and peach.__y in startingPointsY:
                self.renderSpeechBubble()
                self.renderBowser()
                self.renderMario()
                self.writeMessage1()
                self.writeMessage2()

            self.renderGround()
            self.renderCastle()

            # associates the sprite with the image in updateSprite()
            peach.updateSprite(peach)

            # self.__FPS stands for frames per second
            self.__clock.tick(self.__FPS)

            pygame.display.update()

        # stops all music from playing
        pygame.mixer.music.stop()

        if self.__state == 2:
            # You won
            playCredits = Credits.Credits()
            playCredits.runCredits()
        else:
            # you lost, game over
            playGameOver = GameOver.GameOver()
            playGameOver.runGameOver()
