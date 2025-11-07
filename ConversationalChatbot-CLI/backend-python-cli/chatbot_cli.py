#!/usr/bin/env python3
"""
Conversational Chatbot CLI Application
Python 3.11+ compatible CLI tool that processes chat messages
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class ChatbotCLI:
    """Command-line chatbot application"""

    def __init__(self, output_dir: str = "output"):
        """
        Initialize the chatbot CLI

        Args:
            output_dir: Directory to save conversation logs
        """
        self.output_dir = Path(__file__).parent / output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_file = self.output_dir / f"session_{self.session_id}.json"
        self.conversations: List[Dict[str, str]] = []

        # Load existing session if it exists
        self._load_session()

    def _load_session(self) -> None:
        """Load existing session from file if it exists"""
        if self.session_file.exists():
            try:
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.conversations = data.get('conversations', [])
            except Exception as e:
                print(f"Warning: Could not load session: {e}", file=sys.stderr)

    def _save_conversation(self) -> None:
        """Save the current session's conversations to a JSON file"""
        try:
            session_data = {
                "session_id": self.session_id,
                "conversations": self.conversations
            }

            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)

            print(f"[LOG] Conversation saved to: {self.session_file}", file=sys.stderr)

        except Exception as e:
            print(f"[ERROR] Failed to save conversation: {e}", file=sys.stderr)

    def process_message(self, user_message: str) -> Dict[str, str]:
        """
        Process a user message and return assistant response

        Args:
            user_message: The message from the user

        Returns:
            Dictionary with assistant_response
        """
        if not user_message or not user_message.strip():
            return {"error": "user_message is required"}

        # Generate assistant response
        assistant_response = f"I listened to you: {user_message}"

        # Log conversation
        conversation_entry = {
            "user": user_message,
            "assistant": assistant_response,
            "timestamp": datetime.now().isoformat()
        }
        self.conversations.append(conversation_entry)

        # Save to file
        self._save_conversation()

        # Log to stderr (so stdout remains clean for JSON output)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] User: {user_message}", file=sys.stderr)
        print(f"[{timestamp}] Assistant: {assistant_response}", file=sys.stderr)

        return {"assistant_response": assistant_response}

    def interactive_mode(self) -> None:
        """Run in interactive mode"""
        print("="*50, file=sys.stderr)
        print("Conversational Chatbot CLI", file=sys.stderr)
        print(f"Session ID: {self.session_id}", file=sys.stderr)
        print("Type 'exit' or 'quit' to end the session", file=sys.stderr)
        print("="*50, file=sys.stderr)
        print(file=sys.stderr)

        while True:
            try:
                user_input = input("You: ").strip()

                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("Goodbye!", file=sys.stderr)
                    break

                if not user_input:
                    continue

                response = self.process_message(user_input)

                if "error" in response:
                    print(f"Error: {response['error']}", file=sys.stderr)
                else:
                    print(f"Assistant: {response['assistant_response']}")

            except KeyboardInterrupt:
                print("\n\nGoodbye!", file=sys.stderr)
                break
            except EOFError:
                break
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)

    def single_message_mode(self, message: str) -> None:
        """
        Process a single message and output JSON response

        Args:
            message: The user message to process
        """
        response = self.process_message(message)
        # Output JSON to stdout for Java to capture
        print(json.dumps(response, ensure_ascii=False))

    def get_health_status(self) -> Dict:
        """Get health status of the CLI application"""
        return {
            "status": "healthy",
            "service": "Python CLI Backend",
            "session_id": self.session_id,
            "total_conversations": len(self.conversations),
            "python_version": sys.version
        }


def main():
    """Main entry point for the CLI application"""
    parser = argparse.ArgumentParser(
        description="Conversational Chatbot CLI Application"
    )
    parser.add_argument(
        '-m', '--message',
        type=str,
        help='Process a single message and output JSON response'
    )
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    parser.add_argument(
        '--health',
        action='store_true',
        help='Output health status as JSON'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='output',
        help='Directory to save conversation logs (default: output)'
    )

    args = parser.parse_args()

    # Create chatbot instance
    chatbot = ChatbotCLI(output_dir=args.output_dir)

    # Health check
    if args.health:
        health = chatbot.get_health_status()
        print(json.dumps(health, indent=2))
        sys.exit(0)

    # Single message mode
    if args.message:
        chatbot.single_message_mode(args.message)
        sys.exit(0)

    # Interactive mode
    if args.interactive:
        chatbot.interactive_mode()
        sys.exit(0)

    # If no arguments provided, try to read from stdin
    if not sys.stdin.isatty():
        try:
            input_data = sys.stdin.read().strip()
            if input_data:
                try:
                    # Try to parse as JSON
                    data = json.loads(input_data)
                    message = data.get('user_message', '')
                except json.JSONDecodeError:
                    # If not JSON, treat as plain text
                    message = input_data

                if message:
                    chatbot.single_message_mode(message)
                    sys.exit(0)
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)

    # Default to interactive mode if no input
    chatbot.interactive_mode()


if __name__ == "__main__":
    main()
