import random
import json
from datetime import datetime
from typing import Dict, Any, List
import logging
from campus_knowledge_base import CampusKnowledgeBase

class ResponseGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize knowledge base
        self.knowledge_base = CampusKnowledgeBase()
        
        # Response templates for different intents
        self.response_templates = {
            'greeting': {
                'responses': [
                    "Hello! I'm your campus assistant. How can I help you today?",
                    "Hi there! Welcome to the campus assistant. What can I do for you?",
                    "Good day! I'm here to help you with campus-related questions.",
                    "Hey! I'm your virtual campus assistant. Ask me anything!"
                ],
                'follow_up': "Feel free to ask about locations, events, classes, or anything else campus-related."
            },
            
            'time_aware_greeting': {
                'morning': [
                    "Good morning! I'm your campus assistant. How are you doing today?",
                    "Morning! I hope you're having a great start to your day. What can I help you with?",
                    "Good morning! Ready to tackle the day? I'm here to assist with any campus questions.",
                    "Top of the morning to you! How can I make your campus experience better today?"
                ],
                'afternoon': [
                    "Good afternoon! How's your day going so far? I'm here to help with campus questions.",
                    "Afternoon! I hope you're having a productive day. What can I assist you with?",
                    "Good afternoon! Taking a break from classes? I'm here to help with any campus information.",
                    "Hey there! How's your day treating you? I'm your campus assistant, ready to help!"
                ],
                'evening': [
                    "Good evening! How was your day? I'm here to help with any campus questions.",
                    "Evening! Wrapping up your day? I'm here to assist with any campus information you need.",
                    "Good evening! Hope you had a great day. What can I help you with before you call it a day?",
                    "Hey! How's your evening going? I'm your campus assistant, here to help!"
                ]
            },
            
            'library_inquiry': {
                'responses': [
                    "I can help you with library information! The main library is located at the center of campus.",
                    "For library services, you can visit the main campus library or use the online portal.",
                    "The library offers various resources including books, study spaces, and computer labs."
                ],
                'follow_up': "Would you like to know about library hours, specific resources, or study spaces?"
            },
            
            'academic_inquiry': {
                'responses': [
                    "I can assist you with academic questions! What specific information do you need about classes or courses?",
                    "For academic matters, I can help you find information about schedules, professors, or course requirements.",
                    "Academic support is available! Let me know what you're looking for regarding your studies."
                ],
                'follow_up': "Are you looking for class schedules, professor information, or course details?"
            },
            
            'event_inquiry': {
                'responses': [
                    "I can help you find information about campus events! What type of event are you interested in?",
                    "Campus events are happening regularly! Let me help you find what's coming up.",
                    "There's always something happening on campus! What kind of events interest you?"
                ],
                'follow_up': "Are you looking for club meetings, sports events, or academic workshops?"
            },
            
            'dining_inquiry': {
                'responses': [
                    "I can help you with dining options on campus! The main cafeteria serves meals throughout the day.",
                    "Campus dining offers various options including the cafeteria, coffee shops, and food courts.",
                    "Hungry? I can help you find dining options and their hours on campus."
                ],
                'follow_up': "Would you like to know about cafeteria hours, menu options, or other dining locations?"
            },
            
            'help_request': {
                'responses': [
                    "I'm here to help! What do you need assistance with?",
                    "I can definitely help you! Let me know what you're looking for.",
                    "Help is here! What can I assist you with today?",
                    "I'm at your service! What do you need help with?"
                ],
                'follow_up': "You can ask me about campus locations, events, academic information, or general assistance."
            },
            
            'general_inquiry': {
                'responses': [
                    "I'm your campus assistant! I can help you with various campus-related questions.",
                    "I'm here to assist you with campus information. What would you like to know?",
                    "As your campus assistant, I can provide information about locations, events, and services.",
                    "I'm here to help! Ask me anything about campus life and services.",
                    "Happy to help! I'm your go-to assistant for all things campus-related.",
                    "I'm at your service! What campus information can I help you find today?",
                    "Great to connect with you! I'm here to make your campus experience better.",
                    "I'm excited to help! What would you like to explore on campus today?"
                ],
                'follow_up': "Feel free to ask about specific campus locations, events, or services."
            }
        }
        
        # Campus information database (simplified version)
        self.campus_info = {
            'library': {
                'location': 'Main Campus Building A',
                'hours': '8:00 AM - 10:00 PM (Monday-Friday), 10:00 AM - 6:00 PM (Weekends)',
                'services': ['Book lending', 'Study spaces', 'Computer labs', 'Research assistance'],
                'contact': 'library@campus.edu'
            },
            'cafeteria': {
                'location': 'Student Center Building',
                'hours': '7:00 AM - 8:00 PM (Daily)',
                'services': ['Breakfast', 'Lunch', 'Dinner', 'Snacks', 'Vegetarian options'],
                'contact': 'dining@campus.edu'
            },
            'gym': {
                'location': 'Recreation Center',
                'hours': '6:00 AM - 11:00 PM (Daily)',
                'services': ['Fitness equipment', 'Sports courts', 'Swimming pool', 'Group classes'],
                'contact': 'recreation@campus.edu'
            },
            'parking': {
                'locations': ['Main Parking Lot A', 'Student Parking Lot B', 'Faculty Parking Lot C'],
                'hours': '24/7 access',
                'services': ['Student parking', 'Faculty parking', 'Visitor parking', 'Electric vehicle charging'],
                'contact': 'parking@campus.edu'
            }
        }
    
    def generate_response(self, processed_text: Dict[str, Any], input_mode: str = 'text') -> Dict[str, Any]:
        """
        Generate a response based on processed text
        
        Args:
            processed_text (Dict): Processed text information from TextProcessor
            input_mode (str): Input mode ('text' or 'voice')
            
        Returns:
            Dict: Generated response with metadata
        """
        try:
            self.logger.info(f"🤖 Generating response for input: {processed_text.get('clean_input', '')[:50]}...")
            
            # Extract relevant information
            clean_input = processed_text.get('clean_input', '')
            intent = processed_text.get('intent', {})
            input_type = processed_text.get('input_type', 'statement')
            entities = processed_text.get('entities', [])
            
            # Generate response based on intent
            response_data = self.generate_intent_based_response(intent, clean_input, entities)
            
            # Add response metadata
            response_data['metadata'] = {
                'input_mode': input_mode,
                'input_type': input_type,
                'intent_confidence': intent.get('confidence', 0.5),
                'timestamp': datetime.now().isoformat(),
                'response_type': response_data.get('response_type', 'text')
            }
            
            self.logger.info(f"✅ Response generated successfully")
            
            return response_data
            
        except Exception as e:
            self.logger.error(f"❌ Error generating response: {e}")
            return {
                'response': "I apologize, but I'm having trouble generating a response right now. Please try again.",
                'response_type': 'error',
                'metadata': {
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
            }
    
    def generate_intent_based_response(self, intent: Dict[str, Any], clean_input: str, entities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate response based on detected intent"""
        primary_intent = intent.get('primary_intent', 'general_inquiry')
        confidence = intent.get('confidence', 0.5)
        
        # Get current time for dynamic responses
        time_of_day = self.get_time_of_day()
        
        # Check if it's a greeting
        if self.is_greeting(clean_input):
            return self.generate_greeting_response()
        
        # Get response template for the intent
        template = self.response_templates.get(primary_intent, self.response_templates['general_inquiry'])
        
        # Select a random response from the template
        main_response = random.choice(template['responses'])
        
        # Add specific information if available
        specific_info = self.get_specific_information(primary_intent, clean_input, entities)
        
        # Combine main response with specific information
        if specific_info:
            full_response = f"{main_response} {specific_info}"
        else:
            full_response = main_response
        
        # Generate dynamic follow-up based on intent and time
        follow_up = self.generate_dynamic_follow_up(primary_intent, time_of_day)
        
        return {
            'response': full_response,
            'follow_up': follow_up,
            'response_type': 'text',
            'intent': primary_intent,
            'confidence': confidence
        }
    
    def is_greeting(self, text: str) -> bool:
        """Check if the input is a greeting"""
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'greetings']
        return any(greeting in text.lower() for greeting in greetings)
    
    def get_time_of_day(self) -> str:
        """Get the current time of day for appropriate greetings"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 17:
            return 'afternoon'
        else:
            return 'evening'
    
    def generate_greeting_response(self) -> Dict[str, Any]:
        """Generate a time-aware greeting response"""
        time_of_day = self.get_time_of_day()
        
        # Use time-aware greetings if available
        if 'time_aware_greeting' in self.response_templates:
            time_greetings = self.response_templates['time_aware_greeting']
            if time_of_day in time_greetings:
                main_response = random.choice(time_greetings[time_of_day])
            else:
                # Fallback to regular greetings
                template = self.response_templates['greeting']
                main_response = random.choice(template['responses'])
        else:
            # Fallback to regular greetings
            template = self.response_templates['greeting']
            main_response = random.choice(template['responses'])
        
        # Generate dynamic follow-up based on intent and time
        follow_up = self.generate_dynamic_follow_up('greeting', time_of_day)
        
        return {
            'response': main_response,
            'follow_up': follow_up,
            'response_type': 'text',
            'intent': 'greeting',
            'confidence': 0.95
        }
    
    def get_specific_information(self, intent: str, clean_input: str, entities: List[Dict[str, Any]]) -> str:
        """Get specific information based on intent and entities using knowledge base"""
        specific_info = ""
        
        if intent == 'library_inquiry':
            services = self.knowledge_base.search_services("library")
            if services:
                service = services[0]
                specific_info = f"The {service['name']} is located at {service['location']} and is open {service['hours']}. Services include: {', '.join(service.get('tags', [])[:3])}."
        
        elif intent == 'dining_inquiry':
            services = self.knowledge_base.search_services("cafeteria")
            if services:
                service = services[0]
                specific_info = f"The main {service['name']} is at {service['location']} and serves meals {service['hours']}."
            else:
                # Check buildings for dining services
                for building_id, building in self.knowledge_base.knowledge_base['buildings'].items():
                    if 'cafeteria' in building.get('services', []):
                        specific_info = f"The cafeteria is located in the {building['name']} at {building['address']} and is open {building['hours']}."
                        break
        
        elif intent == 'academic_inquiry':
            if any(word in clean_input for word in ['schedule', 'time', 'when']):
                specific_info = "You can check your class schedule through the student portal or mobile app."
            elif any(word in clean_input for word in ['professor', 'teacher']):
                specific_info = "Professor information is available in the course catalog or department websites."
            elif any(word in clean_input for word in ['course', 'class']):
                specific_info = "Course information is available through the registrar's office or online course catalog."
        
        elif intent == 'event_inquiry':
            # Search for upcoming events
            events = self.knowledge_base.get_upcoming_events(30)
            if events:
                if len(events) == 1:
                    event = events[0]
                    specific_info = f"Upcoming event: {event['title']} on {event['date']} at {event['time']} in {event['location']}."
                else:
                    event_list = ', '.join([f"{event['title']} ({event['date']})" for event in events[:3]])
                    specific_info = f"Upcoming events include: {event_list}. There are {len(events)} total events coming up."
            else:
                specific_info = "I don't see any upcoming events in the next 30 days. Check the campus events calendar for the latest updates."
        
        elif intent == 'help_request':
            specific_info = "I can help you with campus locations, events, academic information, and general assistance."
        
        return specific_info
    
    def generate_dynamic_follow_up(self, intent: str, time_of_day: str) -> str:
        """Generate dynamic follow-up responses based on intent and time"""
        follow_up_options = {
            'greeting': {
                'morning': ["Ready to start your day? I can help with classes, breakfast spots, or morning events!",
                           "Need help finding your first class? I'm here to guide you!",
                           "Looking for a good study spot this morning? I can suggest some great places!"],
                'afternoon': ["Need a break or help with afternoon activities? I'm here for campus info and assistance!",
                             "How are your classes going? I can help with any questions you might have!",
                             "Looking for lunch spots or study areas? I've got you covered!"],
                'evening': ["Wrapping up your day? I can help with evening events, dining, or study spaces!",
                           "Need help with homework or finding a quiet place to study? I'm here to help!",
                           "Looking for dinner options or evening activities? Let me assist you!"]
            },
            'general_inquiry': {
                'morning': ["What would you like to know about campus this morning?", 
                           "I can help you find classrooms, dining halls, or morning events!",
                           "What's on your mind for today's campus activities?"],
                'afternoon': ["What campus information can I help you find this afternoon?",
                             "Need help with afternoon campus activities or services?",
                             "What would you like to explore on campus this afternoon?"],
                'evening': ["What can I help you with as you wrap up your day?",
                           "Looking for evening campus information or services?",
                           "What campus questions do you have this evening?"]
            },
            'library_inquiry': {
                'morning': ["Would you like to know about library hours, study spaces, or morning availability?",
                           "Need help finding books or quiet study spots this morning?",
                           "Looking for group study areas or research assistance this morning?"],
                'afternoon': ["Would you like to know about library hours, specific resources, or study spaces?",
                             "Need help finding research materials or quiet study areas this afternoon?",
                             "Looking for computer labs or group study rooms this afternoon?"],
                'evening': ["Would you like to know about evening library hours or late-night study spaces?",
                           "Need help finding 24/7 study areas or evening library services?",
                           "Looking for quiet study spots or research assistance this evening?"]
            }
        }
        
        # Get intent-specific follow-ups, fallback to general inquiry
        intent_follow_ups = follow_up_options.get(intent, follow_up_options.get('general_inquiry', {}))
        
        # Get time-specific follow-ups, fallback to any time
        time_follow_ups = intent_follow_ups.get(time_of_day, list(intent_follow_ups.values())[0] if intent_follow_ups else [])
        
        if time_follow_ups:
            return random.choice(time_follow_ups)
        else:
            # Ultimate fallback
            return "Feel free to ask about specific campus locations, events, or services."
    
    def generate_error_response(self, error_message: str) -> Dict[str, Any]:
        """Generate an error response"""
        return {
            'response': "I apologize, but I encountered an error while processing your request. Please try again or contact support if the issue persists.",
            'response_type': 'error',
            'error': error_message,
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_fallback_response(self) -> Dict[str, Any]:
        """Generate a fallback response when intent is unclear"""
        fallback_responses = [
            "I'm not sure I understand. Could you please rephrase your question?",
            "I'm still learning! Could you try asking in a different way?",
            "I didn't quite catch that. Could you provide more details?",
            "I want to help, but I need more information. Could you be more specific?"
        ]
        
        return {
            'response': random.choice(fallback_responses),
            'response_type': 'fallback',
            'intent': 'unknown',
            'confidence': 0.1
        }
    
    def format_response_for_voice(self, response_data: Dict[str, Any]) -> str:
        """Format response for voice output"""
        response_text = response_data.get('response', '')
        follow_up = response_data.get('follow_up', '')
        
        # Combine response and follow-up for voice
        if follow_up:
            voice_response = f"{response_text} {follow_up}"
        else:
            voice_response = response_text
        
        # Clean up for better speech synthesis
        voice_response = self.clean_text_for_voice(voice_response)
        
        return voice_response
    
    def clean_text_for_voice(self, text: str) -> str:
        """Clean text for better voice synthesis"""
        # Replace abbreviations with full words
        replacements = {
            'AM': 'A M',
            'PM': 'P M',
            'etc.': 'et cetera',
            'e.g.': 'for example',
            'i.e.': 'that is'
        }
        
        for abbr, full in replacements.items():
            text = text.replace(abbr, full)
        
        # Add pauses for better readability
        text = text.replace('.', '. ')
        text = text.replace(',', ', ')
        
        return text.strip()

# Test function
def test_response_generator():
    """Test the response generator functionality"""
    generator = ResponseGenerator()
    
    # Test cases
    test_cases = [
        {
            'clean_input': 'hello',
            'intent': {'primary_intent': 'greeting', 'confidence': 0.9},
            'input_type': 'statement',
            'entities': []
        },
        {
            'clean_input': 'where is the library',
            'intent': {'primary_intent': 'library_inquiry', 'confidence': 0.8},
            'input_type': 'question',
            'entities': []
        },
        {
            'clean_input': 'what time does the cafeteria close',
            'intent': {'primary_intent': 'dining_inquiry', 'confidence': 0.7},
            'input_type': 'question',
            'entities': []
        },
        {
            'clean_input': 'help me find my classroom',
            'intent': {'primary_intent': 'help_request', 'confidence': 0.9},
            'input_type': 'command',
            'entities': []
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n🤖 Test Case {i+1}: '{test_case['clean_input']}'")
        response = generator.generate_response(test_case)
        
        print(f"✅ Response: {response['response']}")
        print(f"✅ Follow-up: {response.get('follow_up', 'None')}")
        print(f"✅ Intent: {response['intent']}")
        print(f"✅ Confidence: {response['confidence']}")

if __name__ == "__main__":
    test_response_generator()
