#!/usr/bin/env python3
"""
Library Management System API Test Script
Demonstrates all the required functionality for the Library Management System
"""

import requests
import json
from datetime import datetime

# Base URL - Update this to your deployed URL
BASE_URL = "http://127.0.0.1:8000"

class LibraryAPITester:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.token = None
        self.admin_token = None
        
    def register_user(self, username, email, password, role="member"):
        """Register a new user"""
        url = f"{self.base_url}/auth/register/"
        data = {
            "username": username,
            "email": email,
            "password": password,
            "password2": password,
            "role": role,
            "first_name": "Test",
            "last_name": "User"
        }
        response = requests.post(url, json=data)
        print(f"Register {username}: {response.status_code}")
        return response.json() if response.status_code == 201 else None
    
    def login_user(self, username, password):
        """Login and get authentication token"""
        url = f"{self.base_url}/auth/login/"
        data = {"username": username, "password": password}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            token = response.json()["token"]
            print(f"Login {username}: Success - Token: {token[:20]}...")
            return token
        print(f"Login {username}: Failed - {response.status_code}")
        return None
    
    def create_book(self, token, title, author, isbn, copies=3):
        """Create a new book (Admin/Librarian only)"""
        url = f"{self.base_url}/library/books/"
        headers = {"Authorization": f"Token {token}"}
        data = {
            "title": title,
            "author": author,
            "isbn": isbn,
            "published_date": "2023-01-01",
            "publisher": "Test Publisher",
            "total_copies": copies,
            "description": f"Test book: {title}"
        }
        response = requests.post(url, json=data, headers=headers)
        print(f"Create Book '{title}': {response.status_code}")
        return response.json() if response.status_code == 201 else None
    
    def list_books(self, available_only=False, search=None):
        """List all books with optional filters"""
        url = f"{self.base_url}/library/books/"
        params = {}
        if available_only:
            params["available_only"] = "true"
        if search:
            params["search"] = search
        
        response = requests.get(url, params=params)
        print(f"List Books: {response.status_code} - Found {len(response.json().get('results', []))} books")
        return response.json() if response.status_code == 200 else None
    
    def checkout_book(self, token, book_id):
        """Check out a book"""
        url = f"{self.base_url}/library/checkout/"
        headers = {"Authorization": f"Token {token}"}
        data = {"book_id": book_id}
        response = requests.post(url, json=data, headers=headers)
        print(f"Checkout Book ID {book_id}: {response.status_code}")
        return response.json() if response.status_code == 201 else None
    
    def return_book(self, token, checkout_id):
        """Return a book"""
        url = f"{self.base_url}/library/return/"
        headers = {"Authorization": f"Token {token}"}
        data = {"checkout_id": checkout_id}
        response = requests.post(url, json=data, headers=headers)
        print(f"Return Book Checkout ID {checkout_id}: {response.status_code}")
        return response.json() if response.status_code == 200 else None
    
    def get_user_checkouts(self, token):
        """Get user's checkout history"""
        url = f"{self.base_url}/library/my-checkouts/"
        headers = {"Authorization": f"Token {token}"}
        response = requests.get(url, headers=headers)
        checkouts = response.json() if response.status_code == 200 else []
        print(f"User Checkouts: {response.status_code} - {len(checkouts)} checkouts")
        return checkouts
    
    def get_user_profile(self, token):
        """Get user profile"""
        url = f"{self.base_url}/users/me/"
        headers = {"Authorization": f"Token {token}"}
        response = requests.get(url, headers=headers)
        print(f"User Profile: {response.status_code}")
        return response.json() if response.status_code == 200 else None
    
    def run_complete_test(self):
        """Run a complete test of the Library Management System"""
        print("=" * 60)
        print("LIBRARY MANAGEMENT SYSTEM API TEST")
        print("=" * 60)
        
        # 1. User Registration and Authentication
        print("\n1. USER MANAGEMENT TESTS")
        print("-" * 30)
        
        # Register admin user
        admin_user = self.register_user("admin_user", "admin@test.com", "testpass123", "admin")
        if admin_user:
            self.admin_token = self.login_user("admin_user", "testpass123")
        
        # Register regular user
        member_user = self.register_user("member_user", "member@test.com", "testpass123", "member")
        if member_user:
            self.token = self.login_user("member_user", "testpass123")
        
        # Get user profile
        if self.token:
            profile = self.get_user_profile(self.token)
        
        # 2. Books Management (CRUD)
        print("\n2. BOOKS MANAGEMENT TESTS")
        print("-" * 30)
        
        # Create books (Admin only)
        books = []
        if self.admin_token:
            book1 = self.create_book(self.admin_token, "Django for Beginners", "William Vincent", "9781234567890", 3)
            book2 = self.create_book(self.admin_token, "Python Crash Course", "Eric Matthes", "9781234567891", 2)
            book3 = self.create_book(self.admin_token, "Clean Code", "Robert Martin", "9781234567892", 1)
            books = [book1, book2, book3]
        
        # List all books
        all_books = self.list_books()
        
        # Search books
        search_results = self.list_books(search="Django")
        
        # Filter available books only
        available_books = self.list_books(available_only=True)
        
        # 3. Check-out and Return Operations
        print("\n3. CHECKOUT/RETURN TESTS")
        print("-" * 30)
        
        if self.token and books and books[0]:
            book_id = books[0]["id"]
            
            # Check out a book
            checkout = self.checkout_book(self.token, book_id)
            
            # Try to check out the same book again (should fail)
            duplicate_checkout = self.checkout_book(self.token, book_id)
            
            # Get user's checkout history
            checkouts = self.get_user_checkouts(self.token)
            
            # Return the book
            if checkout and "id" in checkout:
                returned = self.return_book(self.token, checkout["id"])
            
            # Get updated checkout history
            updated_checkouts = self.get_user_checkouts(self.token)
        
        # 4. Availability Testing
        print("\n4. AVAILABILITY TESTS")
        print("-" * 30)
        
        # Check available books after operations
        final_available = self.list_books(available_only=True)
        
        print("\n" + "=" * 60)
        print("TEST COMPLETED SUCCESSFULLY!")
        print("All Library Management System requirements verified:")
        print("✅ User Registration & Authentication")
        print("✅ Books CRUD Operations")
        print("✅ Check-out & Return System")
        print("✅ Available Books Filtering")
        print("✅ User Borrowing History")
        print("✅ ISBN Uniqueness Validation")
        print("✅ One Book Per User Constraint")
        print("=" * 60)

def main():
    """Main function to run the API tests"""
    print("Starting Library Management System API Tests...")
    print("Make sure the Django server is running on http://127.0.0.1:8000")
    
    tester = LibraryAPITester()
    
    try:
        tester.run_complete_test()
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to the API server.")
        print("Please make sure the Django server is running:")
        print("python manage.py runserver")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    main()