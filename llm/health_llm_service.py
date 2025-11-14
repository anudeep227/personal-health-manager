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

# Optional AI dependencies
try:
    import openai
    import torch
    from transformers import pipeline
    AI_AVAILABLE = True
except ImportError as e:
    AI_AVAILABLE = False
    # Create dummy classes for type hints
    class openai:
        class OpenAI:
            def __init__(self, api_key): pass

from src.utils.config import Config


class HealthLLMService:
    """Service for AI/LLM integration in health management"""
    
    def __init__(self):
        self.config = Config()
        self.openai_client = None
        self.local_model = None
        self.setup_models()
    
    def setup_models(self):
        """Initialize AI models"""
        if not AI_AVAILABLE:
            print("AI libraries not available. Document analysis will use basic text processing only.")
            return
            
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
    
    def analyze_document_comprehensive(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive document analysis with specialized handling for different document types
        """
        try:
            text_content = document_data.get('text_content', '')
            document_type = document_data.get('document_type', 'unknown')
            metadata = document_data.get('metadata', {})
            
            if not text_content.strip():
                return {"error": "No text content to analyze"}
            
            # Route to specialized analysis based on document type
            if document_type == 'ecg':
                return self.analyze_ecg_report(text_content, metadata)
            elif document_type == 'blood_test':
                return self.analyze_blood_test_results(text_content, metadata)
            elif document_type == 'prescription':
                return self.analyze_prescription(text_content, metadata)
            elif document_type == 'radiology':
                return self.analyze_radiology_report(text_content, metadata)
            elif document_type == 'lab_report':
                return self.analyze_lab_report(text_content, metadata)
            else:
                return self.analyze_general_medical_document(text_content, metadata)
                
        except Exception as e:
            print(f"Error in comprehensive document analysis: {e}")
            return {"error": str(e)}
    
    def analyze_ecg_report(self, text_content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze ECG/EKG reports"""
        try:
            prompt = f"""
            Analyze this ECG/EKG report and extract key cardiac information:
            
            {text_content}
            
            Please identify and explain:
            1. Heart rate and rhythm
            2. Any abnormalities detected
            3. Clinical significance of findings
            4. Recommendations for follow-up
            5. Key measurements (intervals, axes, etc.)
            
            Provide a clear, structured analysis that a patient can understand.
            Include appropriate medical disclaimers.
            """
            
            if self.openai_client:
                response = self._query_openai(prompt, max_tokens=1000)
                return {
                    "document_type": "ecg_analysis",
                    "analysis": response,
                    "extracted_data": self._extract_ecg_data(text_content),
                    "recommendations": self._get_ecg_recommendations(response),
                    "disclaimer": "This analysis is for informational purposes only. Consult a cardiologist for medical interpretation."
                }
            else:
                return self._basic_ecg_analysis(text_content)
                
        except Exception as e:
            return {"error": f"ECG analysis failed: {e}"}
    
    def analyze_blood_test_results(self, text_content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze blood test results"""
        try:
            prompt = f"""
            Analyze these blood test results and provide patient-friendly explanations:
            
            {text_content}
            
            Please provide:
            1. Summary of all test values
            2. Which values are within/outside normal ranges
            3. Clinical significance of abnormal values
            4. Lifestyle factors that might influence results
            5. Recommendations for follow-up
            
            Use clear, non-technical language while remaining accurate.
            """
            
            if self.openai_client:
                response = self._query_openai(prompt, max_tokens=1200)
                return {
                    "document_type": "blood_test_analysis",
                    "analysis": response,
                    "extracted_values": self._extract_lab_values(text_content),
                    "abnormal_flags": self._identify_abnormal_values(text_content),
                    "trending_data": self._suggest_trending_parameters(text_content),
                    "disclaimer": "Results should be discussed with your healthcare provider for proper medical interpretation."
                }
            else:
                return self._basic_blood_test_analysis(text_content)
                
        except Exception as e:
            return {"error": f"Blood test analysis failed: {e}"}
    
    def analyze_prescription(self, text_content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze prescription documents"""
        try:
            prompt = f"""
            Analyze this prescription and provide medication information:
            
            {text_content}
            
            Please extract and explain:
            1. All medications prescribed (name, dosage, frequency)
            2. Purpose of each medication
            3. Important side effects to watch for
            4. Drug interactions to be aware of
            5. Instructions for taking medications
            6. Duration of treatment
            
            Provide clear, actionable information for the patient.
            """
            
            if self.openai_client:
                response = self._query_openai(prompt, max_tokens=1000)
                medications = self._extract_medications_from_text(text_content)
                
                return {
                    "document_type": "prescription_analysis",
                    "analysis": response,
                    "medications": medications,
                    "interaction_check": self.analyze_medication_interactions([med['name'] for med in medications]),
                    "adherence_tips": self._get_medication_adherence_tips(medications),
                    "disclaimer": "Follow your doctor's instructions. Contact your healthcare provider with any concerns."
                }
            else:
                return self._basic_prescription_analysis(text_content)
                
        except Exception as e:
            return {"error": f"Prescription analysis failed: {e}"}
    
    def analyze_radiology_report(self, text_content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze radiology reports (X-ray, CT, MRI, etc.)"""
        try:
            prompt = f"""
            Analyze this radiology report and provide patient-friendly explanations:
            
            {text_content}
            
            Please explain:
            1. Type of imaging study performed
            2. Key findings in simple terms
            3. What normal vs abnormal findings mean
            4. Clinical significance of any abnormalities
            5. Recommended follow-up actions
            
            Translate medical terminology into understandable language.
            """
            
            if self.openai_client:
                response = self._query_openai(prompt, max_tokens=1000)
                return {
                    "document_type": "radiology_analysis",
                    "analysis": response,
                    "imaging_type": self._identify_imaging_type(text_content),
                    "key_findings": self._extract_radiology_findings(text_content),
                    "follow_up_needed": self._assess_follow_up_urgency(text_content),
                    "disclaimer": "Radiology results should be reviewed with your doctor for proper medical context."
                }
            else:
                return self._basic_radiology_analysis(text_content)
                
        except Exception as e:
            return {"error": f"Radiology analysis failed: {e}"}
    
    def analyze_lab_report(self, text_content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze general laboratory reports"""
        try:
            prompt = f"""
            Analyze this laboratory report and provide comprehensive insights:
            
            {text_content}
            
            Please provide:
            1. Summary of all test results
            2. Normal vs abnormal values with explanations
            3. Potential health implications
            4. Lifestyle recommendations based on results
            5. Questions to ask your healthcare provider
            
            Make the information accessible and actionable for patients.
            """
            
            if self.openai_client:
                response = self._query_openai(prompt, max_tokens=1200)
                return {
                    "document_type": "lab_report_analysis",
                    "analysis": response,
                    "test_categories": self._categorize_lab_tests(text_content),
                    "critical_values": self._identify_critical_values(text_content),
                    "trend_recommendations": self._suggest_monitoring_schedule(text_content),
                    "disclaimer": "Laboratory results require professional medical interpretation."
                }
            else:
                return self._basic_lab_analysis(text_content)
                
        except Exception as e:
            return {"error": f"Lab report analysis failed: {e}"}
    
    def analyze_general_medical_document(self, text_content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze general medical documents"""
        try:
            prompt = f"""
            Analyze this medical document and extract important information:
            
            {text_content}
            
            Please provide:
            1. Document summary and purpose
            2. Key medical information
            3. Important dates and appointments
            4. Action items or follow-up requirements
            5. Questions to discuss with healthcare providers
            
            Organize the information in a patient-friendly format.
            """
            
            if self.openai_client:
                response = self._query_openai(prompt, max_tokens=1000)
                return {
                    "document_type": "general_medical_analysis",
                    "analysis": response,
                    "key_points": self._extract_key_points(text_content),
                    "action_items": self._identify_action_items(text_content),
                    "medical_terms": self._explain_medical_terms(text_content),
                    "disclaimer": "This analysis is for informational purposes. Consult your healthcare provider for medical advice."
                }
            else:
                return self._basic_document_summary(text_content)
                
        except Exception as e:
            return {"error": f"Document analysis failed: {e}"}
    
    def generate_document_summary(self, document_data: Dict[str, Any]) -> str:
        """Generate a concise summary of the document analysis"""
        try:
            analysis = self.analyze_document_comprehensive(document_data)
            
            if "error" in analysis:
                return f"Analysis Error: {analysis['error']}"
            
            doc_type = analysis.get('document_type', 'unknown')
            analysis_text = analysis.get('analysis', '')
            
            summary_prompt = f"""
            Create a concise 2-3 sentence summary of this medical document analysis:
            
            Document Type: {doc_type}
            Analysis: {analysis_text}
            
            Focus on the most important findings and recommendations.
            """
            
            if self.openai_client:
                summary = self._query_openai(summary_prompt, max_tokens=200)
                return summary.strip()
            else:
                return f"Document processed: {doc_type}. {len(analysis_text)} characters of analysis generated."
                
        except Exception as e:
            return f"Summary generation failed: {e}"
    
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
    
    # Helper methods for document analysis
    def _extract_ecg_data(self, text: str) -> Dict[str, Any]:
        """Extract ECG-specific data from text"""
        import re
        
        data = {}
        
        # Extract heart rate
        hr_match = re.search(r'heart rate[:\s]*(\d+)', text, re.IGNORECASE)
        if hr_match:
            data['heart_rate'] = int(hr_match.group(1))
        
        # Extract PR interval
        pr_match = re.search(r'PR[:\s]*(interval[:\s]*)?(\d+)', text, re.IGNORECASE)
        if pr_match:
            data['pr_interval'] = int(pr_match.group(2))
        
        # Extract QRS duration
        qrs_match = re.search(r'QRS[:\s]*(\d+)', text, re.IGNORECASE)
        if qrs_match:
            data['qrs_duration'] = int(qrs_match.group(1))
        
        return data
    
    def _extract_lab_values(self, text: str) -> List[Dict[str, Any]]:
        """Extract laboratory values from text"""
        import re
        
        values = []
        
        # Common lab value patterns
        patterns = [
            r'(\w+)[:\s]*([\d.]+)\s*([a-zA-Z/]+)',  # Test: Value Unit
            r'(\w+)[:\s]*([\d.]+)',  # Test: Value
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match) == 3:
                    values.append({
                        'test': match[0],
                        'value': float(match[1]),
                        'unit': match[2]
                    })
                elif len(match) == 2:
                    values.append({
                        'test': match[0],
                        'value': float(match[1]),
                        'unit': ''
                    })
        
        return values
    
    def _extract_medications_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract medication information from prescription text"""
        import re
        
        medications = []
        
        # Common medication patterns
        med_patterns = [
            r'(\w+)\s*(\d+(?:\.\d+)?)\s*(mg|g|ml|mcg)',  # Name Dose Unit
            r'(\w+)\s*-\s*(\d+)\s*(mg|g|ml|mcg)',  # Name - Dose Unit
        ]
        
        for pattern in med_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                medications.append({
                    'name': match[0],
                    'dose': float(match[1]),
                    'unit': match[2].lower()
                })
        
        return medications
    
    def _identify_abnormal_values(self, text: str) -> List[str]:
        """Identify values flagged as abnormal"""
        abnormal_indicators = ['high', 'low', 'abnormal', 'elevated', 'decreased', '*', 'H', 'L']
        abnormal_values = []
        
        lines = text.split('\n')
        for line in lines:
            if any(indicator in line.lower() for indicator in abnormal_indicators):
                abnormal_values.append(line.strip())
        
        return abnormal_values
    
    def _extract_key_points(self, text: str) -> List[str]:
        """Extract key points from medical document"""
        # Simple extraction - look for sentences with medical keywords
        medical_keywords = ['diagnosis', 'treatment', 'medication', 'follow-up', 'recommendation']
        
        sentences = text.split('.')
        key_points = []
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in medical_keywords):
                key_points.append(sentence.strip())
        
        return key_points[:5]  # Return top 5
    
    def _identify_action_items(self, text: str) -> List[str]:
        """Identify action items from medical document"""
        action_keywords = ['follow up', 'schedule', 'return', 'contact', 'monitor', 'continue', 'stop']
        
        sentences = text.split('.')
        actions = []
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in action_keywords):
                actions.append(sentence.strip())
        
        return actions
    
    def _explain_medical_terms(self, text: str) -> Dict[str, str]:
        """Basic medical term explanations"""
        # This would ideally use a medical dictionary API
        common_terms = {
            'hypertension': 'High blood pressure',
            'diabetes': 'High blood sugar condition',
            'hyperlipidemia': 'High cholesterol',
            'tachycardia': 'Fast heart rate',
            'bradycardia': 'Slow heart rate'
        }
        
        found_terms = {}
        text_lower = text.lower()
        
        for term, explanation in common_terms.items():
            if term in text_lower:
                found_terms[term] = explanation
        
        return found_terms
    
    # Fallback methods for when AI is not available
    def _basic_ecg_analysis(self, text: str) -> Dict[str, Any]:
        """Basic ECG analysis without AI"""
        return {
            "document_type": "ecg_analysis",
            "analysis": "ECG document detected. Professional interpretation recommended.",
            "extracted_data": self._extract_ecg_data(text),
            "disclaimer": "Consult a cardiologist for proper ECG interpretation."
        }
    
    def _basic_blood_test_analysis(self, text: str) -> Dict[str, Any]:
        """Basic blood test analysis without AI"""
        return {
            "document_type": "blood_test_analysis",
            "analysis": "Blood test results detected. Review with healthcare provider.",
            "extracted_values": self._extract_lab_values(text),
            "disclaimer": "Discuss results with your healthcare provider."
        }
    
    def _basic_prescription_analysis(self, text: str) -> Dict[str, Any]:
        """Basic prescription analysis without AI"""
        medications = self._extract_medications_from_text(text)
        return {
            "document_type": "prescription_analysis",
            "analysis": "Prescription document processed.",
            "medications": medications,
            "disclaimer": "Follow your doctor's instructions exactly."
        }
    
    def _basic_document_summary(self, text: str) -> Dict[str, Any]:
        """Basic document summary without AI"""
        return {
            "document_type": "general_medical_analysis",
            "analysis": f"Medical document processed. {len(text)} characters extracted.",
            "key_points": self._extract_key_points(text),
            "disclaimer": "Consult healthcare providers for medical interpretation."
        }