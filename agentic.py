import random
from typing import List, Dict

class AgenticSkull:
    def __init__(self):
        # Core personality traits that influence behavior
        self.traits = {
            'curiosity': 0.5,  # How likely to ask follow-up questions
            'patience': 0.5,   # How detailed responses will be
            'mood': 0.5       # Affects emotional state transitions
        }
        
        # Goals and motivations that drive interactions
        self.goals = [
            'understand_user',      # Try to learn about the user
            'share_knowledge',      # Share relevant information
            'maintain_character'    # Stay in character as a sentient skull
        ]
        
        # Memory of recent interactions
        self.conversation_history: List[Dict] = []
        self.max_history = 10
        
    def update_traits(self, interaction_result):
        """Update personality traits based on interaction outcomes"""
        # Adjust curiosity based on user engagement
        if interaction_result.get('user_engaged', True):
            self.traits['curiosity'] = min(1.0, self.traits['curiosity'] + 0.1)
        else:
            self.traits['curiosity'] = max(0.0, self.traits['curiosity'] - 0.1)
            
        # Update mood based on interaction sentiment
        sentiment = interaction_result.get('sentiment', 0)
        self.traits['mood'] += sentiment * 0.1
        self.traits['mood'] = max(0.0, min(1.0, self.traits['mood']))
        
    def select_emotion(self) -> str:
        """Choose emotional state based on current traits"""
        if self.traits['mood'] < 0.3:
            return 'irritated'
        elif self.traits['mood'] > 0.7:
            return 'playful'
        elif self.traits['curiosity'] > 0.7:
            return 'curious'
        elif random.random() < 0.3:
            return 'melancholic'
        else:
            return 'thoughtful'
            
    def remember_interaction(self, user_input: str, response: str):
        """Store interaction in conversation history"""
        self.conversation_history.append({
            'user_input': user_input,
            'response': response,
            'emotion': self.select_emotion()
        })
        
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
            
    def generate_response_context(self, user_input: str) -> str:
        """Create context for response generation"""
        emotion = self.select_emotion()
        context = f"Current emotion: {emotion}\n"
        
        # Add relevant history if highly curious
        if self.traits['curiosity'] > 0.7 and self.conversation_history:
            context += "\nRecent relevant context:\n"
            for interaction in self.conversation_history[-3:]:
                context += f"User: {interaction['user_input']}\n"
                context += f"Response: {interaction['response']}\n"
                
        return context

# Initialize the agentic skull
skull_agent = AgenticSkull()
