"""
Automated runner for the ConversationalChatbot GenAI project.

This script:
- Creates a Python virtual environment in the project backend directory.
- Installs required packages from backend-python/requirements.txt.
- Launches the Flask backend (app.py).
- Sends a batch of 20 input questions to /chat within a single session.
- After each input, it reads and extracts the full session conversation from the designated output file.
- Prints a reasoning summary before the full conversation (as requested).

Usage:
    python run_conversational_chatbot.py [PROJECT_ROOT]

Where PROJECT_ROOT is the path to the existing extracted project directory. It can be:
- The root that directly contains "ConversationalChatbot" (e.g., /path/to/your/extracted/ConversationalChatbot).
- Or a root that contains the folder "extracted_projects/5_20251104_215514_591515/ConversationalChatbot".
If not provided, the current working directory will be used.

Notes:
- The script does not modify any project source files. It only creates a venv (runtime files) and reads the output JSON produced by the project.
- The designated output directory to read from is expected at:
  extracted_projects\5_20251104_215514_591515\ConversationalChatbot\backend-python\output
  within the existing project directory submitted by the user. If not found, the script falls back to the backend's own output folder.

"""

import os
import sys
import subprocess
import time
import json
import urllib.request
import urllib.error
import socket

# --------------- Configuration and Batched Inputs -----------------

BATCHED_INPUTS_TEXT = """1. What is the effective date of the Pro Referral Network Program?
2. Am I eligible for the referral reward if I'm an AVP?
3. How much reward will I get for referring a Python developer with 5 years of experience?
4. Can I refer my friend who left Bitwise 8 months ago?
5. How do I submit a referral?
6. When will I receive the referral bonus?
7. Can I email the resume to HR instead of using the portal?
8. What happens if someone else already referred the same candidate?
9. Is DevOps considered a niche skill?
10. How much would I get for referring a React JS developer with 10 years experience?
11. Can I track my referral status in real-time?
12. Can I refer someone who applied to Bitwise 4 months ago?
13. What if I resign before the referral bonus is paid?
14. Is there a limit on how many people I can refer?
15. reward for super niche skill
16. What are the Super Niche skills?
17. Who should I contact if I have questions about the referral program?
18. Can third-party contractors get the referral bonus?
19. What's the salary range for a Python developer at Bitwise?
20. How long does the referral ownership last?"""

# Endpoint configuration
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5001
CHAT_ENDPOINT = "/chat"
HEALTH_ENDPOINT = "/health"
RESET_ENDPOINT = "/reset"  # not used, but available

# --------------- Utility Functions -----------------

def is_windows():
    return os.name == "nt"

def norm(p):
    return os.path.normpath(p)

def http_get_json(url, timeout=3.0):
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        data = resp.read().decode(charset, errors="replace")
        return json.loads(data)

def http_post_json(url, payload, timeout=5.0):
    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        body = resp.read().decode(charset, errors="replace")
        return json.loads(body)

def wait_for_health(base_url, timeout=60.0, interval=1.0):
    start = time.time()
    last_err = None
    while time.time() - start < timeout:
        try:
            health = http_get_json(base_url + HEALTH_ENDPOINT, timeout=interval)
            return health
        except (urllib.error.URLError, urllib.error.HTTPError, socket.timeout) as e:
            last_err = e
            time.sleep(interval)
    raise RuntimeError(f"Backend health check failed after {timeout}s. Last error: {last_err}")

def parse_batched_inputs(text_block):
    inputs = []
    for line in text_block.splitlines():
        line = line.strip()
        if not line:
            continue
        # Remove leading enumeration like "1. " if present
        if ". " in line:
            parts = line.split(". ", 1)
            # only drop the leading number if it looks like a number
            if parts[0].isdigit():
                line = parts[1]
        inputs.append(line)
    return inputs

def create_venv(venv_path):
    # Create virtual environment
    print(f"[Setup] Creating virtual environment at: {venv_path}")
    subprocess.check_call([sys.executable, "-m", "venv", venv_path])
    print("[Setup] Virtual environment created.")

def get_venv_python_and_pip(venv_path):
    if is_windows():
        python_exe = os.path.join(venv_path, "Scripts", "python.exe")
        pip_exe = os.path.join(venv_path, "Scripts", "pip.exe")
    else:
        python_exe = os.path.join(venv_path, "bin", "python")
        pip_exe = os.path.join(venv_path, "bin", "pip")
    return python_exe, pip_exe

def install_requirements(pip_exe, requirements_path):
    if not os.path.isfile(requirements_path):
        raise FileNotFoundError(f"requirements.txt not found at: {requirements_path}")
    print(f"[Setup] Installing dependencies from: {requirements_path}")
    subprocess.check_call([pip_exe, "install", "-r", requirements_path])
    print("[Setup] Dependencies installed.")

def launch_flask_app(python_exe, app_path, workdir):
    print(f"[Run] Launching Flask backend: {app_path}")
    # Start the Flask app in a subprocess
    proc = subprocess.Popen(
        [python_exe, app_path],
        cwd=workdir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    return proc

def safe_terminate(proc):
    if proc and proc.poll() is None:
        print("[Run] Terminating Flask backend...")
        try:
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()
        except Exception as e:
            print(f"[Run] Error terminating process: {e}")

def detect_backend_dir(project_root):
    """
    Detect backend-python directory. Tries:
    - project_root/ConversationalChatbot/backend-python
    - project_root/extracted_projects/5_20251104_215514_591515/ConversationalChatbot/backend-python
    - project_root/backend-python
    - Recursive search for a dir named 'backend-python' containing 'app.py'
    """
    candidates = [
        os.path.join(project_root, "ConversationalChatbot", "backend-python"),
        os.path.join(project_root, "extracted_projects", "5_20251104_215514_591515", "ConversationalChatbot", "backend-python"),
        os.path.join(project_root, "backend-python"),
    ]
    for c in candidates:
        if os.path.isfile(os.path.join(c, "app.py")) and os.path.isfile(os.path.join(c, "requirements.txt")):
            return c

    # Fallback: recursive search
    for root, dirs, files in os.walk(project_root):
        if "app.py" in files and "requirements.txt" in files and os.path.basename(root) == "backend-python":
            return root

    raise FileNotFoundError("Could not locate backend-python directory with app.py and requirements.txt under the provided project root.")

def get_designated_output_dir(project_root, backend_dir):
    """
    Primary read location (as per instructions):
      extracted_projects\5_20251104_215514_591515\ConversationalChatbot\backend-python\output
    Fallback:
      backend_dir/output
    """
    primary = os.path.join(project_root, "extracted_projects", "5_20251104_215514_591515", "ConversationalChatbot", "backend-python", "output")
    if os.path.isdir(primary):
        return primary
    fallback = os.path.join(backend_dir, "output")
    if os.path.isdir(fallback):
        return fallback
    # If neither exists yet, prefer primary path for reading after the app writes;
    # do NOT create directories here, per instruction to avoid modifying project files.
    return primary

def read_session_file(output_dir, session_id):
    """
    Reads session_<session_id>.json from output_dir.
    """
    filename = f"session_{session_id}.json"
    filepath = os.path.join(output_dir, filename)
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Session file not found at: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f), filepath

# --------------- Main Workflow -----------------

def main():
    # Determine project root path
    project_root = None
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = os.environ.get("PROJECT_DIR", os.getcwd())

    project_root = norm(project_root)
    print(f"[Init] Using project root: {project_root}")

    # Detect backend-python directory
    backend_dir = detect_backend_dir(project_root)
    backend_dir = norm(backend_dir)
    print(f"[Init] Detected backend directory: {backend_dir}")

    requirements_path = os.path.join(backend_dir, "requirements.txt")
    app_path = os.path.join(backend_dir, "app.py")

    # Create venv in backend directory (runtime-only; does not modify source files)
    venv_path = os.path.join(backend_dir, ".venv")
    if not os.path.isdir(venv_path):
        create_venv(venv_path)
    else:
        print(f"[Setup] Reusing existing virtual environment: {venv_path}")

    python_exe, pip_exe = get_venv_python_and_pip(venv_path)

    # Install dependencies
    install_requirements(pip_exe, requirements_path)

    # Launch Flask backend
    proc = launch_flask_app(python_exe, app_path, backend_dir)

    # Optionally, capture some startup logs briefly
    time.sleep(1.0)
    print("[Run] Waiting for backend health to become ready...")
    base_url = f"http://{DEFAULT_HOST}:{DEFAULT_PORT}"
    health = None
    try:
        health = wait_for_health(base_url, timeout=60.0, interval=1.0)
    except Exception as e:
        # Drain any logs to help diagnose
        try:
            print("[Run] Backend output (last 50 lines):")
            out = proc.stdout.read() if proc and proc.stdout else ""
            lines = out.splitlines()[-50:]
            for ln in lines:
                print(ln)
        except Exception:
            pass
        safe_terminate(proc)
        raise

    # Extract session ID from health
    session_id = str(health.get("session_id"))
    total_conv = int(health.get("total_conversations", 0))
    print(f"[Run] Backend healthy. Session ID: {session_id}, Existing conversations: {total_conv}")

    # Determine designated output directory to read
    designated_output_dir = get_designated_output_dir(project_root, backend_dir)
    print(f"[Run] Designated output directory (read only): {designated_output_dir}")

    # Prepare inputs
    inputs = parse_batched_inputs(BATCHED_INPUTS_TEXT)
    print(f"[Run] Prepared {len(inputs)} batched inputs for a single session.")

    # Send each input, then read and print session file
    for idx, question in enumerate(inputs, start=1):
        payload = {"user_message": question}
        print(f"\n[Run {idx}] Sending message: {question}")
        try:
            resp = http_post_json(base_url + CHAT_ENDPOINT, payload, timeout=10.0)
            assistant_response = resp.get("assistant_response", "")
            print(f"[Run {idx}] Assistant responded: {assistant_response}")
        except Exception as e:
            print(f"[Run {idx}] Error posting to /chat: {e}")
            safe_terminate(proc)
            raise

        # After sending, re-check health (to confirm session stats)
        try:
            health = http_get_json(base_url + HEALTH_ENDPOINT, timeout=3.0)
            session_id = str(health.get("session_id", session_id))
            total_conv = int(health.get("total_conversations", 0))
        except Exception as e:
            print(f"[Run {idx}] Warning: Failed to retrieve health after message: {e}")

        # Read session conversation file from designated output dir
        time.sleep(0.2)  # small delay to allow file write
        try:
            session_data, session_file_path = read_session_file(designated_output_dir, session_id)
        except FileNotFoundError as e:
            # Fallback: if primary directory is not where the app wrote, try backend_dir/output
            fallback_dir = os.path.join(backend_dir, "output")
            try:
                session_data, session_file_path = read_session_file(fallback_dir, session_id)
            except Exception as e2:
                print(f"[Run {idx}] Failed to read session file from primary and fallback output dirs.")
                print(f"  Primary error: {e}")
                print(f"  Fallback error: {e2}")
                safe_terminate(proc)
                raise

        # Print reasoning summary before full conversation (as requested)
        conversations = session_data.get("conversations", [])
        print(f"[Run {idx}] Reasoning Summary:")
        print(f"  - Session file: {session_file_path}")
        print(f"  - Total conversations recorded: {len(conversations)}")
        if conversations:
            last_pair = conversations[-1]
            print(f"  - Last user: {last_pair.get('user')}")
            print(f"  - Last assistant: {last_pair.get('assistant')}")

        # Conclusion: print the complete conversation so far
        print(f"[Run {idx}] Conclusion: Full conversation so far:")
        for i, pair in enumerate(conversations, start=1):
            print(f"    [{i}] User: {pair.get('user')}")
            print(f"        Assistant: {pair.get('assistant')}")

    # Final session dump
    print("\n[Final] Completed all runs. Reading final session file...")
    try:
        final_session_data, final_session_file_path = read_session_file(designated_output_dir, session_id)
    except FileNotFoundError:
        final_session_data, final_session_file_path = read_session_file(os.path.join(backend_dir, "output"), session_id)

    print(f"[Final] Session ID: {final_session_data.get('session_id')}")
    print(f"[Final] Session file path: {final_session_file_path}")
    print(f"[Final] Total conversations: {len(final_session_data.get('conversations', []))}")

    # Clean up
    safe_terminate(proc)
    print("[Done] Backend process terminated. All steps completed successfully.")

if __name__ == "__main__":
    main()