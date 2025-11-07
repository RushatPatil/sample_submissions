# API Documentation - GenAI Evaluator

This document describes the three main endpoints of the GenAI Evaluator API.

## Base URL
```
http://localhost:5000
```

## Endpoints Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/generic_evaluation` | POST | Performs generic evaluation with language-based static validation |
| `/use_level_validation` | POST | Performs detailed user-level validation and evaluation |
| `/ranking` | POST | Ranks multiple teams based on their evaluation results |

---

## 1. Generic Evaluation Endpoint

**Endpoint:** `/generic_evaluation`
**Method:** `POST`
**Content-Type:** `multipart/form-data`

### Description
This endpoint performs a comprehensive generic evaluation with the following flow:
1. Extracts and saves the submitted project to a dedicated folder
2. Performs language-based static validation:
   - **Python**: Uses `py_compile` (syntax errors), `pylint` (coding style), and `bandit` (security issues)
   - **Java, JavaScript, C#**: Placeholder for future implementation
3. Uploads the project file to Azure OpenAI
4. Performs technical and prompt injection validation using GPT-4.1
5. **Uses o3-mini to verify evaluation completeness** (checks if assistant needs to continue evaluation)
6. Validates and rectifies results using GPT-5

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `team_name` | string | Yes | Name of the team submitting the project |
| `language` | string | Yes | Programming language (`python`, `java`, `javascript`, `csharp`) |
| `problem_statement` | string | Yes | The problem statement or project requirements |
| `submission_file` | file | Yes | ZIP file containing the project (max 100MB) |

### Example Request (cURL)
```bash
curl -X POST http://localhost:5000/generic_evaluation \
  -F "team_name=Team Alpha" \
  -F "language=python" \
  -F "problem_statement=Build a REST API for user management" \
  -F "submission_file=@/path/to/project.zip"
```

### Example Request (Python)
```python
import requests

url = "http://localhost:5000/generic_evaluation"

files = {
    'submission_file': open('project.zip', 'rb')
}

data = {
    'team_name': 'Team Alpha',
    'language': 'python',
    'problem_statement': 'Build a REST API for user management'
}

response = requests.post(url, files=files, data=data)
print(response.json())
```

### Response Format

#### Success Response (200 OK)
```json
{
  "status": "success",
  "message": "Generic evaluation completed",
  "result": {
    "team_name": "Team Alpha",
    "language": "python",
    "problem_statement": "Build a REST API for user management",
    "extraction": {
      "status": "success",
      "project_path": "extracted_projects/Team Alpha",
      "file_count": 25,
      "message": "Successfully extracted 25 files"
    },
    "static_validation": {
      "status": "completed",
      "total_files": 10,
      "files_validated": 10,
      "files_with_errors": 2,
      "summary": {
        "total_files": 10,
        "files_with_errors": 2,
        "py_compile": {
          "files_with_syntax_errors": 0,
          "files_clean": 10
        },
        "pylint": {
          "total_errors": 5,
          "total_warnings": 12,
          "total_conventions": 8,
          "total_refactors": 3
        },
        "bandit": {
          "total_issues": 2,
          "high_severity": 0,
          "medium_severity": 1,
          "low_severity": 1
        }
      },
      "validation_results": [
        {
          "file": "src/main.py",
          "has_errors": true,
          "py_compile": {
            "status": "success",
            "message": "No syntax errors found"
          },
          "pylint": {
            "status": "completed",
            "error_count": 2,
            "warning_count": 5,
            "convention_count": 3,
            "refactor_count": 1,
            "total_issues": 11
          },
          "bandit": {
            "status": "completed",
            "issue_count": 1,
            "high_severity": 0,
            "medium_severity": 1,
            "low_severity": 0
          }
        }
      ]
    },
    "criteria_evaluation": {
      "status": "completed",
      "criteria_count": 4,
      "results": {
        "technical": {
          "status": "completed",
          "response": "Detailed technical evaluation..."
        },
        "prompt_injection": {
          "status": "completed",
          "response": "Detailed prompt injection analysis..."
        }
      }
    },
    "status": "completed"
  }
}
```

#### Error Response (400 Bad Request)
```json
{
  "error": "Missing required fields: team_name, language, problem_statement"
}
```

#### Error Response (500 Internal Server Error)
```json
{
  "status": "error",
  "message": "Error message details"
}
```

---

## 2. Use Level Validation Endpoint

**Endpoint:** `/use_level_validation`
**Method:** `POST`
**Content-Type:** `multipart/form-data`

### Description
This endpoint performs detailed user-level validation and evaluation. It focuses on in-depth analysis using the evaluation orchestrator with multiple criteria checks.

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `team_name` | string | Yes | Name of the team submitting the project |
| `language` | string | Yes | Programming language (`python`, `java`, `javascript`, `csharp`) |
| `problem_statement` | string | Yes | The problem statement or project requirements |
| `submission_file` | file | Yes | ZIP file containing the project (max 100MB) |

### Example Request (cURL)
```bash
curl -X POST http://localhost:5000/use_level_validation \
  -F "team_name=Team Beta" \
  -F "language=python" \
  -F "problem_statement=Implement a machine learning model" \
  -F "submission_file=@/path/to/project.zip"
```

### Response Format

#### Success Response (200 OK)
```json
{
  "status": "success",
  "message": "Evaluation completed",
  "result": {
    "team_name": "Team Beta",
    "language": "python",
    "criteria_count": 4,
    "criteria_results": {
      "technical": {
        "status": "completed",
        "response": "Technical evaluation details..."
      },
      "prompt_engineering": {
        "status": "completed",
        "response": "Prompt engineering evaluation..."
      },
      "prompt_injection": {
        "status": "completed",
        "response": "Prompt injection analysis..."
      },
      "genai_boilerplate": {
        "status": "completed",
        "response": "GenAI boilerplate evaluation..."
      }
    },
    "status": "completed"
  }
}
```

---

## 3. Ranking Endpoint

**Endpoint:** `/ranking`
**Method:** `POST`
**Content-Type:** `application/json`

### Description
This endpoint ranks multiple teams based on their evaluation results. It groups teams by problem statement and performs two levels of ranking:
1. **Primary Ranking**: Teams are ranked within each problem statement group
2. **Secondary Ranking**: Top submissions from different problem statements are ranked against each other

### Request Parameters

The request body should be a JSON object with the following structure:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `teams_data` | array | Yes | Array of team evaluation data objects |

#### Team Data Object Structure
```json
{
  "team_name": "string",
  "language": "string",
  "problem_statement": "string",
  "evaluation_results": {},
  "criteria_count": 0
}
```

### Example Request (cURL)
```bash
curl -X POST http://localhost:5000/ranking \
  -H "Content-Type: application/json" \
  -d '{
    "teams_data": [
      {
        "team_name": "Team A",
        "language": "python",
        "problem_statement": "Build a REST API",
        "evaluation_results": {
          "technical": {
            "status": "completed",
            "response": "Evaluation..."
          }
        },
        "criteria_count": 3
      },
      {
        "team_name": "Team B",
        "language": "python",
        "problem_statement": "Build a REST API",
        "evaluation_results": {
          "technical": {
            "status": "completed",
            "response": "Evaluation..."
          }
        },
        "criteria_count": 3
      }
    ]
  }'
```

### Example Request (Python)
```python
import requests
import json

url = "http://localhost:5000/ranking"

payload = {
    "teams_data": [
        {
            "team_name": "Team A",
            "language": "python",
            "problem_statement": "Build a REST API",
            "evaluation_results": {
                "technical": {
                    "status": "completed",
                    "response": "Evaluation details..."
                }
            },
            "criteria_count": 3
        },
        {
            "team_name": "Team B",
            "language": "python",
            "problem_statement": "Build a REST API",
            "evaluation_results": {
                "technical": {
                    "status": "completed",
                    "response": "Evaluation details..."
                }
            },
            "criteria_count": 3
        }
    ]
}

headers = {'Content-Type': 'application/json'}
response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

### Response Format

#### Success Response (200 OK)
```json
{
  "status": "success",
  "message": "Ranking completed successfully",
  "preparation": {
    "total_teams": 5,
    "team_json_files": {
      "Team A": "data/team_evaluations/Team A_evaluation.json",
      "Team B": "data/team_evaluations/Team B_evaluation.json"
    },
    "file_mappings": {
      "Team A": "file-abc123",
      "Team B": "file-def456"
    }
  },
  "primary_ranking": {
    "timestamp": 1234567890,
    "total_teams": 5,
    "total_problem_statements": 2,
    "rankings_by_problem_statement": {
      "Build a REST API": {
        "total_teams": 3,
        "teams": ["Team A", "Team B", "Team C"],
        "ranking_response": "Detailed ranking analysis...",
        "gpt5_status": "completed",
        "problem_statement": "Build a REST API",
        "first_position": "Team A",
        "first_position_eval_file": "file-abc123",
        "first_position_submission_file": "file-xyz789",
        "file_ids_used": ["file-abc123", "file-def456", "file-ghi789"]
      }
    },
    "status": "completed"
  },
  "secondary_ranking": {
    "timestamp": 1234567890,
    "total_top_submissions": 2,
    "top_submissions": [
      {
        "team_name": "Team A",
        "problem_statement": "Build a REST API",
        "eval_file_id": "file-abc123",
        "submission_file_id": "file-xyz789"
      }
    ],
    "ranking_response": "Final ranking across all problem statements...",
    "gpt5_status": "completed",
    "file_ids_used": ["file-abc123", "file-pqr456"],
    "status": "completed",
    "result_file": "results/rankings/secondary_ranking_1234567890.json"
  }
}
```

#### Error Response (400 Bad Request)
```json
{
  "error": "teams_data is required and must not be empty"
}
```

#### Error Response (500 Internal Server Error)
```json
{
  "status": "error",
  "message": "Error message details"
}
```

---

## Health Check Endpoint

**Endpoint:** `/health`
**Method:** `GET`

### Description
Check if the API service is running and healthy.

### Example Request
```bash
curl http://localhost:5000/health
```

### Response
```json
{
  "status": "healthy",
  "service": "GenAI Evaluator API"
}
```

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters or missing required fields |
| 413 | Payload Too Large - File exceeds 100MB limit |
| 500 | Internal Server Error |

---

## Static Validation Details

### Python Static Validation

For Python projects, the following tools are used:

1. **py_compile**: Checks for syntax errors and compilation issues
   - Validates Python syntax
   - Identifies import errors
   - Detects indentation problems

2. **pylint**: Analyzes code quality and style
   - Coding standards (PEP 8)
   - Code smells and anti-patterns
   - Potential bugs and errors
   - Refactoring suggestions

3. **bandit**: Security vulnerability scanning
   - Identifies common security issues
   - Checks for hardcoded passwords
   - Detects SQL injection vulnerabilities
   - Finds insecure function usage

### Excluded Files and Directories

The static validation automatically excludes:
- `__pycache__/` directories
- `venv/`, `env/`, `.venv/`, `virtualenv/` directories
- `site-packages/` directories
- `setup.py` files (by default)

---

## Notes

1. **File Size Limit**: Maximum upload size is 100MB
2. **Supported Languages**: python, java, javascript, csharp (only Python has full static validation implemented)
3. **Azure OpenAI**: Requires valid Azure OpenAI credentials in `.env` file
4. **Results Storage**: All evaluation results are saved in the `results/` directory
5. **Extracted Projects**: Submitted projects are extracted to `extracted_projects/{team_name}/`

---

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=your_endpoint
# ... other configuration
```

3. Run the server:
```bash
python src/main.py
```

4. The API will be available at `http://localhost:5000`

---

## Version Information

- API Version: 1.0.0
- Last Updated: 2025
- Python Version: 3.8+
