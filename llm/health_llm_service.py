"""
LLM Integration Module for AI-powered health insights
This module provides AI capabilities for future features like:
- Medical document analysis
- Symptom assessment
- Health recommendations
- Medication interaction checking
"""

import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import openai
from transformers import pipeline
import torch

from utils.config import Config


class HealthLLMService:
    """Service for AI/LLM integration in health management"""
    
    def __init__(self):
        self.config = Config()
        self.openai_client = None
        self.local_model = None
        self.setup_models()
    
    def setup_models(self):
        """Initialize AI models"""
        try:
            # Setup OpenAI (for production use)
            openai_key = os.getenv('OPENAI_API_KEY')
            if openai_key and openai_key != 'your_openai_api_key_here':
                self.openai_client = openai.OpenAI(api_key=openai_key)
                print("OpenAI client initialized")
            else:
                print("OpenAI API key not configured. AI features will use local models only.")
            
            # Setup local model for privacy-sensitive tasks
            if torch.cuda.is_available():
                device = "cuda"
            else:
                device = "cpu"
            
            # Initialize a lightweight local model for basic tasks
            try:
                self.local_model = pipeline(
                    "text-generation",
                    model="microsoft/DialoGPT-small",  # Lightweight conversational model
                    device=device
                )
                print(f"Local model initialized on {device}")
            except Exception as e:
                print(f"Could not initialize local model: {e}")
                
        except Exception as e:
            print(f"Error setting up AI models: {e}")
    
    def analyze_medication_interactions(self, medications: List[str]) -> Dict[str, Any]:
        """
        Analyze potential medication interactions
        """
        try:
            if not medications or len(medications) < 2:
                return {"interactions": [], "warnings": []}
            
            # Create prompt for medication interaction analysis
            medications_list = ", ".join(medications)
            prompt = f"""
            Analyze potential interactions between these medications: {medications_list}
            
            Please provide:
            1. Any known dangerous interactions
            2. Mild interactions to be aware of
            3. General recommendations
            
            Format the response as a structured analysis.
            """
            
            if self.openai_client:
                response = self._query_openai(prompt, max_tokens=500)
                return self._parse_interaction_response(response)
            else:
                # Fallback to local analysis or simple warnings
                return self._basic_interaction_check(medications)
                
        except Exception as e:
            print(f"Error analyzing medication interactions: {e}")
            return {"error": str(e)}
    
    def analyze_health_document(self, document_text: str) -> Dict[str, Any]:
        """
        Analyze medical documents and extract key information
        """
        try:
            if not document_text.strip():
                return {"error": "No document text provided"}
            
            prompt = f"""
            Analyze this medical document and extract key information:
            
            {document_text}
            
            Please identify:
            1. Key findings or results
            2. Medications mentioned
            3. Diagnoses or conditions
            4. Important dates
            5. Follow-up recommendations
            
            Provide a structured summary.
            """
            
            if self.openai_client:
                response = self._query_openai(prompt, max_tokens=800)
                return self._parse_document_analysis(response)
            else:
                return self._basic_document_analysis(document_text)
                
        except Exception as e:
            print(f"Error analyzing health document: {e}")
            return {"error": str(e)}
    
    def get_health_recommendations(self, user_profile: Dict[str, Any], 
                                 recent_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate personalized health recommendations
        """
        try:
            # Create context from user profile and recent records
            context = self._build_health_context(user_profile, recent_records)
            
            prompt = f"""
            Based on this health information, provide personalized health recommendations:
            
            {context}
            
            Please provide:
            1. General health tips
            2. Lifestyle recommendations
            3. Areas that might need attention
            4. Preventive care suggestions
            
            Keep recommendations general and emphasize consulting healthcare providers.
            """
            
            if self.openai_client:
                response = self._query_openai(prompt, max_tokens=600)
                return self._parse_recommendations(response)
            else:
                return self._basic_health_recommendations(user_profile)
                
        except Exception as e:
            print(f"Error generating health recommendations: {e}")
            return {"error": str(e)}
    
    def symptom_assessment(self, symptoms: List[str], user_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provide basic symptom assessment (NOT medical diagnosis)
        """
        try:
            if not symptoms:
                return {"error": "No symptoms provided"}
            
            symptoms_text = ", ".join(symptoms)
            
            prompt = f"""
            A person is experiencing these symptoms: {symptoms_text}
            
            Please provide:
            1. General information about these symptoms
            2. When to seek medical attention
            3. Basic self-care suggestions
            4. Clear disclaimer that this is not medical advice
            
            IMPORTANT: Emphasize seeking professional medical advice and do not provide diagnosis.
            """
            
            if self.openai_client:
                response = self._query_openai(prompt, max_tokens=500)
                return self._parse_symptom_assessment(response)
            else:
                return self._basic_symptom_guidance(symptoms)
                
        except Exception as e:
            print(f"Error in symptom assessment: {e}")
            return {"error": str(e)}
    
    def _query_openai(self, prompt: str, max_tokens: int = 500) -> str:
        """Query OpenAI API"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful health information assistant. Always emphasize consulting healthcare professionals and never provide medical diagnoses."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return ""
    
    def _basic_interaction_check(self, medications: List[str]) -> Dict[str, Any]:
        """Basic medication interaction check without AI"""
        # This is a simple fallback - in practice, you'd use a medical database
        common_interactions = {
            ("warfarin", "aspirin"): "Increased bleeding risk",
            ("metformin", "alcohol"): "Risk of lactic acidosis",
            ("statins", "grapefruit"): "Increased statin levels"
        }
        
        interactions = []
        for i, med1 in enumerate(medications):
            for med2 in medications[i+1:]:
                key1 = (med1.lower(), med2.lower())
                key2 = (med2.lower(), med1.lower())
                
                if key1 in common_interactions:
                    interactions.append({
                        "medications": [med1, med2],
                        "interaction": common_interactions[key1],
                        "severity": "moderate"
                    })
                elif key2 in common_interactions:
                    interactions.append({
                        "medications": [med1, med2],
                        "interaction": common_interactions[key2],
                        "severity": "moderate"
                    })
        
        return {
            "interactions": interactions,
            "warnings": ["Always consult your healthcare provider about medication interactions"]
        }
    
    def _basic_document_analysis(self, text: str) -> Dict[str, Any]:
        """Basic document analysis without AI"""
        # Simple keyword extraction
        keywords = {
            "medications": ["medication", "drug", "prescription", "pill", "tablet"],
            "conditions": ["diagnosis", "condition", "disease", "syndrome"],
            "results": ["result", "finding", "test", "level", "count"]
        }
        
        findings = {}
        for category, words in keywords.items():
            findings[category] = []
            for word in words:
                if word in text.lower():
                    findings[category].append(f"Contains {word} references")
        
        return {
            "summary": "Basic document analysis completed",
            "findings": findings,
            "recommendation": "Use AI analysis for detailed insights"
        }
    
    def _basic_health_recommendations(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Basic health recommendations without AI"""
        recommendations = [
            "Maintain a balanced diet with fruits and vegetables",
            "Exercise regularly (at least 30 minutes, 5 days a week)",
            "Get adequate sleep (7-9 hours per night)",
            "Stay hydrated throughout the day",
            "Schedule regular check-ups with your healthcare provider",
            "Take medications as prescribed",
            "Monitor your health metrics regularly"
        ]
        
        return {
            "general_recommendations": recommendations,
            "note": "These are general health tips. Consult your healthcare provider for personalized advice."
        }
    
    def _basic_symptom_guidance(self, symptoms: List[str]) -> Dict[str, Any]:
        """Basic symptom guidance without AI"""
        emergency_keywords = ["chest pain", "difficulty breathing", "severe headache", "loss of consciousness"]
        
        urgent_care = any(keyword in " ".join(symptoms).lower() for keyword in emergency_keywords)
        
        return {
            "guidance": "Symptom information is available",
            "urgent_care_needed": urgent_care,
            "recommendation": "Consult a healthcare professional for proper evaluation",
            "disclaimer": "This is not medical advice. Always seek professional medical attention for health concerns."
        }
    
    def _build_health_context(self, profile: Dict[str, Any], records: List[Dict[str, Any]]) -> str:
        """Build context string from health data"""
        context_parts = []
        
        if profile:
            context_parts.append(f"User Profile: Age range, medical conditions, medications")
        
        if records:
            context_parts.append(f"Recent health records: {len(records)} entries")
        
        return "\n".join(context_parts)
    
    def _parse_interaction_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for medication interactions"""
        # This would parse the AI response into structured data
        return {
            "interactions": [],
            "analysis": response,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _parse_document_analysis(self, response: str) -> Dict[str, Any]:
        """Parse AI response for document analysis"""
        return {
            "analysis": response,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _parse_recommendations(self, response: str) -> Dict[str, Any]:
        """Parse AI response for health recommendations"""
        return {
            "recommendations": response,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _parse_symptom_assessment(self, response: str) -> Dict[str, Any]:
        """Parse AI response for symptom assessment"""
        return {
            "assessment": response,
            "disclaimer": "This is not medical advice. Always consult healthcare professionals.",
            "timestamp": datetime.utcnow().isoformat()
        }