from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routers import card_number, utils


app = FastAPI(title="Image Prediction API",
              description="A simple image prediction API",
              version="1.0.0")


app.include_router(card_number.router)
app.include_router(utils.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
