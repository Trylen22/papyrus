from flask_socketio import SocketIO
import time
import logging

class VoiceManager:
    _instance = None
    _socketio = None
    _initialized = False

    @classmethod
    def initialize(cls, sio):
        cls._socketio = sio
        if cls._instance is None:
            cls._instance = cls()
        cls._initialized = True
        return cls._instance

    @classmethod
    def get_instance(cls):
        # Wait for initialization for up to 5 seconds
        start_time = time.time()
        while not cls._initialized and time.time() - start_time < 5:
            time.sleep(0.1)
        
        if not cls._initialized:
            cls._instance = cls()  # Create a dummy instance if initialization fails
            cls._socketio = None
            cls._initialized = True
            
        return cls._instance

    def __init__(self):
        self.is_speaking = False

    def speak(self, text):
        """Send text to client for speech synthesis"""
        try:
            if self._socketio and self._initialized:
                self.is_speaking = True
                self._socketio.emit('speak', {'text': text})
            else:
                logging.warning("Waiting for voice server to initialize...")
                time.sleep(1)  # Give server time to initialize
                if self._socketio and self._initialized:
                    self.is_speaking = True
                    self._socketio.emit('speak', {'text': text})
                else:
                    logging.warning("Voice server not available - continuing without voice")
        except Exception as e:
            logging.error(f"Voice error: {e}")

    def stop_speaking(self):
        """Stop current speech on client"""
        if self._socketio:
            self.is_speaking = False
            self._socketio.emit('stop_speaking')

    def handle_speech_ended(self):
        logging.info("Speech ended")
        self.is_speaking = False
