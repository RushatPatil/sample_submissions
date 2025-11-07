# Quick Start Guide - GenAI Evaluator

This guide will help you get started with the new 3-endpoint architecture.

---

## Installation

1. **Install dependencies**:
```bash
cd evaluator_python_1
pip install -r requirements.txt
```

2. **Set up environment variables**:
Create a `.env` file in the project root with your Azure OpenAI credentials:
```env
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=your_endpoint_here
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
# Add other required environment variables
```

3. **Start the server**:
```bash
python src/main.py
```

The server will start on `http://localhost:5000`

---

## Endpoint 1: Generic Evaluation (Python Projects)

### Use Case
You want to evaluate a Python project with comprehensive static validation (syntax, style, security) plus AI-based evaluation.

### Example Request
```bash
curl -X POST http://localhost:5000/generic_evaluation \
  -F "team_name=TeamAlpha" \
  -F "language=python" \
  -F "problem_statement=Build a REST API for user management with authentication" \
  -F "submission_file=@path/to/project.zip"
```

### What Happens
1. Project is extracted to `extracted_projects/TeamAlpha/`
2. All `.py` files are validated using:
   - **py_compile**: Syntax errors
   - **pylint**: Code quality and style
   - **bandit**: Security vulnerabilities
3. Project is uploaded to Azure OpenAI
4. GPT-4.1 evaluates based on criteria (technical, prompt injection, etc.)
5. **o3-mini checks if evaluation is complete** (ensures thorough evaluation)
6. GPT-5 validates and refines the evaluation
7. Results are saved to `results/TeamAlpha_generic_evaluation_[timestamp].json`

### Check Results
```bash
# View extracted project
ls extracted_projects/TeamAlpha/

# View results
cat results/TeamAlpha_generic_evaluation_*.json
```

---

## Endpoint 2: Use-Level Validation

### Use Case
You want detailed criteria-based evaluation without static validation.

### Example Request
```bash
curl -X POST http://localhost:5000/use_level_validation \
  -F "team_name=TeamBeta" \
  -F "language=python" \
  -F "problem_statement=Implement a machine learning model for sentiment analysis" \
  -F "submission_file=@path/to/project.zip"
```

### What Happens
1. Project is uploaded to Azure OpenAI
2. GPT-4.1 evaluates based on multiple criteria
3. GPT-5 validates each criterion
4. Results are saved to `results/TeamBeta_evaluation_[timestamp].json`

---

## Endpoint 3: Ranking

### Use Case
You want to rank multiple teams that have already been evaluated.

### Example Request
```bash
curl -X POST http://localhost:5000/ranking \
  -H "Content-Type: application/json" \
  -d '{
    "teams_data": [
      {
        "team_name": "TeamAlpha",
        "language": "python",
        "problem_statement": "Build a REST API",
        "evaluation_results": {
          "technical": {
            "status": "completed",
            "response": "Good implementation with RESTful principles..."
          },
          "prompt_injection": {
            "status": "completed",
            "response": "No prompt injection vulnerabilities found..."
          }
        },
        "criteria_count": 2
      },
      {
        "team_name": "TeamBeta",
        "language": "python",
        "problem_statement": "Build a REST API",
        "evaluation_results": {
          "technical": {
            "status": "completed",
            "response": "Basic implementation, missing authentication..."
          },
          "prompt_injection": {
            "status": "completed",
            "response": "Minor vulnerabilities detected..."
          }
        },
        "criteria_count": 2
      }
    ]
  }'
```

### What Happens
1. Team evaluation JSONs are created/updated in `data/team_evaluations/`
2. Teams are grouped by problem statement
3. GPT-5 ranks teams within each problem statement
4. Top submissions from different problems are ranked against each other
5. Results are saved to `results/rankings/ranking_[timestamp].json`

---

## Python Testing Examples

### Test Generic Evaluation
```python
import requests

# Prepare test data
url = "http://localhost:5000/generic_evaluation"
files = {'submission_file': open('test_project.zip', 'rb')}
data = {
    'team_name': 'TestTeam',
    'language': 'python',
    'problem_statement': 'Create a simple calculator application'
}

# Send request
response = requests.post(url, files=files, data=data)
result = response.json()

# Check results
print(f"Status: {result['status']}")
print(f"Static Validation Summary:")
print(f"  Total files: {result['result']['static_validation']['total_files']}")
print(f"  Files with errors: {result['result']['static_validation']['files_with_errors']}")
print(f"  Pylint errors: {result['result']['static_validation']['summary']['pylint']['total_errors']}")
print(f"  Bandit issues: {result['result']['static_validation']['summary']['bandit']['total_issues']}")
```

### Test Use-Level Validation
```python
import requests

url = "http://localhost:5000/use_level_validation"
files = {'submission_file': open('project.zip', 'rb')}
data = {
    'team_name': 'TeamGamma',
    'language': 'python',
    'problem_statement': 'Implement a chatbot with context awareness'
}

response = requests.post(url, files=files, data=data)
result = response.json()

print(f"Status: {result['status']}")
print(f"Criteria evaluated: {result['result']['criteria_count']}")
for criterion, details in result['result']['criteria_results'].items():
    print(f"  {criterion}: {details['status']}")
```

### Test Ranking
```python
import requests
import json

url = "http://localhost:5000/ranking"
payload = {
    "teams_data": [
        {
            "team_name": "Team1",
            "language": "python",
            "problem_statement": "Build a web scraper",
            "evaluation_results": {...},  # From previous evaluation
            "criteria_count": 3
        },
        {
            "team_name": "Team2",
            "language": "python",
            "problem_statement": "Build a web scraper",
            "evaluation_results": {...},  # From previous evaluation
            "criteria_count": 3
        }
    ]
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Status: {result['status']}")
print(f"Total teams ranked: {result['primary_ranking']['total_teams']}")
print(f"Problem statements: {result['primary_ranking']['total_problem_statements']}")
```

---

## Common Issues and Solutions

### Issue 1: "Pylint not found"
**Solution**: Install pylint
```bash
pip install pylint>=3.0.0
```

### Issue 2: "Bandit is not installed"
**Solution**: Install bandit
```bash
pip install bandit>=1.7.0
```

### Issue 3: Static validation shows "timeout"
**Solution**: The default timeout is 30 seconds per tool. For large files, this might not be enough. You can modify the timeout in `src/validators/python_validator.py`.

### Issue 4: "Project path does not exist"
**Solution**: Ensure the ZIP file is valid and properly formatted. Check that it contains Python files.

### Issue 5: Azure OpenAI errors
**Solution**:
- Verify `.env` file has correct credentials
- Check that Azure OpenAI service is accessible
- Ensure you have proper API permissions

---

## Understanding Static Validation Results

### py_compile Results
```json
{
  "status": "success",  // or "error"
  "message": "No syntax errors found"
}
```
- `status: success` = No syntax errors
- `status: error` = Syntax error found (check `message` for details)

### pylint Results
```json
{
  "status": "completed",
  "error_count": 2,      // Critical issues
  "warning_count": 5,    // Potential problems
  "convention_count": 8, // Style violations
  "refactor_count": 3,   // Code smells
  "total_issues": 18,
  "issues": [...]        // First 10 issues
}
```
- Lower counts = better code quality
- Focus on `error_count` first, then `warning_count`

### bandit Results
```json
{
  "status": "completed",
  "issue_count": 2,
  "high_severity": 1,    // Critical security issues
  "medium_severity": 1,  // Important concerns
  "low_severity": 0,     // Minor suggestions
  "issues": [...]        // First 10 issues
}
```
- `high_severity` should be 0 for production code
- Review all `medium_severity` issues carefully

---

## Directory Structure After Running

```
evaluator_python_1/
├── extracted_projects/       # Extracted submissions
│   ├── TeamAlpha/
│   ├── TeamBeta/
│   └── TestTeam/
├── results/                  # Evaluation results
│   ├── TeamAlpha_generic_evaluation_123456.json
│   ├── TeamBeta_evaluation_123457.json
│   └── rankings/
│       ├── ranking_123458.json
│       └── secondary_ranking_123459.json
├── data/
│   ├── team_evaluations/    # Team evaluation JSONs for ranking
│   │   ├── TeamAlpha_evaluation.json
│   │   └── TeamBeta_evaluation.json
│   └── assistant_mapping.json
├── uploads/                 # Temporary file storage (cleaned after use)
└── src/
    ├── validators/          # NEW - Validation modules
    │   ├── __init__.py
    │   └── python_validator.py
    └── ...
```

---

## Best Practices

### 1. For Python Projects
- Ensure `__pycache__` and `venv` are not included in ZIP
- Fix high-severity bandit issues before submission
- Address pylint errors (warnings are optional)

### 2. For Ranking
- Run evaluations first (generic or use-level)
- Collect all team data with same problem statement
- Submit all teams in one ranking request for accurate comparison

### 3. For Production
- Set up proper logging in `.env`
- Monitor `extracted_projects/` disk usage
- Regularly clean old results from `results/`
- Implement rate limiting on endpoints

---

## Example Workflow

### Complete Evaluation Flow
```bash
# Step 1: Evaluate Team A with static validation
curl -X POST http://localhost:5000/generic_evaluation \
  -F "team_name=TeamA" \
  -F "language=python" \
  -F "problem_statement=Build REST API" \
  -F "submission_file=@teamA.zip"

# Step 2: Evaluate Team B with static validation
curl -X POST http://localhost:5000/generic_evaluation \
  -F "team_name=TeamB" \
  -F "language=python" \
  -F "problem_statement=Build REST API" \
  -F "submission_file=@teamB.zip"

# Step 3: Rank teams
curl -X POST http://localhost:5000/ranking \
  -H "Content-Type: application/json" \
  -d @ranking_request.json

# ranking_request.json contains evaluation results from Step 1 & 2
```

---

## Health Check

Always verify the service is running:
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "GenAI Evaluator API"
}
```

---

## Next Steps

1. ✅ Test each endpoint with sample data
2. ✅ Review static validation results for accuracy
3. ✅ Configure Azure OpenAI credentials
4. ✅ Read `API_DOCUMENTATION.md` for detailed API reference
5. ✅ Read `CHANGES_SUMMARY.md` for architecture details
6. 🚀 Start evaluating real projects!

---

## Support & Documentation

- **API Reference**: `API_DOCUMENTATION.md`
- **Architecture Details**: `CHANGES_SUMMARY.md`
- **Existing Docs**: `README.md`, `USAGE.md`, `IMPLEMENTATION_SUMMARY.md`

---

**Happy Evaluating! 🎉**
