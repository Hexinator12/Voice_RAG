import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI

# Load environment variables
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '.env')
load_dotenv(env_path)

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
MODEL_NAME = "deepseek/deepseek-chat-v3.1:free"

# Validate required environment variables
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY must be set in .env file")

# Initialize OpenAI client for OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def generate_response(messages):
    """Generate a response using OpenRouter with DeepSeek model"""
    try:
        # Add system message if not present
        if not any(msg.get('role') == 'system' for msg in messages):
            messages.insert(0, {
                "role": "system",
                "content": "You are a helpful campus assistant. Provide concise, friendly, and informative responses to student queries about the university."
            })
        
        print(f"Sending to OpenRouter with messages: {json.dumps(messages, indent=2)}")
            
        # Make the API call with required headers
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            extra_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "VOICERAG"
            },
            extra_body={
                "transforms": ["middleware"]
            }
        )
        
        print(f"Received response from OpenRouter: {completion}")
        
        if hasattr(completion, 'choices') and len(completion.choices) > 0:
            return completion.choices[0].message.content.strip()
        else:
            print("Unexpected response format:", completion)
            return "I'm sorry, I received an unexpected response format from the model."
            
    except Exception as e:
        print(f"Error calling OpenRouter API: {str(e)}")
        return "I'm sorry, I'm having trouble generating a response right now."

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Simple in-memory storage for chat history
chat_history = [
    {
        'id': 1,
        'text': 'Hello! I\'m your VOICERAG assistant. How can I help you today?',
        'sender': 'bot',
        'timestamp': datetime.now().isoformat()
    }
]

@app.route('/')
def home():
    return "VOICERAG Backend is running!"

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'version': '1.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/text', methods=['POST'])
def handle_text_input():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400
    
    # Add user message to history
    user_message = {
        'id': len(chat_history) + 1,
        'text': data['message'],
        'sender': 'user',
        'timestamp': datetime.now().isoformat()
    }
    chat_history.append(user_message)
    
    # Prepare messages for OpenRouter API
    # The system message is now handled in generate_response
    messages = [
        {"role": "user", "content": data['message']}
    ]
    
    bot_text = generate_response(messages)
    
    # Log the generated response for debugging
    print(f"Generated response: {bot_text}")
    
    bot_response = {
        'id': len(chat_history) + 1,
        'text': bot_text,
        'sender': 'bot',
        'timestamp': datetime.now().isoformat()
    }
    chat_history.append(bot_response)
    
    return jsonify({
        'status': 'success',
        'response': bot_response
    })

@app.route('/api/chat/history', methods=['GET'])
def get_chat_history():
    return jsonify({
        'status': 'success',
        'history': chat_history
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
