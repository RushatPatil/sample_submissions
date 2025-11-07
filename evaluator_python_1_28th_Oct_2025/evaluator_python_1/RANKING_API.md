# Ranking API Documentation

## Overview
The `/rank` endpoint allows you to rank multiple teams based on their evaluation results using GPT-5.

## Endpoint
`POST /rank`

## Process Flow
1. **Step 1**: Create/Update JSON files for each team's evaluation data
2. **Step 2**: Upload new files if `submission_file_path` is provided
3. **Step 3**: Use GPT-5 to analyze and rank teams
4. **Step 4**: Return comprehensive ranking results

**Simple Approach**: JSON files are always created/updated. Files are uploaded only if you provide `submission_file_path`.

## Request Format

### Headers
```
Content-Type: application/json
```

### Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `teams_data` | Array | Yes | Array of team evaluation data objects |

### Team Data Object Structure

```json
{
    "team_name": "Team A",
    "language": "python",
    "problem_statement": "Solve the conversion use-case",
    "evaluation_results": {
        "technical": {
            "status": "completed",
            "human_approval": true,
            "response": "..."
        },
        "prompt_engineering": {
            "status": "completed",
            "human_approval": true,
            "response": "..."
        }
    },
    "pre_validation_results": {
        "prompt_injection": {
            "status": "pass",
            "check_passed": true
        },
        "genai_boilerplate": {
            "status": "pass",
            "check_passed": true
        }
    },
    "average_score": 85.5,
    "criteria_count": 2,
    "clubbed_response": "Complete evaluation report...",
    "submission_file_path": "/path/to/team_a.zip"
}
```

## Example Request

### Example 1: Ranking with Evaluation Data Only

```bash
curl -X POST http://localhost:5000/rank \
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
                    "response": "Excellent implementation"
                }
            },
            "pre_validation_results": {
                "prompt_injection": {"status": "pass", "check_passed": true},
                "genai_boilerplate": {"status": "pass", "check_passed": true}
            },
            "average_score": 90.0,
            "criteria_count": 2
        },
        {
            "team_name": "Team B",
            "language": "javascript",
            "problem_statement": "Build a REST API",
            "evaluation_results": {
                "technical": {
                    "status": "completed",
                    "response": "Good implementation"
                }
            },
            "pre_validation_results": {
                "prompt_injection": {"status": "pass", "check_passed": true},
                "genai_boilerplate": {"status": "pass", "check_passed": true}
            },
            "average_score": 75.0,
            "criteria_count": 2
        }
    ]
}'
```

### Example 2: Ranking with File Uploads

```bash
curl -X POST http://localhost:5000/rank \
  -H "Content-Type: application/json" \
  -d '{
    "teams_data": [
        {
            "team_name": "Team A",
            "language": "python",
            "submission_file_path": "C:\\Users\\user\\Downloads\\team_a.zip",
            "evaluation_results": {...},
            "average_score": 90.0
        },
        {
            "team_name": "Team B",
            "language": "java",
            "submission_file_path": "C:\\Users\\user\\Downloads\\team_b.zip",
            "evaluation_results": {...},
            "average_score": 85.0
        }
    ]
}'
```

**Note**: When `submission_file_path` is provided, new files will be uploaded to Azure OpenAI.

## Response Format

### Success Response (200)

```json
{
    "status": "success",
    "message": "Ranking completed successfully",
    "preparation": {
        "total_teams": 2,
        "team_json_files": {
            "Team A": "C:\\path\\to\\data\\team_evaluations\\Team A_evaluation.json",
            "Team B": "C:\\path\\to\\data\\team_evaluations\\Team B_evaluation.json"
        },
        "file_mappings": {
            "Team A": "file-abc123",
            "Team B": "file-xyz789"
        }
    },
    "ranking": {
        "timestamp": 1678901234,
        "total_teams": 2,
        "ranking_criteria": "Overall code quality and completeness",
        "teams_evaluated": ["Team A", "Team B"],
        "file_mappings": {
            "Team A": "file-abc123",
            "Team B": "file-xyz789"
        },
        "ranking_response": "## Overall Ranking\n\n1. Team A - 90.0/100\n2. Team B - 85.0/100\n\n## Detailed Analysis...",
        "gpt5_status": "completed",
        "status": "completed",
        "result_file": "C:\\path\\to\\results\\rankings\\ranking_1678901234.json"
    }
}
```

### Error Response (400/500)

```json
{
    "status": "error",
    "message": "Error description"
}
```

## File Structure Created

When you call `/rank`, the following files are created:

### 1. Team Evaluation JSON Files
Location: `data/team_evaluations/`

Example: `Team A_evaluation.json`
```json
{
    "team_name": "Team A",
    "language": "python",
    "problem_statement": "...",
    "file_id": "file-abc123",
    "evaluation_results": {...},
    "pre_validation_results": {...},
    "average_score": 90.0,
    "criteria_count": 2,
    "clubbed_response": "...",
    "timestamp": 1678901234
}
```

### 2. File Mappings
Location: `src/data/ranking_file_mappings.json`

```json
{
    "Team A": {
        "file_id": "file-abc123",
        "filename": "team_a.zip",
        "language": "python",
        "uploaded_at": 1678901234
    },
    "Team B": {
        "file_id": "file-xyz789",
        "filename": "team_b.zip",
        "language": "java",
        "uploaded_at": 1678901234
    }
}
```

### 3. Ranking Results
Location: `results/rankings/ranking_<timestamp>.json`

Contains the complete ranking analysis from GPT-5.

## Notes

1. **Simplified Approach**: No need to worry about reusing uploads - the system is straightforward:
   - JSON files are **always** created/updated for each team
   - Files are uploaded **only if** `submission_file_path` is provided

2. **File Upload**: If `submission_file_path` is provided, a new file will be uploaded to Azure OpenAI

3. **JSON Files**: Team evaluation JSON files are always created/updated in `data/team_evaluations/`

4. **GPT-5 Analysis**: Uses the GPT-5 Response API with code_interpreter for comprehensive ranking

5. **Results Storage**: All ranking results are saved with timestamps in `results/rankings/`

## Customizing Ranking Prompt

You can customize the ranking system prompt by editing:
```
prompts/ranking/system_prompt.txt
```

## Error Handling

Common errors:
- `400`: Missing or invalid request data
- `500`: Server error (file upload failed, GPT-5 API error, etc.)

All errors are logged with detailed information for debugging.
