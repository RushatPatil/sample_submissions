# GenAI Evaluator - Usage Guide

## Complete Evaluation Flow

This system implements a complete evaluation pipeline using Azure OpenAI Assistant API with the following flow:

### Flow Overview

1. **Receive Submission** → Flask API receives team submission (zip file)
2. **Upload to Azure** → File uploaded using Azure OpenAI File API
3. **Track File** → file_id mapped to team name (stored in `data/file_mappings.json`)
4. **Create Assistant** → Assistant created with code interpreter tool
5. **For Each Criteria**:
   - Create thread with code interpreter + attached file
   - Track thread_id for team-criteria pair (stored in `data/thread_mappings.json`)
   - Create and poll run sequentially
   - Collect evaluation results
6. **Aggregate Results** → Combine all criteria results
7. **Save Results** → Store in `results/` directory

## Setup

### 1. Install Dependencies

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows

# Install packages
pip install -r requirements.txt
```

### 2. Configure Environment

Your `.env` file is already configured. Ensure your Azure OpenAI credentials are correct.

### 3. Verify Prompt Files

The system uses prompt files in the `prompts/` directory:
- `criteria_1_code_quality.txt` - Evaluates code quality
- `criteria_2_functionality.txt` - Evaluates functionality & implementation

You can add more criteria by creating additional `criteria_*.txt` files.

## Running the Application

### Start the Flask API

```bash
cd evaluator_python
python src/api/flask_app.py
```

The API will start on `http://localhost:5000`

## API Endpoints

### 1. Health Check

```bash
GET http://localhost:5000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "GenAI Evaluator API"
}
```

### 2. Submit Evaluation

```bash
POST http://localhost:5000/evaluate
Content-Type: multipart/form-data

Fields:
- team_name: string (required)
- language: string (required) - one of: java, javascript, python, csharp
- problem_statement: string (required)
- submission_file: file (required) - must be a .zip file
```

Example using curl:
```bash
curl -X POST http://localhost:5000/evaluate \
  -F "team_name=TeamAlpha" \
  -F "language=python" \
  -F "problem_statement=Build a web scraper that extracts product information" \
  -F "submission_file=@/path/to/submission.zip"
```

Example using Python:
```python
import requests

url = "http://localhost:5000/evaluate"

files = {
    'submission_file': ('submission.zip', open('submission.zip', 'rb'), 'application/zip')
}

data = {
    'team_name': 'TeamAlpha',
    'language': 'python',
    'problem_statement': 'Build a web scraper that extracts product information'
}

response = requests.post(url, files=files, data=data)
print(response.json())
```

Response:
```json
{
  "status": "success",
  "message": "Evaluation completed",
  "result": {
    "team_name": "TeamAlpha",
    "language": "python",
    "average_score": 85.5,
    "criteria_count": 2,
    "criteria_results": {
      "1 Code Quality": {
        "criteria": "Code Quality",
        "score": 88,
        "strengths": [...],
        "weaknesses": [...],
        "recommendations": [...]
      },
      "2 Functionality": {
        "criteria": "Functionality & Implementation",
        "score": 83,
        ...
      }
    },
    "status": "completed"
  }
}
```

### 3. Get Evaluation Status

```bash
GET http://localhost:5000/status/<team_name>
```

Example:
```bash
curl http://localhost:5000/status/TeamAlpha
```

Response:
```json
{
  "status": "success",
  "team_name": "TeamAlpha",
  "evaluation_status": {
    "team_name": "TeamAlpha",
    "total_criteria": 2,
    "criteria_status": {
      "1 Code Quality": {
        "status": "created",
        "run_status": "completed"
      },
      "2 Functionality": {
        "status": "created",
        "run_status": "completed"
      }
    }
  }
}
```

### 4. Get Evaluation Results

```bash
GET http://localhost:5000/results/<team_name>
```

Example:
```bash
curl http://localhost:5000/results/TeamAlpha
```

Returns the complete evaluation results stored in `results/` directory.

## Data Storage

### File Mappings (`data/file_mappings.json`)

Tracks which Azure OpenAI file_id belongs to which team:

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

### Thread Mappings (`data/thread_mappings.json`)

Tracks which thread_id is associated with which team-criteria combination:

```json
{
  "TeamAlpha": {
    "threads": {
      "1 Code Quality": {
        "thread_id": "thread_xyz789",
        "file_id": "file-abc123",
        "created_at": "2024-01-15T10:31:00",
        "status": "created",
        "run_id": "run_def456",
        "run_status": "completed"
      },
      "2 Functionality": {
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

### Evaluation Results (`results/<team_name>_evaluation.json`)

Complete evaluation results for each team.

## Adding More Evaluation Criteria

1. Create a new prompt file in `prompts/` directory:
   ```
   prompts/criteria_3_security.txt
   ```

2. Write the evaluation instructions in the file (see existing criteria files for format)

3. Restart the Flask application

4. The new criteria will automatically be included in evaluations

## Logs

Application logs are stored in the `logs/` directory with daily rotation:
- Format: `evaluator_YYYY-MM-DD.log`
- Retention: 30 days
- Compression: zip

## Error Handling

The system handles various error scenarios:

- **File upload fails**: Returns error with details
- **Run timeout**: Waits up to 300 seconds (configurable)
- **Run fails**: Captures error and continues with other criteria
- **JSON parsing fails**: Stores raw response for debugging

## Architecture Components

### 1. Flask API (`src/api/flask_app.py`)
- Handles HTTP requests
- Validates inputs
- Manages file uploads
- Calls orchestrator

### 2. Evaluation Orchestrator (`src/evaluators/evaluation_orchestrator.py`)
- Manages complete evaluation flow
- Coordinates Azure API calls
- Tracks progress
- Aggregates results

### 3. Azure Client (`src/api/azure_client.py`)
- Handles Azure OpenAI API interactions
- File upload
- Thread creation with code interpreter
- Run creation and polling

### 4. File Manager (`src/utils/file_manager.py`)
- Maps file_id to teams
- Persistent storage

### 5. Thread Manager (`src/utils/thread_manager.py`)
- Maps thread_id to team-criteria pairs
- Tracks run status
- Persistent storage

## Testing

To test the complete flow:

1. Create a sample zip file with code
2. Submit via API:
```bash
curl -X POST http://localhost:5000/evaluate \
  -F "team_name=TestTeam" \
  -F "language=python" \
  -F "problem_statement=Create a simple calculator" \
  -F "submission_file=@test_submission.zip"
```

3. Check logs in `logs/` directory
4. Check results in `results/TestTeam_evaluation.json`
5. Check mappings in `data/` directory

## Troubleshooting

### Issue: File upload fails
- Check Azure OpenAI credentials in `.env`
- Verify file size is under 100MB
- Check network connectivity

### Issue: Run times out
- Increase `max_wait` parameter in `create_and_poll_run()`
- Check Azure OpenAI service status

### Issue: JSON parsing fails
- Check prompt formatting
- Review raw response in error message
- Update prompt to ensure JSON output

### Issue: Assistant not found
- Verify deployment names in `.env`
- Check Azure OpenAI resource access

## Performance Considerations

- **Sequential Evaluation**: Each criteria is evaluated sequentially to avoid API rate limits
- **Polling Interval**: Default 2 seconds (adjustable)
- **Max Wait Time**: Default 300 seconds (5 minutes) per criteria
- **File Size Limit**: 100MB max for uploads

## Security Notes

- `.env` file is gitignored (never commit credentials)
- Uploaded files are temporarily stored and deleted after processing
- API runs on localhost by default (configure for production deployment)
