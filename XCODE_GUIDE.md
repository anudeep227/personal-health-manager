# Xcode Quick Reference for Health App Development

## 🚀 Quick Start Commands

```bash
# 1. Set up iOS project for Xcode
./xcode_setup.sh

# 2. Open project in Xcode
./open_xcode.sh

# 3. Build and run from command line (optional)
xcodebuild -project HealthApp-ios/HealthApp.xcodeproj -scheme HealthApp -destination 'platform=iOS Simulator,name=iPhone 15 Pro' build
```

## 📱 Xcode Essential Shortcuts

| Action | Shortcut | Description |
|--------|----------|-------------|
| Build & Run | `Cmd + R` | Builds and runs app on selected device/simulator |
| Build Only | `Cmd + B` | Builds the project without running |
| Clean Build | `Cmd + Shift + K` | Cleans build folder and intermediate files |
| Stop Running | `Cmd + .` | Stops the currently running app |
| Open Console | `Cmd + Shift + Y` | Shows debug console with Python print statements |
| Device Manager | `Cmd + Shift + 2` | Opens Devices and Simulators window |

## 🛠️ Project Configuration Checklist

### ✅ Before First Build
- [ ] Set **Bundle Identifier** (e.g., `com.yourname.health-app`)
- [ ] Select **Development Team** in Signing & Capabilities
- [ ] Set **iOS Deployment Target** (minimum iOS 13.0)
- [ ] Add required **permissions** to Info.plist

### ✅ Required Info.plist Permissions
```xml
<key>NSCameraUsageDescription</key>
<string>This app needs camera access to scan medical documents</string>

<key>NSPhotoLibraryUsageDescription</key>
<string>This app needs photo library access to import medical images</string>

<key>NSHealthShareUsageDescription</key>
<string>This app can import health data for better health management</string>
```

## 🎯 Build Targets Explained

### iPhone Simulator
- **Pros**: Fast testing, no device needed, debugging tools
- **Cons**: Different performance, some features unavailable (camera, notifications)
- **Use for**: UI testing, basic functionality verification

### Physical Device
- **Pros**: Real performance, all features work, true user experience
- **Cons**: Requires developer account, device setup
- **Use for**: Final testing, performance validation, App Store preparation

## 🐛 Common Issues & Solutions

### Issue: "Failed to prepare device for development"
**Solution:**
1. Open **Window → Devices and Simulators**
2. Select your device
3. Click **"Use for Development"**
4. Trust computer on iOS device

### Issue: "No signing certificate"
**Solution:**
1. **Xcode → Preferences → Accounts**
2. Add Apple ID
3. **Download Manual Profiles**
4. Return to project → **Signing & Capabilities** → Select Team

### Issue: "Module 'kivymd' not found"
**Solution:**
```bash
# Rebuild iOS dependencies
toolchain build python3 kivy kivymd

# Clean Xcode build
# In Xcode: Product → Clean Build Folder
```

### Issue: App crashes on launch
**Check Console Output:**
1. **Window → Devices and Simulators**
2. Select device → **Open Console**
3. Look for Python traceback errors
4. Common fixes:
   - Check file paths (iOS uses different filesystem)
   - Verify all imports are iOS-compatible
   - Ensure database file permissions

## 📊 Debugging Python Code in Xcode

### Console Logging
```python
# In your Python code, use print statements for debugging
print(f"DEBUG: Current screen: {self.current_screen}")
print(f"DEBUG: User data: {user_data}")
print(f"ERROR: Failed to load: {error}")

# These appear in Xcode console
```

### File System Debugging
```python
import os
print(f"Current working directory: {os.getcwd()}")
print(f"App bundle path: {os.path.dirname(__file__)}")
print(f"Documents directory: {os.path.expanduser('~/Documents')}")
```

### Memory Monitoring
- **Debug Navigator** in Xcode shows real-time memory usage
- Watch for memory leaks during extended app usage
- iOS will terminate apps using too much memory

## 🚢 Deployment Workflow

### 1. Development Testing
```bash
# Build for simulator
Cmd + R (in Xcode with simulator selected)

# Build for device
Cmd + R (in Xcode with device selected)
```

### 2. TestFlight Beta
```bash
# Archive build
Product → Archive (in Xcode)

# Upload to TestFlight
Window → Organizer → Distribute App → TestFlight
```

### 3. App Store Release
```bash
# Create release archive
Product → Archive (with Release configuration)

# Upload to App Store
Window → Organizer → Distribute App → App Store Connect
```

## 📋 Pre-Submission Checklist

### Code Quality
- [ ] All Python code tested on iOS device
- [ ] No hardcoded file paths
- [ ] Error handling for iOS-specific scenarios
- [ ] Memory usage optimized for mobile

### App Store Requirements
- [ ] App icons (all required sizes)
- [ ] Launch screen
- [ ] Privacy policy (required for health apps)
- [ ] Age rating set appropriately
- [ ] All permissions properly described
- [ ] No prohibited content or functionality

### Testing
- [ ] Tested on multiple iOS device sizes
- [ ] Tested on different iOS versions
- [ ] All features work without internet (if offline app)
- [ ] App handles background/foreground transitions
- [ ] Notifications work properly

## 📞 Getting Help

### Apple Developer Resources
- [iOS Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/ios/)
- [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [Xcode User Guide](https://developer.apple.com/documentation/xcode)

### Kivy iOS Resources
- [Kivy iOS Documentation](https://github.com/kivy/kivy-ios)
- [Python for iOS Guide](https://kivy.org/doc/stable/guide/packaging-ios.html)

### Health App Specific
- [HealthKit Framework](https://developer.apple.com/healthkit/) (if integrating)
- [Medical App Guidelines](https://developer.apple.com/app-store/review/guidelines/#health-and-health-research)

---

**Remember**: Always test thoroughly on real iOS devices before submitting to App Store!