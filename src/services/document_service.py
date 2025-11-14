"""
Document Service Layer for Health Management App
Coordinates document processing, LLM analysis, and database storage
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from pathlib import Path

from src.services.database_service import DatabaseService
from src.services.document_processing_service import DocumentProcessingService
from llm.health_llm_service import HealthLLMService
from src.models.database_models import (
    DocumentAnalysis, DocumentTag, ExtractedMedication, 
    ExtractedLabValue, DocumentSummary
)


class DocumentService:
    """
    High-level service for managing document analysis workflow
    Orchestrates document processing, AI analysis, and data storage
    """
    
    def __init__(self):
        self.db_service = DatabaseService()
        self.doc_processor = DocumentProcessingService()
        self.llm_service = HealthLLMService()
        self.logger = logging.getLogger(__name__)
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
    
    def analyze_document_complete(self, file_path: str, user_id: int = 1) -> Dict[str, Any]:
        """
        Complete document analysis workflow:
        1. Process document (extract text/data)
        2. Analyze with LLM
        3. Store results in database
        4. Return comprehensive results
        """
        try:
            start_time = datetime.now()
            
            # Step 1: Validate and process document
            is_valid, validation_message = self.doc_processor.validate_file(file_path)
            if not is_valid:
                return {"error": f"File validation failed: {validation_message}"}
            
            self.logger.info(f"Processing document: {file_path}")
            processing_result = self.doc_processor.process_document(file_path)
            
            if processing_result.get('error'):
                return {"error": f"Document processing failed: {processing_result['error']}"}
            
            # Step 2: Analyze with LLM
            self.logger.info("Starting AI analysis...")
            llm_analysis = self.llm_service.analyze_document_comprehensive(processing_result)
            
            # Step 3: Generate summary
            summary = self.llm_service.generate_document_summary(processing_result)
            
            # Step 4: Store in database
            processing_duration = (datetime.now() - start_time).total_seconds()
            document_id = self._store_analysis_results(
                processing_result, llm_analysis, summary, user_id, processing_duration
            )
            
            # Step 5: Extract and store structured data
            self._extract_and_store_structured_data(document_id, processing_result, llm_analysis)
            
            # Step 6: Prepare comprehensive response
            response = {
                "document_id": document_id,
                "processing_result": processing_result,
                "llm_analysis": llm_analysis,
                "summary": summary,
                "processing_duration": processing_duration,
                "success": True
            }
            
            self.logger.info(f"Document analysis completed successfully. ID: {document_id}")
            return response
            
        except Exception as e:
            self.logger.error(f"Document analysis failed: {e}")
            return {"error": f"Analysis failed: {str(e)}", "success": False}
    
    def _store_analysis_results(self, processing_result: Dict[str, Any], 
                              llm_analysis: Dict[str, Any], summary: str,
                              user_id: int, processing_duration: float) -> int:
        """Store document analysis results in database"""
        try:
            with self.db_service.get_session() as session:
                # Create main document analysis record
                document_analysis = DocumentAnalysis(
                    user_id=user_id,
                    file_name=processing_result.get('file_name', ''),
                    file_path=processing_result.get('file_path', ''),
                    file_extension=processing_result.get('file_extension', ''),
                    file_size_bytes=processing_result.get('file_size_bytes', 0),
                    document_type=processing_result.get('document_type', 'unknown'),
                    confidence_score=processing_result.get('confidence_score', 0.0),
                    
                    # Processing metadata
                    processing_method=processing_result.get('metadata', {}).get('method', 'unknown'),
                    processing_duration=processing_duration,
                    
                    # Content
                    text_content=processing_result.get('text_content', ''),
                    extracted_data=json.dumps(processing_result.get('metadata', {})),
                    
                    # AI Analysis
                    llm_analysis=json.dumps(llm_analysis),
                    key_findings=json.dumps(llm_analysis.get('key_findings', [])),
                    recommendations=json.dumps(llm_analysis.get('recommendations', [])),
                    medical_terms=json.dumps(llm_analysis.get('medical_terms', {})),
                    
                    analysis_status='completed'
                )
                
                session.add(document_analysis)
                session.flush()  # Get the ID
                document_id = document_analysis.id
                
                # Create document summary
                doc_summary = DocumentSummary(
                    document_id=document_id,
                    short_summary=summary,
                    detailed_summary=llm_analysis.get('analysis', ''),
                    key_points=json.dumps(llm_analysis.get('key_points', [])),
                    action_items=json.dumps(llm_analysis.get('action_items', [])),
                    summary_type='ai_generated',
                    model_used='gpt-3.5-turbo' if llm_analysis else 'local_processing'
                )
                
                session.add(doc_summary)
                
                # Add system tags based on document type
                self._add_system_tags(session, document_id, processing_result.get('document_type', 'unknown'))
                
                session.commit()
                return document_id
                
        except Exception as e:
            self.logger.error(f"Failed to store analysis results: {e}")
            raise
    
    def _extract_and_store_structured_data(self, document_id: int, 
                                         processing_result: Dict[str, Any],
                                         llm_analysis: Dict[str, Any]):
        """Extract and store structured data (medications, lab values, etc.)"""
        try:
            with self.db_service.get_session() as session:
                # Extract medications if present
                medications = llm_analysis.get('medications', [])
                if isinstance(medications, dict):
                    medications = medications.get('medications', [])
                
                for med_data in medications:
                    if isinstance(med_data, dict):
                        extracted_med = ExtractedMedication(
                            document_id=document_id,
                            medication_name=med_data.get('name', ''),
                            dosage=med_data.get('dose', ''),
                            frequency=med_data.get('frequency', ''),
                            duration=med_data.get('duration', ''),
                            instructions=med_data.get('instructions', ''),
                            extracted_confidence=med_data.get('confidence', 0.8)
                        )
                        session.add(extracted_med)
                
                # Extract lab values if present
                lab_values = llm_analysis.get('extracted_values', [])
                if isinstance(lab_values, dict):
                    lab_values = lab_values.get('values', [])
                
                for lab_data in lab_values:
                    if isinstance(lab_data, dict):
                        extracted_lab = ExtractedLabValue(
                            document_id=document_id,
                            test_name=lab_data.get('test', ''),
                            value=str(lab_data.get('value', '')),
                            unit=lab_data.get('unit', ''),
                            is_abnormal=lab_data.get('is_abnormal', False),
                            abnormal_flag=lab_data.get('flag', ''),
                            extracted_confidence=lab_data.get('confidence', 0.8)
                        )
                        session.add(extracted_lab)
                
                session.commit()
                
        except Exception as e:
            self.logger.error(f"Failed to extract structured data: {e}")
            # Don't raise - this is non-critical
    
    def _add_system_tags(self, session, document_id: int, document_type: str):
        """Add system-generated tags based on document type"""
        tag_mappings = {
            'ecg': ['cardiology', 'heart', 'diagnostic'],
            'blood_test': ['laboratory', 'blood', 'test_results'],
            'prescription': ['medication', 'pharmacy', 'treatment'],
            'radiology': ['imaging', 'diagnostic', 'radiology'],
            'lab_report': ['laboratory', 'test_results', 'clinical'],
            'medical_document': ['medical', 'healthcare', 'clinical']
        }
        
        tags = tag_mappings.get(document_type, ['medical', 'document'])
        
        for tag_name in tags:
            tag = DocumentTag(
                document_id=document_id,
                tag_name=tag_name,
                tag_type='system'
            )
            session.add(tag)
    
    def get_user_documents(self, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user's document analyses with summaries"""
        try:
            with self.db_service.get_session() as session:
                documents = session.query(DocumentAnalysis)\
                    .filter(DocumentAnalysis.user_id == user_id)\
                    .order_by(DocumentAnalysis.created_at.desc())\
                    .limit(limit)\
                    .all()
                
                result = []
                for doc in documents:
                    # Get summary
                    summary = session.query(DocumentSummary)\
                        .filter(DocumentSummary.document_id == doc.id)\
                        .first()
                    
                    # Get tags
                    tags = session.query(DocumentTag)\
                        .filter(DocumentTag.document_id == doc.id)\
                        .all()
                    
                    doc_data = {
                        'id': doc.id,
                        'file_name': doc.file_name,
                        'document_type': doc.document_type,
                        'confidence_score': doc.confidence_score,
                        'created_at': doc.created_at.isoformat(),
                        'short_summary': summary.short_summary if summary else '',
                        'tags': [tag.tag_name for tag in tags],
                        'is_critical': doc.is_critical,
                        'is_favorite': doc.is_favorite
                    }
                    result.append(doc_data)
                
                return result
                
        except Exception as e:
            self.logger.error(f"Failed to get user documents: {e}")
            return []
    
    def get_document_details(self, document_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific document"""
        try:
            with self.db_service.get_session() as session:
                # Get main document
                doc = session.query(DocumentAnalysis)\
                    .filter(DocumentAnalysis.id == document_id)\
                    .filter(DocumentAnalysis.user_id == user_id)\
                    .first()
                
                if not doc:
                    return None
                
                # Get summary
                summary = session.query(DocumentSummary)\
                    .filter(DocumentSummary.document_id == document_id)\
                    .first()
                
                # Get extracted medications
                medications = session.query(ExtractedMedication)\
                    .filter(ExtractedMedication.document_id == document_id)\
                    .all()
                
                # Get extracted lab values
                lab_values = session.query(ExtractedLabValue)\
                    .filter(ExtractedLabValue.document_id == document_id)\
                    .all()
                
                # Get tags
                tags = session.query(DocumentTag)\
                    .filter(DocumentTag.document_id == document_id)\
                    .all()
                
                # Compile detailed response
                return {
                    'document': {
                        'id': doc.id,
                        'file_name': doc.file_name,
                        'file_path': doc.file_path,
                        'document_type': doc.document_type,
                        'confidence_score': doc.confidence_score,
                        'text_content': doc.text_content,
                        'processing_duration': doc.processing_duration,
                        'created_at': doc.created_at.isoformat()
                    },
                    'analysis': json.loads(doc.llm_analysis) if doc.llm_analysis else {},
                    'summary': {
                        'short': summary.short_summary if summary else '',
                        'detailed': summary.detailed_summary if summary else '',
                        'key_points': json.loads(summary.key_points) if summary and summary.key_points else [],
                        'action_items': json.loads(summary.action_items) if summary and summary.action_items else []
                    },
                    'extracted_data': {
                        'medications': [
                            {
                                'name': med.medication_name,
                                'dosage': med.dosage,
                                'frequency': med.frequency,
                                'confidence': med.extracted_confidence
                            }
                            for med in medications
                        ],
                        'lab_values': [
                            {
                                'test': lab.test_name,
                                'value': lab.value,
                                'unit': lab.unit,
                                'is_abnormal': lab.is_abnormal,
                                'confidence': lab.extracted_confidence
                            }
                            for lab in lab_values
                        ]
                    },
                    'tags': [tag.tag_name for tag in tags]
                }
                
        except Exception as e:
            self.logger.error(f"Failed to get document details: {e}")
            return None
    
    def add_user_tag(self, document_id: int, user_id: int, tag_name: str) -> bool:
        """Add a user-defined tag to a document"""
        try:
            with self.db_service.get_session() as session:
                # Verify document belongs to user
                doc = session.query(DocumentAnalysis)\
                    .filter(DocumentAnalysis.id == document_id)\
                    .filter(DocumentAnalysis.user_id == user_id)\
                    .first()
                
                if not doc:
                    return False
                
                # Check if tag already exists
                existing_tag = session.query(DocumentTag)\
                    .filter(DocumentTag.document_id == document_id)\
                    .filter(DocumentTag.tag_name == tag_name.lower().strip())\
                    .first()
                
                if existing_tag:
                    return True  # Tag already exists
                
                # Add new tag
                new_tag = DocumentTag(
                    document_id=document_id,
                    tag_name=tag_name.lower().strip(),
                    tag_type='user'
                )
                session.add(new_tag)
                session.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to add user tag: {e}")
            return False
    
    def search_documents(self, user_id: int, query: str, document_type: str = None) -> List[Dict[str, Any]]:
        """Search user's documents by text content or metadata"""
        try:
            with self.db_service.get_session() as session:
                base_query = session.query(DocumentAnalysis)\
                    .filter(DocumentAnalysis.user_id == user_id)
                
                if document_type:
                    base_query = base_query.filter(DocumentAnalysis.document_type == document_type)
                
                # Search in file name, text content, and analysis
                search_terms = query.lower().split()
                for term in search_terms:
                    base_query = base_query.filter(
                        (DocumentAnalysis.file_name.ilike(f'%{term}%')) |
                        (DocumentAnalysis.text_content.ilike(f'%{term}%')) |
                        (DocumentAnalysis.llm_analysis.ilike(f'%{term}%'))
                    )
                
                documents = base_query.order_by(DocumentAnalysis.created_at.desc()).all()
                
                result = []
                for doc in documents:
                    summary = session.query(DocumentSummary)\
                        .filter(DocumentSummary.document_id == doc.id)\
                        .first()
                    
                    doc_data = {
                        'id': doc.id,
                        'file_name': doc.file_name,
                        'document_type': doc.document_type,
                        'confidence_score': doc.confidence_score,
                        'created_at': doc.created_at.isoformat(),
                        'short_summary': summary.short_summary if summary else '',
                        'relevance_score': self._calculate_relevance_score(doc, query)
                    }
                    result.append(doc_data)
                
                # Sort by relevance
                result.sort(key=lambda x: x['relevance_score'], reverse=True)
                return result
                
        except Exception as e:
            self.logger.error(f"Document search failed: {e}")
            return []
    
    def _calculate_relevance_score(self, document: DocumentAnalysis, query: str) -> float:
        """Calculate relevance score for search results"""
        score = 0.0
        query_lower = query.lower()
        
        # File name match (high weight)
        if query_lower in document.file_name.lower():
            score += 0.5
        
        # Document type match
        if query_lower in document.document_type.lower():
            score += 0.3
        
        # Text content matches (lower weight due to potentially large text)
        if document.text_content and query_lower in document.text_content.lower():
            score += 0.2
        
        return score
    
    def get_document_statistics(self, user_id: int) -> Dict[str, Any]:
        """Get statistics about user's documents"""
        try:
            with self.db_service.get_session() as session:
                documents = session.query(DocumentAnalysis)\
                    .filter(DocumentAnalysis.user_id == user_id)\
                    .all()
                
                if not documents:
                    return {'total_documents': 0}
                
                # Calculate statistics
                total_docs = len(documents)
                doc_types = {}
                total_size = 0
                confidence_scores = []
                
                for doc in documents:
                    # Count by type
                    doc_type = doc.document_type
                    doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
                    
                    # Total size
                    total_size += doc.file_size_bytes or 0
                    
                    # Confidence scores
                    if doc.confidence_score:
                        confidence_scores.append(doc.confidence_score)
                
                avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
                
                return {
                    'total_documents': total_docs,
                    'document_types': doc_types,
                    'total_size_mb': total_size / (1024 * 1024),
                    'average_confidence': avg_confidence,
                    'most_common_type': max(doc_types, key=doc_types.get) if doc_types else 'unknown'
                }
                
        except Exception as e:
            self.logger.error(f"Failed to get document statistics: {e}")
            return {'error': str(e)}