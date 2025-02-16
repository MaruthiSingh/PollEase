from fastapi import FastAPI

app = FastAPI()

@app.post("/polls/")
async def create_poll(poll: dict):
    return {"message": "Poll created successfully", "data": poll}
