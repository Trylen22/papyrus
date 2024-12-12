import pygame
import math
import threading
import queue
from local_model import LocalModel

# Initialize the LocalModel
model = LocalModel("mistral")

# Initialize Pygame
pygame.init()

# Full-screen mode
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Sentient Skull Avatar")

# Font settings
FONT_SIZE = 24
font = pygame.font.SysFont("couriernew", FONT_SIZE)
LINE_SPACING = 5

# Skull ASCII Art
skull_expressions = {
    'idle': r"""
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

# Avatar settings
avatar_position = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4]
oscillation_angle = 0
state = 'idle'

# Queue for streaming text
response_queue = queue.Queue()
conversation_history = []  # Store user input and responses
talking_animation_counter = 0
talking_face_switch_rate = 15

# Scroll state
scroll_offset = 0
scroll_step = FONT_SIZE + LINE_SPACING

# Text box dimensions
TEXT_BOX_WIDTH = SCREEN_WIDTH - 40
TEXT_BOX_HEIGHT = SCREEN_HEIGHT // 3
TEXT_BOX_X = 20
TEXT_BOX_Y = SCREEN_HEIGHT - TEXT_BOX_HEIGHT - 40

# Function to render ASCII art
def render_ascii_art(ascii_art, x, y, scale=1):
    lines = ascii_art.strip("\n").split("\n")
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, (255, 255, 255))
        scaled_surface = pygame.transform.scale(
            text_surface, (int(text_surface.get_width() * scale), int(FONT_SIZE * scale))
        )
        screen.blit(scaled_surface, (x, y + i * FONT_SIZE * scale))

# Function to render conversation history in the text box
def render_conversation_history():
    global scroll_offset
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

    # Blit the text surface onto the main screen
    screen.blit(text_surface, (TEXT_BOX_X, TEXT_BOX_Y))

# Function to wrap text within a given width
def wrap_text(text, max_width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width - 20:  # Account for padding
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    return lines

# Function to handle streaming responses
def stream_response(query):
    global state
    state = 'talking_open'
    try:
        response_generator = model.respond(query)
        for sentence in response_generator:
            response_queue.put(sentence.strip())
        response_queue.put(None)  # Signal the end of the response
    except Exception as e:
        response_queue.put(None)
        print(f"Error in streaming response: {e}")

# Main function
def main():
    global state, talking_animation_counter, oscillation_angle, scroll_offset

    running = True
    user_input = ""
    current_response = ""
    streaming = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input.strip():
                        conversation_history.append({'user': user_input, 'response': ""})
                        threading.Thread(target=stream_response, args=(user_input,)).start()
                        streaming = True
                        user_input = ""
                        current_response = ""  # Reset for new response
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    scroll_offset = max(scroll_offset - scroll_step, 0)  # Scroll up
                elif event.key == pygame.K_DOWN:
                    scroll_offset = min(scroll_offset + scroll_step, max(0, len(conversation_history) * scroll_step - TEXT_BOX_HEIGHT))  # Scroll down
                else:
                    user_input += event.unicode

        # Handle streaming text
        if streaming:
            try:
                while not response_queue.empty():
                    chunk = response_queue.get_nowait()
                    if chunk is None:  # End of response
                        streaming = False
                        state = 'idle'
                        conversation_history[-1]['response'] = current_response.strip()
                    else:
                        current_response += chunk + " "
            except queue.Empty:
                pass

        # Alternate talking animation while streaming
        if streaming:
            talking_animation_counter += 1
            if talking_animation_counter >= talking_face_switch_rate:
                state = 'talking_closed' if state == 'talking_open' else 'talking_open'
                talking_animation_counter = 0

        # Update skull state
        if state == 'idle':
            oscillation_angle += 0.05
            avatar_position[1] = SCREEN_HEIGHT // 4 + math.sin(oscillation_angle) * 10

        # Clear the screen
        screen.fill((0, 0, 0))

        # Render conversation history
        render_conversation_history()

        # Render the skull
        x = avatar_position[0] - 150  # Centering adjustment
        y = avatar_position[1]
        render_ascii_art(skull_expressions[state], x, y)

        # Render input prompt
        input_prompt = f"Ask the skull anything: {user_input}"
        input_surface = font.render(input_prompt, True, (255, 255, 255))
        screen.blit(input_surface, (20, SCREEN_HEIGHT - 30))

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
