#!/bin/bash

# Health App Development Setup Script
# This script sets up the development environment for the Personal Health Management App

echo "🏥 Personal Health Management App - Development Setup"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "health_env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv health_env
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source health_env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Dependencies installed successfully"
else
    echo "❌ requirements.txt not found"
    exit 1
fi

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p data/reports
mkdir -p data/backups
mkdir -p assets/images
mkdir -p assets/icons

echo "✅ Directory structure created"

# Initialize database
echo "🗄️ Initializing database..."
python3 -c "
import sys
import os
sys.path.insert(0, 'src')
from services.database_service import DatabaseService
from utils.config import Config

try:
    config = Config()
    db_service = DatabaseService()
    db_service.initialize_database()
    print('✅ Database initialized successfully')
except Exception as e:
    print(f'❌ Database initialization failed: {e}')
"

# Create .env file template
if [ ! -f ".env" ]; then
    echo "📝 Creating .env template..."
    cat > .env << EOL
# OpenAI API Key for AI features (optional)
OPENAI_API_KEY=your_openai_api_key_here

# App configuration
DEBUG=true
LOG_LEVEL=INFO
EOL
    echo "✅ .env template created"
fi

# Create launch script
echo "🚀 Creating launch script..."
cat > run_app.sh << 'EOL'
#!/bin/bash
# Launch script for Health Management App

echo "🏥 Starting Personal Health Management App..."

# Activate virtual environment
source health_env/bin/activate

# Run the application
python main.py
EOL

chmod +x run_app.sh
echo "✅ Launch script created (run_app.sh)"

# Create development tools script
cat > dev_tools.sh << 'EOL'
#!/bin/bash
# Development tools for Health Management App

case "$1" in
    "test")
        echo "🧪 Running tests..."
        source health_env/bin/activate
        python -m pytest tests/ -v
        ;;
    "lint")
        echo "🔍 Running linter..."
        source health_env/bin/activate
        flake8 src/ --max-line-length=100
        ;;
    "format")
        echo "🎨 Formatting code..."
        source health_env/bin/activate
        black src/
        ;;
    "clean")
        echo "🧹 Cleaning cache files..."
        find . -type d -name "__pycache__" -exec rm -rf {} +
        find . -name "*.pyc" -delete
        ;;
    "backup")
        echo "💾 Creating backup..."
        timestamp=$(date +"%Y%m%d_%H%M%S")
        tar -czf "backups/health_app_backup_$timestamp.tar.gz" data/ --exclude="data/backups"
        echo "Backup created: backups/health_app_backup_$timestamp.tar.gz"
        ;;
    *)
        echo "Health App Development Tools"
        echo "Usage: $0 {test|lint|format|clean|backup}"
        echo ""
        echo "Commands:"
        echo "  test    - Run unit tests"
        echo "  lint    - Run code linter"
        echo "  format  - Format code with Black"
        echo "  clean   - Clean cache files"
        echo "  backup  - Create data backup"
        ;;
esac
EOL

chmod +x dev_tools.sh
echo "✅ Development tools script created (dev_tools.sh)"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Run the app: ./run_app.sh"
echo "2. Or manually: source health_env/bin/activate && python main.py"
echo "3. Use dev tools: ./dev_tools.sh [command]"
echo ""
echo "📖 See README.md for detailed usage instructions"
echo ""
echo "Note: For AI features, add your OpenAI API key to the .env file"