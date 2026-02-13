#!/bin/bash

# Nicole Demo Test Script
# Quick verification that everything is configured correctly

echo "🧪 Nicole Demo Test Suite"
echo "=========================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASS=0
FAIL=0

# Function to test
test_check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ PASS${NC}: $1"
        ((PASS++))
    else
        echo -e "${RED}❌ FAIL${NC}: $1"
        ((FAIL++))
    fi
}

# Check 1: Directory structure
echo "📁 Checking project structure..."
[ -d "api" ] && [ -d "widget" ] && [ -d "gmail" ] && [ -d "knowledge" ]
test_check "Project directories exist"

# Check 2: Core files
echo ""
echo "📄 Checking core files..."
[ -f "api/main.py" ] && [ -f "api/nicole.py" ] && [ -f "api/chat.py" ]
test_check "Core API files exist"

[ -f "widget/nicole-widget.js" ] && [ -f "widget/nicole-widget.css" ]
test_check "Widget files exist"

[ -f "knowledge/woodthumb.md" ]
test_check "Knowledge base exists"

# Check 3: Configuration
echo ""
echo "⚙️  Checking configuration..."
[ -f ".env" ]
test_check ".env file exists"

if [ -f ".env" ]; then
    grep -q "ANTHROPIC_API_KEY" .env
    test_check ".env contains API key field"

    if grep -q "your_key_here" .env; then
        echo -e "${YELLOW}⚠️  WARNING${NC}: API key not set yet (still using placeholder)"
        echo "   Get your key from: https://console.anthropic.com/settings/keys"
        echo "   Then edit .env and replace 'your_key_here_get_from_anthropic_console'"
    else
        echo -e "${GREEN}✅${NC} API key appears to be configured"
    fi
fi

# Check 4: Dependencies
echo ""
echo "📦 Checking Python dependencies..."
[ -f "requirements.txt" ]
test_check "requirements.txt exists"

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo -e "${GREEN}✅${NC} Virtual environment is active"
else
    echo -e "${YELLOW}⚠️  WARNING${NC}: Not in a virtual environment"
    echo "   Consider running: python3 -m venv venv && source venv/bin/activate"
fi

# Check 5: Python packages (if venv active)
if [[ "$VIRTUAL_ENV" != "" ]]; then
    python -c "import fastapi" 2>/dev/null
    test_check "FastAPI installed"

    python -c "import anthropic" 2>/dev/null
    test_check "Anthropic SDK installed"
else
    echo -e "${YELLOW}⚠️  SKIP${NC}: Python package check (activate venv first)"
fi

# Check 6: Port availability
echo ""
echo "🔌 Checking if port 8000 is available..."
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}⚠️  WARNING${NC}: Port 8000 is already in use"
    echo "   Either stop the existing service or use a different port"
else
    echo -e "${GREEN}✅${NC} Port 8000 is available"
fi

# Summary
echo ""
echo "=========================="
echo "📊 Test Results"
echo "=========================="
echo -e "${GREEN}Passed: $PASS${NC}"
echo -e "${RED}Failed: $FAIL${NC}"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}🎉 All checks passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Make sure your Anthropic API key is set in .env"
    echo "2. Run: ./start.sh"
    echo "3. Open widget/test.html in your browser"
    echo "4. Follow DEMO_SETUP.md for detailed testing"
else
    echo -e "${RED}⚠️  Some checks failed${NC}"
    echo "Please review the errors above and fix them before proceeding."
fi

echo ""
