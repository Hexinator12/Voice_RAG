#!/usr/bin/env python3

"""
Sample campus data to populate the knowledge base
This demonstrates how to add real campus information to the system
"""

from campus_knowledge_base import CampusKnowledgeBase

def create_sample_campus_data():
    """Create sample campus data for demonstration"""
    
    # Initialize knowledge base
    kb = CampusKnowledgeBase()
    
    # Update campus info
    kb.knowledge_base["campus_info"] = {
        "name": "Tech University",
        "address": "123 University Ave, Tech City, TC 12345",
        "phone": "(555) 123-4567",
        "website": "https://www.techuniversity.edu",
        "description": "A leading technology university focused on innovation and research."
    }
    
    # Add buildings
    kb.add_building({
        "name": "Science & Engineering Building",
        "code": "SEB",
        "address": "456 Innovation Dr",
        "floors": 5,
        "departments": ["Computer Science", "Engineering", "Physics"],
        "services": ["Computer Labs", "Research Labs", "Study Rooms"],
        "hours": "7:00 AM - 10:00 PM (Monday-Friday), 8:00 AM - 6:00 PM (Weekends)",
        "description": "Main building for science and engineering departments with state-of-the-art facilities.",
        "coordinates": {"lat": 40.7128, "lng": -74.0060}
    })
    
    kb.add_building({
        "name": "Student Center",
        "code": "SC",
        "address": "789 Campus Blvd",
        "floors": 3,
        "departments": ["Student Affairs", "Career Services"],
        "services": ["Cafeteria", "Bookstore", "Student Lounge", "Game Room"],
        "hours": "6:00 AM - 11:00 PM (Daily)",
        "description": "Central hub for student activities and services.",
        "coordinates": {"lat": 40.7129, "lng": -74.0061}
    })
    
    # Add events
    from datetime import datetime, timedelta
    
    # Get current date and add days for future events
    current_date = datetime.now()
    
    kb.add_event({
        "title": "Welcome Week Festival",
        "description": "Join us for a week of fun activities to welcome new and returning students!",
        "type": "social",
        "date": (current_date + timedelta(days=7)).strftime("%Y-%m-%d"),
        "time": "12:00 PM - 4:00 PM",
        "location": "Main Quad",
        "building": "Student Center",
        "organizer": "Student Affairs",
        "contact": "studentaffairs@techuniversity.edu",
        "registration_required": False,
        "capacity": 1000,
        "tags": ["welcome", "festival", "social", "new-students"],
        "cost": 0,
        "recurring": False,
        "status": "upcoming"
    })
    
    kb.add_event({
        "title": "Career Fair 2024",
        "description": "Meet with top employers and explore internship and job opportunities.",
        "type": "academic",
        "date": (current_date + timedelta(days=14)).strftime("%Y-%m-%d"),
        "time": "10:00 AM - 3:00 PM",
        "location": "Gymnasium",
        "building": "Recreation Center",
        "organizer": "Career Services",
        "contact": "careers@techuniversity.edu",
        "registration_required": True,
        "capacity": 500,
        "tags": ["career", "jobs", "internships", "networking"],
        "cost": 0,
        "recurring": False,
        "status": "upcoming"
    })
    
    kb.add_event({
        "title": "Hackathon 2024",
        "description": "48-hour coding competition with prizes and networking opportunities.",
        "type": "academic",
        "date": (current_date + timedelta(days=21)).strftime("%Y-%m-%d"),
        "time": "6:00 PM - 6:00 PM (next day)",
        "location": "Computer Labs",
        "building": "Science & Engineering Building",
        "organizer": "Computer Science Club",
        "contact": "hackathon@techuniversity.edu",
        "registration_required": True,
        "capacity": 200,
        "tags": ["programming", "competition", "coding", "technology"],
        "cost": 25,
        "recurring": False,
        "status": "upcoming"
    })
    
    # Add clubs
    kb.add_club({
        "name": "Computer Science Club",
        "description": "A club for students interested in computer science, programming, and technology.",
        "type": "academic",
        "category": "Technology",
        "president": "John Doe",
        "advisor": "Dr. Smith",
        "email": "csclub@techuniversity.edu",
        "meeting_location": "SEB 301",
        "meeting_time": "6:00 PM",
        "meeting_frequency": "Every Thursday",
        "member_count": 45,
        "membership_fee": 20,
        "website": "https://csclub.techuniversity.edu",
        "tags": ["programming", "technology", "coding", "computer-science"],
        "active": True,
        "founded_date": "2020-09-01"
    })
    
    kb.add_club({
        "name": "Photography Club",
        "description": "For photography enthusiasts to share their work and learn new techniques.",
        "type": "arts",
        "category": "Arts & Media",
        "president": "Jane Smith",
        "advisor": "Prof. Johnson",
        "email": "photoclub@techuniversity.edu",
        "meeting_location": "Arts Building 204",
        "meeting_time": "5:00 PM",
        "meeting_frequency": "Every Tuesday",
        "member_count": 30,
        "membership_fee": 15,
        "tags": ["photography", "arts", "media", "creative"],
        "active": True,
        "founded_date": "2019-01-15"
    })
    
    kb.add_club({
        "name": "Basketball Club",
        "description": "Competitive and recreational basketball for all skill levels.",
        "type": "sports",
        "category": "Sports & Recreation",
        "president": "Mike Johnson",
        "advisor": "Coach Williams",
        "email": "basketball@techuniversity.edu",
        "meeting_location": "Gymnasium",
        "meeting_time": "7:00 PM",
        "meeting_frequency": "Every Monday and Wednesday",
        "member_count": 25,
        "membership_fee": 30,
        "tags": ["basketball", "sports", "fitness", "team"],
        "active": True,
        "founded_date": "2018-09-01"
    })
    
    # Add services
    kb.add_service({
        "name": "Library Services",
        "description": "Comprehensive library services including book lending, research assistance, and study spaces.",
        "type": "academic",
        "location": "Main Library",
        "building": "Library Building",
        "hours": "8:00 AM - 10:00 PM (Monday-Friday), 10:00 AM - 6:00 PM (Weekends)",
        "phone": "(555) 123-4568",
        "email": "library@techuniversity.edu",
        "website": "https://library.techuniversity.edu",
        "cost": 0,
        "requirements": ["Student ID"],
        "appointment_required": False,
        "tags": ["library", "study", "research", "books"],
        "available_to": "all"
    })
    
    kb.add_service({
        "name": "Health Center",
        "description": "Medical services and health counseling for students and staff.",
        "type": "health",
        "location": "Health Services Building",
        "building": "Health Services",
        "hours": "9:00 AM - 5:00 PM (Monday-Friday)",
        "phone": "(555) 123-4569",
        "email": "health@techuniversity.edu",
        "cost": 0,
        "requirements": ["Student ID", "Insurance Information"],
        "appointment_required": True,
        "tags": ["health", "medical", "wellness", "counseling"],
        "available_to": "all"
    })
    
    kb.add_service({
        "name": "Career Services",
        "description": "Career counseling, job search assistance, and internship opportunities.",
        "type": "career",
        "location": "Student Center, Room 205",
        "building": "Student Center",
        "hours": "9:00 AM - 5:00 PM (Monday-Friday)",
        "phone": "(555) 123-4570",
        "email": "careers@techuniversity.edu",
        "website": "https://careers.techuniversity.edu",
        "cost": 0,
        "requirements": ["Student ID", "Resume"],
        "appointment_required": True,
        "tags": ["career", "jobs", "internships", "resume"],
        "available_to": "students"
    })
    
    # Save the knowledge base
    kb.save_knowledge_base()
    
    # Print summary
    summary = kb.get_knowledge_summary()
    print("✅ Sample campus data created successfully!")
    print(f"📊 Knowledge Base Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    return kb

if __name__ == "__main__":
    create_sample_campus_data()
