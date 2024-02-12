from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    scope = "user-library-read"
    return {"Hello": "World"}

"""
FLOW:
- Hit Spotify API "authorize" route, and obtain URL and return to frontend
- Frontend does "window.replace" with that URL to get spotify auth
- After auth, redirect URL will go to backend and retrieve code and then will get access token, storing it in session
- User in frontend will hit the BFS depth and track vs artist (check on that)
- Then user will be informed that playlist is creating and will be done in x seconds/mins
- Backend does graph search and creates playlist
"""