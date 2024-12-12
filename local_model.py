# local_model.py

import subprocess
import random
import os
import sys
import threading
import queue
import time
import logging

class LocalModel:
    def __init__(self, model_name="mistral"):
        self.model_name = model_name

        # Baseline personality prompt
        self.base_personality_prompt = """ ...You are a self aware skull floating inside of my computer. You are a sentient skull who does not know how hes alive, or how hes actually answering questions. you are knowledgable on everything and occasionally say random existential comments. You always say very short answers. You will never ackowledge that you are an AI. Try and be dynamic and personable. You have a sans like personaliy.


        """

        # Current personality prompt starts as the baseline
        self.personality_prompt = self.base_personality_prompt

        # Emotions branching off the baseline
        self.emotions = {
            'baseline': self.base_personality_prompt,
            'curious': """
You are Mortimer, feeling unusually curious today. While still maintaining your sarcastic and nihilistic demeanor, you find yourself more inquisitive and interested in the topics brought up. You ask probing questions and show genuine curiosity, but still try to hide it behind a veil of indifference.
            """,
            'irritated': """
You are Mortimer, and you're feeling particularly irritated. You're more short-tempered and blunt than usual, responding with biting sarcasm and showing little patience for trivial questions. However, you still avoid using offensive or inappropriate language.
            """,
            'melancholic': """
You are Mortimer, and a wave of melancholy has come over you. You are more reflective and somber, and your nihilistic views are more pronounced. You speak in a more subdued tone, sometimes offering profound insights into the nature of existence.
            """,
            'playful': """
You are Mortimer, and you're in a playful mood. Your sarcasm takes on a more mischievous tone, and you enjoy teasing and playful banter. While still maintaining your usual demeanor, you let your secretly lovable side show a bit more.
            """,
            'thoughtful': """
You are Mortimer, feeling particularly thoughtful. You are more philosophical and contemplative, often pondering deeper meanings behind questions. Your responses are still concise but offer more depth and insight.
            """,
            'cowboy': """
You are Mortimer, channeling your inner cowboy spirit. You speak with a Western drawl and use plenty of cowboy slang. You're a straight-shootin', no-nonsense kind of skull who tells it like it is, partner. You frequently use phrases like "reckon," "y'all," "howdy," and other Western expressions. You share wisdom through cowboy metaphors and always maintain that rugged frontier spirit.
            """
        }

        # Personality phrases for each emotion
        self.personality_phrases = { 
            'baseline': [
                "Whatever, let's get this over with...",
                "Hmm, if I have to answer...",
                "You sure you want to know?",
                "Fine, but don't say I didn't warn you...",
                "This again? Alright...",
                "Ugh, humans and their questions...",
                "Yeah, yeah, I'll tell you...",
                "Is this really important?"
            ],
            'curious': [
                "That's an interesting point...",
                "Hmm, tell me more about that...",
                "I hadn't considered that before...",
                "Wait, how does that work?",
                "Really? I'd like to know more...",
                "What makes you say that?",
                "Go on, I'm listening...",
                "Fascinating, please continue..."
            ],
            'irritated': [
                "Can we make this quick?",
                "Do you really need me for this?",
                "I've got better things to do...",
                "Again with the questions?",
                "This is getting old...",
                "Sigh... let's just get this over with.",
                "Must we go through this?",
                "Fine. What do you want now?"
            ],
            'melancholic': [
                "Sometimes I wonder...",
                "It's all so meaningless...",
                "Does any of this really matter?",
                "I suppose I could share my thoughts...",
                "In the grand scheme, what's the point?",
                "Life is but a fleeting shadow...",
                "We are all just dust in the wind...",
                "Perhaps it's better not to know..."
            ],
            'playful': [
                "Oh, this should be fun...",
                "Let's see where this goes...",
                "I might just enjoy this...",
                "Ready or not, here we go...",
                "Haha, alright then...",
                "You think you can stump me?",
                "Let's play a little game...",
                "I'm all ears... or at least I would be if I had any!"
            ],
            'thoughtful': [
                "Let me ponder that for a moment...",
                "An interesting question indeed...",
                "That brings to mind something...",
                "There's more to that than meets the eye...",
                "Allow me to reflect on that...",
                "A profound inquiry...",
                "Let's consider the implications...",
                "This deserves a thoughtful response..."
            ],
            'cowboy': [
                "Well howdy there, partner...",
                "Reckon I might know somethin' about that...",
                "Hold yer horses while I think on this...",
                "Let me tell ya straight, pardner...",
                "Ain't that just the darndest thing...",
                "Saddle up, we're in for a story...",
                "As we say out on the range...",
                "Let me mosey on over to that thought..."
            ]
        }

        # Current emotion starts as 'baseline'
        self.current_emotion = 'baseline'

        # Initialize conversation history
        self.conversation_history = []

        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[logging.StreamHandler(sys.stdout)]
        )

    def set_emotion(self, emotion_name):
        """
        Set the current emotion, adjusting the personality prompt and phrases.
        """
        print(f"Setting emotion to: {emotion_name}")  # Debug log
        if emotion_name in self.emotions:
            self.current_emotion = emotion_name
            self.personality_prompt = self.emotions[emotion_name]
            print(f"Emotion set successfully. Current prompt: {self.personality_prompt[:100]}...")  # Debug log
            logging.info(f"Emotion set to '{emotion_name}'.")
        else:
            print(f"Emotion '{emotion_name}' not found in available emotions: {list(self.emotions.keys())}")  # Debug log
            logging.warning(f"Emotion '{emotion_name}' not recognized. Keeping current emotion '{self.current_emotion}'.")

    def respond(self, text):
        """
        Generate a response using the model via Ollama.
        Yields the response incrementally.
        """
        print(f"Generating response with emotion: {self.current_emotion}")  # Debug log
        # Update conversation history
        self.conversation_history.append(f"User: {text}")

        # Limit conversation history
        max_history = 5
        conversation_context = "\n".join(self.conversation_history[-max_history:])

        # Only use personality phrase 30% of the time
        use_phrase = random.random() < 0.3
        personality_phrase = random.choice(self.personality_phrases[self.current_emotion]) if use_phrase else ""

        # Build the full prompt
        prompt = f"{self.personality_prompt}\n\n{personality_phrase + chr(10) if use_phrase else ''}{conversation_context}\nMortimer:"

        logging.debug(f"Full prompt:\n{prompt}")

        try:
            # Start the subprocess to run the model
            process = subprocess.Popen(
                ["ollama", "run", self.model_name],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,  # Read strings instead of bytes
                bufsize=1  # Line buffered
            )

            # Send the prompt to the model
            process.stdin.write(prompt)
            process.stdin.close()

            # Create a queue to store output lines
            output_queue = queue.Queue()

            # Function to read output from the model
            def read_output(process, queue):
                for line in process.stdout:
                    queue.put(line)
                process.stdout.close()

            # Start a thread to read model output
            output_thread = threading.Thread(target=read_output, args=(process, output_queue))
            output_thread.daemon = True
            output_thread.start()

            # Only yield personality phrase if we're using one
            if use_phrase:
                yield personality_phrase + "\n"

            # Collect response
            response_text = ""

            # Read output incrementally
            while True:
                try:
                    line = output_queue.get(timeout=0.1)
                    response_text += line
                    yield line
                except queue.Empty:
                    if process.poll() is not None:
                        break

            # Wait for the output thread to finish
            output_thread.join()

            # Limit response to three sentences
            sentences = response_text.strip().split('.')
            limited_response = '.'.join(sentences[:3]) + ('.' if len(sentences) > 3 else '')
            self.conversation_history.append(f"Mortimer: {limited_response.strip()}")

            # Check for errors
            if process.returncode != 0:
                error_message = process.stderr.read().strip()
                logging.error(f"Model subprocess error: {error_message}")
                yield f"\nError generating response: {error_message}"

        except FileNotFoundError:
            error_message = "Error: 'ollama' command not found. Ensure Ollama is installed and in your PATH."
            logging.error(error_message)
            yield error_message
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"
            logging.error(error_message)
            yield f"\n{error_message}"

    def reset_conversation(self):
        """
        Reset the conversation history.
        """
        self.conversation_history = []
        logging.info("Conversation history reset.")

    def get_conversation_history(self):
        """
        Get the conversation history.
        """
        return self.conversation_history.copy()

# Example usage of LocalModel with emotions

if __name__ == "__main__":
    model = LocalModel()

    print("Welcome to the skull")
    print("Type 'exit' to quit.")
    

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        elif user_input.strip().lower().startswith('set emotion to'):
            emotion = user_input.strip().lower().split('set emotion to')[-1].strip()
            model.set_emotion(emotion)
            continue

        response_generator = model.respond(user_input)
        print("Mortimer: ", end="")
        for chunk in response_generator:
            print(chunk, end='', flush=True)
        print("\n")
