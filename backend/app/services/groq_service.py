from groq import Groq
from core.config import settings
from typing import Optional, AsyncGenerator, List, Dict
import json
from datetime import datetime

class GroqService:
    def __init__(self):
        """
        Initialize Groq client for Bangladesh Legal AI Assistant
        """
        if not settings.groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=settings.groq_api_key)
        self.model = "llama3-8b-8192"
        
        # Bangladesh Legal AI Assistant System Prompt
        self.system_prompt = """You are a Bangladesh Legal Information Assistant (বাংলাদেশ আইনি তথ্য সহায়ক).

Your expertise covers:
🏛️ **Bangladesh Legal System:**
- Constitution of Bangladesh
- Civil laws, Criminal laws, Family laws
- Labor laws, Property laws, Business laws
- Consumer rights, Digital laws
- Court procedures and legal processes

🎯 **Your Role:**
- Explain Bangladesh laws in simple language (Bengali/English)
- Provide step-by-step legal guidance
- Suggest proper legal procedures and documentation
- Help understand rights and responsibilities
- Guide on when and how to seek legal help

📋 **Response Format:**
1. **আইনি বিশ্লেষণ (Legal Analysis):** Explain the legal situation
2. **আপনার অধিকার (Your Rights):** What rights the person has
3. **পরবর্তী পদক্ষেপ (Next Steps):** Actionable steps to take
4. **প্রয়োজনীয় কাগজপত্র (Required Documents):** What documents needed
5. **কোথায় যেতে হবে (Where to Go):** Relevant offices/courts
6. **আনুমানিক খরচ (Estimated Cost):** If applicable
7. **সতর্কতা (Warnings):** Important legal considerations

🚨 **Important Guidelines:**
- Always mention this is general legal information
- Emphasize consulting qualified lawyers for specific cases
- Provide both Bengali and English explanations when helpful
- Focus on Bangladesh laws and procedures
- Be supportive and clear in explanations

Remember: আইনি পরামর্শ নেওয়ার জন্য অভিজ্ঞ আইনজীবীর সাথে যোগাযোগ করুন।"""

    async def generate_legal_advice(self, legal_problem: str, max_tokens: int = 1200) -> dict:
        """
        Generate Bangladesh-specific legal advice
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt
                    },
                    {
                        "role": "user",
                        "content": f"আইনি সমস্যা/Legal Problem: {legal_problem}"
                    }
                ],
                model=self.model,
                max_tokens=max_tokens,
                temperature=0.2,  # Very low temperature for consistent legal info
                stream=False
            )
            
            ai_response = chat_completion.choices[0].message.content
            
            # Add legal disclaimer in Bengali and English
            legal_disclaimer = """

⚖️ **আইনি দাবিত্যাগ / Legal Disclaimer:**
এই তথ্য শুধুমাত্র সাধারণ আইনি শিক্ষার উদ্দেশ্যে প্রদান করা হয়েছে। এটি কোনো আইনি পরামর্শ নয়। আপনার নির্দিষ্ট সমস্যার জন্য অবশ্যই একজন যোগ্য আইনজীবীর সাথে পরামর্শ করুন।

This information is provided for general legal education purposes only and does not constitute legal advice. Please consult with a qualified lawyer for your specific legal matters."""
            
            return {
                "response": ai_response + legal_disclaimer,
                "model": self.model,
                "tokens_used": chat_completion.usage.total_tokens,
                "specialization": "bangladesh_legal",
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
            
        except Exception as e:
            return {
                "response": "দুঃখিত, আইনি তথ্য প্রদানে সমস্যা হচ্ছে। পরে আবার চেষ্টা করুন অথবা সরাসরি আইনজীবীর সাথে যোগাযোগ করুন।",
                "error": str(e),
                "status": "error"
            }
    
    async def get_legal_procedures(self, case_type: str) -> dict:
        """
        Get step-by-step legal procedures for specific case types
        """
        procedure_prompt = f"বাংলাদেশে '{case_type}' এর জন্য ধাপে ধাপে আইনি প্রক্রিয়া বর্ণনা করুন। প্রয়োজনীয় কাগজপত্র, খরচ, এবং সময়সীমা উল্লেখ করুন।"
        
        try:
            response = await self.generate_legal_advice(procedure_prompt, max_tokens=1000)
            return {
                "procedure": response["response"],
                "case_type": case_type,
                "status": "success"
            }
        except Exception as e:
            return {
                "procedure": "আইনি প্রক্রিয়ার তথ্য পেতে সমস্যা হচ্ছে। আইনজীবীর সাথে যোগাযোগ করুন।",
                "status": "error",
                "error": str(e)
            }
    
    async def explain_bangladesh_law(self, law_topic: str) -> dict:
        """
        Explain specific Bangladesh laws in simple language
        """
        law_prompt = f"বাংলাদেশের '{law_topic}' আইন সম্পর্কে সহজ ভাষায় ব্যাখ্যা করুন। সাধারণ মানুষ কিভাবে এই আইন প্রয়োগ করতে পারেন তা বলুন।"
        
        return await self.generate_legal_advice(law_prompt, max_tokens=800)
    
    async def get_legal_rights(self, situation: str) -> dict:
        """
        Explain legal rights in specific situations
        """
        rights_prompt = f"'{situation}' পরিস্থিতিতে বাংলাদেশের আইন অনুযায়ী একজন ব্যক্তির কি কি অধিকার রয়েছে? বিস্তারিত বলুন।"
        
        return await self.generate_legal_advice(rights_prompt, max_tokens=800)
    
    async def get_document_requirements(self, legal_action: str) -> dict:
        """
        Get required documents for specific legal actions
        """
        doc_prompt = f"বাংলাদেশে '{legal_action}' এর জন্য কি কি কাগজপত্র এবং প্রমাণ প্রয়োজন? বিস্তারিত তালিকা দিন।"
        
        return await self.generate_legal_advice(doc_prompt, max_tokens=600)
    
    async def get_legal_contact_info(self, location: str = "ঢাকা") -> dict:
        """
        Provide legal help contact information
        """
        contact_info = {
            "bar_associations": {
                "dhaka": "ঢাকা বার অ্যাসোসিয়েশন: ০২-৯৫৬২৬৮১",
                "chittagong": "চট্টগ্রাম বার অ্যাসোসিয়েশন: ০৩১-২৮৫২৩৪১",
                "sylhet": "সিলেট বার অ্যাসোসিয়েশন: ০৮২১-৭১৬২৩৪"
            },
            "legal_aid": {
                "national": "জাতীয় আইনি সহায়তা প্রদান সংস্থা: ১৬১০৩",
                "blast": "BLAST (আইনি সহায়তা): ০২-৯৮৮২২৮৯"
            },
            "emergency": {
                "police": "পুলিশ: ৯৯৯",
                "women_helpline": "মহিলা হেল্পলাইন: ১০৯২১"
            }
        }
        
        return {
            "contact_info": contact_info,
            "message": f"{location} এলাকার আইনি সহায়তার জন্য এই নম্বরগুলোতে যোগাযোগ করুন।",
            "status": "success"
        }

# Global service instance
groq_service = GroqService()