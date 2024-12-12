import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, scroll_step, skull_expressions, TEXT_BOX_X, TEXT_BOX_WIDTH, TEXT_BOX_Y
from rendering import render_ascii_art, render_conversation_history, render_input_prompt, render_animated_text
from state_manager import update_state, get_next_animation_state
from text_streamer import stream_response, response_queue

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Sentient Skull Avatar")

# Global Variables
conversation_history = []  # Store user input and responses
oscillation_angle = 0
scroll_offset = 0
state = 'idle'  # Initial state
talking_animation_counter = 0  # Counter for slower animation
talking_face_switch_rate = 15  # How many frames before switching face
current_response = ""  # Current streaming response
frame_counter = 0  # For animated text rendering

def main():
    global state, oscillation_angle, scroll_offset, talking_animation_counter, current_response, frame_counter

    running = True
    user_input = ""
    streaming = False

    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input.strip():
                        conversation_history.append({'user': user_input, 'response': ""})
                        stream_response(user_input)  # Start streaming response
                        streaming = True
                        user_input = ""
                        current_response = ""  # Reset for new response
                        frame_counter = 0  # Reset animation counter
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    scroll_offset = max(scroll_offset - scroll_step, 0)  # Scroll up
                elif event.key == pygame.K_DOWN:
                    scroll_offset = min(scroll_offset + scroll_step, max(0, len(conversation_history) * scroll_step - SCREEN_HEIGHT // 3))  # Scroll down
                else:
                    user_input += event.unicode

        # Handle Streaming Text
        if streaming:
            while not response_queue.empty():
                chunk = response_queue.get_nowait()
                if chunk is None:  # End of response
                    streaming = False
                    state = 'idle'
                    conversation_history[-1]['response'] = current_response.strip()
                else:
                    current_response += chunk + " "  # Append chunk (word) to the response
                    frame_counter += len(chunk) + 1  # Advance animation counter for each word

        # Alternate Talking Animation While Streaming
        if streaming:
            talking_animation_counter += 1
            if talking_animation_counter >= talking_face_switch_rate:
                state = get_next_animation_state(state)
                talking_animation_counter = 0

        # Update Avatar State
        if state == 'idle':
            oscillation_angle += 0.05
            avatar_y = update_state(state, oscillation_angle)
        else:
            avatar_y = SCREEN_HEIGHT // 4  # Fixed Y-position for non-idle states

        # Clear the Screen
        screen.fill((0, 0, 0))

        # Render Conversation History
        render_conversation_history(screen, conversation_history, scroll_offset)

        # Render the Skull
        render_ascii_art(screen, skull_expressions[state], SCREEN_WIDTH // 2 - 150, avatar_y)

        # Render Animated Text (Streaming Response)
        # Render Animated Text (Streaming Response)
        render_animated_text(screen, current_response, TEXT_BOX_X, TEXT_BOX_Y, TEXT_BOX_WIDTH, frame_counter)


        # Render Input Prompt
        render_input_prompt(screen, user_input)

        # Update the Display
        pygame.display.flip()
        pygame.time.Clock().tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
