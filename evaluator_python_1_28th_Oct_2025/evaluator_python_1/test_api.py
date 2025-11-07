"""
Simple test script to test the evaluation API
"""

import requests
import json
from pathlib import Path


def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get("http://localhost:5000/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)


def test_evaluation(zip_file_path: str, team_name: str = "TestTeam"):
    """Test evaluation endpoint"""
    print(f"Testing evaluation for team: {team_name}")

    # Check if file exists
    if not Path(zip_file_path).exists():
        print(f"Error: File not found: {zip_file_path}")
        return

    url = "http://localhost:5000/evaluate"

    files = {
        'submission_file': (Path(zip_file_path).name, open(zip_file_path, 'rb'), 'application/zip')
    }

    data = {
        'team_name': team_name,
        'language': 'python',
        'problem_statement': 'Build a simple calculator application with basic arithmetic operations'
    }

    print("Submitting evaluation request...")
    print(f"Team: {team_name}")
    print(f"Language: python")
    print(f"File: {zip_file_path}")
    print("This may take several minutes...")
    print("-" * 50)

    try:
        response = requests.post(url, files=files, data=data, timeout=600)
        print(f"Status Code: {response.status_code}")
        print(f"Response:")
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.Timeout:
        print("Request timed out. The evaluation may still be processing.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        files['submission_file'][1].close()

    print("-" * 50)


def test_status(team_name: str = "TestTeam"):
    """Test status endpoint"""
    print(f"Testing status for team: {team_name}")

    url = f"http://localhost:5000/status/{team_name}"
    response = requests.get(url)

    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))
    print("-" * 50)


def test_results(team_name: str = "TestTeam"):
    """Test results endpoint"""
    print(f"Testing results for team: {team_name}")

    url = f"http://localhost:5000/results/{team_name}"
    response = requests.get(url)

    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))
    print("-" * 50)


if __name__ == "__main__":
    print("=" * 50)
    print("GenAI Evaluator API Test Script")
    print("=" * 50)
    print()

    # Test 1: Health check
    test_health()

    # Test 2: Evaluation (you need to provide a zip file path)
    # Uncomment and provide a valid zip file path to test
    # test_evaluation("path/to/your/submission.zip", "TestTeam")

    # Test 3: Status
    # Uncomment to test (only after running an evaluation)
    # test_status("TestTeam")

    # Test 4: Results
    # Uncomment to test (only after evaluation is complete)
    # test_results("TestTeam")

    print("\nNote: Uncomment the test functions in the script and provide")
    print("a valid zip file path to test the evaluation flow.")
