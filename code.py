import time
import board
import displayio
import framebufferio
import rgbmatrix
import random

displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

bitmap = displayio.Bitmap(display.width, display.height, 2)
palette = displayio.Palette(2)
palette[0] = 0x000000  # Background
palette[1] = 0xFFFFFF  # Objects

tg = displayio.TileGrid(bitmap, pixel_shader=palette)
group = displayio.Group()
group.append(tg)
display.root_group = group

# constants
PADDLE_HEIGHT = 8
PADDLE_WIDTH = 2
BALL_SIZE = 2

HEIGHT = 32
WIDTH = 64

WHITE = 1
BLACK = 0

class PongGame:
    def __init__(self):
        self.reset()
     
    def reset(self):
        self.left_y = (HEIGHT - PADDLE_HEIGHT) // 2
        self.right_y = (HEIGHT - PADDLE_HEIGHT) // 2
     
        self.ball_x = WIDTH / 2
        self.ball_y = HEIGHT / 2
        self.xvelocity = 1
        self.yvelocity = 1
     
    def move_paddles(self):
        reaction_dist = 20
        target_y=HEIGHT/2
        # left paddle
        if self.ball_x < reaction_dist:
            
            if random.random() < 0.8:
                target_y = self.ball_y - PADDLE_HEIGHT // 2
                self.left_y += int((target_y - self.left_y) * 0.5)
        else:
            self.right_y += random.choice([-2, 1, 2])
     
        # right paddle (they are not the same to make it less boring)
        if self.ball_x > (WIDTH - reaction_dist):
            if random.random() < 0.7:
                target_y = self.ball_y - PADDLE_HEIGHT // 2
                self.right_y += int((target_y - self.right_y) * 0.5)
        else:
            self.right_y += random.choice([-1, 0, 1])
     
        # keep paddles in bounds
        self.left_y = max(-2, min(34 - PADDLE_HEIGHT, self.left_y))
        self.right_y = max(-2, min(34 - PADDLE_HEIGHT, self.right_y))
        self.left_y = max(0, min(32 - PADDLE_HEIGHT, self.left_y))
        self.right_y = max(0, min(32 - PADDLE_HEIGHT, self.right_y))

    def update_ball(self):
        self.ball_x += self.xvelocity
        self.ball_y += self.yvelocity

        if self.ball_y <= 0 or self.ball_y >= HEIGHT - BALL_SIZE:
            self.yvelocity *= -1

        if (self.ball_x <= PADDLE_WIDTH and self.left_y <= self.ball_y <= self.left_y + PADDLE_HEIGHT):
            self.xvelocity *= -1
            self.yvelocity += random.choice([-1, 0, 1])

        elif (self.ball_x >= WIDTH - PADDLE_WIDTH - BALL_SIZE and self.right_y <= self.ball_y <= self.right_y + PADDLE_HEIGHT):
            self.xvelocity *= -1
            self.yvelocity += random.choice([-1, 0, 1])

        if self.ball_x < 0:
            self.reset()
        elif self.ball_x >= WIDTH - BALL_SIZE:
            self.reset()

    def draw(self):
        bitmap.fill(BLACK)
        for h in range(PADDLE_HEIGHT):
            for w in range(PADDLE_WIDTH):
                bitmap[w, self.left_y + h] = WHITE
                bitmap[63 - w, self.right_y + h] = WHITE
        for w in range(BALL_SIZE):
            for h in range(BALL_SIZE):
                bitmap[int(self.ball_x) + w, int(self.ball_y) + h] = WHITE
        display.refresh()

game = PongGame()

while True:
    game.move_paddles()
    game.update_ball()
    game.draw()
