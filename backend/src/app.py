from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("../../models/instrusion_detector.pkl")


class PredictionRequest(BaseModel):
    data: List

@app.get("/")
def home():
    return {
        "message": "Backend Connected Successfully!"
    }


@app.get("/ping")
def ping():
    return {
        "status": "online"
    }


@app.post("/predict")
def predict(request: PredictionRequest):

    print("Request received!")
    print("Length:", len(request.data))
    print("First 10 values:", request.data[:10])

    result = model.predict([request.data])[0]

    label = "Normal" if result == 1 else "Attack"

    return {
        "prediction": label
    }