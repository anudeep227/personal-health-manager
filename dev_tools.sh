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
