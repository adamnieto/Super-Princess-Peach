from SpriteSheet import *
import pygame
import random


class Snake:
    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.music.load('Overworld.ogg')
            pygame.mixer.music.set_volume(.5)
            pygame.mixer.music.play(-1)
        except pygame.error as err:
                        print(err)
        self.__score = 0
        self.__screenSize = (640, 480)
        self.__screen = pygame.display.set_mode(self.__screenSize)
        pygame.display.set_caption("Snake Mini-Game")
        self.__clock = pygame.time.Clock()
        # FPS = Frames per second
        self.__FPS = 20
        # initializes snake head coordinates in middle (center) of screen
        self.__head_x = 320
        self.__head_y = 240
        # amount the head x/y coordinates should change
        self.__head_x_change = 0
        self.__head_y_change = 0

        # sets the directions and coordinate changes
        # first element is x coordinate change
        # second element is y coordinate change
        self.__left = [-10, 0]
        self.__right = [10, 0]
        self.__up = [0, -10]
        self.__down = [0, 10]
        self.__direction = [0, 0]

        # block / snake segment size
        self.__snakeSize = 10

        self.__snakeList = []

        # initial whole snake length (only the head at first so 1)
        self.__snakeLength = 1

        # creates the apple at random coordinates but as a multiple of 10
        self.__randAppleX = round(random.randrange(0, 640 - self.__snakeSize) /
                                  10.0) * 10.0
        self.__randAppleY = round(random.randrange(0, 480 - self.__snakeSize) /
                                  10.0) * 10.0

        # this takes the images from sprite sheet
        ss = SpriteSheet("item_spritesheet.png")
        # Sprite is 17x16 pixels at location (128, 192)
        # the first part is the rectangular area
        # the second part makes the image transparent so black doesnt
        # show up around the image
        self.__mushroom = ss.image_at((128, 192, 17, 16), (0, 0, 0))

        # game states
        self.__completed = False
        self.__gameOver = False
        self.__state = 0
        self.__mode = "Mini Game"

        self.__font = pygame.font.SysFont("Helvetica", 20, bold=True,
                                          italic=False)

    def drawSnake(self, snakeSize, snakeList):
        # coordinates are the snakeHead list coordinates
        # [0] is x and [1] is y
        # This draws the rest of the snake body
        for coordinates in snakeList:
            pygame.draw.rect(self.__screen, (255, 105, 180),
                             [coordinates[0], coordinates[1],
                              snakeSize, snakeSize])

    def displayScore(self):
        # creates an image (or surface) with text
        # font.render("text", anti alias, color)
        # anti alias is a boolean and if true has smooth edges on text
        # can have optional background color argument
        fontSurface = self.__font.render("SCORE: " + str(self.__score), True,
                                         (0, 0, 0))
        # this draws a source surface onto another surface (screen)
        # surface.blit(source surface, (top-left corner coordinates of source))
        self.__screen.blit(fontSurface, (260, 10))

    def message(self):
        if self.__state == 0:
            message = "Press SPACE to start or Q to quit."
            # creates an image (or surface) with text
            # font.render("text", anti alias, color)
            # anti alias is a boolean and if true has smooth edges on text
            # can have optional background color argument
            fontSurface = self.__font.render(message, True, (0, 0, 0))
            # this draws a source surface onto another surface (screen)
            # surface.blit(source surface, (top-left corner coordinates
            #  of source))
            self.__screen.blit(fontSurface, (160, 180))

            directions = "Press ARROW KEYS to move"
            directionsSurface = self.__font.render(directions, True, (0, 0, 0))
            self.__screen.blit(directionsSurface, (170, 150))

            goal = "Eat 20 mushrooms to win"
            goalSurface = self.__font.render(goal, True, (0, 0, 0))
            self.__screen.blit(goalSurface, (190, 50))

            rules = "If you hit yourself it's game over"
            rulesSurface = self.__font.render(rules, True, (0, 0, 0))
            self.__screen.blit(rulesSurface, (160, 80))

        elif self.__state == 2:
            if self.__mode == "Story":
                message = "You won! Press Q to continue story mode"
            else:
                message = "You won! Press ENTER to play again or Q to quit"
            fontSurface = self.__font.render(message, True, (0, 0, 0))
            self.__screen.blit(fontSurface, (80, 180))
        else:
            message = "Game over. Press ENTER to play again or Q to quit"
            fontSurface = self.__font.render(message, True, (0, 0, 0))
            self.__screen.blit(fontSurface, (80, 180))

    def runSnake(self, mode):
        # while game is playing
        while not self.__completed:
            # makes screen white
            self.__screen.fill((255, 255, 255))
            # while game is over but still running, displays a message
            # to start over or totally quit
            while self.__gameOver:
                # makes screen white
                self.__screen.fill((255, 255, 255))
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

            # determines what keys are pressed
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

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.__state = 1
                    if event.key == pygame.K_q:
                            self.__state = 3
                            try:
                                pygame.mixer.music.stop()
                                gameOver = pygame.mixer.Sound('game over.ogg')
                                gameOver.set_volume(.5)
                                gameOver.play(0)
                            except pygame.error as err:
                                print(err)
                            self.__gameOver = True
                    if self.__state == 1:
                        # sets the direction of snake
                        # (but ensures it can't go the opposite direction)
                        if event.key == pygame.K_LEFT and \
                                self.__direction != self.__right:
                            self.__direction = self.__left
                        if event.key == pygame.K_RIGHT and \
                                self.__direction != self.__left:
                            self.__direction = self.__right
                        if event.key == pygame.K_UP and \
                                self.__direction != self.__down:
                            self.__direction = self.__up
                        if event.key == pygame.K_DOWN and \
                                self.__direction != self.__up:
                            self.__direction = self.__down

                    # head x/y changes depend on the direction
                    self.__head_x_change = self.__direction[0]
                    self.__head_y_change = self.__direction[1]

            # head_x / head_y is the position of snake head and
            # it changes depending on head_x_change / head_y_change
            self.__head_x += self.__head_x_change
            self.__head_y += self.__head_y_change

            # # if snake head goes past screen, game over
            # if self.__head_x > 640 or self.__head_x < 0 \
            #    or self.__head_y > 480 or self.__head_y < 0:
            #     self.__state = 3
            #     self.__gameOver = True

            self.__mode = mode

            # perhaps for an alternate version of snake
            # if snake goes past screen, will come back on other side of screen
            if self.__head_x < 0:
                self.__head_x = 640
            if self.__head_x > 640:
                self.__head_x = 0
            if self.__head_y < 0:
                self.__head_y = 480
            if self.__head_y > 480:
                self.__head_y = 0

            # draws the mushroom in a random spot
            mushroom = pygame.draw.rect(self.__screen, (255, 255, 255),
                                        [self.__randAppleX, self.__randAppleY,
                                         15, 15])
            self.__screen.blit(self.__mushroom, (self.__randAppleX,
                                                 self.__randAppleY))

            # draws the snake
            snake = pygame.draw.rect(self.__screen, (255, 105, 180),
                                     [self.__head_x, self.__head_y,
                                      self.__snakeSize, self.__snakeSize])

            snakeHead = []
            # appends position of snake to snakeHead List so that the body
            # knows the correct coordinates to follow the head
            snakeHead.append(self.__head_x)
            snakeHead.append(self.__head_y)
            # appends snakeHead List to snakeList so there is a list of
            # full snake positions with each head coordinates within the List
            # i.e. snakeList[ [head_position], [next_head_pos (body 1)], [etc]]
            self.__snakeList.append(snakeHead)

            # deletes the old snake head position
            # if snakeList length is greater than length of whole snake
            # (ensures snake stays the correct length)
            if len(self.__snakeList) > self.__snakeLength:
                del self.__snakeList[0]

            # for each body part in entire snakeList
            for body_part in self.__snakeList[:-1]:
                # if any body part touches another part of the snake, game over
                if body_part == snakeHead:
                    self.__state = 3
                    try:
                        pygame.mixer.music.stop()
                        gameOver = pygame.mixer.Sound('game over.ogg')
                        gameOver.set_volume(.5)
                        gameOver.play(0)
                    except pygame.error as err:
                        print(err)
                    self.__gameOver = True

            # draws rest of snake body
            self.drawSnake(self.__snakeSize, self.__snakeList)

            # displays the score
            self.displayScore()

            # if game not being played, a message displays on screen
            if self.__state != 1:
                self.message()

            # if score = 20, game is won
            if self.__score == 20:
                self.__state = 2
                try:
                    pygame.mixer.music.stop()
                    gameWon = pygame.mixer.Sound('World Clear.ogg')
                    gameWon.play(0)
                except pygame.error as err:
                    print(err)
                self.__gameOver = True

            pygame.display.update()

            # if head coordinates are equal to apple coordinates (apple eaten)
            # apple coordinates are recreated and snake length increases
            # if self.__head_x == self.__randAppleX and
            # self.__head_y == self.__randAppleY:
            if snake.colliderect(mushroom):
                self.__randAppleX = round(random.randrange
                                          (0, 640 - self.__snakeSize) /
                                          10.0) * 10.0
                self.__randAppleY = round(random.randrange
                                          (0, 480 - self.__snakeSize) /
                                          10.0) * 10.0
                try:
                    growSound = pygame.mixer.Sound('smb_powerup.wav')
                    growSound.play(0)
                except pygame.error as err:
                    print(err)
                self.__snakeLength += 4
                self.__score += 1

            self.__clock.tick(self.__FPS)

        # stops all sounds from playing
        pygame.mixer.stop()

        if self.__mode == "Story":
            # returns the game state (not playing, playing, win, or game over)
            # back to story mode
            return self.__state
