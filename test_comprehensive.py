#!/usr/bin/env python3
"""
Comprehensive test suite for Health Management App
Tests all core components without launching GUI
"""

import sys
import os
from pathlib import Path

# Add src directory to path
current_dir = Path(__file__).parent
src_dir = current_dir / 'src'
sys.path.insert(0, str(src_dir))

def test_imports():
    """Test if all modules can be imported"""
    print("🔍 Testing module imports...")
    
    try:
        from utils.config import Config
        print("  ✅ Config module: OK")
    except Exception as e:
        print(f"  ❌ Config module: {e}")
        return False
    
    try:
        from services.database_service import DatabaseService
        print("  ✅ Database service: OK")
    except Exception as e:
        print(f"  ❌ Database service: {e}")
        return False
    
    try:
        from services.notification_service import NotificationService
        print("  ✅ Notification service: OK")
    except Exception as e:
        print(f"  ❌ Notification service: {e}")
        return False
    
    try:
        from models.database_models import User, Medication, MedicalReport
        print("  ✅ Database models: OK")
    except Exception as e:
        print(f"  ❌ Database models: {e}")
        return False
    
    return True

def test_config():
    """Test configuration system"""
    print("\n🔧 Testing configuration system...")
    
    try:
        from utils.config import Config
        config = Config()
        
        # Test paths
        assert config.database_path, "Database path not set"
        assert config.reports_dir, "Reports directory not set"
        
        # Test settings
        app_settings = config.get_app_settings()
        assert app_settings['app_name'] == 'Personal Health Manager'
        
        notification_settings = config.get_notification_settings()
        assert 'medication_reminders' in notification_settings
        
        print("  ✅ Configuration system: OK")
        return True
        
    except Exception as e:
        print(f"  ❌ Configuration system: {e}")
        return False

def test_database():
    """Test database functionality"""
    print("\n🗄️ Testing database system...")
    
    try:
        from services.database_service import DatabaseService
        from models.database_models import User
        from datetime import datetime
        
        # Initialize database
        db_service = DatabaseService()
        db_service.initialize_database()
        print("  ✅ Database initialization: OK")
        
        # Test user creation
        test_user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'created_at': datetime.utcnow()
        }
        
        user = db_service.create_user(test_user_data)
        assert user.id is not None
        print("  ✅ User creation: OK")
        
        # Test user retrieval
        retrieved_user = db_service.get_user(user.id)
        assert retrieved_user.first_name == 'Test'
        print("  ✅ User retrieval: OK")
        
        # Test user update
        update_data = {'last_name': 'UpdatedUser'}
        updated_user = db_service.update_user(user.id, update_data)
        assert updated_user.last_name == 'UpdatedUser'
        print("  ✅ User update: OK")
        
        # Test medication functionality
        med_data = {
            'user_id': user.id,
            'name': 'Test Medication',
            'dosage': '500mg',
            'frequency': '2 times daily',
            'start_date': datetime.utcnow(),
            'is_active': True
        }
        
        medication = db_service.add_medication(med_data)
        assert medication.id is not None
        print("  ✅ Medication creation: OK")
        
        # Test getting active medications
        active_meds = db_service.get_active_medications(user.id)
        assert len(active_meds) > 0
        print("  ✅ Medication retrieval: OK")
        
        print("  ✅ Database system: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"  ❌ Database system: {e}")
        return False

def test_notifications():
    """Test notification system"""
    print("\n🔔 Testing notification system...")
    
    try:
        from services.notification_service import NotificationService
        from services.database_service import DatabaseService
        
        # Initialize services
        db_service = DatabaseService()
        db_service.initialize_database()
        
        notification_service = NotificationService()
        notification_service.set_database_service(db_service)
        
        # Test custom notification
        notification_service.send_custom_notification(
            "Test Notification", 
            "This is a test notification from the Health Manager"
        )
        print("  ✅ Custom notification: OK")
        
        # Test scheduler setup
        notification_service.start_medication_scheduler()
        print("  ✅ Scheduler start: OK")
        
        notification_service.stop_scheduler()
        print("  ✅ Scheduler stop: OK")
        
        print("  ✅ Notification system: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"  ❌ Notification system: {e}")
        return False

def test_gui_components():
    """Test GUI component imports"""
    print("\n🖥️ Testing GUI components...")
    
    try:
        import kivy
        print(f"  ✅ Kivy: v{kivy.__version__}")
        
        import kivymd
        print(f"  ✅ KivyMD: Available")
        
        # Test key imports
        from kivymd.app import MDApp
        from kivymd.uix.screen import MDScreen
        from kivymd.uix.toolbar import MDTopAppBar
        from kivymd.uix.button import MDRaisedButton
        from kivymd.uix.label import MDLabel
        
        print("  ✅ GUI component imports: OK")
        return True
        
    except Exception as e:
        print(f"  ❌ GUI components: {e}")
        return False

def main():
    """Run all tests"""
    print("🏥 Personal Health Management App - Test Suite")
    print("=" * 55)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration System", test_config),
        ("Database System", test_database),
        ("Notification System", test_notifications),
        ("GUI Components", test_gui_components)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"  ❌ {test_name}: FAILED - {e}")
    
    print("\n" + "=" * 55)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Your Health Management App is working perfectly!")
        print("\n🚀 Ready to launch GUI with: ./test_app.sh")
    else:
        print(f"⚠️ {total - passed} tests failed - Please check the errors above")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)