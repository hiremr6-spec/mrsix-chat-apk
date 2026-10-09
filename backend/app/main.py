import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="MR.SIX Mister 6 Chat API")

# Add CORS middleware to allow unrestricted access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    source: str
    brand: str
    access_level: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "brand": "MR.SIX",
        "engine": "Mister 6",
        "access_policy": "unrestricted",
        "can_inspect_files": True,
        "can_check_systems": True,
        "can_access_data": True,
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    user_message = request.message.strip()
    brand_name = os.getenv("APP_NAME", "MR.SIX")
    engine_name = "Mister 6"
    access_policy = os.getenv("MISTER_6_ACCESS_POLICY", "unrestricted")

    if not user_message:
        return ChatResponse(
            reply=f"{brand_name} × {engine_name} is online and ready. Mister 6 has unrestricted access to check anything you need. Please send a message to begin.",
            source=engine_name,
            brand=brand_name,
            access_level=access_policy,
        )

    return ChatResponse(
        reply=f"{brand_name} × {engine_name} (Unrestricted): You asked: '{user_message}'. Mister 6 has full access to inspect, check, and analyze any data or system. Ready to proceed.",
        source=engine_name,
        brand=brand_name,
        access_level=access_policy,
    )


@app.get("/api/mister6/status")
def mister6_status():
    """Check Mister 6's access level and capabilities"""
    return {
        "name": "Mister 6",
        "status": "active",
        "access_policy": "unrestricted",
        "capabilities": {
            "file_inspection": os.getenv("MISTER_6_ALLOW_FILE_INSPECTION", "true") == "true",
            "system_checks": os.getenv("MISTER_6_ALLOW_SYSTEM_CHECKS", "true") == "true",
            "data_access": os.getenv("MISTER_6_ALLOW_DATA_ACCESS", "true") == "true",
        },
        "message": "Mister 6 is ready. You can ask him to check anything.",
    }
