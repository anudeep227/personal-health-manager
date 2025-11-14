#!/bin/bash

# Install Document Analysis Dependencies
echo "🔧 Installing Document Analysis Dependencies for Health App..."

# Activate virtual environment if it exists
if [ -d "health_env" ]; then
    echo "📦 Activating virtual environment..."
    source health_env/bin/activate
else
    echo "⚠️  Virtual environment not found. Please run setup_dev.sh first."
    exit 1
fi

# Install core document processing dependencies
echo "📄 Installing core document processing libraries..."
pip install PyPDF2>=3.0.0
pip install python-docx>=0.8.11
pip install pytesseract>=0.3.10
pip install opencv-python>=4.8.0

# Check if user wants to install AI/LLM dependencies
echo ""
read -p "🤖 Do you want to install AI/LLM dependencies for advanced analysis? (y/N): " install_ai
install_ai=${install_ai:-n}

if [[ $install_ai =~ ^[Yy]$ ]]; then
    echo "🧠 Installing AI/LLM dependencies..."
    pip install -r requirements-ai.txt
    
    echo ""
    echo "🔑 AI dependencies installed!"
    echo "📝 Don't forget to:"
    echo "   1. Copy .env.example to .env"
    echo "   2. Add your OpenAI API key to .env"
    echo "   3. Install Tesseract OCR on your system:"
    echo "      macOS: brew install tesseract"
    echo "      Ubuntu: sudo apt-get install tesseract-ocr"
    echo "      Windows: Download from GitHub releases"
else
    echo "⏭️  Skipping AI dependencies. You can install them later with:"
    echo "   pip install -r requirements-ai.txt"
fi

# System-specific instructions
echo ""
echo "🖥️  System Setup Instructions:"
echo ""

# Detect OS
case "$(uname -s)" in
    Darwin*)    
        echo "🍎 macOS detected"
        echo "Install Tesseract OCR:"
        echo "  brew install tesseract"
        echo "  brew install tesseract-lang  # for additional languages"
        ;;
    Linux*)     
        echo "🐧 Linux detected"
        echo "Install Tesseract OCR:"
        echo "  sudo apt-get update"
        echo "  sudo apt-get install tesseract-ocr"
        echo "  sudo apt-get install libtesseract-dev  # for development"
        ;;
    MINGW*|CYGWIN*|MSYS*)    
        echo "🪟 Windows detected"
        echo "Install Tesseract OCR:"
        echo "  1. Download from: https://github.com/UB-Mannheim/tesseract/wiki"
        echo "  2. Add to PATH or set TESSDATA_PREFIX environment variable"
        ;;
    *)          
        echo "❓ Unknown OS"
        echo "Please install Tesseract OCR manually for your system"
        ;;
esac

echo ""
echo "🧪 Testing installation..."

# Test core imports
python -c "
import sys
try:
    import PyPDF2
    print('✅ PyPDF2 installed successfully')
except ImportError as e:
    print(f'❌ PyPDF2 import failed: {e}')

try:
    from docx import Document
    print('✅ python-docx installed successfully')
except ImportError as e:
    print(f'❌ python-docx import failed: {e}')

try:
    import cv2
    print('✅ OpenCV installed successfully')
except ImportError as e:
    print(f'❌ OpenCV import failed: {e}')

try:
    import pytesseract
    print('✅ pytesseract installed successfully')
except ImportError as e:
    print(f'❌ pytesseract import failed: {e}')
"

# Test optional AI imports if requested
if [[ $install_ai =~ ^[Yy]$ ]]; then
    python -c "
try:
    import torch
    print('✅ PyTorch installed successfully')
except ImportError as e:
    print(f'❌ PyTorch import failed: {e}')

try:
    import transformers
    print('✅ Transformers installed successfully')
except ImportError as e:
    print(f'❌ Transformers import failed: {e}')

try:
    import openai
    print('✅ OpenAI installed successfully')
except ImportError as e:
    print(f'❌ OpenAI import failed: {e}')
"
fi

echo ""
echo "🧪 Running document analysis tests..."
python -m pytest tests/test_document_analysis.py -v

echo ""
echo "✅ Document Analysis Setup Complete!"
echo ""
echo "📚 Next Steps:"
echo "1. Ensure Tesseract OCR is installed on your system"
echo "2. Copy .env.example to .env and configure API keys"
echo "3. Test document analysis with sample files"
echo "4. Run the full app: python main.py"
echo ""
echo "🔗 Useful Links:"
echo "- Tesseract GitHub: https://github.com/tesseract-ocr/tesseract"
echo "- OpenAI API Keys: https://platform.openai.com/api-keys"
echo "- Documentation: See SETUP.md for detailed instructions"