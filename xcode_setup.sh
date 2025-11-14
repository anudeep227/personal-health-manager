#!/bin/bash

# Xcode Setup Script for Health App
# This script prepares the iOS project for Xcode development

set -e

echo "🏗️  Setting up Kivy Health App for Xcode Development"
echo "=================================================="

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: iOS development requires macOS with Xcode"
    exit 1
fi

# Check if Xcode is installed
if ! command -v xcodebuild &> /dev/null; then
    echo "❌ Error: Xcode is not installed. Please install from Mac App Store"
    exit 1
fi

# Check if virtual environment is active
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "📦 Activating virtual environment..."
    source health_env/bin/activate
fi

echo "1️⃣ Installing iOS development tools..."

# Install kivy-ios if not already installed
if ! command -v toolchain &> /dev/null; then
    echo "   Installing kivy-ios toolchain..."
    pip install kivy-ios
else
    echo "   ✅ kivy-ios already installed"
fi

echo "2️⃣ Building iOS dependencies..."

# Build Python for iOS
echo "   Building Python3 for iOS..."
toolchain build python3

# Build Kivy
echo "   Building Kivy for iOS..."
toolchain build kivy

# Build KivyMD dependencies
echo "   Building PIL (Pillow) for iOS..."
toolchain build pillow

# Build SQLite
echo "   Building SQLite3 for iOS..."
toolchain build sqlite3

# Build SSL support
echo "   Building OpenSSL for iOS..."
toolchain build openssl

echo "3️⃣ Creating iOS project structure..."

# Create the iOS project
PROJECT_NAME="HealthApp"
if [ ! -d "${PROJECT_NAME}-ios" ]; then
    echo "   Creating iOS project: $PROJECT_NAME"
    toolchain create $PROJECT_NAME $(pwd)
else
    echo "   ✅ iOS project already exists"
fi

echo "4️⃣ Copying app resources..."

# Copy Python source files to iOS project
IOS_PROJECT_DIR="${PROJECT_NAME}-ios"
if [ -d "$IOS_PROJECT_DIR" ]; then
    echo "   Copying source files to iOS project..."
    
    # Copy main Python files
    cp main.py "$IOS_PROJECT_DIR/"
    cp -r src/ "$IOS_PROJECT_DIR/"
    cp -r assets/ "$IOS_PROJECT_DIR/" 2>/dev/null || echo "   Note: assets/ directory not found"
    
    # Create iOS-specific main file
    cat > "$IOS_PROJECT_DIR/main_ios.py" << 'EOF'
#!/usr/bin/env python3
"""
iOS-specific entry point for Health App
"""
import sys
import os

# Add the application directory to Python path
app_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_dir)
sys.path.insert(0, os.path.join(app_dir, 'src'))

try:
    # Import and run the main app
    from main import HealthApp
    
    if __name__ == '__main__':
        app = HealthApp()
        app.run()
        
except Exception as e:
    print(f"Error starting Health App: {e}")
    import traceback
    traceback.print_exc()
EOF

    echo "   ✅ Files copied to iOS project"
fi

echo "5️⃣ Creating iOS-specific configuration..."

# Create Info.plist template additions
cat > ios_permissions.plist << 'EOF'
<!-- Add these permissions to your Info.plist in Xcode -->
<key>NSCameraUsageDescription</key>
<string>This app needs camera access to scan medical documents and ECG reports</string>

<key>NSPhotoLibraryUsageDescription</key>
<string>This app needs photo library access to import medical images and documents</string>

<key>NSHealthShareUsageDescription</key>
<string>This app can import health data to provide better health management</string>

<key>NSHealthUpdateUsageDescription</key>
<string>This app can export health data to HealthKit for integrated health tracking</string>

<key>NSMicrophoneUsageDescription</key>
<string>This app may use microphone for voice notes (optional feature)</string>
EOF

echo "6️⃣ Creating Xcode launch script..."

# Create script to open Xcode project
cat > open_xcode.sh << EOF
#!/bin/bash
# Quick script to open the iOS project in Xcode

PROJECT_PATH="${PROJECT_NAME}-ios/${PROJECT_NAME}.xcodeproj"

if [ -f "\$PROJECT_PATH/project.pbxproj" ]; then
    echo "🚀 Opening Health App in Xcode..."
    open "\$PROJECT_PATH"
else
    echo "❌ Xcode project not found at: \$PROJECT_PATH"
    echo "Run ./xcode_setup.sh first to create the iOS project"
    exit 1
fi
EOF

chmod +x open_xcode.sh

echo "✅ Xcode setup complete!"
echo ""
echo "📱 Next Steps:"
echo "1. Run: ./open_xcode.sh to open the project in Xcode"
echo "2. In Xcode:"
echo "   - Select your development team in Signing & Capabilities"
echo "   - Add permissions from ios_permissions.plist to Info.plist"
echo "   - Choose iPhone Simulator or connect iOS device"
echo "   - Click the Play button (▶️) to build and run"
echo ""
echo "📖 For detailed Xcode instructions, see the README.md file"
echo ""
echo "🎉 Happy iOS development!"