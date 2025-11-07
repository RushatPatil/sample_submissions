# Auto Executor Setup Guide

## Virtual Environment Setup

### 1. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory (already created) with your Azure OpenAI credentials.

### 4. Run the Application

```bash
python app.py
```

The application will start on `http://0.0.0.0:5000`

## Deactivate Virtual Environment

When you're done working:
```bash
deactivate
```

## Project Structure

```
auto_executor/
├── venv/                  # Virtual environment (excluded from git)
├── app.py                 # Main Flask application
├── utility/
│   ├── azure_api.py      # Azure OpenAI client
│   └── extraction.py     # Tag extraction utilities
├── prompts/
│   ├── instructions/
│   │   └── askbit.txt    # Analysis prompt
│   └── script_gen/
│       └── askbit.txt    # Script generation prompt
├── test_data/
│   └── askbit.txt        # Test data for multiple runs
├── uploads/              # Uploaded files (excluded from git)
├── extracted_projects/   # Extracted projects (excluded from git)
├── logs/                 # Application logs (excluded from git)
├── requirements.txt      # Python dependencies
└── .env                  # Environment variables (excluded from git)
```
