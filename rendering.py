import pygame
from constants import FONT_SIZE, LINE_SPACING, TEXT_BOX_X, TEXT_BOX_Y, TEXT_BOX_WIDTH, TEXT_BOX_HEIGHT, SCREEN_HEIGHT, font

def render_ascii_art(screen, ascii_art, x, y, scale=1):
    """
    Renders ASCII art on the screen at the specified position and scale.
    """
    lines = ascii_art.strip("\n").split("\n")
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, (255, 255, 255))
        scaled_surface = pygame.transform.scale(
            text_surface, (int(text_surface.get_width() * scale), int(FONT_SIZE * scale))
        )
        screen.blit(scaled_surface, (x, y + i * FONT_SIZE * scale))

def render_conversation_history(screen, conversation_history, scroll_offset):
    """
    Renders the conversation history in a scrollable text box.
    """
    text_surface = pygame.Surface((TEXT_BOX_WIDTH, TEXT_BOX_HEIGHT))
    text_surface.fill((30, 30, 30))  # Background color for the text box

    y_offset = -scroll_offset
    for entry in conversation_history:
        user_text = f"You: {entry['user']}"
        model_text = f"Skull: {entry['response']}"

        # Render user text
        for line in wrap_text(user_text, TEXT_BOX_WIDTH):
            text_line_surface = font.render(line, True, (200, 200, 200))
            text_surface.blit(text_line_surface, (10, y_offset))
            y_offset += FONT_SIZE + LINE_SPACING

        # Render model text
        for line in wrap_text(model_text, TEXT_BOX_WIDTH):
            text_line_surface = font.render(line, True, (255, 255, 255))
            text_surface.blit(text_line_surface, (10, y_offset))
            y_offset += FONT_SIZE + LINE_SPACING + 10

    screen.blit(text_surface, (TEXT_BOX_X, TEXT_BOX_Y))

def wrap_text(text, max_width):
    """
    Wraps text to fit within the specified width, splitting words as necessary.
    """
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width - 20:  # Subtract padding from max width
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    return lines


def render_animated_text(screen, text, x, y, max_width, frame_counter):
    """
    Renders text one word at a time to create an animated effect within the text box.
    """
    # Clear the text box background
    text_box_height = SCREEN_HEIGHT // 3
    pygame.draw.rect(screen, (30, 30, 30), (x, y, max_width, text_box_height))

    visible_text = text[:frame_counter]  # Only render up to the current frame
    lines = wrap_text(visible_text, max_width)

    # Render each line within the text box
    for i, line in enumerate(lines):
        line_y = y + i * (FONT_SIZE + LINE_SPACING)
        if line_y < y + text_box_height - FONT_SIZE:  # Ensure it stays within the text box
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (x + 10, line_y))  # Add padding inside the box


        
def render_input_prompt(screen, user_input):
    """
    Renders the input prompt at the bottom of the screen.
    """
    input_prompt = f"Ask the skull anything: {user_input}"
    input_surface = font.render(input_prompt, True, (255, 255, 255))
    screen.blit(input_surface, (20, SCREEN_HEIGHT - 30))