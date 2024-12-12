import math
from constants import SCREEN_HEIGHT

def update_state(state, oscillation_angle):
    """
    Update the avatar's position based on its state and oscillation angle.
    """
    if state == 'idle':
        return SCREEN_HEIGHT // 4 + math.sin(oscillation_angle) * 10
    elif state == 'busy':
        return SCREEN_HEIGHT // 4 + math.cos(oscillation_angle) * 5  # Slight movement for busy
    elif state == 'thinking':
        return SCREEN_HEIGHT // 4  # No movement for thinking

def get_next_animation_state(current_state):
    """
    Alternate between talking_open and talking_closed states.
    """
    if current_state == 'talking_open':
        return 'talking_closed'
    elif current_state == 'talking_closed':
        return 'talking_open'
    return current_state

def transition_to_state(current_state, trigger):
    """
    Transition between states dynamically based on triggers.
    """
    if trigger == 'start_thinking':
        return 'thinking'
    elif trigger == 'start_talking':
        return 'talking_open'
    elif trigger == 'finish_talking':
        return 'idle'
    elif trigger == 'busy_task':
        return 'busy'
    return current_state
