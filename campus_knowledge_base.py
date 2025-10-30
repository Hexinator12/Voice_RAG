#!/usr/bin/env python3

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import logging

class CampusKnowledgeBase:
    """
    A comprehensive knowledge base for storing and retrieving campus information
    """
    
    def __init__(self, knowledge_file: str = "campus_knowledge.json"):
        self.logger = logging.getLogger(__name__)
        self.knowledge_file = knowledge_file
        self.knowledge_base = self._load_knowledge_base()
        
    def _load_knowledge_base(self) -> Dict[str, Any]:
        """Load knowledge base from file or create default structure"""
        if os.path.exists(self.knowledge_file):
            try:
                with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading knowledge base: {e}")
                return self._create_default_structure()
        else:
            return self._create_default_structure()
    
    def _create_default_structure(self) -> Dict[str, Any]:
        """Create default knowledge base structure"""
        return {
            "campus_info": {
                "name": "Your Campus",
                "address": "",
                "phone": "",
                "website": "",
                "description": ""
            },
            "buildings": {},
            "departments": {},
            "services": {},
            "events": {},
            "clubs": {},
            "courses": {},
            "faculty": {},
            "staff": {},
            "policies": {},
            "faqs": {},
            "last_updated": datetime.now().isoformat()
        }
    
    def save_knowledge_base(self):
        """Save knowledge base to file"""
        try:
            self.knowledge_base["last_updated"] = datetime.now().isoformat()
            with open(self.knowledge_file, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)
            self.logger.info(f"✅ Knowledge base saved to {self.knowledge_file}")
        except Exception as e:
            self.logger.error(f"❌ Error saving knowledge base: {e}")
    
    def add_building(self, building_data: Dict[str, Any]):
        """Add or update building information"""
        building_id = building_data.get("id", building_data.get("name", "").lower().replace(" ", "_"))
        self.knowledge_base["buildings"][building_id] = {
            "name": building_data.get("name", ""),
            "code": building_data.get("code", ""),
            "address": building_data.get("address", ""),
            "floors": building_data.get("floors", 0),
            "departments": building_data.get("departments", []),
            "services": building_data.get("services", []),
            "hours": building_data.get("hours", ""),
            "description": building_data.get("description", ""),
            "image_url": building_data.get("image_url", ""),
            "coordinates": building_data.get("coordinates", {}),
            "accessibility": building_data.get("accessibility", {}),
            "last_updated": datetime.now().isoformat()
        }
        self.save_knowledge_base()
    
    def add_event(self, event_data: Dict[str, Any]):
        """Add or update event information"""
        event_id = event_data.get("id", event_data.get("title", "").lower().replace(" ", "_"))
        self.knowledge_base["events"][event_id] = {
            "title": event_data.get("title", ""),
            "description": event_data.get("description", ""),
            "type": event_data.get("type", "general"),
            "date": event_data.get("date", ""),
            "time": event_data.get("time", ""),
            "location": event_data.get("location", ""),
            "building": event_data.get("building", ""),
            "room": event_data.get("room", ""),
            "organizer": event_data.get("organizer", ""),
            "contact": event_data.get("contact", ""),
            "registration_required": event_data.get("registration_required", False),
            "capacity": event_data.get("capacity", 0),
            "attendees": event_data.get("attendees", 0),
            "tags": event_data.get("tags", []),
            "image_url": event_data.get("image_url", ""),
            "cost": event_data.get("cost", 0),
            "recurring": event_data.get("recurring", False),
            "recurring_pattern": event_data.get("recurring_pattern", ""),
            "status": event_data.get("status", "upcoming"),
            "last_updated": datetime.now().isoformat()
        }
        self.save_knowledge_base()
    
    def add_club(self, club_data: Dict[str, Any]):
        """Add or update club information"""
        club_id = club_data.get("id", club_data.get("name", "").lower().replace(" ", "_"))
        self.knowledge_base["clubs"][club_id] = {
            "name": club_data.get("name", ""),
            "description": club_data.get("description", ""),
            "type": club_data.get("type", "general"),
            "category": club_data.get("category", ""),
            "president": club_data.get("president", ""),
            "advisor": club_data.get("advisor", ""),
            "email": club_data.get("email", ""),
            "phone": club_data.get("phone", ""),
            "meeting_location": club_data.get("meeting_location", ""),
            "meeting_time": club_data.get("meeting_time", ""),
            "meeting_frequency": club_data.get("meeting_frequency", ""),
            "member_count": club_data.get("member_count", 0),
            "membership_fee": club_data.get("membership_fee", 0),
            "website": club_data.get("website", ""),
            "social_media": club_data.get("social_media", {}),
            "tags": club_data.get("tags", []),
            "image_url": club_data.get("image_url", ""),
            "active": club_data.get("active", True),
            "founded_date": club_data.get("founded_date", ""),
            "last_updated": datetime.now().isoformat()
        }
        self.save_knowledge_base()
    
    def add_service(self, service_data: Dict[str, Any]):
        """Add or update service information"""
        service_id = service_data.get("id", service_data.get("name", "").lower().replace(" ", "_"))
        self.knowledge_base["services"][service_id] = {
            "name": service_data.get("name", ""),
            "description": service_data.get("description", ""),
            "type": service_data.get("type", "general"),
            "location": service_data.get("location", ""),
            "building": service_data.get("building", ""),
            "hours": service_data.get("hours", ""),
            "phone": service_data.get("phone", ""),
            "email": service_data.get("email", ""),
            "website": service_data.get("website", ""),
            "cost": service_data.get("cost", 0),
            "requirements": service_data.get("requirements", []),
            "providers": service_data.get("providers", []),
            "appointment_required": service_data.get("appointment_required", False),
            "accessibility": service_data.get("accessibility", {}),
            "tags": service_data.get("tags", []),
            "image_url": service_data.get("image_url", ""),
            "available_to": service_data.get("available_to", "all"),
            "last_updated": datetime.now().isoformat()
        }
        self.save_knowledge_base()
    
    def search_events(self, query: str = "", event_type: str = "", date_range: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
        """Search for events based on query, type, and date range"""
        events = []
        current_date = datetime.now().date()
        
        for event_id, event in self.knowledge_base["events"].items():
            # Filter by query
            if query and query.lower() not in event["title"].lower() and query.lower() not in event["description"].lower():
                continue
            
            # Filter by type
            if event_type and event["type"] != event_type:
                continue
            
            # Filter by date range
            if date_range:
                event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
                start_date = datetime.strptime(date_range.get("start", ""), "%Y-%m-%d").date() if date_range.get("start") else current_date
                end_date = datetime.strptime(date_range.get("end", ""), "%Y-%m-%d").date() if date_range.get("end") else current_date + timedelta(days=30)
                
                if not (start_date <= event_date <= end_date):
                    continue
            
            # Only include upcoming events by default
            if event["status"] == "upcoming":
                events.append(event)
        
        # Sort by date
        events.sort(key=lambda x: x["date"])
        return events
    
    def search_clubs(self, query: str = "", category: str = "", active_only: bool = True) -> List[Dict[str, Any]]:
        """Search for clubs based on query and category"""
        clubs = []
        
        for club_id, club in self.knowledge_base["clubs"].items():
            # Filter by active status
            if active_only and not club["active"]:
                continue
            
            # Filter by query
            if query and query.lower() not in club["name"].lower() and query.lower() not in club["description"].lower():
                continue
            
            # Filter by category
            if category and club["category"] != category:
                continue
            
            clubs.append(club)
        
        # Sort by member count
        clubs.sort(key=lambda x: x["member_count"], reverse=True)
        return clubs
    
    def search_services(self, query: str = "", service_type: str = "", available_to: str = "all") -> List[Dict[str, Any]]:
        """Search for services based on query and type"""
        services = []
        
        for service_id, service in self.knowledge_base["services"].items():
            # Filter by availability
            if available_to != "all" and service["available_to"] != available_to and service["available_to"] != "all":
                continue
            
            # Filter by query
            if query and query.lower() not in service["name"].lower() and query.lower() not in service["description"].lower():
                continue
            
            # Filter by type
            if service_type and service["type"] != service_type:
                continue
            
            services.append(service)
        
        return services
    
    def get_upcoming_events(self, days_ahead: int = 30) -> List[Dict[str, Any]]:
        """Get upcoming events within the specified number of days"""
        current_date = datetime.now().date()
        end_date = current_date + timedelta(days=days_ahead)
        
        date_range = {
            "start": current_date.strftime("%Y-%m-%d"),
            "end": end_date.strftime("%Y-%m-%d")
        }
        
        return self.search_events(date_range=date_range)
    
    def get_event_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get event by ID"""
        return self.knowledge_base["events"].get(event_id)
    
    def get_club_by_id(self, club_id: str) -> Optional[Dict[str, Any]]:
        """Get club by ID"""
        return self.knowledge_base["clubs"].get(club_id)
    
    def get_service_by_id(self, service_id: str) -> Optional[Dict[str, Any]]:
        """Get service by ID"""
        return self.knowledge_base["services"].get(service_id)
    
    def get_knowledge_summary(self) -> Dict[str, Any]:
        """Get a summary of the knowledge base"""
        return {
            "total_buildings": len(self.knowledge_base["buildings"]),
            "total_departments": len(self.knowledge_base["departments"]),
            "total_services": len(self.knowledge_base["services"]),
            "total_events": len(self.knowledge_base["events"]),
            "total_clubs": len(self.knowledge_base["clubs"]),
            "total_courses": len(self.knowledge_base["courses"]),
            "total_faculty": len(self.knowledge_base["faculty"]),
            "total_staff": len(self.knowledge_base["staff"]),
            "total_policies": len(self.knowledge_base["policies"]),
            "total_faqs": len(self.knowledge_base["faqs"]),
            "last_updated": self.knowledge_base["last_updated"]
        }
    
    def export_knowledge_base(self, filename: str = None):
        """Export knowledge base to a file"""
        if not filename:
            filename = f"campus_knowledge_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)
            self.logger.info(f"✅ Knowledge base exported to {filename}")
            return filename
        except Exception as e:
            self.logger.error(f"❌ Error exporting knowledge base: {e}")
            return None
    
    def import_knowledge_base(self, filename: str):
        """Import knowledge base from a file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)
            
            # Merge with existing knowledge base
            for key, value in imported_data.items():
                if key in self.knowledge_base and isinstance(self.knowledge_base[key], dict) and isinstance(value, dict):
                    self.knowledge_base[key].update(value)
                else:
                    self.knowledge_base[key] = value
            
            self.save_knowledge_base()
            self.logger.info(f"✅ Knowledge base imported from {filename}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Error importing knowledge base: {e}")
            return False
