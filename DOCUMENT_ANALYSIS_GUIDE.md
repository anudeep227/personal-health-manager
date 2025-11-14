# Document Analysis Feature Guide

## Overview

The Document Analysis feature uses AI and machine learning to automatically process, extract, and analyze medical documents including:

- **PDFs**: Medical reports, lab results, prescriptions
- **Images**: ECG printouts, X-rays, medical charts, handwritten notes
- **Word Documents**: Medical summaries, discharge notes
- **Text Files**: Any medical text documents

## Features

### 🔍 **Document Processing**
- **Multi-format Support**: PDF, DOCX, TXT, JPG, PNG, TIFF
- **OCR Technology**: Extract text from images and scanned documents
- **Intelligent Classification**: Automatically identify document types (ECG, blood test, prescription, etc.)
- **Confidence Scoring**: Quality assessment of text extraction

### 🤖 **AI-Powered Analysis**
- **Medical Document Understanding**: Specialized analysis for different medical document types
- **Key Information Extraction**: Medications, lab values, diagnoses, recommendations
- **Plain Language Summaries**: Convert medical jargon into understandable language
- **Action Item Identification**: Extract follow-up requirements and recommendations

### 📊 **Structured Data Extraction**
- **Medication Information**: Name, dosage, frequency, instructions
- **Lab Values**: Test results with normal/abnormal flags
- **Vital Signs**: Blood pressure, heart rate, temperature
- **Medical Terms**: Automatic explanation of complex terminology

### 🗄️ **Data Management**
- **Secure Storage**: All documents stored locally with encryption
- **Search & Filter**: Find documents by content, type, or date
- **Tagging System**: Organize documents with custom and auto-generated tags
- **History Tracking**: Complete audit trail of all analyses

## Document Types Supported

### 📋 **Lab Reports & Blood Tests**
- Complete blood count (CBC)
- Chemistry panels
- Lipid profiles
- Glucose tolerance tests
- Hormone levels
- **Analysis Includes**: Normal/abnormal flags, trend analysis, lifestyle recommendations

### ❤️ **Cardiovascular Documents**
- ECG/EKG reports
- Echocardiogram results
- Stress test results
- Holter monitor reports
- **Analysis Includes**: Heart rhythm interpretation, rate analysis, clinical significance

### 💊 **Prescriptions & Medications**
- Electronic prescriptions
- Medication lists
- Pharmacy receipts
- **Analysis Includes**: Drug interaction checking, dosage verification, adherence tips

### 🏥 **Radiology & Imaging**
- X-ray reports
- CT scan results
- MRI reports
- Ultrasound findings
- **Analysis Includes**: Finding explanations, follow-up recommendations

### 📄 **General Medical Documents**
- Discharge summaries
- Doctor's notes
- Referral letters
- Medical histories

## Getting Started

### Prerequisites

1. **Install Dependencies**:
   ```bash
   ./install_document_analysis.sh
   ```

2. **Install Tesseract OCR**:
   - **macOS**: `brew install tesseract`
   - **Ubuntu**: `sudo apt-get install tesseract-ocr`
   - **Windows**: Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)

3. **Configure AI Features** (Optional):
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

### Basic Usage

1. **Open Document Analysis Screen**
   - From home screen, click "Analyze Document"
   - Or navigate: Menu → Document Analysis

2. **Upload Document**
   - Click "Select Document"
   - Choose your medical document
   - Supported formats: PDF, DOCX, TXT, JPG, PNG

3. **Start Analysis**
   - Click "Analyze Document"
   - Wait for processing (usually 10-30 seconds)
   - Review results

4. **Review Results**
   - Document information and classification
   - AI-generated analysis and summary
   - Extracted structured data
   - Actionable recommendations

## AI Analysis Types

### 🩺 **ECG Analysis**
```
Input: ECG report or image
Output:
- Heart rate and rhythm interpretation
- Interval measurements (PR, QRS, QT)
- Clinical significance of findings
- Recommendations for follow-up
- Patient-friendly explanations
```

### 🧪 **Lab Results Analysis**
```
Input: Blood test results
Output:
- All test values with reference ranges
- Normal/abnormal value identification
- Clinical significance explanations
- Lifestyle recommendations
- Trending suggestions
```

### 💊 **Prescription Analysis**
```
Input: Prescription document
Output:
- Complete medication list with dosages
- Drug interaction warnings
- Side effects to monitor
- Adherence tips and schedules
- Cost-saving suggestions
```

### 📷 **Radiology Report Analysis**
```
Input: Imaging study report
Output:
- Finding explanations in plain language
- Clinical significance assessment
- Follow-up recommendations
- Questions to ask your doctor
```

## API Integration

### OpenAI Configuration
```bash
# .env file
OPENAI_API_KEY=your_actual_api_key_here
DEBUG=false
LOG_LEVEL=INFO
```

### Local Processing Fallback
The system works without AI API keys using:
- **Rule-based text extraction**
- **Pattern matching for structured data**
- **Basic medical term recognition**
- **Simple document classification**

## Security & Privacy

### 🔒 **Data Protection**
- **Local Storage**: All documents stored on your device
- **Encryption**: Sensitive data encrypted at rest
- **No Cloud Upload**: Documents never leave your device (unless using AI APIs)
- **Secure Deletion**: Complete removal of sensitive files

### 🛡️ **API Security**
- **Encrypted Transmission**: All API calls use HTTPS
- **Data Minimization**: Only necessary text sent to AI services
- **No Persistent Storage**: AI providers don't store your data
- **Configurable**: Can disable AI features entirely

## Troubleshooting

### Common Issues

#### **"OCR not working"**
- Install Tesseract: `brew install tesseract` (macOS)
- Check PATH: Tesseract must be in system PATH
- Image quality: Use high-resolution, clear images

#### **"AI analysis failed"**
- Check API key in .env file
- Verify internet connection
- Review API usage limits
- Fallback: Works without AI (basic analysis)

#### **"Unsupported file format"**
- Supported: PDF, DOCX, TXT, JPG, PNG, TIFF
- Convert other formats before upload
- Check file size (max 50MB)

#### **"Low confidence score"**
- Poor image quality or resolution
- Handwritten text (harder to read)
- Rotated or skewed documents
- Try different file format

### Performance Tips

1. **Optimize Images**:
   - Use 300+ DPI resolution
   - Ensure good contrast
   - Crop to document area
   - Straighten rotated images

2. **File Preparation**:
   - Clear, readable text
   - Standard medical formats
   - Remove unnecessary pages
   - Combine related documents

3. **System Resources**:
   - Close other applications during processing
   - Ensure sufficient disk space
   - Use wired internet for AI features

## Advanced Features

### Custom Tags
```python
# Add custom tags to documents
document_service.add_user_tag(document_id, user_id, "cardiology")
```

### Search Documents
```python
# Search by content or metadata
results = document_service.search_documents(user_id, "blood pressure")
```

### Batch Processing
```python
# Process multiple documents
for file_path in document_files:
    result = document_service.analyze_document_complete(file_path, user_id)
```

## Development

### Testing
```bash
# Run document analysis tests
python -m pytest tests/test_document_analysis.py -v

# Test specific functionality
python -m pytest tests/test_document_analysis.py::TestDocumentProcessingService -v
```

### Custom Document Types
Extend the system by adding new document patterns:

```python
# In DocumentProcessingService
self.medical_patterns['new_type'] = ['keyword1', 'keyword2', 'keyword3']
```

### Custom AI Prompts
Modify LLM prompts for specific use cases:

```python
# In HealthLLMService
def analyze_custom_document(self, text_content: str):
    prompt = f"""
    Custom analysis prompt for: {text_content}
    """
    return self._query_openai(prompt)
```

## Support

### Documentation
- **Setup Guide**: `SETUP.md`
- **API Reference**: Code documentation in source files
- **Testing Guide**: `TESTING_GUIDE.md`

### Community
- **Issues**: Report bugs via GitHub issues
- **Features**: Request features via GitHub discussion
- **Contributions**: Submit PRs for improvements

### Medical Disclaimer
⚠️ **Important**: This tool is for informational purposes only and should not replace professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical decisions.

---

*Document Analysis Feature - Version 1.0*
*Part of the Personal Health Management App*