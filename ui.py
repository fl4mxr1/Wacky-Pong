import pygame

pygame.init()

font_cache = {}

screen = None

def init(Screen):
    global screen
    screen = Screen

def clicked(pos):
    for button in Button.buttons:
        # Calculate button bounds based on background rectangle
        button_width = button.width if button.width != "auto" else button.textSurface.get_width() + button.padding*2
        button_height = button.height if button.height != "auto" else button.textSurface.get_height() + button.padding*2
        
        if button.x < pos[0] < button.x + button_width and \
           button.y < pos[1] < button.y + button_height:
            if button.on_click:
                button.on_click()

def hover(pos):
    for button in Button.buttons:
        # Calculate button bounds based on background rectangle
        button_width = button.width if button.width != "auto" else button.textSurface.get_width() + button.padding*2
        button_height = button.height if button.height != "auto" else button.textSurface.get_height() + button.padding*2
        
        if button.x < pos[0] < button.x + button_width and \
           button.y < pos[1] < button.y + button_height:
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
        return self
        
    def render(self):
        screen.blit(self.surface, (self.x, self.y))
        return self
        
    def set_text(self, text):
        self.text = text
        self.update_surface()
        return self
        
    def set_color(self, color):
        self.color = color
        self.update_surface()
        return self
        
    def set_font(self, font_name, size):
        self.font = get_font(size, font_name)
        self.update_surface()
        return self
        
    def set_position(self, x, y):
        self.x = x
        if self.align == "center":
            self.x = x - self.surface.get_width()/2
        elif self.align == "right":
            self.x = x - self.surface.get_width()
        self.y = y
        return self

    def get_width(self):
        return self.surface.get_width()
    def get_height(self):
        return self.surface.get_height()


class Button:
    buttons = []
    def __init__(self, text, font_name="Arial", size=12, color=(255,255,255), x=0, y=0, width="auto", height="auto", align="left", padding=5, bg_color=(0,0,0), on_click=None, on_hover=None, on_stop_hover=None):
        self.textSurface = Text(text, font_name, size, color, x + padding, y + padding, align)
        self.text = text
        self.font_name = font_name
        self.size = size
        self.padding = padding
        self.color = color
        self.bg_color = bg_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.on_click = on_click
        self.on_hover = on_hover
        self.on_stop_hover = on_stop_hover
        self.align = align
        Button.buttons.append(self)
        
    def render(self):
        tw, th = self.textSurface.get_width(), self.textSurface.get_height()
        bgw, bgh = self.padding*2, self.padding*2
        if self.width == "auto":
            bgw += tw
        elif int(self.width) > 0:
            bgw += self.width
        
        if self.height == "auto":
            bgh += th
        elif int(self.height) > 0:
            bgh += self.height
        pygame.draw.rect(screen, self.bg_color, (self.x, self.y, bgw, bgh))
        self.textSurface.render()
        return self

    def update_surface(self):
        self.textSurface = Text(self.text, self.font_name, self.size, self.color, 
                        self.x + self.padding, self.y + self.padding, self.align)
        return self
        
    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.update_surface()
        return self
        
    def set_text(self, text):
        self.text = text
        self.update_surface()
        return self
        
    def set_color(self, color):
        self.color = color
        self.update_surface()
        return self
        
    def set_font(self, font_name, size):
        self.font_name = font_name
        self.size = size
        self.update_surface()
        return self
        
    def set_bg_color(self, color):
        self.bg_color = color
        return self
    
    def set_size(self, width=None, height=None):
        # Set width/height to given value or keep current value
        if width:
            self.width = width or self.width
        if height:
            self.height = height or self.height
        return self


def render_ui():
    for label in Text.labels:
        label.render()
    for button in Button.buttons:
        button.render()

