import time
import pygame
import random
from pygame.locals import *

# Image size
size = 49


class Apple:
    def __init__(self, surface):
        self.apple = pygame.image.load("resources/apple.png")
        self.surface = surface
        self.x_apple = size * 3
        self.y_apple = size * 3

    def draw(self):
        self.surface.blit(self.apple, (self.x_apple, self.y_apple))

        return self.x_apple, self.y_apple

    def change_coords(self):
        # Generates random int
        self.random_x = random.randrange(1, 24)
        self.random_y = random.randrange(1, 12)

        self.x_apple = size * self.random_x
        self.y_apple = size * self.random_y

        self.draw()


class Snake:

    def __init__(self, surface, length):
        self.length = length
        self.surface = surface

        # Load image
        self.head = pygame.image.load("resources/head.png")
        self.body = pygame.image.load("resources/body.png")
        self.tail = pygame.image.load("resources/tail.png")

        # Coordinates list
        self.x = [size*5] * self.length
        self.y = [size*7] * self.length
        self.direction = 'up'

        # Rotation list
        self.rotation = [0] * self.length

        # Turned List
        self.isTurned = [0] * self.length

    def increase_length(self):
        self.length += 1

        self.x.append(self.x[-1])
        self.y.append(self.y[-1])

        self.rotation.append(self.rotation[-1])
        self.isTurned.append(self.isTurned[-1])

    def draw_body(self):
        for i in range(1, self.length - 1):
            if self.isTurned[i] == 4:
                self.turnedBody = pygame.image.load("resources/turned_body.png")
                self.rotatedBody = pygame.transform.rotate(self.turnedBody, 180)

            elif self.isTurned[i] == 2:
                self.turnedBody = pygame.image.load("resources/turned_body.png")
                self.rotatedBody = pygame.transform.rotate(self.turnedBody, 270)

            elif self.isTurned[i] == 3:
                self.turnedBody = pygame.image.load("resources/turned_body.png")
                self.rotatedBody = pygame.transform.rotate(self.turnedBody, 90)

            elif self.isTurned[i] == 1:
                self.turnedBody = pygame.image.load("resources/turned_body.png")
                self.rotatedBody = pygame.transform.rotate(self.turnedBody, 0)

            else:
                self.rotatedBody = pygame.transform.rotate(self.body, self.rotation[i])
            self.surface.blit(self.rotatedBody, (self.x[i], self.y[i]))

    def draw_snake(self):
        # Draws Head
        self.rotatedHead = pygame.transform.rotate(self.head, self.rotation[0])
        self.surface.blit(self.rotatedHead, (self.x[0], self.y[0]))

        # Draws Tail
        self.rotatedTail = pygame.transform.rotate(self.tail, self.rotation[self.length - 1])
        self.surface.blit(self.rotatedTail, (self.x[self.length - 1], self.y[self.length - 1]))

        # Draws Body
        self.draw_body()

    def move_left(self):
        self.rotation[0] = 90
        self.direction = 'left'

    def move_right(self):
        self.rotation[0] = 270
        self.direction = 'right'

    def move_up(self):
        self.rotation[0] = 0
        self.direction = 'up'

    def move_down(self):
        self.rotation[0] = 180
        self.direction = 'down'

    def rotationStuff(self):
        # Moves rotation list by 1 index
        for j in range(self.length - 1, 0, -1):
            self.rotation[j] = self.rotation[j - 1]

        # Moves isTurned list by 1 index
        self.isTurned.insert(0, 0)
        self.isTurned.pop(self.length)

        # Rotation
        if self.rotation[0] == self.rotation[2]:  # Determines the type of body it's going to draw (turned or not)
            pass
        elif self.rotation[0] == 0 and self.rotation[2] == 270 or self.rotation[0] == 90 and self.rotation[2] == 180:
            self.isTurned[1] = 4
        elif self.rotation[0] == 0 and self.rotation[2] == 90 or self.rotation[0] == 270 and self.rotation[2] == 180:
            self.isTurned[1] = 3
        elif self.rotation[0] == 180 and self.rotation[2] == 270 or self.rotation[0] == 90 and self.rotation[2] == 0:
            self.isTurned[1] = 2
        elif self.rotation[0] == 180 and self.rotation[2] == 90 or self.rotation[0] == 270 and self.rotation[2] == 0:
            self.isTurned[1] = 1

    def walk(self):
        # Basically it determines the next location the entire x,y body coordinates
        # It does this by getting the value of the block in front of it and making it its own
        # And loop it until every block has the coordinates of the block in front of it
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # Head Coordinates | Determines x,y coordinates
        if self.direction == 'up':
            self.y[0] -= size
        if self.direction == 'down':
            self.y[0] += size
        if self.direction == 'right':
            self.x[0] += size
        if self.direction == 'left':
            self.x[0] -= size

        # Rotation
        self.rotationStuff()  # Determines Head and Body rotation

        self.draw_snake()

        return self.x, self.y


class Game:
    def __init__(self):
        self.render_background()
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()


        # Objects
        self.snake = Snake(self.surface, 3)
        self.apple = Apple(self.surface)

        # For the first iteration
        self.snake.draw_snake()
        self.snake.move_up()

        # Plays background music
        pygame.mixer.music.load('resources/Mounika - Cut My Hair (feat. Cavetown).mp3')
        pygame.mixer.music.play(-1, 0)
        
    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface = pygame.display.set_mode((1176, 588))
        self.surface.blit(bg, (0, 0))

    def collision_apple(self):
        if self.x[0] == self.x_apple and self.y[0] == self.y_apple:
            self.eat = pygame.mixer.Sound("resources/eat.mp3")
            pygame.mixer.Sound.play(self.eat)
            self.apple.change_coords()
            self.snake.increase_length()

    def collision_body(self):
        for i in range(2, len(self.x)):
            if self.x[0] == self.x[i] and self.y[0] == self.y[i]:
                self.crash = pygame.mixer.Sound("resources/crash.mp3")
                pygame.mixer.Sound.play(self.crash)
                raise ValueError

    def collision_wall(self):
        if self.x[0] > 1175 or self.y[0] > 580 or self.x[0] < 0 or self.y[0] < 0:  # If it goes out of game window
            self.crash = pygame.mixer.Sound("resources/crash.mp3")
            pygame.mixer.Sound.play(self.crash)
            raise ValueError

    def game_over(self):
        self.render_background()
        font = pygame.font.SysFont('Arial', 30)

        line1 = font.render("Game Over! Your Score is "+str(self.snake.length-2), True, (200, 200, 200))
        self.surface.blit(line1, (430, 240))
        line2 = font.render("Press Space to play again", True, (200, 200, 200))
        self.surface.blit(line2, (440, 280))

        pygame.display.flip()

    def display_score(self):
        font = pygame.font.SysFont('Arial', 20)
        score = font.render("Score: "+str(self.snake.length-2), True, (200, 200, 200))
        self.surface.blit(score, (1080, 565))

    def reset(self):
        self.snake = Snake(self.surface, 3)
        self.apple = Apple(self.surface)
        self.move_down = False  # Needs to reassign self.move_down since self.move_down is enabled in the first iteration after reset
        self.move_left = True
        self.move_right = True
        self.move_up = True

    def run(self):
        running = True
        pause = False

        # Movement Restrictions
        self.move_down = False
        self.move_up = True
        self.move_right = True
        self.move_left = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                elif event.type == KEYDOWN:
                    # Checks keyboard input for pause/quit
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_SPACE:
                        pause = False

                    # Checks keyboard input for movement
                    if not pause:
                        if event.key == K_w and self.move_up or event.key == K_UP and self.move_up:
                            self.snake.move_up()

                            self.move_down = False
                            self.move_right = True
                            self.move_up = True
                            self.move_left = True
                        if event.key == K_s and self.move_down or event.key == K_DOWN and self.move_down:
                            self.snake.move_down()

                            self.move_up = False
                            self.move_right = True
                            self.move_down = True
                            self.move_left = True
                        if event.key == K_a and self.move_left or event.key == K_LEFT and self.move_left:
                            self.snake.move_left()

                            self.move_right = False
                            self.move_up = True
                            self.move_down = True
                            self.move_left = True
                        if event.key == K_d and self.move_right or event.key == K_RIGHT and self.move_right:
                            self.snake.move_right()

                            self.move_left = False
                            self.move_right = True
                            self.move_up = True
                            self.move_down = True
            try:
                if not pause:
                    self.play()
            except ValueError:
                self.game_over()
                pause = True
                self.reset()

    def play(self):
        self.render_background()

        # Calls function and assigns the return value
        self.x_apple, self.y_apple = self.apple.draw()
        self.x, self.y = self.snake.walk()
        self.display_score()

        pygame.display.flip()
        time.sleep(0.2)

        # Checks collision with different 'objects'
        self.collision_apple()
        self.collision_body()
        self.collision_wall()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
