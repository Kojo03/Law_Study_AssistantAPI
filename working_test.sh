#!/bin/bash

echo "=== Working Library API Test ==="

# Function to check HTTP status
check_status() {
    local status=$1
    local test_name=$2
    if [ "$status" -ge 200 ] && [ "$status" -lt 300 ]; then
        echo "✓ $test_name: SUCCESS (HTTP $status)"
    else
        echo "✗ $test_name: FAILED (HTTP $status)"
    fi
}

# Test 1: Books (working)
echo "1. Testing books..."
response=$(curl -s -w "%{http_code}" "http://127.0.0.1:8000/library/books/" || echo "Connection failed")
if [[ "$response" == *"Connection failed"* ]]; then
    echo "✗ Books test: Server not running"
else
    status=${response: -3}
    body=${response%???}
    echo "Response: $body"
    check_status $status "Books test"
fi

# Test 2: Register with all required fields
echo -e "\n\n2. Registering user..."
response=$(curl -s -w "%{http_code}" -X POST "http://127.0.0.1:8000/auth/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser123", 
    "email": "test@example.com", 
    "first_name": "Test",
    "last_name": "User",
    "password": "strongpass123", 
    "password2": "strongpass123"
  }' || echo "Connection failed")
if [[ "$response" == *"Connection failed"* ]]; then
    echo "✗ Registration test: Server not running"
else
    status=${response: -3}
    body=${response%???}
    echo "Response: $body"
    check_status $status "Registration test"
fi

# Test 3: Login
echo -e "\n\n3. Login..."
response=$(curl -s -w "%{http_code}" -X POST "http://127.0.0.1:8000/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser123", "password": "strongpass123"}' || echo "Connection failed")
if [[ "$response" == *"Connection failed"* ]]; then
    echo "✗ Login test: Server not running"
else
    status=${response: -3}
    body=${response%???}
    echo "Response: $body"
    check_status $status "Login test"
    
    # Extract token if login successful
    if [ "$status" -ge 200 ] && [ "$status" -lt 300 ]; then
        token=$(echo "$body" | grep -o '"token":"[^"]*' | cut -d'"' -f4)
        echo "Token extracted: $token"
    fi
fi

# Test 4: Create book (requires authentication)
echo -e "\n\n4. Create book..."
if [ -n "$token" ]; then
    response=$(curl -s -w "%{http_code}" -X POST "http://127.0.0.1:8000/library/books/" \
      -H "Content-Type: application/json" \
      -H "Authorization: Token $token" \
      -d '{"title": "Working Book", "author": "Test Author", "isbn": "1111111111", "published_date": "2024-01-01", "total_copies": 1}' || echo "Connection failed")
    if [[ "$response" == *"Connection failed"* ]]; then
        echo "✗ Create book test: Server not running"
    else
        status=${response: -3}
        body=${response%???}
        echo "Response: $body"
        check_status $status "Create book test"
    fi
else
    echo "✗ Create book test: No token available (login failed)"
fi

echo -e "\n\n=== Test Complete ==="