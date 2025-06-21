#!/usr/bin/env python3
"""
Comprehensive API Testing Script for UX/UI Academy Management System
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5001"

def test_endpoint(endpoint, method="GET", data=None, expected_status=200):
    """Test a single API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=5)
        elif method == "PUT":
            response = requests.put(url, json=data, timeout=5)
        elif method == "DELETE":
            response = requests.delete(url, timeout=5)
        
        if response.status_code == expected_status:
            print(f"✅ {method} {endpoint} - OK")
            if response.content:
                try:
                    return response.json()
                except:
                    return response.text
            return None
        else:
            print(f"❌ {method} {endpoint} - Status {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ {method} {endpoint} - Error: {e}")
        return None

def main():
    print("🧪 Starting Comprehensive API Test")
    print("=" * 50)
    
    # Test main page
    print("\n1. Testing Main Page:")
    test_endpoint("/")
    
    # Test Owner Dashboard API
    print("\n2. Testing Owner Dashboard:")
    owner_data = test_endpoint("/api/owner/summary")
    if owner_data:
        print(f"   📊 Charts: {len(owner_data.get('charts', {}))} items")
        print(f"   📚 Courses: {len(owner_data.get('courses', {}))} items")
        print(f"   💰 Financials: {len(owner_data.get('financials', {}))} items")
    
    # Test Content Generator API
    print("\n3. Testing Content Generator:")
    content_data = test_endpoint("/api/content/summary")
    if content_data:
        print(f"   📝 Posts: {content_data.get('total_posts', 0)}")
        print(f"   📅 Scheduled: {content_data.get('scheduled_posts', 0)}")
    
    # Test Telegram Bot APIs
    print("\n4. Testing Telegram Bot:")
    test_endpoint("/api/telegram/scheduled_posts")
    test_endpoint("/api/telegram/main_summary")
    test_endpoint("/api/telegram/stats")
    
    # Test Groups Management API
    print("\n5. Testing Groups Management:")
    groups_data = test_endpoint("/api/telegram/groups")
    if groups_data:
        print(f"   📱 Groups: {len(groups_data)} items")
    
    # Test Courses Management API
    print("\n6. Testing Courses Management:")
    courses_data = test_endpoint("/api/courses")
    if courses_data:
        print(f"   🎓 Courses: {len(courses_data)} items")
    
    # Test Financial Transactions API
    print("\n7. Testing Financial Transactions:")
    transactions_data = test_endpoint("/api/transactions")
    if transactions_data:
        print(f"   💳 Transactions: {len(transactions_data)} items")
    
    # Test Team Management API
    print("\n8. Testing Team Management:")
    team_data = test_endpoint("/api/team")
    if team_data:
        print(f"   👥 Team members: {len(team_data)} items")
    
    # Test Campaigns API
    print("\n9. Testing Campaigns:")
    campaigns_data = test_endpoint("/api/campaigns")
    if campaigns_data:
        print(f"   📢 Campaigns: {len(campaigns_data)} items")
    
    # Test Students API
    print("\n10. Testing Students:")
    students_data = test_endpoint("/api/students")
    if students_data:
        print(f"   👨‍🎓 Students: {len(students_data)} items")
    
    # Test Partners API
    print("\n11. Testing Partners:")
    partners_data = test_endpoint("/api/partners")
    if partners_data:
        print(f"   🤝 Partners: {len(partners_data)} items")
    
    # Test Page Routes
    print("\n12. Testing Page Routes:")
    pages = [
        "/manage-courses",
        "/financial-report", 
        "/manage-team",
        "/manage-campaigns",
        "/student-analytics",
        "/partner-program"
    ]
    
    for page in pages:
        response = requests.get(f"{BASE_URL}{page}", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ {page} - OK")
        else:
            print(f"   ❌ {page} - Status {response.status_code}")
    
    print("\n" + "=" * 50)
    print("🎉 API Testing Complete!")
    print("\nTo test the full UI functionality:")
    print("1. Open http://127.0.0.1:5001/ in your browser")
    print("2. Navigate through all dashboard sections")
    print("3. Test CRUD operations in each module")

if __name__ == "__main__":
    main() 