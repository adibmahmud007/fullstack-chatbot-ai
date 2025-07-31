from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class LegalQueryRequest(BaseModel):
    """
    Request model for legal queries
    """
    problem_description: str = Field(..., min_length=10, max_length=2000, description="বিস্তারিত আইনি সমস্যার বর্ণনা")
    problem_type: Optional[str] = Field(default="general", description="সমস্যার ধরণ (family, property, criminal, civil, etc.)")
    location: Optional[str] = Field(default="ঢাকা", description="অবস্থান (ঢাকা, চট্টগ্রাম, সিলেট, etc.)")
    urgency_level: Optional[str] = Field(default="normal", description="জরুরি মাত্রা (low, normal, high, emergency)")

class LegalAdviceResponse(BaseModel):
    """
    Response model for legal advice
    """
    legal_analysis: str
    user_rights: str
    next_steps: str
    required_documents: str
    where_to_go: str
    estimated_cost: Optional[str] = None
    warnings: str
    problem_type: str
    location: str
    timestamp: datetime
    status: str

class LegalProcedureRequest(BaseModel):
    """
    Request for legal procedure information
    """
    case_type: str = Field(..., description="মামলার ধরণ (divorce, property dispute, criminal case, etc.)")
    location: Optional[str] = Field(default="ঢাকা", description="অবস্থান")

class LawExplanationRequest(BaseModel):
    """
    Request for law explanation
    """
    law_topic: str = Field(..., description="আইনের বিষয় (consumer rights, labor law, family law, etc.)")
    complexity_level: Optional[str] = Field(default="simple", description="ব্যাখ্যার মাত্রা (simple, detailed)")

class LegalRightsRequest(BaseModel):
    """
    Request for legal rights information
    """
    situation: str = Field(..., description="পরিস্থিতির বর্ণনা")
    person_type: Optional[str] = Field(default="general", description="ব্যক্তির ধরণ (employee, tenant, consumer, etc.)")

class DocumentRequirementRequest(BaseModel):
    """
    Request for document requirements
    """
    legal_action: str = Field(..., description="আইনি কাজের বর্ণনা")
    location: Optional[str] = Field(default="ঢাকা", description="অবস্থান")

class EmergencyLegalRequest(BaseModel):
    """
    Emergency legal help request
    """
    emergency_type: str = Field(..., description="জরুরি অবস্থার ধরণ")
    location: str = Field(..., description="বর্তমান অবস্থান")
    immediate_help_needed: bool = Field(default=True, description="তাৎক্ষণিক সাহায্য প্রয়োজন কিনা")

# Original chat models (keep these too)
class ChatRequest(BaseModel):
    """
    General chat request model
    """
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    max_tokens: Optional[int] = Field(default=1000, ge=10, le=2000, description="Maximum response tokens")
    temperature: Optional[float] = Field(default=0.2, ge=0.0, le=1.0, description="Response creativity (lower for legal)")

class ChatResponse(BaseModel):
    """
    Response model for chat
    """
    user_message: str
    ai_response: str
    model: str
    tokens_used: Optional[int] = None
    specialization: str = "bangladesh_legal"
    timestamp: datetime
    status: str

class ErrorResponse(BaseModel):
    """
    Error response model
    """
    message: str
    error_type: str
    status: str = "error"