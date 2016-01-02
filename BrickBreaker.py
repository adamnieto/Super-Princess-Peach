import pygame


class BrickBreaker:

    def __init__(self):
        # initializes pygame
        pygame.init()
        try:
            pygame.mixer.music.load('Overworld.ogg')
            # sets the volume lower -- .set_volume(x) where x is between 0 and 1
            pygame.mixer.music.set_volume(.5)
            # at -1, the song/music repeats.
            pygame.mixer.music.play(-1)
        except pygame.error as err:
            print(err)
        # sets the width and height of screen
        self.__screenSize = (640, 480)
        self.__screen = pygame.display.set_mode(self.__screenSize)
        pygame.display.set_caption("Brick Breaker Mini-Game")
        # used to control the frame rate of game
        self.__clock = pygame.time.Clock()
        self.__score = 0
        self.__lives = 3
        # state starts with ball on paddle
        self.__state = 0
        self.__blockX = 300
        # Rect stores rectangular coordinates/areas = (x, y, width, height)
        self.__block = pygame.Rect((self.__blockX, 445, 60, 10))
        self.__ballX = self.__blockX + 23
        self.__ball = pygame.Rect(self.__ballX, 430, 7, 7)

        # causes ball to go in up-right direction
        self.__ballVelocity = [5, -5]
        self.__bricks = []
        self.__brick = None
        # retrieves a font from system.
        # pygame.font.SysFont(name, size, bold=boolean, italic=boolean)
        self.__font = pygame.font.SysFont("Helvetica", 20, bold=True,
                                          italic=False)
        self.__completed = False
        self.__gameOver = False
        self.__mode = "Mini Game"

        self.createBricks()

    def createColor(self, startY):
        if startY == 35:
            # red
            color = (255, 0, 0)
        elif startY == 55:
            # orange
            color = (255, 140, 0)
        elif startY == 75:
            # yellow
            color = (255, 255, 0)
        elif startY == 95:
            # green
            color = (50, 205, 50)
        elif startY == 115:
            # light blue
            color = (0, 191, 255)
        elif startY == 135:
            # dark blue
            color = (0, 0, 205)
        else:
            # purple
            color = (148, 0, 211)
        return color

    def createBricks(self):
        # Starting y coordinate of brick
        startY = 35
        # Number of rows
        for rows in range(7):
            # Starting x coordinate for brick
            startX = 29
            # Number of columns
            for columns in range(8):
                # Brick width is 60
                # Brick height is 15
                # pygame.draw.rect(screen, color, (x,y,width,height), thickness)
                rowColor = self.createColor(startY)
                self.__brick = pygame.Rect(startX, startY, 60, 15)
                self.__brick = pygame.draw.rect(self.__screen, rowColor,
                                                self.__brick)
                self.__bricks.append(self.__brick)
                # Makes the next brick an extra 15 x-coordinates over
                startX += 75
            # Makes the next brick an extra 10 y-coordinates over
            startY += 20

    def findInput(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            # moves both ball and block to left while game not playing
            if self.__state == 0:
                # moves the left side of block 10 pixels to left
                # if you change number, the block will change speed
                self.__block.left -= 10
                # ensures the left side of the block doesnt go past
                # the left side of the screen (0)
                if self.__block.left < 0:
                    self.__block.left = 0

                # moves the ball as you move the block if state = 0
                # moves the left side of the ball 10 pixels to the left
                # if you change number, the ball will change speed
                self.__ball.left -= 10
                # ensures the ball stays in middle of block but doesnt go
                # past pixel 23 (where ball stays in middle of block but
                # doesnt go past the left side of the screen)
                if self.__ball.left < 23:
                    self.__ball.left = 23

            # moves only block to left while game is playing
            if self.__state > 0:
                # moves the left side of block 10 pixels to left
                # if you change number, the block will change speed
                self.__block.left -= 10
                # ensures the left side of the block doesnt go past
                # the left side of the screen (0)
                if self.__block.left < 0:
                    self.__block.left = 0

        if keys[pygame.K_RIGHT]:
            # moves both ball and block to right while game not playing
            if self.__state == 0:
                # moves the left side of block 10 pixels to right
                # if you change number, the block will change speed
                self.__block.left += 10
                # ensures right side of block doesnt go past
                # the right side of the screen (640)
                if self.__block.right > 640:
                    self.__block.right = 640

                # moves the ball as you move the block if state = 0
                # moves the left side ball 10 pixels to the right
                # if you change number, the ball will change speed
                self.__ball.left += 10
                # ensures the ball stays in middle of block but doesnt go
                # past pixel 617 (where ball stays in middle of block but
                # doesnt go past the right side of the screen)
                if self.__ball.right > 617:
                    self.__ball.right = 617

            # moves only block to right while game is playing
            if self.__state > 0:
                # moves the left side of block 10 pixels to right
                # if you change number, the block will change speed
                self.__block.left += 10
                # ensures right side of block doesnt go past
                # the right side of the screen (640)
                if self.__block.right > 640:
                    self.__block.right = 640

        # If player presses space and the ball is on the paddle,
        # the ball starts to go in up-right direction and
        # ball is launched (what the 1 stands for)
        if keys[pygame.K_SPACE] and self.__state == 0:
            self.__ballVelocity = [5, -5]
            self.__state = 1
            if self.__lives < 3:
                try:
                    pygame.mixer.music.play(-1)
                except pygame.error as err:
                    print(err)

        # Allows player to quit game if not playing and press Q
        if keys[pygame.K_q]:
            if self.__state != 2:
                self.__state = 3
            try:
                pygame.mixer.music.stop()
                gameOver = pygame.mixer.Sound('game over.ogg')
                gameOver.set_volume(.5)
                gameOver.play(0)
            except pygame.error as err:
                print(err)
            self.__gameOver = True

    def moveBall(self):
        # To change the ball speed multiply the velocity by a number
        self.__ball.left += (1.2 * self.__ballVelocity[0])
        self.__ball.top += (1.2 * self.__ballVelocity[1])

        # stops the left side of ball from going further than screen on left
        if self.__ball.left <= 0:
            self.__ball.left = 0
            self.__ballVelocity[0] = -self.__ballVelocity[0]
        # stops right side of ball from going further than screen on right
        elif self.__ball.right >= 640:
            self.__ball.right = 640
            self.__ballVelocity[0] = -self.__ballVelocity[0]

        # stops the top of ball from going further than top of screen
        if self.__ball.top < 0:
            self.__ball.top = 0
            self.__ballVelocity[1] = -self.__ballVelocity[1]
        # stops the bottom of ball from going below bottom of screen
        elif self.__ball.bottom > 480:
            self.__ball.bottom = 480
            self.__ballVelocity[1] = -self.__ballVelocity[1]

    def collision(self):
        for self.__brick in self.__bricks:
            if self.__ball.colliderect(self.__brick):
                self.__score += 1
                # Remember self.__ballVelocity = [5, -5]. Velocity has
                # has become [5, 5]. Makes the ball change direction after there
                # has been a collision.
                self.__ballVelocity[1] = -self.__ballVelocity[1]
                self.__bricks.remove(self.__brick)
                self.__brick = pygame.draw.rect(self.__screen, (0, 0, 0),
                                                self.__brick)
                try:
                    brickSmash = pygame.mixer.Sound('smb_breakblock.wav')
                    brickSmash.play(0)
                except pygame.error as err:
                    print(err)
                break

        if len(self.__bricks) == 0:
            # state 2 = game won
            self.__state = 2
            try:
                pygame.mixer.music.stop()
                gameWon = pygame.mixer.Sound('World Clear.ogg')
                gameWon.play(0)
            except pygame.error as err:
                print(err)
            self.__gameOver = True

        if self.__ball.colliderect(self.__block):
            # (445 - 14) = Block Y Coordinate minus ball diameter
            self.__ball.top = (445 - 14)
            self.__ballVelocity[1] = -self.__ballVelocity[1]

        # if the bottom of the ball hits the bottom of the screen,
        # a life is lost
        elif self.__ball.bottom == 480:
            self.__lives -= 1
            if self.__lives > 0:
                try:
                    pygame.mixer.music.stop()
                    lifeLost = pygame.mixer.Sound('Life Lost.ogg')
                    lifeLost.play(0)
                except pygame.error as err:
                    print(err)
                # restarts with ball and block back in middle of screen
                self.__state = 0
                self.__blockX = 300
                self.__block = pygame.Rect((self.__blockX, 445, 60, 10))
                self.__ballX = self.__blockX + 20
                self.__ball = pygame.Rect(self.__ballX, 430, 7, 7)
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

    def displayScoreLives(self):
        # stops scores/lives from overlaying on top of each other
        pygame.draw.rect(self.__screen, (0, 0, 0), (0, 0, 640, 25))
        # creates an image (or surface) with text
        # font.render("text", anti alias, color)
        # anti alias is a boolean and if true has smooth edges on text
        # can have optional background color argument
        fontSurface = self.__font.render("SCORE: " + str(self.__score) +
                                         "    LIVES: " + str(self.__lives), True,
                                         (255, 255, 255))
        # this draws a source surface onto another surface (screen)
        # surface.blit(source surface, (top-left corner coordinates of source))
        self.__screen.blit(fontSurface, (205, 5))

    def message(self):
        # stops messages from overlaying on top of each other
        pygame.draw.rect(self.__screen, (0, 0, 0), (40, 270, 640, 100))
        if self.__state == 0:
            directionsMsg = "Clear all the bricks by bouncing" + \
                            " the ball on the block"
            directionsMsgSurface = self.__font.render(directionsMsg, True,
                                                      (255, 255, 255))
            self.__screen.blit(directionsMsgSurface, (50, 270))

            message = "Press SPACE to launch the ball or Q to quit"

            arrowKeyMsg = "Use ARROW KEYS to move the block"
            arrowKeyMsgSurface = self.__font.render(arrowKeyMsg, True,
                                                    (255, 255, 255))
            self.__screen.blit(arrowKeyMsgSurface, (120, 330))

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
        self.__screen.blit(fontSurface, (100, 300))

    def runBrickBreaker(self, mode):
        while not self.__completed:
            # while game is over but still running, displays a message
            # to start over or totally quit
            while self.__gameOver:
                self.displayScoreLives()
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

            # pygame.event.get() makes sure that the windows
            # do not pile up while game is running.
            # If the event that the user clicks is pygame.QUIT
            # it will stop the game or end the loop
            for event in pygame.event.get():
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

            if self.__state == 1:
                # stops messages from overlaying on top of each other
                pygame.draw.rect(self.__screen, (0, 0, 0), (40, 270, 640, 100))
                self.moveBall()
                self.collision()
            else:
                # displays instructions and/or message to user
                self.message()

            # displays the score and lives left
            self.displayScoreLives()

            # draws the block and ball
            # pygame.draw.rect(surface, color, Rect area)
            # Rect stores rectangular coordinates/areas = (x, y, width, height)
            # pygame.draw.circle(surface, color, (center of circle), radius)
            self.__block = pygame.draw.rect(self.__screen, (255, 255, 225),
                                            self.__block)
            self.__ball = pygame.draw.circle(self.__screen, (255, 105, 180),
                                             (self.__ball.left + 7,
                                              self.__ball.top + 7), 7)

            # the pygame.display.flip() allows for any changes you make
            # in the code to become visible on the window (updates screen)
            # the pygame.display.flip() makes changes visible. I created two
            # different colors so we can see the movement / stop overlaying
            pygame.display.flip()

            # stops overlaying
            self.__block = pygame.draw.rect(self.__screen, (0, 0, 0),
                                            self.__block)
            self.__ball = pygame.draw.circle(self.__screen, (0, 0, 0),
                                             (self.__ball.left + 7,
                                              self.__ball.top + 7), 7)
        # stops all sounds from playing
        pygame.mixer.stop()

        if self.__mode == "Story":
            # returns the game state (not playing, playing, win, or game over)
            # back to story mode
            return self.__state
