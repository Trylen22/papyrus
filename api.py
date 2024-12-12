# api.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from local_model import LocalModel
from fastapi.middleware.cors import CORSMiddleware
import logging
from voice import VoiceManager

# Initialize the model
model = LocalModel("mistral")

app = FastAPI()

# Mount static files (if you have any CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify a list like ["http://localhost:8080"] for stricter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    avatar: str = None

@app.post("/ask")
async def ask_endpoint(data: QueryRequest):
    user_query = data.query.strip()
    if not user_query:
        raise HTTPException(status_code=400, detail="Please provide a valid query.")

    # Check for cowboy themes
    cowboy_terms = ['cowboy', 'country', 'farm', 'ranch', 'horse', 'cattle', 'yeehaw']
    # More aggressive check for cowboy terms
    query_lower = user_query.lower()
    if any(term in query_lower for term in cowboy_terms):
        model.set_emotion('cowboy')
        print("🤠 Cowboy mode activated!")  # Debug log
    elif 'cowboy' in str(data.avatar).lower():
        model.set_emotion('cowboy')
        print("🤠 Cowboy avatar selected!")  # Debug log
    elif data.avatar:
        model.set_emotion(data.avatar)
        print(f"Setting emotion to: {data.avatar}")  # Debug log

    response_fragments = []
    try:
        for chunk in model.respond(user_query):
            response_fragments.append(chunk)
        
        full_response = "".join(response_fragments).strip()
        # Send response to voice manager for speech
        voice_manager = VoiceManager.get_instance()
        voice_manager.speak(full_response)
        return {"response": full_response}
    except Exception as e:
        logging.error(f"Error generating response: {str(e)}")
        return JSONResponse({"response": f"Error generating response: {str(e)}"}, status_code=500)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("lndex.html", "r") as f:
        return f.read()

if __name__ == "__main__":
    # Run the server, accessible at http://localhost:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
