from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from models.schemas import (
    LegalQueryRequest, LegalAdviceResponse, LegalProcedureRequest,
    LawExplanationRequest, LegalRightsRequest, DocumentRequirementRequest,
    EmergencyLegalRequest, ChatResponse, ErrorResponse
)
from services.groq_service import groq_service
from datetime import datetime

router = APIRouter()

@router.post("/legal-advice", response_model=ChatResponse)
async def get_legal_advice(request: LegalQueryRequest):
    """
    বাংলাদেশের আইন অনুযায়ী আইনি পরামর্শ পান
    Get legal advice according to Bangladesh law
    """
    try:
        # Create detailed prompt with user's problem
        detailed_prompt = f"""
        আইনি সমস্যা: {request.problem_description}
        সমস্যার ধরণ: {request.problem_type}
        অবস্থান: {request.location}
        জরুরি মাত্রা: {request.urgency_level}
        
        দয়া করে নিম্নলিখিত format এ উত্তর দিন:
        
        ১. আইনি বিশ্লেষণ:
        ২. আপনার অধিকার:
        ৩. পরবর্তী পদক্ষেপ:
        ৪. প্রয়োজনীয় কাগজপত্র:
        ৫. কোথায় যেতে হবে:
        ৬. আনুমানিক খরচ:
        ৭. গুরুত্বপূর্ণ সতর্কতা:
        """
        
        result = await groq_service.generate_legal_advice(detailed_prompt, max_tokens=1200)
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["error"])
        
        return ChatResponse(
            user_message=request.problem_description,
            ai_response=result["response"],
            model=result["model"],
            tokens_used=result.get("tokens_used"),
            specialization="bangladesh_legal_advisor",
            timestamp=datetime.now(),
            status="success"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"আইনি পরামর্শ প্রাপ্তিতে সমস্যা: {str(e)}"
        )

@router.post("/legal-procedure")
async def get_legal_procedure(request: LegalProcedureRequest):
    """
    নির্দিষ্ট ধরণের মামলার জন্য ধাপে ধাপে আইনি প্রক্রিয়া
    Step-by-step legal procedure for specific case types
    """
    try:
        result = await groq_service.get_legal_procedures(request.case_type)
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["error"])
        
        return {
            "case_type": request.case_type,
            "location": request.location,
            "procedure": result["procedure"],
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"আইনি প্রক্রিয়ার তথ্য পেতে সমস্যা: {str(e)}"
        )

@router.post("/explain-law")
async def explain_bangladesh_law(request: LawExplanationRequest):
    """
    বাংলাদেশের নির্দিষ্ট আইন সম্পর্কে সহজ ব্যাখ্যা
    Simple explanation of specific Bangladesh laws
    """
    try:
        result = await groq_service.explain_bangladesh_law(request.law_topic)
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["error"])
        
        return {
            "law_topic": request.law_topic,
            "explanation": result["response"],
            "complexity_level": request.complexity_level,
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"আইন ব্যাখ্যায় সমস্যা: {str(e)}"
        )

@router.post("/legal-rights")
async def get_legal_rights(request: LegalRightsRequest):
    """
    নির্দিষ্ট পরিস্থিতিতে আইনি অধিকার জানুন
    Know your legal rights in specific situations
    """
    try:
        result = await groq_service.get_legal_rights(request.situation)
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["error"])
        
        return {
            "situation": request.situation,
            "person_type": request.person_type,
            "rights": result["response"],
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"অধিকার সম্পর্কিত তথ্য পেতে সমস্যা: {str(e)}"
        )

@router.post("/document-requirements")
async def get_document_requirements(request: DocumentRequirementRequest):
    """
    আইনি কাজের জন্য প্রয়োজনীয় কাগজপত্রের তালিকা
    List of required documents for legal actions
    """
    try:
        result = await groq_service.get_document_requirements(request.legal_action)
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["error"])
        
        return {
            "legal_action": request.legal_action,
            "location": request.location,
            "documents": result["response"],
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"কাগজপত্রের তথ্য পেতে সমস্যা: {str(e)}"
        )

@router.get("/emergency-contacts")
async def get_emergency_legal_contacts(location: str = Query(default="ঢাকা", description="আপনার অবস্থান")):
    """
    জরুরি আইনি সহায়তার যোগাযোগের তথ্য
    Emergency legal help contact information
    """
    try:
        result = await groq_service.get_legal_contact_info(location)
        
        return {
            "location": location,
            "emergency_contacts": result["contact_info"],
            "message": result["message"],
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
    except Exception as e:
        return {
            "location": location,
            "error": f"যোগাযোগের তথ্য পেতে সমস্যা: {str(e)}",
            "emergency_contacts": {
                "police": "৯৯৯",
                "national_legal_aid": "১৬১০৩",
                "women_helpline": "১০৯২১"
            },
            "status": "error"
        }

@router.get("/legal-categories")
async def get_legal_categories():
    """
    বাংলাদেশের আইনের বিভিন্ন ক্যাটাগরি
    Different categories of Bangladesh law
    """
    categories = {
        "family_law": {
            "name": "পারিবারিক আইন (Family Law)",
            "topics": ["বিবাহ", "তালাক", "ভরণপোষণ", "সন্তানের অধিকার", "উত্তরাধিকার"],
            "description": "পারিবারিক সম্পর্ক এবং দায়বদ্ধতা সংক্রান্ত আইন"
        },
        "property_law": {
            "name": "সম্পত্তি আইন (Property Law)",
            "topics": ["জমি ক্রয়-বিক্রয়", "ভাড়া", "দখল", "রেজিস্ট্রেশন", "মালিকানা"],
            "description": "সম্পত্তির মালিকানা এবং লেনদেন সংক্রান্ত আইন"
        },
        "criminal_law": {
            "name": "ফৌজদারি আইন (Criminal Law)",
            "topics": ["চুরি", "প্রতারণা", "আক্রমণ", "হত্যা", "মাদক"],
            "description": "অপরাধ এবং শাস্তি সংক্রান্ত আইন"
        },
        "labor_law": {
            "name": "শ্রম আইন (Labor Law)",
            "topics": ["চাকরি", "বেতন", "ছুটি", "অবসর", "কর্মী অধিকার"],
            "description": "কর্মী এবং মালিকের অধিকার ও দায়বদ্ধতা"
        },
        "consumer_law": {
            "name": "ভোক্তা অধিকার (Consumer Rights)",
            "topics": ["পণ্য ফেরত", "প্রতারণা", "গুণগত মান", "বিজ্ঞাপন", "সেবা"],
            "description": "ভোক্তাদের অধিকার এবং সুরক্ষা"
        },
        "cyber_law": {
            "name": "সাইবার আইন (Cyber Law)",
            "topics": ["হ্যাকিং", "অনলাইন প্রতারণা", "ডিজিটাল নিরাপত্তা", "সামাজিক মাধ্যম"],
            "description": "ডিজিটাল অপরাধ এবং অনলাইন নিরাপত্তা"
        }
    }
    
    return {
        "legal_categories": categories,
        "total_categories": len(categories),
        "message": "বাংলাদেশের আইনের প্রধান ক্যাটাগরিসমূহ",
        "timestamp": datetime.now().isoformat(),
        "status": "success"
    }

@router.get("/quick-legal-tips")
async def get_quick_legal_tips():
    """
    দৈনন্দিন জীবনে কাজে আসে এমন আইনি টিপস
    Quick legal tips for daily life
    """
    tips = [
        {
            "title": "কাগজপত্র সংরক্ষণ",
            "tip": "সব গুরুত্বপূর্ণ কাগজপত্রের ফটোকপি এবং স্ক্যান কপি রাখুন।",
            "importance": "high"
        },
        {
            "title": "চুক্তিপত্র",
            "tip": "যেকোনো চুক্তি সাক্ষর করার আগে ভালোভাবে পড়ুন এবং বুঝুন।",
            "importance": "high"
        },
        {
            "title": "আইনি সাহায্য",
            "tip": "জটিল আইনি সমস্যায় অভিজ্ঞ আইনজীবীর পরামর্শ নিন।",
            "importance": "high"
        },
        {
            "title": "প্রমাণ সংরক্ষণ",
            "tip": "যেকোনো বিরোধের ক্ষেত্রে প্রমাণ (SMS, ইমেইল, রসিদ) সংরক্ষণ করুন।",
            "importance": "medium"
        },
        {
            "title": "সময়সীমা",
            "tip": "আইনি মামলার সময়সীমা (limitation period) সম্পর্কে সচেতন থাকুন।",
            "importance": "medium"
        }
    ]
    
    return {
        "legal_tips": tips,
        "total_tips": len(tips),
        "message": "দৈনন্দিন জীবনে কাজে আসে এমন আইনি পরামর্শ",
        "timestamp": datetime.now().isoformat(),
        "status": "success"
    }