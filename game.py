import pygame, sys
import spring as Spring
import random
import ui as UI

pygame.init()

sw, sh = 1000, 600
screen = pygame.display.set_mode((sw, sh))
UI.init(screen)

pygame.display.set_caption("Wacky Balls.")

clock = pygame.time.Clock()

PHYSICS_DRAG = 0.995
PHYSICS_GRAVITY = 0.2
PHYSICS_TIMESCALE = 1

GAME_STATE = "menu"
GAME_PLAYERPADDLE = None
GAME_BALL = None

class Paddle:
    paddles = []
    def __init__(self, x, y, width, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = 15
        self.color = color
        self.spring = Spring.Spring(self.x, 9, 1.5, 0, sw - width)
        self.paddles.append(self)
    def render(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    def set_position(self, x, y):
        self.spring.target = x - self.width/2
        self.x = self.spring.position
        self.y = y

class Ball:
    balls = []
    def __init__(self, x, y, radius, color, onDestroy=None):
        self.x = x
        self.y = y
        self.xv = 0
        self.yv = 0
        self.radius = radius
        self.color = color
        self.balls.append(self)
        self.onDestroy = onDestroy
    def render(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    def update_physics(self):
        self.yv += PHYSICS_GRAVITY
        self.yv *= PHYSICS_DRAG
        self.xv *= PHYSICS_DRAG
        self.x += self.xv * PHYSICS_TIMESCALE
        self.y += self.yv * PHYSICS_TIMESCALE
    def update_collision(self):
        for paddle in Paddle.paddles:
            if self.x <= 0:
                self.x = 0
                self.xv = -self.xv
            if self.x >= sw - self.radius:
                self.x = sw - self.radius
                self.xv = -self.xv

            if (self.x > paddle.x) and (self.x < paddle.x + paddle.width) and (self.y >= paddle.y - self.radius) and (self.y <= paddle.y + paddle.height):
                # Calculate where on the paddle the ball hit (0 to 1)
                hit_position = (self.x - paddle.x) / paddle.width
                
                # Convert hit position to a -1 to 1 range (centered on paddle)
                hit_factor = (hit_position - 0.5) * 2
                
                # Apply horizontal velocity based on hit position
                self.xv = hit_factor * 15  # Adjust the 15 to change maximum horizontal speed
                
                # Reset position and apply upward velocity
                self.y = paddle.y - self.radius
                self.yv = random.randint(-15, -5)
    def update_misc(self):
        if self.y > sh:
            self.destroy()
    def destroy(self):
        self.balls.remove(self)
        if self.onDestroy:
            self.onDestroy()

def Update_Events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            UI.clicked(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            UI.hover(event.pos)

def Update_Springs():
    for spring in Spring.Spring.springs:
        spring.update(1/60)

def Update_Class():
    for ball in Ball.balls:
        ball.update_physics()
        ball.update_collision()
        ball.update_misc()

def Update():
    mx, my = pygame.mouse.get_pos()
    if GAME_STATE == "game" and GAME_PLAYERPADDLE:
        GAME_PLAYERPADDLE.set_position(mx, sh - 30)

def Update_Render():
    screen.fill((0,0,0))

    for paddle in Paddle.paddles:
        paddle.render()

    for ball in Ball.balls:
        ball.render()

mainMenuUIElements = {}
mainMenuUIElements["StartButton"] = UI.Button("Start", x=100, y=100, font_name="Comic Sans MS", size=24, color=(60,60,60), bg_color=(255,255,255), on_click=lambda: print("CLICK!!!!!!"))
mainMenuUIElements["StartButton"].on_hover = (lambda: (
    mainMenuUIElements["StartButton"].set_bg_color((60,60,60)),
    mainMenuUIElements["StartButton"].set_color((255,255,255))
))
mainMenuUIElements["StartButton"].on_stop_hover = (lambda: (
    mainMenuUIElements["StartButton"].set_bg_color((255,255,255)),
    mainMenuUIElements["StartButton"].set_color((60,60,60))
))

while True:
    Update_Events()
    Update_Springs()
    Update_Class()
    Update()
    Update_Render()
    UI.render_ui()
    pygame.display.update()
    clock.tick(60)



