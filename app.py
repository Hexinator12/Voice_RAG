from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import json
from datetime import datetime

# Import our voice and text processing modules
from voice_processor import VoiceProcessor
from text_processor import TextProcessor
from response_generator import ResponseGenerator

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize processors
voice_processor = VoiceProcessor()
text_processor = TextProcessor()
response_generator = ResponseGenerator()

@app.route('/')
def home():
    """Home route - serves the main page"""
    return jsonify({
        'message': 'VOICERAG Campus Assistant API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'health': '/health',
            'text_input': '/api/text',
            'voice_input': '/api/voice',
            'chat_history': '/api/chat/history'
        }
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'voice_processor': 'ready',
            'text_processor': 'ready',
            'response_generator': 'ready'
        }
    })

@app.route('/api/text', methods=['POST'])
def handle_text_input():
    """Handle text input from users"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing required field: text',
                'status': 'error'
            }), 400
        
        user_input = data['text']
        input_type = data.get('input_type', 'text')
        
        # Process the text input
        processed_text = text_processor.process_text(user_input)
        
        # Generate response
        response = response_generator.generate_response(processed_text, input_type)
        
        return jsonify({
            'status': 'success',
            'input': user_input,
            'processed_input': processed_text,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/voice', methods=['POST'])
def handle_voice_input():
    """Handle voice input from users"""
    try:
        # Check if audio file is provided
        if 'audio' not in request.files:
            return jsonify({
                'error': 'No audio file provided',
                'status': 'error'
            }), 400
        
        audio_file = request.files['audio']
        
        if audio_file.filename == '':
            return jsonify({
                'error': 'No file selected',
                'status': 'error'
            }), 400
        
        # Save the audio file temporarily
        temp_audio_path = f"temp_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        audio_file.save(temp_audio_path)
        
        # Process voice input
        voice_result = voice_processor.process_voice(temp_audio_path)
        
        if voice_result['status'] != 'success':
            return jsonify(voice_result), 400
        
        # Process the transcribed text
        processed_text = text_processor.process_text(voice_result['transcribed_text'])
        
        # Generate response
        response = response_generator.generate_response(processed_text, 'voice')
        
        # Clean up temporary file
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
        
        return jsonify({
            'status': 'success',
            'transcribed_text': voice_result['transcribed_text'],
            'confidence': voice_result['confidence'],
            'processed_input': processed_text,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/chat/history', methods=['GET'])
def get_chat_history():
    """Get chat history (placeholder for now)"""
    return jsonify({
        'status': 'success',
        'history': [],
        'message': 'Chat history feature will be implemented soon'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error',
        'available_endpoints': [
            '/',
            '/health',
            '/api/text',
            '/api/voice',
            '/api/chat/history'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'status': 'error'
    }), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('temp', exist_ok=True)
    
    print("🚀 Starting VOICERAG Campus Assistant API...")
    print("📡 Server running on http://localhost:5001")
    print("🔍 Health check: http://localhost:5001/health")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
