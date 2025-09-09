#!/bin/bash

echo "=== Simple Library API Test ==="

# Test 1: Books endpoint
echo "1. Testing books endpoint..."
curl -s "http://127.0.0.1:8000/library/books" | head -1

# Test 2: Register user
echo -e "\n2. Registering user..."
curl -s -X POST "http://127.0.0.1:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@test.com", "password": "testpass123", "password2": "testpass123"}' | head -1

# Test 3: Login user
echo -e "\n3. Logging in..."
TOKEN=$(curl -s -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}' | \
  grep -o '"token":"[^"]*"' | cut -d'"' -f4)

echo "Token: $TOKEN"

# Test 4: Create book
echo -e "\n4. Creating book..."
curl -s -X POST "http://127.0.0.1:8000/library/books" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Book", "author": "Test Author", "isbn": "1234567890"}' | head -1

# Test 5: Checkout book
if [ ! -z "$TOKEN" ]; then
  echo -e "\n5. Checking out book..."
  curl -s -X POST "http://127.0.0.1:8000/library/checkout" \
    -H "Authorization: Token $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"book_id": 1}' | head -1
else
  echo -e "\n5. Skipping checkout - no token"
fi

echo -e "\n=== Test Complete ==="