#!/bin/bash
# Test script for python_rag

cd "$(dirname "$0")"
source .venv/bin/activate

echo "============================================"
echo "Testing python_rag with various queries"
echo "============================================"
echo ""

echo "Test 1: Korean query about RAG"
echo "-------------------------------------------"
python main.py "RAG가 무엇인가요?" --top-k 5
echo ""
echo ""

echo "Test 2: English query about pgvector"
echo "-------------------------------------------"
python main.py "What is pgvector?" --language en --top-k 5
echo ""
echo ""

echo "Test 3: Impact analysis query in Korean"
echo "-------------------------------------------"
python main.py "chunk 함수를 수정하면 어떤 영향이 있나요?" --top-k 5
echo ""
echo ""

echo "Test 4: Code understanding query"
echo "-------------------------------------------"
python main.py "How does embedding generation work?" --language en --top-k 5
echo ""
echo ""

echo "============================================"
echo "All tests completed!"
echo "============================================"

