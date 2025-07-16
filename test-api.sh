#!/bin/bash
echo "Testing TopV Adaptor Python API..."

echo
echo "1. Testing health check..."
curl -X GET http://localhost:8080/health

echo
echo "2. Testing find_last..."
curl -X POST http://localhost:8080/api/find_last -H "Content-Type: application/json" -d '{"projectID":"test","tag":"group1.dev1.a","device":false}'

echo
echo "3. Testing set_value..."
curl -X POST http://localhost:8080/api/set_value -H "Content-Type: application/json" -d '{"projectID":"test","tag":"group1.dev1.a","value":"25.5","time":1640995200000}'

echo
echo "4. Testing query_history..."
curl -X POST http://localhost:8080/api/query_history -H "Content-Type: application/json" -d '{"projectID":"test","tag":["group1.dev1.a"],"start":"2022-01-01T00:00:00Z","end":"2022-01-02T00:00:00Z"}'

echo
echo "5. Testing query_points..."
curl -X POST http://localhost:8080/api/query_points -H "Content-Type: application/json" -d '{"projectID":"test","parentTag":"group1.dev1"}'

echo
echo "6. Testing query_devices..."
curl -X POST http://localhost:8080/api/query_devices -H "Content-Type: application/json" -d '{"projectID":"test"}'

echo
echo "API testing completed." 