import pygame, sys, time
import spring as Spring
import random
import ui as UI
from threading import Timer

pygame.init()

sw, sh = 1000, 600
screen = pygame.display.set_mode((sw, sh))
UI.init(screen)

pygame.display.set_caption("Wacky Balls.")

clock = pygame.time.Clock()

PHYSICS_DRAG = 0.995
PHYSICS_GRAVITY = 0.2
PHYSICS_TIMESCALE = 1
FIXED_TIMESTEP = 1/60  # Fixed time step for physics (60 FPS)

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
    def destroy(self):
        self.paddles.remove(self)

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
        self.frozen = True
    def render(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    def update_physics(self, delta_scale=1.0):
        if self.frozen:
            return
        self.yv += PHYSICS_GRAVITY * delta_scale
        self.yv *= pow(PHYSICS_DRAG, delta_scale)
        self.xv *= pow(PHYSICS_DRAG, delta_scale)
        self.x += self.xv * PHYSICS_TIMESCALE * delta_scale
        self.y += self.yv * PHYSICS_TIMESCALE * delta_scale
    def update_collision(self):
        if self.frozen:
            return
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
                self.yv = random.randint(-15, -10)
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
    current_time = time.time()
    delta_time = current_time - Update_Springs.last_time
    Update_Springs.last_time = current_time
    
    for spring in Spring.Spring.springs:
        spring.update(delta_time)
Update_Springs.last_time = time.time()  # Initialize last_time

def Update_Class():
    current_time = time.time()
    delta_time = current_time - Update_Class.last_time
    delta_scale = delta_time / FIXED_TIMESTEP  # Scale factor for physics updates
    
    for ball in Ball.balls:
        ball.update_physics(delta_scale)
        ball.update_collision()
        ball.update_misc()
    
    Update_Class.last_time = current_time
Update_Class.last_time = time.time()  # Initialize last_time

def Update():
    mx, _ = pygame.mouse.get_pos()
    if GAME_STATE == "game" and GAME_PLAYERPADDLE:
        GAME_PLAYERPADDLE.set_position(mx, sh - 30)

def Update_Render():
    screen.fill((0,0,0))

    for paddle in Paddle.paddles:
        print("Rendering paddle")
        paddle.render()

    for ball in Ball.balls:
        print("Rendering ball")
        ball.render()

def start_game():
    for paddle in Paddle.paddles:
        paddle.destroy()
    global GAME_STATE, GAME_PLAYERPADDLE, GAME_BALL
    GAME_STATE = "game"
    GAME_PLAYERPADDLE = Paddle(sw/2, sh - 30, 175, (255,255,255))
    GAME_BALL = Ball(sw/2 - 5, 150, 10, (255,255,255))

    def game_over():
        global GAME_STATE
        GAME_STATE = "menu"
        UI.Text("GAME OVER @!!!!@!!!@#1").set_position(sw/2, sh/2).set_font("Comic Sans MS", 24).set_color((255,0,0))
    GAME_BALL.onDestroy = game_over
    
    def afterCountdown():
        GAME_BALL.frozen = False
    Timer(3, afterCountdown).start()

mainMenuUIElements = {}
mainMenuUIElements["StartButton"] = UI.Button("Start").set_position(0,sw/2).set_size(100,50).set_bg_color((255,255,255)).set_color((60,60,60)).set_font("Comic Sans MS", 24)
mainMenuUIElements["StartButton"].on_hover = (lambda: (
    mainMenuUIElements["StartButton"].set_bg_color((60,60,60)),
    mainMenuUIElements["StartButton"].set_color((255,255,255))
))
mainMenuUIElements["StartButton"].on_stop_hover = (lambda: (
    mainMenuUIElements["StartButton"].set_bg_color((255,255,255)),
    mainMenuUIElements["StartButton"].set_color((60,60,60))
))
mainMenuUIElements["StartButton"].on_click = start_game

print("GGGGGGGGG")
while True:
    
    Update_Events()
    Update_Springs()
    Update_Class()
    Update()
    Update_Render()
    UI.render_ui()
    pygame.display.update()
    clock.tick(60)



