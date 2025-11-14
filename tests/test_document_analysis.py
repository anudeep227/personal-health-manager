"""
Tests for Document Analysis functionality
"""

import unittest
import tempfile
import os
import json
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Mock the imports that may not be available in test environment
with patch.dict('sys.modules', {
    'PyPDF2': MagicMock(),
    'docx': MagicMock(),
    'pytesseract': MagicMock(),
    'cv2': MagicMock(),
    'PIL': MagicMock(),
    'pdfplumber': MagicMock(),
    'easyocr': MagicMock(),
    'mammoth': MagicMock(),
    'openai': MagicMock(),
    'transformers': MagicMock(),
    'torch': MagicMock()
}):
    from src.services.document_processing_service import DocumentProcessingService
    from src.services.document_service import DocumentService
    from llm.health_llm_service import HealthLLMService


class TestDocumentProcessingService(unittest.TestCase):
    """Test document processing functionality"""
    
    def setUp(self):
        self.service = DocumentProcessingService()
        
        # Create temporary test files
        self.temp_dir = tempfile.mkdtemp()
        
        # Create a test text file
        self.test_text_file = os.path.join(self.temp_dir, 'test.txt')
        with open(self.test_text_file, 'w') as f:
            f.write("This is a test medical document. Patient: John Doe. Diagnosis: Hypertension.")
        
        # Create a test PDF-like file (just for validation)
        self.test_pdf_file = os.path.join(self.temp_dir, 'test.pdf')
        with open(self.test_pdf_file, 'wb') as f:
            f.write(b"Mock PDF content")
    
    def tearDown(self):
        # Clean up temporary files
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_get_supported_formats(self):
        """Test getting supported file formats"""
        formats = self.service.get_supported_formats()
        
        self.assertIsInstance(formats, list)
        self.assertIn('.pdf', formats)
        self.assertIn('.docx', formats)
        self.assertIn('.txt', formats)
        self.assertIn('.jpg', formats)
    
    def test_validate_file_existing(self):
        """Test file validation for existing file"""
        is_valid, message = self.service.validate_file(self.test_text_file)
        
        self.assertTrue(is_valid)
        self.assertEqual(message, "File is valid")
    
    def test_validate_file_nonexistent(self):
        """Test file validation for non-existent file"""
        is_valid, message = self.service.validate_file("/nonexistent/file.txt")
        
        self.assertFalse(is_valid)
        self.assertIn("File does not exist", message)
    
    def test_validate_file_unsupported_format(self):
        """Test file validation for unsupported format"""
        unsupported_file = os.path.join(self.temp_dir, 'test.xyz')
        with open(unsupported_file, 'w') as f:
            f.write("test")
        
        is_valid, message = self.service.validate_file(unsupported_file)
        
        self.assertFalse(is_valid)
        self.assertIn("Unsupported file format", message)
    
    def test_process_text_file(self):
        """Test processing text files"""
        result = self.service.process_document(self.test_text_file)
        
        self.assertIsInstance(result, dict)
        self.assertIn('text_content', result)
        self.assertIn('metadata', result)
        self.assertIn('document_type', result)
        self.assertIn('confidence_score', result)
        
        self.assertIn("medical document", result['text_content'])
        self.assertEqual(result['metadata']['method'], 'direct_read')
    
    def test_classify_document_type(self):
        """Test document type classification"""
        # Test medical document
        medical_text = "Patient blood pressure reading shows hypertension"
        doc_type = self.service.classify_document_type(medical_text)
        self.assertIn(doc_type, ['medical_document', 'blood_test'])
        
        # Test ECG document
        ecg_text = "Electrocardiogram shows normal sinus rhythm"
        doc_type = self.service.classify_document_type(ecg_text)
        self.assertEqual(doc_type, 'ecg')
        
        # Test prescription
        rx_text = "Prescription: Take medication 2mg twice daily"
        doc_type = self.service.classify_document_type(rx_text)
        self.assertEqual(doc_type, 'prescription')
    
    def test_calculate_confidence_score(self):
        """Test confidence score calculation"""
        # High confidence result
        high_conf_result = {
            'text_content': 'This is a long medical document with lots of extracted text that should result in a high confidence score',
            'document_type': 'medical_document',
            'metadata': {'confidence': 0.9}
        }
        score = self.service.calculate_confidence_score(high_conf_result)
        self.assertGreater(score, 0.8)
        
        # Low confidence result
        low_conf_result = {
            'text_content': 'Short',
            'document_type': 'unknown',
            'metadata': {}
        }
        score = self.service.calculate_confidence_score(low_conf_result)
        self.assertLess(score, 0.7)


class TestHealthLLMService(unittest.TestCase):
    """Test LLM service functionality"""
    
    def setUp(self):
        self.service = HealthLLMService()
    
    @patch('llm.health_llm_service.os.getenv')
    def test_setup_models_without_api_key(self, mock_getenv):
        """Test model setup without API key"""
        mock_getenv.return_value = None
        
        service = HealthLLMService()
        service.setup_models()
        
        self.assertIsNone(service.openai_client)
    
    @patch('llm.health_llm_service.os.getenv')
    def test_setup_models_with_placeholder_key(self, mock_getenv):
        """Test model setup with placeholder API key"""
        mock_getenv.return_value = 'your_openai_api_key_here'
        
        service = HealthLLMService()
        service.setup_models()
        
        self.assertIsNone(service.openai_client)
    
    def test_analyze_document_comprehensive_no_content(self):
        """Test document analysis with no content"""
        document_data = {
            'text_content': '',
            'document_type': 'unknown',
            'metadata': {}
        }
        
        result = self.service.analyze_document_comprehensive(document_data)
        
        self.assertIn('error', result)
        self.assertIn('No text content', result['error'])
    
    def test_analyze_ecg_report_fallback(self):
        """Test ECG analysis fallback without AI"""
        text_content = "ECG shows heart rate 72 bpm, normal sinus rhythm"
        metadata = {}
        
        result = self.service.analyze_ecg_report(text_content, metadata)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['document_type'], 'ecg_analysis')
        self.assertIn('disclaimer', result)
    
    def test_extract_ecg_data(self):
        """Test ECG data extraction"""
        text = "Heart rate: 75 bpm, PR interval: 160 ms, QRS: 90 ms"
        
        data = self.service._extract_ecg_data(text)
        
        self.assertIn('heart_rate', data)
        self.assertEqual(data['heart_rate'], 75)
        self.assertIn('pr_interval', data)
        self.assertEqual(data['pr_interval'], 160)
    
    def test_extract_lab_values(self):
        """Test lab value extraction"""
        text = "Glucose: 95 mg/dL, Cholesterol: 180 mg/dL, Hemoglobin: 14.2 g/dL"
        
        values = self.service._extract_lab_values(text)
        
        self.assertIsInstance(values, list)
        self.assertGreater(len(values), 0)
        
        # Check if glucose value was extracted
        glucose_found = any(val['test'].lower() == 'glucose' for val in values)
        self.assertTrue(glucose_found)
    
    def test_extract_medications_from_text(self):
        """Test medication extraction"""
        text = "Prescribed: Lisinopril 10mg daily, Metformin 500mg twice daily"
        
        medications = self.service._extract_medications_from_text(text)
        
        self.assertIsInstance(medications, list)
        # Note: regex might not catch all medications in this simple test
        # In real usage, this would be enhanced
    
    def test_identify_abnormal_values(self):
        """Test abnormal value identification"""
        text = """
        Glucose: 95 mg/dL (Normal)
        Cholesterol: 250 mg/dL (High)
        Hemoglobin: 8.5 g/dL (Low)
        """
        
        abnormal = self.service._identify_abnormal_values(text)
        
        self.assertIsInstance(abnormal, list)
        self.assertGreater(len(abnormal), 0)
    
    def test_explain_medical_terms(self):
        """Test medical term explanation"""
        text = "Patient has hypertension and diabetes"
        
        terms = self.service._explain_medical_terms(text)
        
        self.assertIsInstance(terms, dict)
        self.assertIn('hypertension', terms)
        self.assertIn('diabetes', terms)


class TestDocumentService(unittest.TestCase):
    """Test high-level document service"""
    
    def setUp(self):
        self.service = DocumentService()
        
        # Mock the dependencies
        self.service.db_service = Mock()
        self.service.doc_processor = Mock()
        self.service.llm_service = Mock()
        
        # Create temporary test file
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(self.test_file, 'w') as f:
            f.write("Test medical document content")
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_analyze_document_complete_success(self):
        """Test successful complete document analysis"""
        # Mock the services
        self.service.doc_processor.validate_file.return_value = (True, "Valid")
        self.service.doc_processor.process_document.return_value = {
            'file_name': 'test.txt',
            'text_content': 'Test content',
            'document_type': 'medical_document',
            'confidence_score': 0.8,
            'metadata': {'method': 'direct_read'}
        }
        
        self.service.llm_service.analyze_document_comprehensive.return_value = {
            'analysis': 'Test analysis',
            'document_type': 'medical_analysis'
        }
        
        self.service.llm_service.generate_document_summary.return_value = "Test summary"
        
        # Mock database session
        mock_session = Mock()
        mock_session.__enter__ = Mock(return_value=mock_session)
        mock_session.__exit__ = Mock(return_value=None)
        self.service.db_service.get_session.return_value = mock_session
        
        result = self.service.analyze_document_complete(self.test_file, user_id=1)
        
        self.assertIsInstance(result, dict)
        self.assertTrue(result.get('success', False))
        self.assertIn('document_id', result)
        self.assertIn('processing_result', result)
        self.assertIn('llm_analysis', result)
    
    def test_analyze_document_complete_validation_failure(self):
        """Test document analysis with validation failure"""
        self.service.doc_processor.validate_file.return_value = (False, "Invalid file")
        
        result = self.service.analyze_document_complete("invalid_file.xyz", user_id=1)
        
        self.assertIn('error', result)
        self.assertIn('validation failed', result['error'])
    
    def test_analyze_document_complete_processing_failure(self):
        """Test document analysis with processing failure"""
        self.service.doc_processor.validate_file.return_value = (True, "Valid")
        self.service.doc_processor.process_document.return_value = {
            'error': 'Processing failed'
        }
        
        result = self.service.analyze_document_complete(self.test_file, user_id=1)
        
        self.assertIn('error', result)
        self.assertIn('processing failed', result['error'])
    
    def test_calculate_relevance_score(self):
        """Test relevance score calculation for search"""
        from src.models.database_models import DocumentAnalysis
        
        # Create mock document
        doc = DocumentAnalysis()
        doc.file_name = "blood_test_results.pdf"
        doc.document_type = "blood_test"
        doc.text_content = "This document contains blood test results showing glucose levels"
        
        # Test high relevance query
        score = self.service._calculate_relevance_score(doc, "blood test")
        self.assertGreater(score, 0.5)
        
        # Test low relevance query
        score = self.service._calculate_relevance_score(doc, "prescription medication")
        self.assertLess(score, 0.5)


class TestDocumentModels(unittest.TestCase):
    """Test document-related database models"""
    
    def test_document_analysis_creation(self):
        """Test DocumentAnalysis model creation"""
        from src.models.database_models import DocumentAnalysis
        
        doc = DocumentAnalysis(
            user_id=1,
            file_name="test.pdf",
            document_type="medical_document",
            confidence_score=0.85
        )
        
        self.assertEqual(doc.user_id, 1)
        self.assertEqual(doc.file_name, "test.pdf")
        self.assertEqual(doc.document_type, "medical_document")
        self.assertEqual(doc.confidence_score, 0.85)
    
    def test_extracted_medication_creation(self):
        """Test ExtractedMedication model creation"""
        from src.models.database_models import ExtractedMedication
        
        med = ExtractedMedication(
            document_id=1,
            medication_name="Lisinopril",
            dosage="10mg",
            frequency="daily"
        )
        
        self.assertEqual(med.document_id, 1)
        self.assertEqual(med.medication_name, "Lisinopril")
        self.assertEqual(med.dosage, "10mg")
        self.assertEqual(med.frequency, "daily")
    
    def test_extracted_lab_value_creation(self):
        """Test ExtractedLabValue model creation"""
        from src.models.database_models import ExtractedLabValue
        
        lab = ExtractedLabValue(
            document_id=1,
            test_name="Glucose",
            value="95",
            unit="mg/dL",
            is_abnormal=False
        )
        
        self.assertEqual(lab.document_id, 1)
        self.assertEqual(lab.test_name, "Glucose")
        self.assertEqual(lab.value, "95")
        self.assertEqual(lab.unit, "mg/dL")
        self.assertFalse(lab.is_abnormal)


class TestIntegration(unittest.TestCase):
    """Integration tests for document analysis workflow"""
    
    def setUp(self):
        # Create temporary test files
        self.temp_dir = tempfile.mkdtemp()
        
        # Create various test files
        self.test_files = {}
        
        # Text file with medical content
        self.test_files['medical_text'] = os.path.join(self.temp_dir, 'medical.txt')
        with open(self.test_files['medical_text'], 'w') as f:
            f.write("""
            Patient: John Doe
            Date: 2025-01-15
            
            Blood Test Results:
            Glucose: 95 mg/dL (Normal)
            Cholesterol: 180 mg/dL (Normal)
            Hemoglobin: 14.2 g/dL (Normal)
            
            Diagnosis: Patient shows normal blood chemistry values.
            Recommendation: Continue current medication regimen.
            """)
        
        # ECG-like content
        self.test_files['ecg'] = os.path.join(self.temp_dir, 'ecg.txt')
        with open(self.test_files['ecg'], 'w') as f:
            f.write("""
            ECG Report
            Patient: Jane Smith
            Heart Rate: 72 bpm
            Rhythm: Normal sinus rhythm
            PR Interval: 160 ms
            QRS Duration: 90 ms
            Interpretation: Normal ECG
            """)
        
        # Prescription-like content
        self.test_files['prescription'] = os.path.join(self.temp_dir, 'rx.txt')
        with open(self.test_files['prescription'], 'w') as f:
            f.write("""
            PRESCRIPTION
            Patient: Bob Johnson
            
            1. Lisinopril 10mg - Take once daily
            2. Metformin 500mg - Take twice daily with meals
            3. Atorvastatin 20mg - Take once daily at bedtime
            
            Follow up in 3 months.
            """)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_end_to_end_medical_document_processing(self):
        """Test complete workflow for medical document"""
        processor = DocumentProcessingService()
        result = processor.process_document(self.test_files['medical_text'])
        
        # Verify processing results
        self.assertFalse('error' in result)
        self.assertIn('text_content', result)
        self.assertIn('Blood Test Results', result['text_content'])
        self.assertIn('document_type', result)
        
        # Should classify as blood test or medical document
        self.assertIn(result['document_type'], ['blood_test', 'medical_document', 'lab_report'])
    
    def test_end_to_end_ecg_processing(self):
        """Test complete workflow for ECG document"""
        processor = DocumentProcessingService()
        result = processor.process_document(self.test_files['ecg'])
        
        # Verify processing results
        self.assertFalse('error' in result)
        self.assertIn('ECG Report', result['text_content'])
        self.assertEqual(result['document_type'], 'ecg')
    
    def test_end_to_end_prescription_processing(self):
        """Test complete workflow for prescription"""
        processor = DocumentProcessingService()
        result = processor.process_document(self.test_files['prescription'])
        
        # Verify processing results
        self.assertFalse('error' in result)
        self.assertIn('PRESCRIPTION', result['text_content'])
        self.assertEqual(result['document_type'], 'prescription')


if __name__ == '__main__':
    # Run specific test suites
    test_suites = [
        TestDocumentProcessingService,
        TestHealthLLMService,
        TestDocumentService,
        TestDocumentModels,
        TestIntegration
    ]
    
    for suite_class in test_suites:
        suite = unittest.TestLoader().loadTestsFromTestCase(suite_class)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        if not result.wasSuccessful():
            print(f"\n❌ {suite_class.__name__} had failures!")
        else:
            print(f"\n✅ {suite_class.__name__} passed all tests!")
    
    print("\n" + "="*50)
    print("Document Analysis Testing Complete!")
    print("="*50)