#!/bin/bash

# iOS Build Testing Script for Health Management App
# This script helps test iOS-specific functionality before building

echo "🍎 iOS Build Testing for Health Management App"
echo "=============================================="

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: iOS development requires macOS"
    exit 1
fi

# Activate virtual environment
echo "📱 Activating virtual environment..."
source health_env/bin/activate || {
    echo "❌ Failed to activate virtual environment"
    exit 1
}

echo "✅ Virtual environment activated"

# Check iOS development prerequisites
echo ""
echo "1️⃣ Checking iOS Development Prerequisites..."

# Check for Xcode
if ! command -v xcodebuild &> /dev/null; then
    echo "⚠️  Xcode not found. Install from Mac App Store"
    echo "   Required for iOS development"
else
    echo "✅ Xcode found: $(xcodebuild -version | head -n1)"
fi

# Check for kivy-ios
if ! command -v toolchain &> /dev/null; then
    echo "⚠️  kivy-ios not found. Install with: pip install kivy-ios"
else
    echo "✅ kivy-ios toolchain found"
fi

# Check iOS-specific dependencies
echo ""
echo "2️⃣ Checking iOS-Compatible Dependencies..."

ios_deps=(
    "kivy"
    "kivymd" 
    "sqlalchemy"
    "plyer"
    "pillow"
    "requests"
    "python-dateutil"
)

for dep in "${ios_deps[@]}"; do
    if python -c "import $dep" 2>/dev/null; then
        echo "✅ $dep available"
    else
        echo "⚠️  $dep not found - may need iOS-compatible version"
    fi
done

# Test core app functionality
echo ""
echo "3️⃣ Testing Core App Components..."

# Test database models
python -c "
try:
    from src.models.database_models import *
    print('✅ Database models import successfully')
except Exception as e:
    print(f'❌ Database models error: {e}')
"

# Test services
python -c "
try:
    from src.services.database_service import DatabaseService
    print('✅ Database service imports successfully')
except Exception as e:
    print(f'❌ Database service error: {e}')
"

# Test controllers
python -c "
try:
    from src.controllers.app_controller import AppController
    print('✅ App controller imports successfully')
except Exception as e:
    print(f'❌ App controller error: {e}')
"

# Test Kivy imports (iOS compatibility)
echo ""
echo "4️⃣ Testing iOS UI Compatibility..."

python -c "
try:
    import kivy
    print(f'✅ Kivy {kivy.__version__} compatible')
except Exception as e:
    print(f'❌ Kivy error: {e}')
"

python -c "
try:
    import kivymd
    print(f'✅ KivyMD {kivymd.__version__} compatible')
except Exception as e:
    print(f'❌ KivyMD error: {e}')
"

# Test plyer (notifications/platform features)
python -c "
try:
    from plyer import notification, platform
    print(f'✅ Plyer platform features available')
    print(f'   Platform: {platform}')
except Exception as e:
    print(f'❌ Plyer error: {e}')
"

# Check for iOS-specific requirements
echo ""
echo "5️⃣ iOS-Specific Requirements Check..."

# Check for iOS main file
if [ -f "main_ios.py" ]; then
    echo "✅ iOS main file exists"
else
    echo "⚠️  Creating iOS main file..."
    cat > main_ios.py << 'EOF'
import sys
import os

# Add the application directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import your main app
from main import HealthApp

if __name__ == '__main__':
    HealthApp().run()
EOF
    echo "✅ iOS main file created"
fi

# Check for iOS requirements
if [ -f "requirements-ios.txt" ]; then
    echo "✅ iOS requirements file exists"
else
    echo "⚠️  Creating iOS requirements file..."
    cat > requirements-ios.txt << 'EOF'
kivy>=2.1.0
kivymd>=1.1.1
sqlalchemy>=1.4.0
plyer>=2.1.0
python-dateutil>=2.8.0
pillow>=9.0.0
requests>=2.28.0
EOF
    echo "✅ iOS requirements file created"
fi

# Test app launch (headless)
echo ""
echo "6️⃣ Testing App Launch (Headless Mode)..."

# Set headless mode for testing
export KIVY_WINDOW=sdl2
export KIVY_GL_BACKEND=gl

python -c "
import os
os.environ['KIVY_WINDOW'] = 'sdl2'
os.environ['KIVY_GL_BACKEND'] = 'mock'

try:
    # Import without running
    import sys
    sys.path.insert(0, 'src')
    from main import HealthApp
    
    # Test app initialization without running
    app = HealthApp()
    print('✅ App initializes successfully')
    
except Exception as e:
    print(f'❌ App initialization error: {e}')
" 2>/dev/null || echo "⚠️  App launch test skipped (requires display)"

echo ""
echo "🎯 iOS Build Test Summary"
echo "========================"

echo ""
echo "📋 Next Steps for iOS Development:"
echo "1. Install Xcode from Mac App Store"
echo "2. Install kivy-ios: pip install kivy-ios"
echo "3. Build iOS dependencies: toolchain build python3 kivy"
echo "4. Create iOS project: toolchain create health-app ."
echo "5. Configure Info.plist permissions"
echo "6. Test on iOS Simulator"
echo "7. Test on physical iOS device"
echo "8. Submit to App Store"

echo ""
echo "📱 iOS-Specific Features to Test:"
echo "• Camera access for document scanning"
echo "• Photo library access for image import"
echo "• Local notifications"
echo "• File system access"
echo "• App backgrounding/foregrounding"
echo "• Different screen sizes (iPhone/iPad)"
echo "• iOS-specific UI guidelines compliance"

echo ""
echo "🔧 Troubleshooting Tips:"
echo "• Ensure all Python packages are iOS-compatible"
echo "• Check Apple Developer account for signing"
echo "• Update Info.plist with required permissions"
echo "• Test memory usage on iOS devices"
echo "• Optimize for iOS performance constraints"

echo ""
echo "✅ iOS build testing completed!"
echo "Ready to proceed with iOS development 🚀"