import os
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import redis
import os

app = FastAPI(
    title="Open Safe-AI Gateway",
    version="1.0.0",
    description="Secure, resilient Gateway for Amazon Bedrock with Redis Semantic Cache"
)

# Redis Connection Setup
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

class PromptRequest(BaseModel):
    prompt: str
    user_id: str | None = None

class PromptResponse(BaseModel):
    response: str
    cached: bool
    status: str

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "open-safe-ai-gateway"}

@app.post("/v1/chat/completions", response_model=PromptResponse)
async def generate_completion(request: PromptRequest):
    # 1. Check Redis Cache
    cache_key = f"cache:{request.prompt}"
    cached_val = redis_client.get(cache_key)
    
    if cached_val:
        return PromptResponse(response=cached_val, cached=True, status="SUCCESS_CACHE")
    
    # 2. Mock Gateway Response (In production, Bedrock API + Guardrails are called here)
    generated_text = f"Processed securely: {request.prompt}"
    
    # 3. Store to Cache
    redis_client.set(cache_key, generated_text, ex=3600)
    
    return PromptResponse(response=generated_text, cached=False, status="SUCCESS_BEDROCK")
