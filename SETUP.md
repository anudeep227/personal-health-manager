# Setup Guide for Development

## Prerequisites
- Python 3.8+ installed
- Git installed

## Initial Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd health-app
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv health_env
   source health_env/bin/activate  # On Windows: health_env\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env file with your actual values
   ```

5. **Make scripts executable (macOS/Linux):**
   ```bash
   chmod +x *.sh
   ```

## Environment Variables

Edit the `.env` file with your configuration:

- `OPENAI_API_KEY`: Your OpenAI API key (optional, for AI features)
- `DEBUG`: Set to `true` for development, `false` for production
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Running the Application

### Development Mode
```bash
./run_app.sh
```

Or manually:
```bash
python main.py
```

### Simple Mode (Basic UI)
```bash
python main_simple.py
```

## Development Tools

- **Format code:** `./dev_tools.sh format`
- **Lint code:** `./dev_tools.sh lint`  
- **Run tests:** `./test_app.sh`

## Optional AI Features

To enable AI features, install additional dependencies:

```bash
pip install transformers torch openai
```

Then set your OpenAI API key in the `.env` file.

## Project Structure

- `src/` - Main application source code
- `tests/` - Test files
- `assets/` - Static assets (icons, images)
- `config.json` - Application configuration
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (not tracked in git)

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests: `./test_app.sh`
4. Format code: `./dev_tools.sh format`
5. Submit a pull request