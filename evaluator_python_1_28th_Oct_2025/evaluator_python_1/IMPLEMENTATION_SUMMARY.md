# GenAI Evaluator - Implementation Summary

## Overview

A complete Python-based evaluation system using Azure OpenAI Assistant API (GPT-4.1) to evaluate GenAI projects in multiple languages (Java, JavaScript, Python, C#).

## Complete Implementation Flow

### 1. Submission Received (Flask API)
- **Endpoint**: `POST /evaluate`
- **Input**: team_name, language, problem_statement, submission_file (zip)
- File saved temporarily in `uploads/` folder

### 2. File Upload to Azure OpenAI
- Zip file uploaded using `client.files.create()`
- Returns `file_id`
- Mapping stored: `team_name` → `file_id` in `data/file_mappings.json`

### 3. For Each Evaluation Criteria

The system evaluates using multiple criteria (currently: technical, prompt_engineering)

#### 3.1 Load Criteria Components
From `prompts/` folder structure:
- `instructions/{criteria}.txt` - Assistant's role and behavior
- `description/{criteria}.txt` - Brief description
- `user_prompt/{criteria}.txt` - Evaluation request with scoring rubric

#### 3.2 Create Assistant
- Assistant created with:
  - Name: "Evaluator - {criteria_name}"
  - Instructions from `instructions/{criteria}.txt`
  - Description from `description/{criteria}.txt`
  - Tool: code_interpreter
- Returns `assistant_id`

#### 3.3 Create Thread with File
- Thread created with code interpreter tool
- File attached via `tool_resources.code_interpreter.file_ids`
- Returns `thread_id`
- Mapping stored: `(team_name, criteria)` → `thread_id` in `data/thread_mappings.json`

#### 3.4 Add User Message
- User prompt from `user_prompt/{criteria}.txt` added to thread
- Problem statement placeholder replaced
- Message added using `client.beta.threads.messages.create()`

#### 3.5 Create and Poll Run
- Run created: `client.beta.threads.runs.create()`
- Polling every 60 seconds until completion
- Statuses tracked: queued → in_progress → completed/failed
- Run info updated in thread mappings

#### 3.6 Extract Results
- All thread messages retrieved
- Response parsed (expects JSON format)
- Results stored per criteria

### 4. Aggregate Results
- Calculate average score across all criteria
- Combine all criteria results
- Generate final evaluation report

### 5. Save Results
- Results saved to `results/{team_name}_evaluation.json`
- Temporary file deleted from `uploads/`

## File Structure

```
evaluator_python/
├── src/
│   ├── api/
│   │   ├── azure_client.py         # Azure OpenAI API interactions
│   │   └── __init__.py
│   ├── evaluators/
│   │   ├── evaluation_orchestrator.py  # Main evaluation flow
│   │   ├── base_evaluator.py
│   │   └── __init__.py
│   ├── utils/
│   │   ├── file_manager.py         # File ID mappings
│   │   ├── thread_manager.py       # Thread ID mappings
│   │   ├── logger.py               # Logging setup
│   │   └── __init__.py
│   └── main.py                     # Flask API endpoints
├── prompts/
│   ├── instructions/               # Assistant instructions per criteria
│   │   ├── technical.txt
│   │   └── prompt_engineering.txt
│   ├── description/                # Assistant descriptions
│   │   ├── technical.txt
│   │   └── prompt_engineering.txt
│   └── user_prompt/                # Evaluation prompts
│       ├── technical.txt
│       └── prompt_engineering.txt
├── data/
│   ├── file_mappings.json          # team → file_id
│   └── thread_mappings.json        # (team, criteria) → thread_id
├── results/                        # Evaluation results
├── logs/                           # Application logs
├── uploads/                        # Temporary file storage
├── config/
│   └── config.yaml                 # Configuration
├── .env                            # Azure credentials
├── requirements.txt
└── README.md

## Key Classes and Methods

### AzureAssistantClient (`src/api/azure_client.py`)

- `upload_file(file_path)` → file_id
- `create_thread_with_file(file_id)` → thread_id
- `add_message_to_thread(thread_id, content, role)` → message_id
- `create_assistant(name, instructions, description, tools)` → assistant_id
- `update_assistant(id_, name, instructions, description, tools)` → assistant_id
- `create_and_poll_run(thread_id, assistant_id, instructions)` → run_result

### EvaluationOrchestrator (`src/evaluators/evaluation_orchestrator.py`)

- `_load_criteria_prompts()` → Dict[criteria_name, {instructions, description, user_prompt}]
- `evaluate_submission(team_name, zip_file_path, language, problem_statement)` → results
- `get_team_status(team_name)` → status
- `get_team_results(team_name)` → results

### FileManager (`src/utils/file_manager.py`)

- `add_mapping(team_name, file_id, filename, language)`
- `get_file_id(team_name)` → file_id
- `get_mapping(team_name)` → mapping_dict

### ThreadManager (`src/utils/thread_manager.py`)

- `add_thread(team_name, criteria_name, thread_id, file_id)`
- `get_thread_id(team_name, criteria_name)` → thread_id
- `update_run_info(team_name, criteria_name, run_id, run_status)`
- `get_team_summary(team_name)` → summary

## API Endpoints

### POST /evaluate
Submit a new evaluation
- **Input**: multipart/form-data with team_name, language, problem_statement, submission_file
- **Output**: Complete evaluation results

### GET /status/<team_name>
Check evaluation status
- **Output**: Thread status for each criteria

### GET /results/<team_name>
Get evaluation results
- **Output**: Complete evaluation results from file

### GET /health
Health check
- **Output**: Service status

## Environment Variables (.env)

```
AZURE_OPENAI_ENDPOINT=<your_endpoint>
AZURE_OPENAI_KEY=<your_key>
AZURE_OPENAI_ASSISTANT_DEPLOYMENT=gpt-4.1
AZURE_OPENAI_RESPONSE_DEPLOYMENT=gpt-5
AZURE_OPENAI_ASSISTANT_API_VERSION=2024-02-15-preview
AZURE_OPENAI_RESPONSE_API_VERSION=2025-03-01-preview
```

## Data Persistence

### file_mappings.json
```json
{
  "TeamAlpha": {
    "file_id": "file-abc123",
    "filename": "TeamAlpha_submission.zip",
    "language": "python",
    "uploaded_at": "2024-01-15T10:30:00",
    "status": "uploaded"
  }
}
```

### thread_mappings.json
```json
{
  "TeamAlpha": {
    "threads": {
      "technical": {
        "thread_id": "thread_xyz789",
        "file_id": "file-abc123",
        "created_at": "2024-01-15T10:31:00",
        "status": "created",
        "run_id": "run_def456",
        "run_status": "completed"
      },
      "prompt_engineering": {
        "thread_id": "thread_uvw456",
        "file_id": "file-abc123",
        "created_at": "2024-01-15T10:35:00",
        "status": "created",
        "run_id": "run_ghi789",
        "run_status": "completed"
      }
    },
    "created_at": "2024-01-15T10:30:00"
  }
}
```

## Running the Application

```bash
# Start the Flask server
cd evaluator_python
python src/main.py

# Server runs on http://localhost:5000
```

## Adding New Evaluation Criteria

1. Create three files in `prompts/`:
   - `instructions/<criteria_name>.txt`
   - `description/<criteria_name>.txt`
   - `user_prompt/<criteria_name>.txt`

2. Restart the application

3. The new criteria will automatically be included in all evaluations

## Key Features

✅ Sequential evaluation of multiple criteria
✅ Persistent file and thread mappings
✅ Automatic prompt loading from file structure
✅ Problem statement placeholder replacement
✅ Comprehensive logging with rotation
✅ JSON-based evaluation results
✅ Support for multiple programming languages
✅ Code interpreter tool integration
✅ Polling mechanism for run completion
✅ Error handling and status tracking

## Improvements Made

1. **Simplified Structure**: Removed separate flask_app.py, consolidated into main.py
2. **Enhanced Prompt System**: Three-component prompt structure (instructions, description, user_prompt)
3. **Better Organization**: Clear separation of concerns across modules
4. **Flexible Criteria**: Easy to add new evaluation criteria
5. **Complete Tracking**: File and thread mappings persisted to disk
6. **Message Support**: Added method to add messages to threads

## Testing

Use the provided `test_api.py` script:

```python
python test_api.py
```

Or test with curl:

```bash
curl -X POST http://localhost:5000/evaluate \
  -F "team_name=TestTeam" \
  -F "language=python" \
  -F "problem_statement=Build a calculator" \
  -F "submission_file=@submission.zip"
```
