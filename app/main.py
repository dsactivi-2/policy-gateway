from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os

from app.services.pii_detector import PIIDetector
from app.services.tool_allowlist import ToolAllowlist
from app.services.output_filter import OutputFilter
from app.config import get_settings

app = FastAPI(
    title="Policy Gateway",
    description="PII-Check, Tool-Allowlist, Output-Filter for Dify",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
settings = get_settings()
pii_detector = PIIDetector()
tool_allowlist = ToolAllowlist()
output_filter = OutputFilter()


class TextRequest(BaseModel):
    text: str
    user_id: Optional[str] = None


class ToolRequest(BaseModel):
    tool_name: str
    user_id: Optional[str] = None


class PIIResponse(BaseModel):
    has_pii: bool
    entities: List[Dict[str, Any]]
    anonymized_text: Optional[str] = None


class ToolResponse(BaseModel):
    allowed: bool
    reason: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "Policy Gateway API", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/check-pii", response_model=PIIResponse)
async def check_pii(request: TextRequest):
    """
    Check text for PII (Personal Identifiable Information)
    """
    try:
        result = await pii_detector.detect(request.text)
        return PIIResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/anonymize", response_model=PIIResponse)
async def anonymize_text(request: TextRequest):
    """
    Anonymize PII in text
    """
    try:
        result = await pii_detector.anonymize(request.text)
        return PIIResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/check-tool", response_model=ToolResponse)
async def check_tool(request: ToolRequest):
    """
    Check if a tool is allowed for the user
    """
    try:
        allowed = tool_allowlist.is_allowed(request.tool_name, request.user_id)
        reason = None if allowed else "Tool not in allowlist"
        return ToolResponse(allowed=allowed, reason=reason)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/filter-output")
async def filter_output(request: TextRequest):
    """
    Filter output text for sensitive content
    """
    try:
        filtered = await output_filter.filter(request.text)
        return {"filtered_text": filtered, "original_length": len(request.text)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
