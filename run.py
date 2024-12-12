import eventlet
eventlet.monkey_patch()

from voice_server import app as voice_app, socketio
from api import app as api_app
import uvicorn
import logging
import threading

def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Start voice server first and wait for initialization
        def run_voice_server():
            logger.info("Starting voice server on port 8001...")
            socketio.run(voice_app, host='0.0.0.0', port=8001, log_output=True)

        voice_server = eventlet.spawn(run_voice_server)
        # Give voice server time to initialize
        eventlet.sleep(2)

        # Start FastAPI server in a separate thread
        def run_api_server():
            logger.info("Starting API server on port 8000...")
            uvicorn.run(api_app, host="0.0.0.0", port=8000)

        api_thread = threading.Thread(target=run_api_server)
        api_thread.daemon = True
        api_thread.start()

        # Keep the main thread running
        eventlet.sleep(float('inf'))

    except KeyboardInterrupt:
        logger.info("\nShutting down servers...")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    main() 