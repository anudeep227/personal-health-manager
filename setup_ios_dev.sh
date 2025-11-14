#!/bin/bash

# iOS Setup Script for Health Management App
# This script helps set up the iOS development environment

echo "🍎 iOS Development Setup for Health Management App"
echo "=================================================="

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: iOS development requires macOS"
    exit 1
fi

echo "✅ Running on macOS - iOS development supported"

# Check for Xcode
echo ""
echo "1️⃣ Checking Xcode Installation..."
if ! command -v xcodebuild &> /dev/null; then
    echo "❌ Xcode not found!"
    echo "📱 Please install Xcode from the Mac App Store"
    echo "   https://apps.apple.com/app/xcode/id497799835"
    echo ""
    read -p "Press Enter after installing Xcode to continue..."
else
    echo "✅ Xcode found: $(xcodebuild -version | head -n1)"
fi

# Install Xcode command line tools
echo ""
echo "2️⃣ Installing Xcode Command Line Tools..."
if xcode-select -p &> /dev/null; then
    echo "✅ Xcode command line tools already installed"
else
    echo "📦 Installing Xcode command line tools..."
    xcode-select --install
    echo "⏳ Please complete the installation dialog and press Enter when done"
    read -p "Press Enter to continue..."
fi

# Activate virtual environment
echo ""
echo "3️⃣ Setting up Python Environment..."
if [ ! -d "health_env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv health_env
fi

source health_env/bin/activate
echo "✅ Virtual environment activated"

# Install kivy-ios
echo ""
echo "4️⃣ Installing kivy-ios toolchain..."
if command -v toolchain &> /dev/null; then
    echo "✅ kivy-ios already installed"
else
    echo "📦 Installing kivy-ios..."
    pip install kivy-ios
    echo "✅ kivy-ios installed"
fi

# Install iOS-compatible dependencies
echo ""
echo "5️⃣ Installing iOS-compatible dependencies..."

# Create iOS requirements if not exists
if [ ! -f "requirements-ios.txt" ]; then
    echo "📝 Creating iOS requirements file..."
    cat > requirements-ios.txt << 'EOF'
kivy>=2.1.0
kivymd>=1.1.1
sqlalchemy>=1.4.0
plyer>=2.1.0
python-dateutil>=2.8.0
pillow>=9.0.0
requests>=2.28.0
EOF
fi

pip install -r requirements-ios.txt
echo "✅ iOS dependencies installed"

# Build iOS toolchain dependencies
echo ""
echo "6️⃣ Building iOS toolchain dependencies..."
echo "⏳ This may take several minutes..."

# Build core dependencies
toolchain build python3
toolchain build kivy

# Build additional dependencies for our app
echo "📦 Building additional dependencies..."
toolchain build sqlite3
toolchain build openssl
toolchain build libffi
toolchain build pillow

echo "✅ iOS toolchain dependencies built"

# Create iOS main file
echo ""
echo "7️⃣ Creating iOS-specific files..."

if [ ! -f "main_ios.py" ]; then
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
else
    echo "✅ iOS main file already exists"
fi

# Create iOS project
echo ""
echo "8️⃣ Creating iOS Xcode project..."
project_name="HealthManager"

if [ ! -d "${project_name}-ios" ]; then
    echo "📱 Creating iOS project..."
    toolchain create "$project_name" .
    echo "✅ iOS Xcode project created: ${project_name}-ios/"
else
    echo "✅ iOS project already exists"
fi

# Create Info.plist template
echo ""
echo "9️⃣ Creating iOS configuration templates..."

mkdir -p ios_config

cat > ios_config/Info.plist.template << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- Camera access for document scanning -->
    <key>NSCameraUsageDescription</key>
    <string>This app needs camera access to scan medical documents and ECG reports</string>
    
    <!-- Photo library access for importing medical images -->
    <key>NSPhotoLibraryUsageDescription</key>
    <string>This app needs photo library access to import medical images and documents</string>
    
    <!-- Microphone access for voice notes (optional) -->
    <key>NSMicrophoneUsageDescription</key>
    <string>This app may need microphone access for voice notes (optional feature)</string>
    
    <!-- HealthKit integration (optional) -->
    <key>NSHealthShareUsageDescription</key>
    <string>This app can integrate with HealthKit to import health data (optional)</string>
    
    <key>NSHealthUpdateUsageDescription</key>
    <string>This app can export health data to HealthKit (optional)</string>
    
    <!-- File system access -->
    <key>NSDocumentsFolderUsageDescription</key>
    <string>This app needs access to documents folder to store health records</string>
    
    <!-- App Transport Security -->
    <key>NSAppTransportSecurity</key>
    <dict>
        <key>NSAllowsArbitraryLoads</key>
        <false/>
        <key>NSExceptionDomains</key>
        <dict>
            <!-- Add your API domains here -->
            <key>api.openai.com</key>
            <dict>
                <key>NSExceptionRequiresForwardSecrecy</key>
                <false/>
                <key>NSExceptionMinimumTLSVersion</key>
                <string>TLSv1.2</string>
                <key>NSThirdPartyExceptionRequiresForwardSecrecy</key>
                <false/>
            </dict>
        </dict>
    </dict>
    
    <!-- Background modes -->
    <key>UIBackgroundModes</key>
    <array>
        <string>background-processing</string>
        <string>background-fetch</string>
    </array>
    
    <!-- Supported interface orientations -->
    <key>UISupportedInterfaceOrientations</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
        <string>UIInterfaceOrientationLandscapeLeft</string>
        <string>UIInterfaceOrientationLandscapeRight</string>
    </array>
    
    <!-- iPad specific orientations -->
    <key>UISupportedInterfaceOrientations~ipad</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
        <string>UIInterfaceOrientationPortraitUpsideDown</string>
        <string>UIInterfaceOrientationLandscapeLeft</string>
        <string>UIInterfaceOrientationLandscapeRight</string>
    </array>
</dict>
</plist>
EOF

echo "✅ Info.plist template created"

# Create build script
cat > build_ios.sh << 'EOF'
#!/bin/bash

echo "🍎 Building Health Manager for iOS..."

# Activate environment
source health_env/bin/activate

# Build for iOS device (arm64)
echo "📱 Building for iOS device..."
toolchain build --arch=arm64 HealthManager

echo "✅ iOS build complete!"
echo ""
echo "📱 Next steps:"
echo "1. Open HealthManager-ios/HealthManager.xcodeproj in Xcode"
echo "2. Configure signing & capabilities"
echo "3. Update Info.plist with permissions"
echo "4. Build and test on device/simulator"
EOF

chmod +x build_ios.sh
echo "✅ iOS build script created"

# Create testing checklist
cat > ios_testing_checklist.md << 'EOF'
# iOS Testing Checklist for Health Manager

## Pre-Build Testing
- [ ] All Python dependencies iOS-compatible
- [ ] App launches without errors in development
- [ ] Database operations work correctly
- [ ] All screens render properly
- [ ] Navigation between screens works

## iOS Simulator Testing  
- [ ] App launches on simulator
- [ ] UI elements scale correctly
- [ ] Touch interactions work
- [ ] Orientation changes handled
- [ ] Memory usage acceptable

## iOS Device Testing
- [ ] App installs successfully
- [ ] Camera access works (document scanning)
- [ ] Photo library access works
- [ ] Notifications appear correctly
- [ ] File system access works
- [ ] App handles background/foreground
- [ ] Performance on target devices

## App Store Preparation
- [ ] All required icons created
- [ ] Launch screens for all device sizes
- [ ] App Store screenshots prepared
- [ ] Privacy policy created
- [ ] Medical disclaimer included
- [ ] Age rating set (17+ recommended)
- [ ] App Store Connect configured

## Compliance & Security
- [ ] HIPAA compliance reviewed (if applicable)
- [ ] Data encryption implemented
- [ ] User privacy protected
- [ ] Medical disclaimers prominent
- [ ] Terms of service created
EOF

echo "✅ iOS testing checklist created"

echo ""
echo "🎉 iOS Development Environment Setup Complete!"
echo "=============================================="
echo ""
echo "📱 What was created:"
echo "• iOS Xcode project: HealthManager-ios/"
echo "• iOS main file: main_ios.py"
echo "• iOS requirements: requirements-ios.txt"
echo "• iOS configuration templates: ios_config/"
echo "• Build script: build_ios.sh"
echo "• Testing checklist: ios_testing_checklist.md"
echo ""
echo "🔧 Next Steps:"
echo "1. Open Xcode project: open HealthManager-ios/HealthManager.xcodeproj"
echo "2. Configure Apple Developer account"
echo "3. Update Info.plist with permissions"
echo "4. Test on iOS Simulator"
echo "5. Test on physical iOS device"
echo "6. Prepare for App Store submission"
echo ""
echo "📝 Important Notes:"
echo "• iOS apps require Apple Developer account ($99/year)"
echo "• Medical apps need thorough testing and disclaimers"
echo "• Consider HIPAA compliance for sensitive health data"
echo "• Test on multiple iOS device sizes"
echo ""
echo "✅ Ready for iOS development! 🚀"