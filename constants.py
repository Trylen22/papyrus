import pygame

# Initialize Pygame display info to get full-screen dimensions
pygame.init()
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h

# Font settings
FONT_SIZE = 24
LINE_SPACING = 5
font = pygame.font.SysFont("couriernew", FONT_SIZE)

# Text box dimensions
TEXT_BOX_WIDTH = SCREEN_WIDTH - 40
TEXT_BOX_HEIGHT = SCREEN_HEIGHT // 3
TEXT_BOX_X = 20
TEXT_BOX_Y = SCREEN_HEIGHT - TEXT_BOX_HEIGHT - 40

# Scroll settings
scroll_step = FONT_SIZE + LINE_SPACING

# Skull ASCII art
skull_expressions = {'idle': r"""
      ______
   .-'      `-.
  /            \
 |,  .-.  .-.  ,|
 | )(_o/  \o_)( |
 |/     --    \|
 (_     ^^     _)
  \__|IIIIII|__/
   | \IIIIII/ |
   \          /
    `--------`
""",
    'talking_open': r"""
      ______
   .-'      `-.
  /            \
 |,  .-.  .-.  ,|
 | )  o    o  ( |
 |/     --     \|
 (_     ^^     _)
  \__|IIIIII|__/
  
   | \IIIIII/ |
   \          /
    `--------`
""",
    'talking_closed': r"""
      ______
   .-'      `-.
  /            \
 |,  .-.  .-.  ,|
 | )  o    o  ( |
 |/     --     \|
 (_     ^^     _)
  \__|IIIIII|__/
   | \IIIIII/ |
   \          /
    `--------`
"""
}
theme = {
    "background_color": (0, 0, 0),
    "text_color": (255, 255, 255),
    "prompt_color": (200, 200, 200)
}