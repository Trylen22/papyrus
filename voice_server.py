import eventlet
eventlet.monkey_patch()

from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
from voice import VoiceManager
import logging

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, 
    cors_allowed_origins="*", 
    async_mode='eventlet'
)

# Initialize the voice manager
voice_manager = VoiceManager.initialize(socketio)

@socketio.on('connect')
def handle_connect():
    logging.info(f"Client connected to voice server from {request.sid}")
    voice_manager._initialized = True

@socketio.on('disconnect')
def handle_disconnect():
    logging.info("Client disconnected from voice server")

@socketio.on('speech_ended')
def handle_speech_ended():
    voice_manager.handle_speech_ended()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting voice server...")
    eventlet.wsgi.server(
        eventlet.listen(('0.0.0.0', 8001)), 
        app,
        log_output=True
    ) 