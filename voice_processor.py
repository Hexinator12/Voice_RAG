import speech_recognition as sr
import pyaudio
import wave
import tempfile
import os
import numpy as np
from datetime import datetime
import logging
import time
from typing import Dict, Any
from text_processor import TextProcessor
from response_generator import ResponseGenerator
import pyttsx3

class VoiceProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.text_processor = TextProcessor()
        self.response_generator = ResponseGenerator()
        self.tts_engine = pyttsx3.init()
        
        # Configure TTS engine
        self.tts_engine.setProperty('rate', 150)  # Speech rate
        self.tts_engine.setProperty('volume', 0.9)  # Volume level
        
        # Configure recognizer settings
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.operation_timeout = None
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.8
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Calibrate microphone for ambient noise
        self.calibrate_microphone()
    
    def calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        try:
            with self.microphone as source:
                self.logger.info("🎤 Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.logger.info("✅ Microphone calibration complete")
        except Exception as e:
            self.logger.warning(f"⚠️ Microphone calibration failed: {e}")
    
    def speak_response(self, text: str):
        """
        Convert text to speech and play it
        
        Args:
            text (str): Text to speak
        """
        try:
            self.logger.info("🔊 Speaking response...")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            self.logger.info("✅ Response spoken successfully")
        except Exception as e:
            self.logger.error(f"❌ Error speaking response: {e}")
    
    def process_voice_with_response(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Process voice input and generate a complete response
        
        Args:
            audio_file_path (str): Path to the audio file
            
        Returns:
            Dict: Complete response with transcription, processing, and generated response
        """
        try:
            # Step 1: Transcribe voice to text
            transcription_result = self.process_voice(audio_file_path)
            
            if transcription_result['status'] != 'success':
                return {
                    'status': 'error',
                    'error': f'Transcription failed: {transcription_result["error"]}',
                    'timestamp': datetime.now().isoformat()
                }
            
            transcribed_text = transcription_result['transcribed_text']
            confidence = transcription_result['confidence']
            
            # Step 2: Process the transcribed text
            processed_text = self.text_processor.process_text(transcribed_text)
            
            # Step 3: Generate response
            response_data = self.response_generator.generate_response(processed_text)
            
            # Step 4: Format response for voice
            voice_response = self.response_generator.format_response_for_voice(response_data)
            
            return {
                'status': 'success',
                'transcription': {
                    'text': transcribed_text,
                    'confidence': confidence
                },
                'processed_text': processed_text,
                'response': response_data,
                'voice_response': voice_response,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error in voice processing with response: {e}")
            return {
                'status': 'error',
                'error': f'Error processing voice with response: {e}',
                'timestamp': datetime.now().isoformat()
            }
    
    def interactive_voice_chat(self):
        """
        Interactive voice chat - records, processes, and responds with voice
        """
        print("🎤 Interactive Voice Chat Started")
        print("💡 Speak naturally and I'll respond with voice!")
        print("🛑 Press Ctrl+C to stop\n")
        
        try:
            while True:
                print("\n🎙️  Listening... (Speak now)")
                
                # Record audio with voice activation
                recording_result = self.record_audio(
                    duration=15,
                    silence_timeout=3.0,
                    voice_activated=True
                )
                
                if recording_result['status'] != 'success':
                    print(f"❌ Recording failed: {recording_result['error']}")
                    continue
                
                print(f"✅ Recording complete ({recording_result['duration']:.1f}s)")
                
                # Process voice and generate response
                response_result = self.process_voice_with_response(recording_result['file_path'])
                
                if response_result['status'] == 'success':
                    # Display text response
                    print(f"\n🧠 You said: '{response_result['transcription']['text']}'")
                    print(f"🎯 Intent: {response_result['processed_text']['intent']['primary_intent']}")
                    print(f"💬 Response: {response_result['response']['response']}")
                    
                    # Speak the response
                    self.speak_response(response_result['voice_response'])
                    
                    # Add a delay to prevent picking up the system's own voice
                    time.sleep(1.0)  # 1 second delay
                    
                    # Wait for user confirmation before listening again
                    input("\n🎤 Press Enter when you're ready to speak again...")
                    
                    # Show follow-up if available
                    if response_result['response'].get('follow_up'):
                        print(f"🔄 Follow-up: {response_result['response']['follow_up']}")
                else:
                    print(f"❌ Processing failed: {response_result['error']}")
                    error_response = "I'm sorry, I couldn't process your request. Please try again."
                    self.speak_response(error_response)
                    
                    # Add a delay even for error responses
                    time.sleep(1.0)
                    
                    # Wait for user confirmation before listening again
                    input("\n🎤 Press Enter when you're ready to speak again...")
                
                # Clean up temporary file
                if os.path.exists(recording_result['file_path']):
                    os.remove(recording_result['file_path'])
                
                print("\n" + "-" * 50)
                
        except KeyboardInterrupt:
            print("\n🛑 Interactive voice chat stopped")
        except Exception as e:
            print(f"\n❌ Error in interactive voice chat: {e}")
    
    def process_voice(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Process voice input from audio file
        
        Args:
            audio_file_path (str): Path to the audio file
            
        Returns:
            dict: Processing result with transcribed text and confidence
        """
        try:
            self.logger.info(f"🔊 Processing audio file: {audio_file_path}")
            
            # Check if file exists
            if not os.path.exists(audio_file_path):
                return {
                    'status': 'error',
                    'error': f'Audio file not found: {audio_file_path}'
                }
            
            # Load audio file
            with sr.AudioFile(audio_file_path) as source:
                # Record the audio from the file
                audio_data = self.recognizer.record(source)
                
                self.logger.info("🎵 Audio loaded successfully")
            
            # Try to recognize speech using Google Speech Recognition
            try:
                self.logger.info("🧠 Transcribing speech...")
                
                # Use Google Speech Recognition (free version)
                text = self.recognizer.recognize_google(audio_data, language='en-US')
                
                # For better accuracy, we could use:
                # text = self.recognizer.recognize_google_cloud(audio_data, credentials_json=GOOGLE_CLOUD_CREDENTIALS)
                
                self.logger.info(f"✅ Transcription successful: '{text}'")
                
                return {
                    'status': 'success',
                    'transcribed_text': text,
                    'confidence': 0.95,  # Google doesn't provide confidence for free API
                    'timestamp': datetime.now().isoformat()
                }
                
            except sr.UnknownValueError:
                self.logger.warning("⚠️ Speech recognition could not understand the audio")
                return {
                    'status': 'error',
                    'error': 'Speech recognition could not understand the audio'
                }
                
            except sr.RequestError as e:
                self.logger.error(f"❌ Speech recognition service error: {e}")
                return {
                    'status': 'error',
                    'error': f'Speech recognition service error: {e}'
                }
                
        except Exception as e:
            self.logger.error(f"❌ Error processing voice: {e}")
            return {
                'status': 'error',
                'error': f'Error processing voice: {e}'
            }
    
    def record_audio(self, duration=15, output_file=None, silence_timeout=3.0, voice_activated=True):
        """
        Enhanced audio recording with voice activation and silence detection
        
        Args:
            duration (int): Maximum recording duration in seconds (default: 15)
            output_file (str): Path to save the recorded audio
            silence_timeout (float): Seconds of silence to stop recording (default: 3.0)
            voice_activated (bool): Start recording only when voice is detected (default: True)
            
        Returns:
            dict: Recording result with enhanced metadata
        """
        try:
            self.logger.info(f"🎙️ Starting enhanced audio recording (max {duration}s, silence timeout {silence_timeout}s)...")
            
            if output_file is None:
                output_file = f"temp_recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            
            # Audio recording parameters
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 16000
            CHUNK = 1024
            
            # Initialize PyAudio
            audio = pyaudio.PyAudio()
            
            # Start recording
            stream = audio.open(format=FORMAT, channels=CHANNELS,
                              rate=RATE, input=True,
                              frames_per_buffer=CHUNK)
            
            frames = []
            silence_counter = 0
            recording_started = False
            start_time = datetime.now()
            
            print("🎤 Ready to record...")
            if voice_activated:
                print("🔊 Speak now - recording will start when voice is detected...")
            else:
                print("🔴 Recording started...")
                recording_started = True
            
            while True:
                # Check maximum duration
                elapsed_time = (datetime.now() - start_time).total_seconds()
                if elapsed_time >= duration:
                    print(f"⏰ Maximum duration ({duration}s) reached.")
                    break
                
                # Read audio chunk
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
                
                # Calculate audio energy for voice detection
                audio_data = np.frombuffer(data, dtype=np.int16)
                energy = np.abs(audio_data).mean()
                
                # Voice activation logic
                if voice_activated and not recording_started:
                    if energy > self.recognizer.energy_threshold * 1.5:  # Voice detected
                        print("🔴 Voice detected - recording started!")
                        recording_started = True
                        silence_counter = 0  # Reset silence counter
                        # Keep the frames that led to voice detection
                        continue
                    else:
                        # Remove pre-voice detection frames
                        frames = frames[-10:]  # Keep only recent frames for context
                        continue
                
                # Silence detection for stopping recording
                if recording_started:
                    if energy < self.recognizer.energy_threshold * 0.5:  # Silence detected
                        silence_counter += 1
                        if silence_counter >= int(silence_timeout * RATE / CHUNK):
                            print("🤫 Silence detected - recording stopped.")
                            break
                    else:
                        silence_counter = 0  # Reset silence counter on voice
                        
                        # Provide feedback during recording
                        if len(frames) % int(RATE / CHUNK) == 0:  # Every second
                            elapsed = len(frames) * CHUNK / RATE
                            print(f"⏱️  Recording... {elapsed:.1f}s")
            
            # Stop recording
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
            # Calculate actual recording duration
            actual_duration = len(frames) * CHUNK / RATE
            
            # Save the recorded audio
            with wave.open(output_file, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(audio.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
            
            self.logger.info(f"✅ Audio recorded and saved to: {output_file}")
            self.logger.info(f"📊 Recording stats: {actual_duration:.1f}s duration, {len(frames)} chunks")
            
            return {
                'status': 'success',
                'file_path': output_file,
                'duration': actual_duration,
                'max_duration': duration,
                'silence_timeout': silence_timeout,
                'voice_activated': voice_activated,
                'chunks_recorded': len(frames),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error recording audio: {e}")
            return {
                'status': 'error',
                'error': f'Error recording audio: {e}'
            }
    
    def real_time_speech_to_text(self):
        """
        Perform real-time speech-to-text conversion
        
        Returns:
            generator: Yields transcribed text as it's recognized
        """
        try:
            self.logger.info("🎤 Starting real-time speech recognition...")
            
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
            
            # Listen for speech in real-time
            with self.microphone as source:
                while True:
                    try:
                        # Listen for audio
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                        
                        # Try to recognize speech
                        text = self.recognizer.recognize_google(audio, language='en-US')
                        
                        if text.strip():
                            yield {
                                'status': 'success',
                                'text': text,
                                'timestamp': datetime.now().isoformat()
                            }
                            
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        yield {
                            'status': 'error',
                            'error': f'Speech recognition service error: {e}'
                        }
                        break
                    except KeyboardInterrupt:
                        self.logger.info("🛑 Real-time speech recognition stopped")
                        break
                        
        except Exception as e:
            self.logger.error(f"❌ Error in real-time speech recognition: {e}")
            yield {
                'status': 'error',
                'error': f'Error in real-time speech recognition: {e}'
            }

# Test function
def test_voice_processor():
    """Test the enhanced voice processor functionality"""
    processor = VoiceProcessor()
    
    print("🎤 Testing Enhanced Voice Processor Features")
    print("=" * 50)
    
    # Test 1: Interactive voice chat
    print("\n📝 Test 1: Interactive Voice Chat")
    print("💡 This test will start an interactive voice conversation.")
    print("💬 Speak naturally and the system will respond with voice!")
    print("🛑 Press Ctrl+C to stop the conversation.")
    
    user_input = input("\n🤔 Do you want to start interactive voice chat? (y/n): ").lower().strip()
    
    if user_input == 'y' or user_input == 'yes':
        processor.interactive_voice_chat()
    else:
        print("\n⏭️  Skipping interactive voice chat test.")
    
    # Test 2: Voice-activated recording with response
    print("\n📝 Test 2: Voice-activated recording with response generation")
    print("💡 This test will record your voice and generate a text response.")
    
    user_input = input("\n🤔 Do you want to test voice recording with response? (y/n): ").lower().strip()
    
    if user_input == 'y' or user_input == 'yes':
        print("\n🎙️  Speak now (I'll listen for 10 seconds max)...")
        
        recording_result = processor.record_audio(
            duration=10, 
            silence_timeout=2.0, 
            voice_activated=True
        )
        
        if recording_result['status'] == 'success':
            print(f"✅ Recording successful!")
            print(f"📁 File: {recording_result['file_path']}")
            print(f"⏱️  Duration: {recording_result['duration']:.1f}s")
            print(f"🔊 Voice activated: {recording_result['voice_activated']}")
            
            # Process with response generation
            print("\n🧠 Processing voice and generating response...")
            response_result = processor.process_voice_with_response(recording_result['file_path'])
            
            if response_result['status'] == 'success':
                print(f"✅ Processing successful!")
                print(f"🎤 You said: '{response_result['transcription']['text']}'")
                print(f"🎯 Intent: {response_result['processed_text']['intent']['primary_intent']}")
                print(f"💬 Response: {response_result['response']['response']}")
                print(f"🔊 Voice response: {response_result['voice_response']}")
                
                # Ask if user wants to hear the response
                speak_input = input("\n🤔 Do you want to hear the voice response? (y/n): ").lower().strip()
                if speak_input == 'y' or speak_input == 'yes':
                    processor.speak_response(response_result['voice_response'])
                
            else:
                print(f"❌ Processing failed: {response_result['error']}")
            
            # Clean up
            if os.path.exists(recording_result['file_path']):
                os.remove(recording_result['file_path'])
                print("🧹 Temporary file cleaned up")
        else:
            print(f"❌ Recording failed: {recording_result['error']}")
    else:
        print("\n⏭️  Skipping voice recording test.")
    
    # Test 3: Manual recording (no voice activation)
    print("\n📝 Test 3: Manual recording (5s fixed duration)")
    print("💡 This test will record immediately for 5 seconds.")
    
    user_input = input("\n🤔 Do you want to test manual recording? (y/n): ").lower().strip()
    
    if user_input == 'y' or user_input == 'yes':
        print("\n🎙️  Recording now for 5 seconds...")
        
        recording_result2 = processor.record_audio(
            duration=5, 
            voice_activated=False
        )
        
        if recording_result2['status'] == 'success':
            print(f"✅ Manual recording successful!")
            print(f"📁 File: {recording_result2['file_path']}")
            print(f"⏱️  Duration: {recording_result2['duration']:.1f}s")
            
            # Clean up
            if os.path.exists(recording_result2['file_path']):
                os.remove(recording_result2['file_path'])
                print("🧹 Temporary file cleaned up")
        else:
            print(f"❌ Manual recording failed: {recording_result2['error']}")
    else:
        print("\n⏭️  Skipping manual recording test.")
    
    print("\n🎉 Enhanced voice processor testing complete!")
    print("\n📋 Summary of New Features:")
    print("• ✅ Interactive voice chat with voice responses")
    print("• ✅ Voice-to-text processing with response generation")
    print("• ✅ Text-to-speech functionality")
    print("• ✅ Integration with text processor and response generator")
    print("• ✅ User-friendly interactive testing")
    print("• ✅ Enhanced recording with voice activation and silence detection")

if __name__ == "__main__":
    test_voice_processor()
