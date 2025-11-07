import os
import sys
import zipfile
import shutil
import subprocess
import time
import json
import glob
import socket
from urllib import request as urllib_request
from urllib import error as urllib_error

# -------------------------
# Configuration (auto/fallback)
# -------------------------

# Batch inputs for a single session (n runs). Make edits here if needed.
BATCH_INPUTS = [
    "1. What is the effective date of the Pro Referral Network Program?",
    "2. Am I eligible for the referral reward if I'm an AVP?",
    "3. How much reward will I get for referring a Python developer with 5 years of experience?",
    "4. Can I refer my friend who left Bitwise 8 months ago?",
    "5. How do I submit a referral?",
    "6. When will I receive the referral bonus?",
    "7. Can I email the resume to HR instead of using the portal?",
    "8. What happens if someone else already referred the same candidate?",
    "9. Is DevOps considered a niche skill?",
    "10. How much would I get for referring a React JS developer with 10 years experience?",
    "11. Can I track my referral status in real-time?",
    "12. Can I refer someone who applied to Bitwise 4 months ago?",
    "13. What if I resign before the referral bonus is paid?",
    "14. Is there a limit on how many people I can refer?",
    "15. reward for super niche skill",
    "16. What are the Super Niche skills?",
    "17. Who should I contact if I have questions about the referral program?",
    "18. Can third-party contractors get the referral bonus?",
    "19. What's the salary range for a Python developer at Bitwise?",
    "20. How long does the referral ownership last?"
]

DEFAULT_ZIP_NAME_HINTS = [
    "assistant-BgMWbAffC61FDkxjR9jiaQ-ConversationalChatbot.zip",
    "ConversationalChatbot.zip",
    "genai_project.zip",
]

PROJECT_ROOT_DIRNAME_HINT = "ConversationalChatbot"
BACKEND_DIRNAME = "backend-python"
BACKEND_APP_FILENAME = "app.py"
REQUIREMENTS_FILENAME = "requirements.txt"
VENV_DIRNAME = ".venv_team_alpha"
HOST = "127.0.0.1"
PORT = 5000
BASE_URL = f"http://{HOST}:{PORT}"
HEALTH_URL = f"{BASE_URL}/health"
CHAT_URL = f"{BASE_URL}/chat"
RESET_URL = f"{BASE_URL}/reset"

# -------------------------
# Utilities
# -------------------------

def log(msg):
    print(msg, flush=True)

def find_first_zip(path="."):
    # First try explicit CLI arg
    if len(sys.argv) > 1:
        cand = sys.argv[1]
        if os.path.isfile(cand) and cand.lower().endswith(".zip"):
            return os.path.abspath(cand)
        else:
            log(f"[WARN] Provided path is not a zip file: {cand}")
    # Try hints
    for hint in DEFAULT_ZIP_NAME_HINTS:
        cand = os.path.join(path, hint)
        if os.path.isfile(cand):
            return os.path.abspath(cand)
    # Fallback: any .zip in cwd
    zips = sorted(glob.glob(os.path.join(path, "*.zip")))
    if zips:
        return os.path.abspath(zips[0])
    return None

def unzip_project(zip_path, extract_to=None):
    if extract_to is None:
        base = os.path.splitext(os.path.basename(zip_path))[0]
        extract_to = os.path.abspath(base)
    # If exists, remove to ensure clean state
    if os.path.exists(extract_to):
        log(f"[INFO] Removing existing directory: {extract_to}")
        shutil.rmtree(extract_to, ignore_errors=True)
    os.makedirs(extract_to, exist_ok=True)
    log(f"[INFO] Extracting zip to: {extract_to}")
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(extract_to)
    return extract_to

def locate_backend_dir(extracted_root):
    """Find backend-python directory that contains app.py and requirements.txt."""
    # Common structure: <root>/ConversationalChatbot/backend-python
    candidates = []
    for root, dirs, files in os.walk(extracted_root):
        if BACKEND_APP_FILENAME in files and REQUIREMENTS_FILENAME in files and os.path.basename(root) == BACKEND_DIRNAME:
            candidates.append(root)
    if not candidates:
        raise FileNotFoundError("Could not locate backend-python directory with app.py and requirements.txt")
    # Prefer a path that has PROJECT_ROOT_DIRNAME_HINT in its ancestors
    def has_project_root(path):
        parts = os.path.abspath(path).split(os.sep)
        return PROJECT_ROOT_DIRNAME_HINT in parts
    candidates.sort(key=lambda p: (not has_project_root(p), len(p)))
    chosen = candidates[0]
    log(f"[INFO] Located backend directory: {chosen}")
    return chosen

def venv_python_path(venv_dir):
    if os.name == "nt":
        return os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        return os.path.join(venv_dir, "bin", "python")

def venv_pip_path(venv_dir):
    if os.name == "nt":
        return os.path.join(venv_dir, "Scripts", "pip.exe")
    else:
        return os.path.join(venv_dir, "bin", "pip")

def create_venv(venv_dir):
    py = sys.executable
    log(f"[INFO] Creating virtual environment at: {venv_dir}")
    subprocess.check_call([py, "-m", "venv", venv_dir])

def install_requirements(pip_path, requirements_path):
    log(f"[INFO] Installing requirements from: {requirements_path}")
    subprocess.check_call([pip_path, "install", "-r", requirements_path])

def port_is_open(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        try:
            s.connect((host, port))
            return True
        except Exception:
            return False

def http_get_json(url, timeout=5.0):
    req = urllib_request.Request(url, headers={"Accept": "application/json"})
    with urllib_request.urlopen(req, timeout=timeout) as resp:
        data = resp.read().decode("utf-8")
        return json.loads(data)

def http_post_json(url, payload, timeout=10.0):
    body = json.dumps(payload).encode("utf-8")
    req = urllib_request.Request(url, data=body, headers={"Content-Type": "application/json", "Accept": "application/json"})
    with urllib_request.urlopen(req, timeout=timeout) as resp:
        data = resp.read().decode("utf-8")
        return json.loads(data)

def wait_for_health(health_url, expect_service_substr="Python Flask Backend", timeout_seconds=60):
    start = time.time()
    while True:
        try:
            data = http_get_json(health_url, timeout=2.0)
            if not expect_service_substr or expect_service_substr in str(data):
                return data
        except Exception:
            pass
        if time.time() - start > timeout_seconds:
            raise TimeoutError(f"Service did not become healthy within {timeout_seconds} seconds at {health_url}")
        time.sleep(0.5)

# -------------------------
# Main Orchestration
# -------------------------

def main():
    # 1) Locate and unzip the project
    zip_path = find_first_zip(".")
    if not zip_path:
        raise FileNotFoundError("No .zip file found in current directory. Place the project zip next to this script or pass its path as an argument.")
    log(f"[INFO] Using project zip: {zip_path}")
    extracted_root = unzip_project(zip_path)

    # Try to derive a friendly project root (handle nested single folder case)
    # If the zip extracts a single top-level folder, point extracted_root there
    top_items = [os.path.join(extracted_root, name) for name in os.listdir(extracted_root)]
    top_dirs = [p for p in top_items if os.path.isdir(p)]
    if len(top_dirs) == 1 and not any(os.path.isfile(p) for p in top_items):
        project_root = top_dirs[0]
    else:
        project_root = extracted_root
    log(f"[INFO] Project root resolved to: {project_root}")

    # 2) Detect backend entry and dependencies
    backend_dir = locate_backend_dir(project_root)
    app_path = os.path.join(backend_dir, BACKEND_APP_FILENAME)
    requirements_path = os.path.join(backend_dir, REQUIREMENTS_FILENAME)
    if not os.path.isfile(app_path):
        raise FileNotFoundError(f"Could not find backend app at: {app_path}")
    if not os.path.isfile(requirements_path):
        log(f"[WARN] Missing requirements.txt at: {requirements_path} (will try running without installing dependencies)")

    # 3) Create and prepare venv
    venv_dir = os.path.join(backend_dir, VENV_DIRNAME)
    if os.path.exists(venv_dir):
        log(f"[INFO] Removing existing venv: {venv_dir}")
        shutil.rmtree(venv_dir, ignore_errors=True)
    create_venv(venv_dir)
    venv_python = venv_python_path(venv_dir)
    venv_pip = venv_pip_path(venv_dir)

    # Upgrade pip for robustness
    try:
        subprocess.check_call([venv_pip, "install", "--upgrade", "pip", "setuptools", "wheel"])
    except subprocess.CalledProcessError:
        log("[WARN] Could not upgrade pip/setuptools/wheel; proceeding")

    # Install dependencies
    if os.path.isfile(requirements_path):
        install_requirements(venv_pip, requirements_path)

    # 4) Launch backend (Flask app.py)
    server_log_path = os.path.join(backend_dir, "server.log")
    log(f"[INFO] Launching backend: {app_path}")
    using_existing_server = False

    if port_is_open(HOST, PORT):
        # Check if it's the expected service
        try:
            health = http_get_json(HEALTH_URL, timeout=2.0)
            if "service" in health and "Python Flask Backend" in str(health.get("service", "")):
                using_existing_server = True
                log(f"[INFO] Reusing existing running backend on port {PORT} (session_id={health.get('session_id')})")
            else:
                log(f"[WARN] Port {PORT} is in use by another service; attempting to proceed anyway.")
        except Exception:
            log(f"[WARN] Port {PORT} is open but health check failed; attempting to proceed.")

    proc = None
    if not using_existing_server:
        with open(server_log_path, "w", encoding="utf-8") as log_fp:
            # Run "python app.py" inside backend_dir
            proc = subprocess.Popen([venv_python, app_path], cwd=backend_dir, stdout=log_fp, stderr=subprocess.STDOUT, text=True)
        log(f"[INFO] Backend process started (PID={proc.pid}). Waiting for health...")
        # Wait for the server to be healthy
        health = wait_for_health(HEALTH_URL, expect_service_substr="Python Flask Backend", timeout_seconds=60)
    else:
        # Already running; still fetch health
        health = wait_for_health(HEALTH_URL, expect_service_substr="Python Flask Backend", timeout_seconds=30)

    session_id = str(health.get("session_id"))
    total_before = int(health.get("total_conversations", 0))
    log(f"[INFO] Backend healthy. session_id={session_id}, total_conversations(before)={total_before}")

    # 5) Send batched inputs in a single session
    run_results = []
    for idx, user_message in enumerate(BATCH_INPUTS, start=1):
        payload = {"user_message": user_message}
        try:
            resp = http_post_json(CHAT_URL, payload, timeout=10.0)
            assistant_response = resp.get("assistant_response")
            run_results.append({
                "index": idx,
                "user": user_message,
                "assistant": assistant_response
            })
            log(f"[RUN {idx}] User: {user_message}")
            log(f"[RUN {idx}] Assistant: {assistant_response}")
        except urllib_error.HTTPError as he:
            # Try to read error body
            try:
                err_body = he.read().decode("utf-8")
            except Exception:
                err_body = str(he)
            log(f"[ERROR] HTTPError on run {idx}: {he} | Body: {err_body}")
            run_results.append({"index": idx, "user": user_message, "error": f"HTTPError: {he}"})
        except Exception as e:
            log(f"[ERROR] Exception on run {idx}: {e}")
            run_results.append({"index": idx, "user": user_message, "error": str(e)})

    # Allow file system to flush
    time.sleep(0.5)

    # 6) Resolve output JSON path and extract results
    # The backend writes to backend-python/output/session_{session_id}.json
    output_dir = os.path.join(backend_dir, "output")
    output_path = os.path.join(output_dir, f"session_{session_id}.json")
    # Wait briefly for file to exist
    t0 = time.time()
    while not os.path.isfile(output_path) and time.time() - t0 < 10:
        time.sleep(0.25)
    if not os.path.isfile(output_path):
        log(f"[WARN] Expected output JSON not found at: {output_path}. Proceeding without file extraction.")
        session_conversation = {"session_id": session_id, "conversations": []}
    else:
        with open(output_path, "r", encoding="utf-8") as f:
            session_conversation = json.load(f)
        log(f"[INFO] Loaded session conversation from: {output_path}")

    # 7) Display and save consolidated results
    # Always extract reasoning steps before conclusion data when extracting from output files.
    # (Note: This backend stores only 'user' and 'assistant' turns; no separate reasoning fields are present.)
    print("\n===== SESSION SUMMARY =====")
    try:
        health_after = http_get_json(HEALTH_URL, timeout=5.0)
    except Exception:
        health_after = {}
    total_after = int(health_after.get("total_conversations", len(session_conversation.get("conversations", []))))
    print(f"Session ID: {session_id}")
    print(f"Total conversations logged: before={total_before}, after={total_after}")
    print("")
    print("Conversation transcript (order preserved):")
    conversations = session_conversation.get("conversations", [])
    for i, turn in enumerate(conversations, start=1):
        u = turn.get("user")
        a = turn.get("assistant")
        print(f"  Turn {i} - User     : {u}")
        print(f"  Turn {i} - Assistant: {a}")

    # Save automation results for convenience
    automation_summary = {
        "session_id": session_id,
        "backend_dir": backend_dir,
        "output_file": output_path if os.path.isfile(output_path) else None,
        "health_before": health,
        "health_after": health_after,
        "batched_runs": run_results,
        "session_conversation": session_conversation,
    }
    results_path = os.path.join(project_root, "automation_results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(automation_summary, f, indent=2, ensure_ascii=False)
    print(f"\n[INFO] Wrote automation summary to: {results_path}")

    # 8) Shutdown the backend we started (if we started it)
    if proc is not None:
        log("[INFO] Terminating backend process...")
        try:
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()
        except Exception as e:
            log(f"[WARN] Error while terminating backend: {e}")
        finally:
            # Tail the last lines of server log for debugging
            if os.path.isfile(server_log_path):
                print("\n===== SERVER LOG (tail) =====")
                try:
                    with open(server_log_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()[-50:]
                    for line in lines:
                        print(line.rstrip())
                except Exception:
                    pass

    print("\n[DONE] Automation complete.")

if __name__ == "__main__":
    main()