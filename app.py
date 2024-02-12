from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    scope = "user-library-read"
    return {"Hello": "World"}