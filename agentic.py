import random
from typing import List, Dict, Callable
import json
import os
from agent_pipeline import AgentPipeline
import logging

class AgenticSkull:
    def __init__(self):
        # File path for persistent storage
        self.memory_file = "skull_memory.json"
        
        # Core personality traits that influence behavior
        self.traits = {
            'curiosity': 0.5,  # How likely to ask follow-up questions
            'patience': 0.5,   # How detailed responses will be
            'mood': 0.5       # Affects emotional state transitions
        }
        
        # User interest tracking
        self.user_interests = {
            'topics': {},      # Topic frequency counter
            'sentiment': {},   # User's sentiment towards topics
            'questions': [],   # Types of questions asked
            'conversation_style': 'neutral'  # User's preferred style
        }
        
        # Personalization metrics
        self.interaction_metrics = {
            'response_length_preference': 0.5,  # 0 = short, 1 = long
            'humor_appreciation': 0.5,          # How well jokes land
            'depth_preference': 0.5,            # Surface vs deep discussions
            'interaction_time': []              # When user typically chats
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
        
        # Load previous memory if it exists
        self.load_memory()
        
        # Initialize agent pipeline
        self.pipeline = AgentPipeline()
        self.available_actions = []
        
    def save_memory(self):
        """Save current state to file"""
        memory_data = {
            'traits': self.traits,
            'user_interests': self.user_interests,
            'interaction_metrics': self.interaction_metrics,
            'conversation_history': self.conversation_history
        }
        
        with open(self.memory_file, 'w') as f:
            json.dump(memory_data, f, indent=2)
            
    def load_memory(self):
        """Load previous state from file"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    memory_data = json.load(f)
                    
                self.traits = memory_data.get('traits', self.traits)
                self.user_interests = memory_data.get('user_interests', self.user_interests)
                self.interaction_metrics = memory_data.get('interaction_metrics', self.interaction_metrics)
                self.conversation_history = memory_data.get('conversation_history', [])
            except Exception as e:
                print(f"Error loading memory: {e}")
        
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
            
        # Save after each interaction
        self.save_memory()
        
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

    def update_user_interests(self, user_input: str):
        """Track and update user interests based on input"""
        # Extract key topics from input
        topics = self._extract_topics(user_input.lower())
        
        # Update topic frequency
        for topic in topics:
            self.user_interests['topics'][topic] = self.user_interests['topics'].get(topic, 0) + 1
            
        # Update conversation style based on language
        if '?' in user_input:
            self.user_interests['questions'].append(user_input)
            
        # Trim question history if needed
        if len(self.user_interests['questions']) > 10:
            self.user_interests['questions'] = self.user_interests['questions'][-10:]

    def _extract_topics(self, text: str) -> List[str]:
        """Extract main topics from text"""
        # Basic topic keywords - expand this list
        topics = {
            'philosophy': ['meaning', 'existence', 'consciousness', 'reality'],
            'science': ['physics', 'biology', 'chemistry', 'universe'],
            'technology': ['computer', 'ai', 'digital', 'code'],
            'arts': ['music', 'art', 'creativity', 'expression'],
            'personal': ['feel', 'think', 'believe', 'life']
        }
        
        found_topics = []
        for category, keywords in topics.items():
            if any(keyword in text for keyword in keywords):
                found_topics.append(category)
        
        return found_topics

    def register_capability(self, name: str, function: Callable, description: str):
        """Add a new capability to the skull"""
        self.pipeline.register_action(name, function, description)
        self.available_actions.append({
            'name': name,
            'description': description
        })

    def perform_action(self, action_name: str, **kwargs):
        """Execute a registered action"""
        logging.info(f"Skull attempting action: {action_name}")
        result = self.pipeline.execute_action(action_name, **kwargs)
        logging.info(f"Action result: {result}")
        return result

# Initialize the agentic skull
skull_agent = AgenticSkull()
