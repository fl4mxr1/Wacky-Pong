import pygame

pygame.init()

font_cache = {}

screen = None

def init(Screen):
    global screen
    screen = Screen

def clicked(pos):
    for button in Button.buttons:
        if button.x < pos[0] < button.x + button.text.get_width() + button.padding*2 and \
           button.y < pos[1] < button.y + button.text.get_height() + button.padding*2:
            if button.on_click:
                button.on_click()

def hover(pos):
    print(pos)
    for button in Button.buttons:
        if button.x < pos[0] < button.x + button.text.get_width() + button.padding*2 and \
           button.y < pos[1] < button.y + button.text.get_height() + button.padding*2:
            if button.on_hover:
                button.on_hover()
        else:
            if button.on_stop_hover:
                button.on_stop_hover()

def get_font(size, font_name):
    cache_key = f"{size}-{font_name}"
    if cache_key not in font_cache:
        font_cache[cache_key] = pygame.font.SysFont(font_name, size)
    return font_cache[cache_key]

class Text:
    labels = []
    def __init__(self, text, font_name="Arial", size=12, color=(255,255,255), x=0, y=0, align="left"):
        self.text = text
        self.font = get_font(size, font_name)
        self.color = color
        self.surface = self.font.render(self.text, True, self.color)
        self.x = x
        self.align = align
        if self.align == "center":
            self.x = x - self.surface.get_width()/2
        elif self.align == "right":
            self.x = x - self.surface.get_width()
        self.y = y
        Text.labels.append(self)
    def update_surface(self):
        self.surface = self.font.render(self.text, True, self.color)
    def render(self):
        screen.blit(self.surface, (self.x, self.y))
    def set_text(self, text):
        self.text = text
        self.update_surface()
    def set_color(self, color):
        self.color = color
        self.update_surface()   
    def set_font(self, font_name, size):
        self.font = get_font(size, font_name)
        self.update_surface()
    def set_position(self, x, y):
        self.x = x
        if self.align == "center":
            self.x = x - self.surface.get_width()/2
        elif self.align == "right":
            self.x = x - self.surface.get_width()
        self.y = y
    def get_width(self):
        return self.surface.get_width()
    def get_height(self):
        return self.surface.get_height()


class Button:
    buttons = []
    def __init__(self, text, font_name="Arial", size=12, color=(255,255,255), x=0, y=0, align="left", padding=5, bg_color=(0,0,0), on_click=None, on_hover=None, on_stop_hover=None):
        self.text = Text(text, font_name, size, color, x + padding, y + padding, align)
        self.font_name = font_name
        self.size = size
        self.padding = padding
        self.color = color
        self.bg_color = bg_color
        self.x = x
        self.y = y
        self.on_click = on_click
        self.on_hover = on_hover
        Button.buttons.append(self)
    def render(self):
        pygame.draw.rect(screen, self.bg_color, (self.x, self.y, self.text.get_width() + self.padding*2, self.text.get_height() + self.padding*2))
        self.text.render()
    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.text = Text(self.text.text, self.text.font_name, self.text.size, self.text.color, self.x + self.padding, self.y + self.padding, self.text.align)
    def set_text(self, text):
        self.text = Text(text, self.text.font_name, self.text.size, self.text.color, self.x + self.padding, self.y + self.padding, self.text.align)
    def set_color(self, color):
        self.text.set_color(color)
    def set_font(self, font_name, size):
        self.text.set_font(font_name, size)
    def set_bg_color(self, color):
        self.bg_color = color
    def set_position(self, x, y):
        self.x = x
        self.y = y


def render_ui():
    for label in Text.labels:
        label.render()
    for button in Button.buttons:
        button.render()

