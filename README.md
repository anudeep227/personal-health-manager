# Personal Health Management App

A comprehensive mobile application for managing personal health data, medical reports, and medication notifications, built with Python and Kivy.

## Features

### Core Functionality
- **Personal Profile Management**: Store and manage your personal health information
- **Medication Management**: Track medications with automated reminders
- **Medical Reports**: Store and organize medical documents and reports
- **Appointment Scheduling**: Manage medical appointments with reminders
- **Health Records**: Track vital signs and health measurements
- **Notification System**: Smart reminders for medications and appointments

### Advanced Features (Future)
- **AI-Powered Insights**: LLM integration for health recommendations
- **Document Analysis**: AI analysis of medical reports
- **Medication Interaction Checking**: AI-powered interaction analysis
- **Symptom Assessment**: Basic symptom guidance with medical disclaimers

## Technology Stack

- **Frontend**: Kivy + KivyMD (Material Design)
- **Backend**: Python with SQLAlchemy ORM
- **Database**: SQLite (local storage)
- **Notifications**: Plyer (cross-platform notifications)
- **AI/LLM**: OpenAI API, Transformers, PyTorch
- **Architecture**: MVC (Model-View-Controller) pattern

## Project Structure

```
health-app/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── src/                   # Source code
│   ├── controllers/       # Application controllers
│   │   └── app_controller.py
│   ├── models/           # Database models
│   │   └── database_models.py
│   ├── services/         # Business logic services
│   │   ├── database_service.py
│   │   └── notification_service.py
│   ├── utils/            # Utility modules
│   │   └── config.py
│   └── views/            # UI screens
│       ├── base_screen.py
│       ├── home_screen.py
│       ├── profile_screen.py
│       ├── medications_screen.py
│       ├── reports_screen.py
│       ├── appointments_screen.py
│       ├── health_records_screen.py
│       └── settings_screen.py
├── data/                 # Data storage
│   ├── health_data.db    # SQLite database
│   ├── reports/          # Medical reports
│   └── backups/          # Data backups
├── assets/               # App assets
│   ├── images/
│   └── icons/
└── llm/                  # AI/LLM integration
    └── health_llm_service.py
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd /Users/anudeep/python-project/health-app
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv health_env
   source health_env/bin/activate  # On macOS/Linux
   # or
   health_env\Scripts\activate     # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (optional)**
   ```bash
   # Create .env file for AI features
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

## iOS Deployment

### Prerequisites for iOS
- **macOS**: Required for iOS development and deployment
- **Xcode**: Install from Mac App Store (latest version recommended)
- **iOS Developer Account**: Required for device testing and App Store deployment
- **kivy-ios**: Python-for-iOS toolchain for building Kivy apps

### iOS Setup Instructions

#### 1. Quick iOS Setup for Xcode (Recommended)
```bash
# Run automated iOS setup script for Xcode development
./xcode_setup.sh

# Open the project in Xcode
./open_xcode.sh
```

#### 2. Manual iOS Development Tools Installation
```bash
# Install Xcode command line tools
xcode-select --install

# Install kivy-ios toolchain
pip install kivy-ios
```

#### 2. Install Required iOS Dependencies
```bash
# Navigate to your project directory
cd /Users/anudeep/python-project/health-app

# Install Python-for-iOS
toolchain build python3 kivy

# Install additional dependencies for our app
toolchain build sqlite3 openssl libffi
toolchain build pillow  # For image processing
toolchain build requests  # For API calls
```

#### 3. Create iOS Project
```bash
# Create iOS project structure
toolchain create health-app /path/to/your/health-app

# This creates:
# - health-app-ios/  (Xcode project)
# - YourApp.xcodeproj
# - main.m, bridge.py files
```

#### 4. Configure iOS Project Settings

**Update Info.plist** (in your Xcode project):
```xml
<key>NSCameraUsageDescription</key>
<string>This app needs camera access to scan medical documents and ECG reports</string>

<key>NSPhotoLibraryUsageDescription</key>
<string>This app needs photo library access to import medical images and documents</string>

<key>NSMicrophoneUsageDescription</key>
<string>This app may need microphone access for voice notes (optional feature)</string>

<key>NSHealthShareUsageDescription</key>
<string>This app can integrate with HealthKit to import health data (optional)</string>

<key>NSHealthUpdateUsageDescription</key>
<string>This app can export health data to HealthKit (optional)</string>
```

#### 5. iOS-Specific Code Modifications

**Create iOS-specific main file** (`main_ios.py`):
```python
import sys
import os

# Add the application directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import your main app
from main import HealthApp

if __name__ == '__main__':
    HealthApp().run()
```

**iOS-specific requirements** (`requirements-ios.txt`):
```
kivy>=2.1.0
kivymd>=1.1.1
sqlalchemy>=1.4.0
plyer>=2.1.0
python-dateutil>=2.8.0
pillow>=9.0.0
requests>=2.28.0
```

#### 6. Build for iOS Device/Simulator

**For iOS Simulator:**
```bash
# Build for simulator
toolchain build --arch=x86_64 health-app

# Open in Xcode
open health-app-ios/health-app.xcodeproj
```

**For iOS Device:**
```bash
# Build for device (arm64)
toolchain build --arch=arm64 health-app

# You'll need to:
# 1. Open Xcode project
# 2. Configure signing & capabilities
# 3. Select your development team
# 4. Build and run on device
```

#### 7. iOS Testing & Debugging

**Test on iOS Simulator:**
1. Open Xcode project
2. Select iPhone simulator
3. Click "Build and Run"
4. Test all features on simulated device

**Test on Physical Device:**
1. Connect iPhone/iPad via USB
2. Trust the computer on device
3. Select device in Xcode
4. Build and install app
5. Trust developer profile in Settings > General > Device Management

#### 8. App Store Deployment

**Prepare for App Store:**
```bash
# Create release build
toolchain build --release health-app

# Archive in Xcode:
# 1. Product > Archive
# 2. Distribute App
# 3. iOS App Store
# 4. Upload to App Store Connect
```

**App Store Requirements:**
- App Store Connect account
- App icons (multiple sizes: 20px, 29px, 40px, 58px, 60px, 76px, 80px, 87px, 120px, 152px, 167px, 180px, 1024px)
- Launch screens for different device sizes
- App Store screenshots
- Privacy policy (required for health apps)
- Medical disclaimer
- Age rating (17+ recommended for medical apps)

### iOS-Specific Features Integration

#### HealthKit Integration (Optional)
```python
# Add to requirements-ios.txt
# pyhealthkit>=1.0.0  # If available

# iOS HealthKit integration
from plyer import platform

if platform == 'ios':
    try:
        # Import iOS-specific health integrations
        from ios_health_integration import HealthKitManager
        health_manager = HealthKitManager()
    except ImportError:
        health_manager = None
```

#### iOS Notifications
```python
# iOS-specific notification settings
from plyer import notification

def send_ios_notification(title, message, badge_count=1):
    if platform == 'ios':
        notification.notify(
            title=title,
            message=message,
            app_name='Health Manager',
            app_icon='assets/icons/app_icon.png',
            timeout=10,
            toast=True
        )
```

### iOS Troubleshooting

**Common Issues:**
1. **Build Errors**: Ensure all dependencies are iOS-compatible
2. **Signing Issues**: Check Apple Developer account and certificates
3. **Permission Denied**: Update Info.plist with required permissions
4. **Performance**: Optimize for mobile - reduce memory usage
5. **UI Scaling**: Test on different iOS device sizes

### iOS-Specific Testing:**
```bash
# Test iOS build compatibility
./test_ios_build.sh

# Build for iOS
./build_ios.sh

# iOS device testing checklist (see ios_testing_checklist.md):
# ✓ App launches successfully
# ✓ All screens render correctly
# ✓ Database operations work
# ✓ Notifications appear
# ✓ Camera/photo access works
# ✓ File system access works
# ✓ App handles background/foreground
```

## Using Xcode to Run the App

Once you've completed the iOS setup above, here's how to use Xcode to build and run your health app:

### Step 1: Open Xcode Project
```bash
# After running the iOS toolchain setup, open the generated Xcode project
open health-app-ios/health-app.xcodeproj
```

### Step 2: Configure Xcode Project Settings

#### A. Set Development Team
1. Select your project in the navigator (top-level "health-app")
2. Go to **Signing & Capabilities** tab
3. Select your **Team** (Apple Developer Account)
4. Xcode will automatically generate provisioning profiles

#### B. Configure Bundle Identifier
1. Change **Bundle Identifier** to something unique like:
   ```
   com.yourname.health-app
   ```
2. This must match your Apple Developer account

#### C. Set Deployment Target
1. Set **iOS Deployment Target** to minimum iOS version (e.g., iOS 13.0)
2. This determines which iOS devices can run your app

### Step 3: Configure App Permissions (Info.plist)

Xcode will show you the Info.plist editor. Add these permissions for the health app:

1. **Camera Usage Description**:
   - Key: `NSCameraUsageDescription`
   - Value: `"This app needs camera access to scan medical documents and ECG reports"`

2. **Photo Library Usage Description**:
   - Key: `NSPhotoLibraryUsageDescription` 
   - Value: `"This app needs photo library access to import medical images and documents"`

3. **Health Records Access** (if using HealthKit):
   - Key: `NSHealthShareUsageDescription`
   - Value: `"This app can import health data to provide better health management"`

### Step 4: Select Build Target

#### For iOS Simulator:
1. Click the device selector next to the "Play" button
2. Choose **iPhone 15 Pro** (or your preferred simulator)
3. Select **iOS 17.x Simulator**

#### For Physical iPhone/iPad:
1. Connect your iOS device via USB
2. Unlock device and trust the computer when prompted
3. Device should appear in the target selector
4. Select your physical device

### Step 5: Build and Run

#### Method 1: Use Xcode Interface
1. Click the **Play button** (▶️) in the top-left corner
2. Or use keyboard shortcut: **Cmd + R**
3. Xcode will build and launch the app

#### Method 2: Use Build Menu
1. **Product → Build** (Cmd + B) to build only
2. **Product → Run** (Cmd + R) to build and run
3. **Product → Clean Build Folder** (Cmd + Shift + K) if you need to clean

### Step 6: Debug and Monitor

#### View Logs:
1. Open **Window → Devices and Simulators**
2. Select your device
3. Click **Open Console** to view app logs
4. Python print statements will appear here

#### Debugging Python Code:
```python
# Add debug prints in your Python code
print(f"DEBUG: User data loaded: {user_data}")
print(f"DEBUG: Screen transition to: {screen_name}")

# These will show up in Xcode console
```

#### Monitor Performance:
1. **Product → Profile** (Cmd + I) opens Instruments
2. Monitor memory usage, CPU, and battery impact
3. Essential for iOS App Store approval

### Step 7: Common Xcode Build Issues & Solutions

#### Issue: "No signing certificate found"
**Solution:**
1. Go to **Xcode → Preferences → Accounts**
2. Add your Apple ID
3. Download development certificates
4. Return to **Signing & Capabilities** and select team

#### Issue: "Module not found" errors
**Solution:**
```bash
# Rebuild Python modules for iOS
toolchain build python3 kivy kivymd pillow sqlalchemy

# Clean and rebuild Xcode project
# In Xcode: Product → Clean Build Folder
```

#### Issue: App crashes on launch
**Solution:**
1. Check **Console** in Xcode for Python errors
2. Verify all Python dependencies are iOS-compatible
3. Check file paths (iOS has different file system structure)

#### Issue: Simulator vs Device differences
**Solution:**
- Always test on both simulator AND real device
- Simulator has different performance characteristics
- Some features (camera, notifications) only work on device

### Step 8: Advanced Xcode Features

#### Breakpoints in Python Code:
While you can't set traditional breakpoints in Python code through Xcode, you can:
```python
# Use strategic print statements
print(f"CHECKPOINT: Function {function_name} called with {parameters}")

# Add pause points for debugging
import time
time.sleep(2)  # Gives time to observe state
```

#### Analyze Build Performance:
1. **Product → Perform Action → Build with Timing Summary**
2. Identifies slow build steps
3. Helps optimize build times

#### Archive for Distribution:
1. **Product → Archive** creates distribution builds
2. **Window → Organizer** manages archived builds
3. Distribute to App Store or TestFlight from here

### Step 9: Testing Workflow in Xcode

#### Quick Testing Loop:
1. Make changes to Python code
2. **Cmd + R** to build and run
3. Test feature in simulator/device
4. Check console for any errors
5. Repeat

#### Memory Testing:
1. **Debug Navigator** shows real-time memory usage
2. Look for memory leaks in long-running sessions
3. iOS will terminate apps that use too much memory

### Step 10: Preparing for App Store

#### Final Build Steps:
1. Set build configuration to **Release**
2. **Product → Archive** to create distribution build
3. Use **Organizer** to upload to App Store Connect
4. TestFlight for beta testing

This workflow gives you full control over building and testing your health app using Xcode's powerful development environment!

### 📖 Additional Xcode Resources

For more detailed Xcode instructions and troubleshooting, see:
- **[XCODE_GUIDE.md](XCODE_GUIDE.md)** - Complete Xcode reference with shortcuts, debugging tips, and deployment workflow
- **[ios_permissions.plist](ios_permissions.plist)** - Ready-to-copy permissions for your Info.plist
- **Quick Scripts**:
  - `./xcode_setup.sh` - Automated iOS project setup for Xcode
  - `./open_xcode.sh` - Quick command to open project in Xcode

### iOS Performance Optimization

**Memory Management:**
- Optimize image loading for iOS memory constraints
- Implement lazy loading for large data sets
- Use iOS-appropriate caching strategies

**Battery Optimization:**
- Minimize background processing
- Optimize notification scheduling
- Reduce network requests

**iOS Human Interface Guidelines:**
- Follow Apple's design principles
- Implement iOS-standard gestures
- Use iOS-appropriate navigation patterns

## Usage

### Getting Started
1. Launch the app using `python main.py`
2. Navigate through different screens using the menu button
3. Start by setting up your profile in the Profile screen
4. Add medications with reminders in the Medications screen
5. Upload medical reports in the Reports screen
6. Schedule appointments in the Appointments screen
7. Track health measurements in Health Records
8. Configure settings in the Settings screen

### Key Features

#### Medication Management
- Add medications with dosage and frequency
- Set up automatic reminders
- Track medication intake
- View medication history

#### Medical Reports
- Upload and organize medical documents
- Categorize reports (Lab Results, X-rays, Prescriptions, etc.)
- Add notes and tags for easy searching
- Secure storage of sensitive documents

#### Appointment Management
- Schedule medical appointments
- Set multiple reminders (30 min, 1 hour, 1 day before)
- Track appointment history
- Add notes and follow-up information

#### Health Records
- Track vital signs (blood pressure, weight, temperature)
- Monitor health trends over time
- Export data for sharing with healthcare providers
- Visual charts and graphs (coming soon)

### AI Features (Future)
- Document analysis for extracting key medical information
- Medication interaction checking
- Personalized health recommendations
- Basic symptom assessment with medical disclaimers

## Security & Privacy

- **Local Storage**: All data is stored locally on your device
- **Encryption**: Sensitive data can be encrypted (configurable)
- **No Cloud Sync**: Data never leaves your device unless you choose to export
- **Backup**: Local backup functionality for data protection

## Development

### Adding New Features
1. Create new models in `src/models/`
2. Add database operations in `src/services/database_service.py`
3. Create new screens in `src/views/`
4. Update the controller in `src/controllers/app_controller.py`

### Running Tests
```bash
pytest tests/  # When tests are added
```

### Building for Mobile

#### Android
```bash
# Install buildozer for Android
pip install buildozer
buildozer android debug
```

#### iOS
```bash
# Install kivy-ios for iOS
pip install kivy-ios

# Build iOS dependencies
toolchain build python3 kivy

# Create iOS project
toolchain create health-app /path/to/your/project

# Build for iOS device
toolchain build --arch=arm64 health-app
```

For detailed iOS setup instructions, see the [iOS Deployment](#ios-deployment) section above.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Disclaimer

This application is for personal health management and informational purposes only. It is not intended to provide medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical decisions.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or questions, please create an issue in the project repository.

## Future Roadmap

- [ ] Mobile app deployment (Android/iOS)
- [ ] Advanced AI health insights
- [ ] Integration with wearable devices
- [ ] Telemedicine features
- [ ] Multi-user support for families
- [ ] Cloud sync option (with end-to-end encryption)
- [ ] Integration with healthcare provider systems
- [ ] Advanced analytics and reporting