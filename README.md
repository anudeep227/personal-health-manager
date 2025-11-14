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
```bash
# Install buildozer for Android
pip install buildozer
buildozer android debug
```

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