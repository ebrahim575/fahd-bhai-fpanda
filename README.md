# FP&A AI Assistant Setup Guide

## Install Python
1. Download Python 3.11+ from [Python.org](https://www.python.org/downloads/)
2. Run installer
   - Windows: Check "Add Python to PATH"
3. Test installation in terminal:

```bash
python --version  # Should show 3.11 or higher
```

## Project Setup

### 1. Create `creds.py` File
This is a new file you need to create. Open any text editor (like Notepad), create a new file, and paste:

```python
open_api_key = "your-api-key-here"  # Replace with your key from platform.openai.com
```

Save this as `creds.py` in your project folder.

### 2. Install Requirements

**Windows:**
```bash
# Open Command Prompt in project folder
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Mac:**
```bash
# Open Terminal in project folder
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run Application

**Windows:**
```bash
python main.py
```

**Mac:**
```bash
python3 main.py
```

Open browser: `http://localhost:5000`

## Project Structure
```
your_folder/
│
├── main.py            # Main Flask application
├── creds.py           # Your API key file (you create this)
├── requirements.txt   # Dependencies
└── templates/
    └── index.html    # Web interface
```

## Getting OpenAI API Key
1. Visit [platform.openai.com](https://platform.openai.com)
2. Sign up/Login
3. Go to API section
4. Create new API key
5. Copy key to your `creds.py` file