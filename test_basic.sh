#!/bin/bash

echo "=== Basic API Test (No Authentication Required) ==="

# Test server connectivity
echo "1. Testing server connectivity..."
response=$(curl -s -w "%{http_code}" "http://127.0.0.1:8000/" || echo "Connection failed")
if [[ "$response" == *"Connection failed"* ]]; then
    echo "❌ Server not running on port 8000"
    echo "Please start the server with: python3 manage.py runserver"
    exit 1
else
    echo "✅ Server is running"
fi

# Test books endpoint (should work without auth)
echo -e "\n2. Testing books list endpoint..."
response=$(curl -s -w "%{http_code}" "http://127.0.0.1:8000/library/books/" || echo "Connection failed")
if [[ "$response" == *"Connection failed"* ]]; then
    echo "❌ Books endpoint failed"
else
    status=${response: -3}
    body=${response%???}
    if [ "$status" -eq 200 ]; then
        echo "✅ Books endpoint working (HTTP $status)"
        echo "Response: $body"
    else
        echo "❌ Books endpoint failed (HTTP $status)"
        echo "Response: $body"
    fi
fi

# Test API documentation
echo -e "\n3. Testing API documentation..."
response=$(curl -s -w "%{http_code}" "http://127.0.0.1:8000/api/docs/" || echo "Connection failed")
if [[ "$response" == *"Connection failed"* ]]; then
    echo "❌ API docs endpoint failed"
else
    status=${response: -3}
    if [ "$status" -eq 200 ]; then
        echo "✅ API documentation available (HTTP $status)"
    else
        echo "❌ API docs failed (HTTP $status)"
    fi
fi

echo -e "\n=== Basic Test Complete ==="