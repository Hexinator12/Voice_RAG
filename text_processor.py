import re
import string
from typing import Dict, List, Any
from datetime import datetime
import logging
from langdetect import detect
from googletrans import Translator

class TextProcessor:
    def __init__(self):
        self.translator = Translator()
        self.logger = logging.getLogger(__name__)
        
        # Common campus-related keywords for context detection
        self.campus_keywords = [
            'library', 'classroom', 'professor', 'lecture', 'exam', 'assignment',
            'campus', 'dorm', 'cafeteria', 'gym', 'parking', 'registration',
            'course', 'schedule', 'deadline', 'grade', 'tuition', 'scholarship',
            'event', 'club', 'sports', 'laboratory', 'office', 'department'
        ]
        
        # Question patterns
        self.question_patterns = [
            r'^\b(what|where|when|why|how|who|which|can|could|would|should|is|are|do|does|did)\b',
            r'\?$'
        ]
        
        # Command patterns
        self.command_patterns = [
            r'^\b(find|search|look for|show me|tell me|help me|calculate|convert)\b',
            r'^\b(open|close|start|stop|pause|resume)\b'
        ]
    
    def process_text(self, text: str) -> Dict[str, Any]:
        """
        Process input text and extract meaningful information
        
        Args:
            text (str): Input text to process
            
        Returns:
            Dict: Processed text information
        """
        try:
            self.logger.info(f"📝 Processing text: '{text[:100]}...'")
            
            # Basic text cleaning
            cleaned_text = self.clean_text(text)
            
            # Detect language
            language = self.detect_language(cleaned_text)
            
            # If not English, translate to English
            if language != 'en':
                translated_text = self.translate_text(cleaned_text, target_lang='en')
            else:
                translated_text = cleaned_text
            
            # Extract text features
            text_features = self.extract_text_features(translated_text)
            
            # Classify input type
            input_type = self.classify_input_type(translated_text)
            
            # Extract entities (simple version)
            entities = self.extract_entities(translated_text)
            
            # Determine intent
            intent = self.determine_intent(translated_text, input_type)
            
            self.logger.info(f"✅ Text processing complete")
            
            return {
                'original_text': text,
                'cleaned_text': cleaned_text,
                'detected_language': language,
                'translated_text': translated_text,
                'features': text_features,
                'input_type': input_type,
                'entities': entities,
                'intent': intent,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error processing text: {e}")
            return {
                'error': f'Error processing text: {e}',
                'status': 'error'
            }
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\?\!\,\;\:\-\'\"]', '', text)
        
        # Convert to lowercase for processing
        text = text.lower()
        
        return text.strip()
    
    def detect_language(self, text: str) -> str:
        """Detect the language of the text"""
        try:
            if len(text) < 3:
                return 'en'  # Default to English for very short texts
            
            detected_lang = detect(text)
            return detected_lang
            
        except Exception as e:
            self.logger.warning(f"⚠️ Language detection failed: {e}")
            return 'en'  # Default to English
    
    def translate_text(self, text: str, target_lang: str = 'en') -> str:
        """Translate text to target language"""
        try:
            if len(text) < 1:
                return text
            
            translation = self.translator.translate(text, dest=target_lang)
            return translation.text
            
        except Exception as e:
            self.logger.warning(f"⚠️ Translation failed: {e}")
            return text  # Return original text if translation fails
    
    def extract_text_features(self, text: str) -> Dict[str, Any]:
        """Extract various features from the text"""
        features = {
            'length': len(text),
            'word_count': len(text.split()),
            'sentence_count': len(re.split(r'[.!?]+', text)),
            'has_campus_keywords': any(keyword in text for keyword in self.campus_keywords),
            'campus_keywords_found': [kw for kw in self.campus_keywords if kw in text],
            'has_numbers': bool(re.search(r'\d+', text)),
            'has_question_marks': '?' in text,
            'has_exclamation': '!' in text,
            'is_uppercase': text.isupper(),
            'is_lowercase': text.islower()
        }
        
        return features
    
    def classify_input_type(self, text: str) -> str:
        """Classify the type of input (question, command, statement)"""
        # Check for question patterns
        for pattern in self.question_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return 'question'
        
        # Check for command patterns
        for pattern in self.command_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return 'command'
        
        # Default to statement
        return 'statement'
    
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract entities from text (simple version)"""
        entities = []
        
        # Extract numbers
        numbers = re.findall(r'\b\d+(?:\.\d+)?\b', text)
        for num in numbers:
            entities.append({
                'type': 'number',
                'value': num,
                'context': 'numeric_value'
            })
        
        # Extract potential dates (simple pattern)
        dates = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text)
        for date in dates:
            entities.append({
                'type': 'date',
                'value': date,
                'context': 'date_reference'
            })
        
        # Extract potential times
        times = re.findall(r'\b\d{1,2}:\d{2}\s*(?:am|pm|AM|PM)?\b', text)
        for time in times:
            entities.append({
                'type': 'time',
                'value': time,
                'context': 'time_reference'
            })
        
        return entities
    
    def determine_intent(self, text: str, input_type: str) -> Dict[str, Any]:
        """Determine the user's intent"""
        intent = {
            'primary_intent': 'general_inquiry',
            'confidence': 0.5,
            'sub_intents': [],
            'context': 'campus_assistant'
        }
        
        # Campus-related intents
        if any(keyword in text for keyword in ['library', 'book', 'study']):
            intent['primary_intent'] = 'library_inquiry'
            intent['confidence'] = 0.8
            intent['sub_intents'] = ['location', 'resources']
        
        elif any(keyword in text for keyword in ['class', 'course', 'lecture', 'professor']):
            intent['primary_intent'] = 'academic_inquiry'
            intent['confidence'] = 0.8
            intent['sub_intents'] = ['schedule', 'information']
        
        elif any(keyword in text for keyword in ['event', 'club', 'activity']):
            intent['primary_intent'] = 'event_inquiry'
            intent['confidence'] = 0.7
            intent['sub_intents'] = ['schedule', 'participation']
        
        elif any(keyword in text for keyword in ['food', 'cafeteria', 'dining']):
            intent['primary_intent'] = 'dining_inquiry'
            intent['confidence'] = 0.7
            intent['sub_intents'] = ['location', 'hours']
        
        elif any(keyword in text for keyword in ['help', 'assist', 'support']):
            intent['primary_intent'] = 'help_request'
            intent['confidence'] = 0.9
            intent['sub_intents'] = ['general_support']
        
        # Adjust confidence based on input type
        if input_type == 'question':
            intent['confidence'] = min(intent['confidence'] + 0.1, 1.0)
        elif input_type == 'command':
            intent['confidence'] = min(intent['confidence'] + 0.05, 1.0)
        
        return intent
    
    def format_response_context(self, processed_text: Dict[str, Any]) -> Dict[str, Any]:
        """Format processed text for response generation"""
        return {
            'clean_input': processed_text['translated_text'],
            'input_type': processed_text['input_type'],
            'intent': processed_text['intent'],
            'entities': processed_text['entities'],
            'features': processed_text['features'],
            'language': processed_text['detected_language']
        }

# Test function
def test_text_processor():
    """Test the text processor functionality"""
    processor = TextProcessor()
    
    test_texts = [
        "Where is the library located?",
        "What time does the cafeteria close?",
        "Help me find my classroom",
        "Show me today's events",
        "Bonjour, comment ça va?"  # French test
    ]
    
    for text in test_texts:
        print(f"\n📝 Testing: '{text}'")
        result = processor.process_text(text)
        
        if 'error' not in result:
            print(f"✅ Language: {result['detected_language']}")
            print(f"✅ Translated: {result['translated_text']}")
            print(f"✅ Type: {result['input_type']}")
            print(f"✅ Intent: {result['intent']['primary_intent']}")
            print(f"✅ Entities: {len(result['entities'])} found")
        else:
            print(f"❌ Error: {result['error']}")

if __name__ == "__main__":
    test_text_processor()
