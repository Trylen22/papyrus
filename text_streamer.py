import queue
import time
from local_model import LocalModel

model = LocalModel("mistral")
response_queue = queue.Queue()

def stream_response(query, speed="word"):
    """
    Streams the response from the model into the queue word-by-word or sentence-by-sentence.
    """
    try:
        response_generator = model.respond(query)
        for sentence in response_generator:
            words = sentence.split()  # Break sentence into words
            for word in words:
                response_queue.put(word)
                if speed == "word":
                    time.sleep(0.1)  # Adjust delay for word-by-word streaming
            response_queue.put(" ")  # Add space between sentences
        response_queue.put(None)  # End of response
    except Exception as e:
        response_queue.put("I'm having trouble responding right now.")
        response_queue.put(None)
        print(f"Error in stream_response: {e}")
