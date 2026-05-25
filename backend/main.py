"""
Render deployment settings:
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
Environment variables:
STRIPE_SECRET_KEY=...
FRONTEND_URL=https://matsoso-portfolio.vercel.app
"""

import os
from pathlib import Path
from typing import Literal

import stripe
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL", "https://matsoso-portfolio.vercel.app")
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INDEX_HTML = PROJECT_ROOT / "index.html"
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

app = FastAPI(title="Matsoso Portfolio Stripe Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://matsoso-portfolio.vercel.app",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "null",
    ],
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)


class CheckoutSessionRequest(BaseModel):
    package: Literal["starter", "standard", "advanced"]
    currency: Literal["zar", "usd"]


PRICES = {
    "starter": {"zar": 30000, "usd": 3000},
    "standard": {"zar": 80000, "usd": 8000},
    "advanced": {"zar": 200000, "usd": 20000},
}

PACKAGE_NAMES = {
    "starter": "Starter Portfolio Package",
    "standard": "Standard Portfolio Package",
    "advanced": "Advanced Portfolio Package",
}


@app.get("/")
def portfolio_home():
    if not INDEX_HTML.exists():
        raise HTTPException(status_code=404, detail="Portfolio index.html was not found.")

    return FileResponse(INDEX_HTML)


@app.post("/create-checkout-session")
def create_checkout_session(payload: CheckoutSessionRequest):
    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="Stripe secret key is not configured.")

    amount = PRICES[payload.package][payload.currency]

    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": payload.currency,
                        "product_data": {
                            "name": PACKAGE_NAMES[payload.package],
                        },
                        "unit_amount": amount,
                    },
                    "quantity": 1,
                }
            ],
            success_url=f"{FRONTEND_URL}?payment=success",
            cancel_url=f"{FRONTEND_URL}?payment=cancelled",
        )
    except stripe.error.StripeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return {"url": session.url}
