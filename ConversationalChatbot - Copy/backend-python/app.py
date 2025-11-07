from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global session storage
current_session = {
    "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
    "conversations": []
}

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle incoming chat messages.
    Accepts: { "user_message": "..." }
    Returns: { "assistant_response": "I listened to you: <user_message>" }
    """
    try:
        data = request.get_json()
        user_message = data.get('user_message', '')

        if not user_message:
            return jsonify({"error": "user_message is required"}), 400

        # Generate assistant response
        assistant_response = f"I listened to you: {user_message}"

        # Log conversation
        conversation_entry = {
            "user": user_message,
            "assistant": assistant_response
        }
        current_session["conversations"].append(conversation_entry)

        # Save to file
        save_conversation()

        # Log to console
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] User: {user_message}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Assistant: {assistant_response}")

        return jsonify({"assistant_response": assistant_response}), 200

    except Exception as e:
        print(f"Error processing chat: {str(e)}")
        return jsonify({"error": str(e)}), 500

def save_conversation():
    """
    Save the current session's conversations to a JSON file.
    """
    try:
        # Ensure output directory exists
        output_dir = os.path.join(os.path.dirname(__file__), 'output')
        os.makedirs(output_dir, exist_ok=True)

        # Create filename with session ID
        filename = f"session_{current_session['session_id']}.json"
        filepath = os.path.join(output_dir, filename)

        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(current_session, f, indent=2, ensure_ascii=False)

        print(f"Conversation saved to: {filepath}")

    except Exception as e:
        print(f"Error saving conversation: {str(e)}")

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Python Flask Backend",
        "session_id": current_session['session_id'],
        "total_conversations": len(current_session['conversations'])
    }), 200

@app.route('/reset', methods=['POST'])
def reset_session():
    """Reset the current session and start a new one"""
    global current_session

    # Save current session one last time
    save_conversation()

    # Create new session
    current_session = {
        "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "conversations": []
    }

    return jsonify({
        "message": "Session reset successfully",
        "new_session_id": current_session['session_id']
    }), 200

if __name__ == '__main__':
    print("="*50)
    print("Python Flask Backend Starting...")
    print(f"Session ID: {current_session['session_id']}")
    print("="*50)
    app.run(host='0.0.0.0', port=5000, debug=True)
