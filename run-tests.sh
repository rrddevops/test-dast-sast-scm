#!/bin/bash

echo "🧪 Running Security Test Application Tests"
echo "=========================================="

# Install dependencies if needed
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run tests with coverage
echo "🔍 Running tests with coverage..."
python -m pytest test_app.py --cov=app --cov-report=html:htmlcov --cov-report=term-missing -v

# Show coverage summary
echo ""
echo "📊 Coverage Summary:"
coverage report

# Open coverage report in browser (if available)
if command -v xdg-open &> /dev/null; then
    echo "🌐 Opening coverage report in browser..."
    xdg-open htmlcov/index.html
elif command -v open &> /dev/null; then
    echo "🌐 Opening coverage report in browser..."
    open htmlcov/index.html
else
    echo "📁 Coverage report available at: htmlcov/index.html"
fi

echo ""
echo "✅ Tests completed!" 