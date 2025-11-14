#!/bin/bash
# Quick script to open the iOS project in Xcode

PROJECT_NAME="HealthApp"
PROJECT_PATH="${PROJECT_NAME}-ios/${PROJECT_NAME}.xcodeproj"

echo "🚀 Opening Health App in Xcode..."

if [ -f "$PROJECT_PATH/project.pbxproj" ]; then
    open "$PROJECT_PATH"
    echo "✅ Xcode project opened successfully!"
    echo ""
    echo "📱 Next steps in Xcode:"
    echo "1. Select your development team in 'Signing & Capabilities'"
    echo "2. Choose iPhone Simulator or connect iOS device"
    echo "3. Add permissions from ios_permissions.plist to Info.plist"
    echo "4. Click the Play button (▶️) to build and run"
    echo ""
    echo "📖 For detailed instructions, see README.md or XCODE_GUIDE.md"
else
    echo "❌ Xcode project not found at: $PROJECT_PATH"
    echo ""
    echo "🛠️  Run this command first to set up the iOS project:"
    echo "   ./xcode_setup.sh"
    echo ""
    echo "📖 Then try opening Xcode again with:"
    echo "   ./open_xcode.sh"
    exit 1
fi