from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.llm import llm_service

router = APIRouter(prefix="/llm", tags=["llm"])


class ChatRequest(BaseModel):
    message: str
    prompt_type: Optional[str] = "general"


@router.post("/chat")
async def chat_with_llm(request: ChatRequest):
    if not llm_service:
        raise HTTPException(status_code=500, detail="LLM服务未初始化")
    try:
        response = await llm_service.get_response(request.message, request.prompt_type)
        return {"response": response, "prompt_type": request.prompt_type, "success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM服务错误: {str(e)}")


@router.get("/prompts")
async def get_available_prompts():
    if not llm_service:
        raise HTTPException(status_code=500, detail="LLM服务未初始化")
    return {"prompts": llm_service.get_available_prompts()}


@router.get("/health")
async def llm_health_check():
    if llm_service:
        return {"status": "healthy"}
    return {"status": "unhealthy", "error": "LLM服务未初始化"}


