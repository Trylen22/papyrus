import time
import os
from local_model import LocalModel

# Initialize the LocalModel
model = LocalModel("mistral")
z
# Function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to animate the talking skull while LLM is responding
def get_llm_response_and_animate(query):
    response = ""
    skull_state = 'open'

    # Get the response generator from the LLM
    response_generator = model.respond(query)

    # Reserve space at the top for the skull
    print('\n' * 20)  # Adjust the number based on your tallest skull

    # Print the prompt
    print(f"> ", end='', flush=True)

    try:
        for chunk in response_generator:
            response += chunk

            # Alternate skull state
            skull_state = 'closed' if skull_state == 'open' else 'open'
            skull = skull_expressions.get(skull_state, ascii_skull_open)

            # Move cursor to top-left corner
            print('\033[H', end='')

            # Clear the skull area
            print('\033[J', end='')

            # Print the skull
            print(skull, end='')

            # Move cursor below the skull
            skull_height = skull.count('\n') + 1  # Calculate skull height
            print('\033[{}E'.format(skull_height), end='')  # Move down

            # Reprint the prompt and response
            print(f"> {response}", end='', flush=True)

            # Adjust animation speed
            time.sleep(0.1)

        # Ensure the skull ends in the 'closed' state
        skull_state = 'closed'
        skull = skull_expressions.get(skull_state, ascii_skull_closed)

        # Move cursor to top-left corner
        print('\033[H', end='')

        # Clear the skull area
        print('\033[J', end='')

        # Print the skull
        print(skull, end='')

        # Move cursor below the skull
        skull_height = skull.count('\n') + 1
        print('\033[{}E'.format(skull_height), end='')

        # Reprint the prompt and final response
        print(f"> {response.strip()}")
        print()

    except Exception as e:
        print(f"\nAn error occurred: {e}")

# Main execution block
if __name__ == "__main__":
    try:
        while True:
            user_input = input("Ask the skull anything: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            get_llm_response_and_animate(user_input)
    except KeyboardInterrupt:
        pass