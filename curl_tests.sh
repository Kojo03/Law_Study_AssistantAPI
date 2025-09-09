#!/bin/bash
# Library Management System API - Curl Test Commands
# Make sure Django server is running: python manage.py runserver

BASE_URL="http://127.0.0.1:8000"

echo "=== LIBRARY MANAGEMENT SYSTEM API TESTS ==="

# 1. Register Admin User
echo -e "\n1. Register Admin User"
curl -X POST $BASE_URL/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin1",
    "email": "admin@test.com",
    "password": "testpass123",
    "password2": "testpass123",
    "role": "admin"
  }'

# 2. Register Member User
echo -e "\n\n2. Register Member User"
curl -X POST $BASE_URL/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "member1",
    "email": "member@test.com",
    "password": "testpass123",
    "password2": "testpass123",
    "role": "member"
  }'

# 3. Login Admin (Save token for next commands)
echo -e "\n\n3. Login Admin"
ADMIN_TOKEN=$(curl -s -X POST $BASE_URL/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin1", "password": "testpass123"}' | \
  python3 -c "import sys, json; print(json.load(sys.stdin)['token'])" 2>/dev/null)
echo "Admin Token: $ADMIN_TOKEN"

# 4. Login Member (Save token for next commands)
echo -e "\n\n4. Login Member"
MEMBER_TOKEN=$(curl -s -X POST $BASE_URL/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "member1", "password": "testpass123"}' | \
  python3 -c "import sys, json; print(json.load(sys.stdin)['token'])" 2>/dev/null)
echo "Member Token: $MEMBER_TOKEN"

# 5. Create Books (Admin only)
echo -e "\n\n5. Create Books (Admin)"
BOOK1_ID=$(curl -s -X POST $BASE_URL/library/books/ \
  -H "Authorization: Token $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Django for Beginners",
    "author": "William Vincent",
    "isbn": "9781234567890",
    "published_date": "2023-01-01",
    "publisher": "Test Publisher",
    "total_copies": 3,
    "description": "Learn Django web development"
  }' | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)
echo "Created Book ID: $BOOK1_ID"

curl -s -X POST $BASE_URL/library/books/ \
  -H "Authorization: Token $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Crash Course",
    "author": "Eric Matthes",
    "isbn": "9781234567891",
    "published_date": "2023-02-01",
    "publisher": "No Starch Press",
    "total_copies": 2,
    "description": "Learn Python programming"
  }' > /dev/null

# 6. List All Books
echo -e "\n\n6. List All Books"
curl -X GET $BASE_URL/library/books/

# 7. Search Books
echo -e "\n\n7. Search Books (Django)"
curl -X GET "$BASE_URL/library/books/?search=Django"

# 8. Filter Available Books Only
echo -e "\n\n8. Filter Available Books"
curl -X GET "$BASE_URL/library/books/?available_only=true"

# 9. Get User Profile
echo -e "\n\n9. Get Member Profile"
curl -X GET $BASE_URL/users/me/ \
  -H "Authorization: Token $MEMBER_TOKEN"

# 10. Checkout Book
echo -e "\n\n10. Checkout Book"
CHECKOUT_ID=$(curl -s -X POST $BASE_URL/library/checkout/ \
  -H "Authorization: Token $MEMBER_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"book_id\": $BOOK1_ID}" | \
  python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)
echo "Checkout ID: $CHECKOUT_ID"

# 11. Try Duplicate Checkout (Should fail)
echo -e "\n\n11. Try Duplicate Checkout (Should fail)"
curl -X POST $BASE_URL/library/checkout/ \
  -H "Authorization: Token $MEMBER_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"book_id\": $BOOK1_ID}"

# 12. View User Checkouts
echo -e "\n\n12. View User Checkouts"
curl -X GET $BASE_URL/library/my-checkouts/ \
  -H "Authorization: Token $MEMBER_TOKEN"

# 13. Return Book
echo -e "\n\n13. Return Book"
curl -X POST $BASE_URL/library/return/ \
  -H "Authorization: Token $MEMBER_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"checkout_id\": $CHECKOUT_ID}"

# 14. View Updated Checkouts
echo -e "\n\n14. View Updated Checkouts"
curl -X GET $BASE_URL/library/my-checkouts/ \
  -H "Authorization: Token $MEMBER_TOKEN"

# 15. Admin - List All Users
echo -e "\n\n15. Admin - List All Users"
curl -X GET $BASE_URL/auth/admin/users/ \
  -H "Authorization: Token $ADMIN_TOKEN"

echo -e "\n\n=== ALL TESTS COMPLETED ==="