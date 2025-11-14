#!/bin/bash
# Quick test script for Health Management App

echo "🏥 Testing Personal Health Management App"
echo "========================================"

cd /Users/anudeep/python-project/health-app

echo "📍 Current directory: $(pwd)"
echo "🐍 Python version:"
./health_env/bin/python --version

echo ""
echo "🔍 Testing database services..."
./health_env/bin/python -c "
import sys
sys.path.insert(0, 'src')
from services.database_service import DatabaseService
from utils.config import Config

try:
    print('✅ Importing services: OK')
    config = Config()
    print('✅ Config service: OK')
    db_service = DatabaseService() 
    print('✅ Database service: OK')
    db_service.initialize_database()
    print('✅ Database initialization: OK')
    print('🗄️ Database location:', config.database_path)
except Exception as e:
    print('❌ Error:', e)
"

echo ""
echo "🖥️ Launching GUI App..."
echo "📝 Instructions:"
echo "   - A window should open with the Health Manager interface"
echo "   - Click 'Test Database' button to verify database functionality"
echo "   - Close the window or press Ctrl+C to exit"
echo ""
echo "🚀 Starting app in 3 seconds..."
sleep 3

./health_env/bin/python main_simple.py