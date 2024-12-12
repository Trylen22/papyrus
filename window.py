import pygame
import time
import threading
import queue
from local_model import LocalModel

# Initialize the LocalModel
model = LocalModel("mistral")

# Define skull expressions
ascii_skull_blink = r"""
      ______
   .-'      `-.
  /            \
 |,  .-.  .-.  ,|
 | ) ---  --- ( |
 |/     --    \|
 (_     ^^     _)
  \__|IIIIII|__/
   | \IIIIII/ |
   \          /
    `--------`
"""

ascii_skull_look_left = r"""
      ______
   .-'      `-.
  /            \
 |,  .-.  .-.  ,|
 | ) 0    0     |
 |/     --     \|
 (_     ^^     _)
  \__|IIIIII|__/
   | \IIIIII/ |
   \          /
    `--------`
"""


ascii_skull_look_right = r"""
      ______
   .-'      `-.
  /            \
 |,  .-.  .-.  ,|
 | )   0     0  |
 |/     --     \|
 (_     ^^     _)
  \__|IIIIII|__/
   | \IIIIII/ |
   \          /
    `--------`
"""

ascii_skull_look_center = r"""
      ______
   .-'      `-.
  /            \
 |,  .-.  .-.  ,|
 | )  0     0   |
 |/     --     \|
 (_     ^^     _)
  \__|IIIIII|__/
   | \IIIIII/ |
   \          /
    `--------`
"""

scii_skull_look_suprised = r"""
      ______
   .-'      `-.
  /  .-.  .-.  \
 |,            ,|
 | )  0     0   |
 |/     --     \|
 (_     ^^     _)
  \__|IIIIII|__/

   | \IIIIII/ |
   \          /
    `--------`
"""


scii_skull_smoking_closed = r"""
     
       ______      
     ;       ~~ \
     |           ;
 ,--------,______|---.
/          \-----`    \    
`.__________`-_______-'             
    |,   --    -- ,|
    | )  0     0   |
    |/     --     \|
    (_     ^^     _)
     \__|IIIIII|__/
               (̅_̅_̅_̅(̅_̅_̅_̅_̅_̅_̅_̅_̅̅_̅()ڪے
     |  \IIIIII/ |
      \          /
       `--------`
"""

scii_skull_smoking_open = r"""
     
       ______      
     ;       ~~ \
     |           ;
 ,--------,______|---.
/          \-----`    \    
`.__________`-_______-'             
    |,   --    -- ,|
    | )  0     0   |
    |/     --     \|
    (_     ^^     _)
     \__|IIIIII|__/
                (̅_̅_̅_̅(̅_̅_̅_̅_̅_̅_̅_̅_̅̅_̅()ڪے
                
     |  \IIIIII/ |
      \          /
       `--------`
"""


ascii_skull_shocked = r"""
      _____
   .-'      `-.
  /  .-.        \
 |,       .-.  ,|
 | )  o    O  ( |
 |/            \|
 (_     ^^     _)
  \__|IIIIII|__/

   | \IIIIII/ |
   \          /
    `--------`

"""

ascii_skull_blushing = r"""
      ______
   .-'      `-.
  /            \
 |,  .-.  .-.  ,|
 | )   .    .  (|
 |/   _     _  \|
 (_     ^^    _)
  \__|IIIIII|__/
   | \IIIIII/ |
   \          /
    `--------`
"""

ascii_skull_winking = r"""
      ______
   .-'      `-.
  /            \
 |,  .-.  .-.  ,|
 | )  ^    o_)( |
 |/     --     \|
 (_     ^^     _)
  \__|IIIIII|__/
   | \IIIIII/ |
   \          /
    `--------`
"""

cat_mode = r"""

       :"-.          .-";                    
        :`.`.__..__.'.';                    
          :-"      "-;                     
       :;              :;                    
       /  .==.    .==.  \                    
      :      _.--._      ;                   
      ; .--.' `--' `.--. :                   
     :   __;`      ':__   ;                  
     ;  '  '-._:;_.-'  '  :                  
     '.       `--'       .'                  
      ."-._          _.-".                   
    .'     ""------""     `.                 
   /`-                    -'\                
  /`-                      -'\               
 :`-   .'              `.   -';              
 ;    /                  \    :              
:    :                    ;    ;             
;    ;                    :    :             
':_:.'                    '.;_;'             
   :_                      _;                
   ; "-._                -" :`-.     _.._    
   :_          ()          _;   "--::__. `.  
    \"-                  -"/`._           :  
   .-"-.                 -"-.  ""--..____.'  
  /         .__  __.         \               
 : / ,       / "" \       . \ ;          
  "-:___..--"      "--..___;-"

"""

ascii_skull_creepy_closed = r"""
                  ___-----------___
           __--~~                 ~~--__
       _-~~                             ~~-_
    _-~                                     ~-_
   /                                           \
  |                                             |
 |                                               |
 |                                               |
|                                                 |
|                                                 |
|                                                 |
 |                                               |
 |  |    _-------_               _-------_    |  |
 |  |  /~         ~\           /~         ~\  |  |
  ||  |             |         |             |  ||
  || |               |       |               | ||
  || |              |         |              | ||
  |   \_           /           \           _/   |
 |      ~~--_____-~    /~V~\    ~-_____--~~      |
 |                    |     |                    |
|                    |       |                    |
|                    |  /^\  |                    |
 |                    ~~   ~~                    |
  \_         _                       _         _/
    ~--____-~ ~\                   /~ ~-____--~
         \     /\                 /\     /
          \    | ( ,           , ) |    /
           |   | (~(__(  |  )__)~) |   |
            |   \/ (  (~~|~~)  ) \/   |
             |   |  [ [  |  ] ]  |   |
              |                     |
               \                   /
                ~-_             _-~
                   ~--___-___--~
"""

ascii_skull_creepy_open = r"""
                  ___-----------___
           __--~~                 ~~--__
       _-~~                             ~~-_
    _-~                                     ~-_
   /                                           \
  |                                             |
 |                                               |
 |                                               |
|                                                 |
|                                                 |
|                                                 |
 |                                               |
 |  |    _-------_               _-------_    |  |
 |  |  /~         ~\           /~         ~\  |  |
  ||  |             |         |             |  ||
  || |               |       |               | ||
  || |              |         |              | ||
  |   \_           /           \           _/   |
 |      ~~--_____-~    /~V~\    ~-_____--~~      |
 |                    |     |                    |
|                    |       |                    |
|                    |  /^\  |                    |
 |                    ~~   ~~                    |
  \_         _                       _         _/
    ~--____-~ ~\                   /~ ~-____--~
         \     /\                 /\     /


         
          \    | ( ,           , ) |    /
           |   | (~(__(  |  )__)~) |   |
            |   \/ (  (~~|~~)  ) \/   |
             |   |  [ [  |  ] ]  |   |
              |                     |
               \                   /
                ~-_             _-~
                   ~--___-___--~
"""

# Define skull expressions
skull_expressions = {
    'open': ascii_skull_open,
    'closed': ascii_skull_closed,
    'shocked': ascii_skull_shocked,
    'blushing': ascii_skull_blushing,
    'winking': ascii_skull_winking,
    'creepy_open': ascii_skull_creepy_open,
    'creepy_closed': ascii_skull_creepy_closed,
}

# Keyword dictionaries for each expression
keywords = {
    'creepy': ["beware", "slumber", "awakened", "haunt", "dead","creepy mode"],
    'shocked': ["time is running out", "hurry", "urgent", "danger"],
    'blushing': ["remember me", "thank you", "grateful", "appreciate", "sweet"],
    'winking': ["farewell", "see you", "bye", "later"],
}

# Initialize Pygame
pygame.init()

# Set up the display with full screen
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h
FONT_SIZE = 24  # Adjust font size as needed
FONT_NAME = 'couriernew'  # Use a monospaced font

# Set up full screen mode
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Talking Skull")

# Set up the font
font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

# Function to render ASCII art
def render_ascii_art(ascii_art, x, y):
    lines = ascii_art.strip('\n').split('\n')
    for i, line in enumerate(lines):
        text_surface = font.render(line.rstrip(), True, (255, 255, 255))
        screen.blit(text_surface, (x, y + i * FONT_SIZE))

# Main execution block
def main():
    running = True
    user_input = ''
    previous_responses = []  # To store previous responses
    current_expression = 'closed'  # Start with the default expression
    in_creepy_mode = False  # Flag to track if we're in creepy mode

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input.strip() == '':
                        continue  # Ignore empty input
                    if user_input.lower() in ["exit", "quit"]:
                        running = False
                        pygame.quit()
                        return
                    else:
                        # Get the LLM response and update the expression
                        response_lines, new_expression, in_creepy_mode = get_llm_response_and_animate(
                            user_input, current_expression, in_creepy_mode, previous_responses
                        )
                        if in_creepy_mode and current_expression != 'creepy':
                            previous_responses.clear()  # Clear previous responses when entering creepy mode
                        if not in_creepy_mode or new_expression == 'blushing':
                            current_expression = new_expression
                        previous_responses.append(response_lines)
                        user_input = ''
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

        # Clear the screen
        screen.fill((0, 0, 0))

        # Render the skull (static when not speaking)
        skull_x = 20
        skull_y = 20

        # Determine which skull to display
        if in_creepy_mode:
            skull_art = skull_expressions.get('creepy_closed', ascii_skull_creepy_closed)
            text_start_y = skull_y + 900  # Adjusted for larger creepy skull
        else:
            skull_art = skull_expressions.get(current_expression, ascii_skull_closed)
            text_start_y = skull_y + 350  # Adjust based on skull height

        render_ascii_art(skull_art, skull_x, skull_y)

        # Render the previous responses
        y_offset = text_start_y
        for prev_resp in previous_responses:
            for line in prev_resp:
                text_surface = font.render(line, True, (255, 255, 255))
                screen.blit(text_surface, (20, y_offset))
                y_offset += FONT_SIZE
            y_offset += FONT_SIZE  # Add spacing between responses

        # Render the prompt with spacing
        prompt_text = "Ask the skull anything: " + user_input
        prompt_surface = font.render(prompt_text, True, (255, 255, 255))
        screen.blit(prompt_surface, (20, SCREEN_HEIGHT - 60))  # Moved up for spacing

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        pygame.time.Clock().tick(30)

def get_llm_response_and_animate(query, current_expression, in_creepy_mode, previous_responses):
    response = ""
    skull_state = 'open'

    # Start with default skulls for animation
    if in_creepy_mode:
        skull_art = {
            'open': ascii_skull_creepy_open,
            'closed': ascii_skull_creepy_closed,
        }
    else:
        skull_art = {
            'open': ascii_skull_open,
            'closed': ascii_skull_closed,
        }

    # Get the response generator from the LLM
    response_generator = model.respond(query)

    # Use a queue to communicate between the LLM thread and the main thread
    q = queue.Queue()

    # Function to read from the LLM and put characters into the queue
    def read_llm_response():
        try:
            for chunk in response_generator:
                q.put(chunk)
            q.put(None)  # Signal that the response is complete
        except Exception as e:
            q.put(None)
            print(f"An error occurred: {e}")

    # Start the LLM response thread
    llm_thread = threading.Thread(target=read_llm_response)
    llm_thread.start()

    # Main animation loop
    clock = pygame.time.Clock()
    running = True
    response_lines = []
    max_line_width = SCREEN_WIDTH - 40  # Margin

    # Variables for skull animation timing
    skull_animation_time = 0.3  # Seconds between frames
    last_animation_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Update skull animation
        current_time = time.time()
        if current_time - last_animation_time >= skull_animation_time:
            skull_state = 'closed' if skull_state == 'open' else 'open'
            last_animation_time = current_time

        # Get new characters from the LLM response
        try:
            while not q.empty():
                char = q.get_nowait()
                if char is None:
                    running = False  # Response is complete
                    break
                response += char
        except queue.Empty:
            pass

        # Clear the screen
        screen.fill((0, 0, 0))

        # Render the skull
        skull_x = 20
        skull_y = 20
        render_ascii_art(skull_art[skull_state], skull_x, skull_y)

        # Adjust text start position based on creepy mode
        if in_creepy_mode:
            text_start_y = skull_y + 900  # Adjusted for larger creepy skull
        else:
            text_start_y = skull_y + 350  # Adjust based on skull height

        # Render the previous responses (if not in creepy mode)
        y_offset = text_start_y
        if not in_creepy_mode:
            for prev_resp in previous_responses:
                for line in prev_resp:
                    text_surface = font.render(line, True, (255, 255, 255))
                    screen.blit(text_surface, (20, y_offset))
                    y_offset += FONT_SIZE
                y_offset += FONT_SIZE  # Add spacing between responses

        # Render the current response text
        words = response.strip().split(' ')
        line = ''
        response_lines = []
        for word in words:
            test_line = f"{line} {word}".strip()
            text_width, _ = font.size(test_line)
            if text_width < max_line_width:
                line = test_line
            else:
                response_lines.append(line)
                line = word
        if line:
            response_lines.append(line)

        for line in response_lines:
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (20, y_offset))
            y_offset += FONT_SIZE

        # Render the prompt
        prompt_text = "Ask the skull anything: "
        prompt_surface = font.render(prompt_text, True, (255, 255, 255))
        screen.blit(prompt_surface, (20, SCREEN_HEIGHT - 60))

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(30)

    # Wait for the LLM thread to finish
    llm_thread.join()

    # After the response is complete, determine the skull expression based on keywords
    new_expression = current_expression  # Default to current expression
    found_expression = None

    for expr, keys in keywords.items():
        if any(keyword in response.lower() for keyword in keys):
            found_expression = expr
            break

    # Handle creepy mode
    if in_creepy_mode:
        if found_expression == 'blushing':
            # Exit creepy mode when the skull says something sweet
            in_creepy_mode = False
            new_expression = 'blushing'
        else:
            # Stay in creepy mode
            new_expression = 'creepy_closed'
    else:
        if found_expression == 'creepy':
            in_creepy_mode = True
            new_expression = 'creepy_closed'
        elif found_expression:
            new_expression = found_expression

    # Return the response lines, new expression, and creepy mode flag
    return response_lines, new_expression, in_creepy_mode

if __name__ == "__main__":
    main()
