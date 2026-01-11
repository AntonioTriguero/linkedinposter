#!/bin/zsh

# LinkedIn Bot Poster - macOS Shortcut Helper Script
# Usage from Shortcut: zsh /path/to/linkedinposter.sh now
# Usage from Terminal: zsh linkedinposter.sh now

# ========== CONFIGURATION ==========
SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
VENV_DIR="$SCRIPT_DIR/venv"
PYTHON_EXECUTABLE="$VENV_DIR/bin/python3"
MAIN_SCRIPT="$SCRIPT_DIR/main.py"

# ========== COLORS FOR OUTPUT ==========
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ========== FUNCTIONS ==========

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  LinkedIn Bot - macOS Shortcut Runner${NC}"
    echo -e "${BLUE}========================================${NC}"
}

check_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        echo -e "${RED}❌ Virtual environment not found at: $VENV_DIR${NC}"
        echo -e "${YELLOW}💡 Create it with:${NC}"
        echo -e "   cd $SCRIPT_DIR"
        echo -e "   python3 -m venv venv"
        echo -e "   source venv/bin/activate"
        echo -e "   pip install -r requirements.txt"
        return 1
    fi
    return 0
}

check_env_file() {
    if [ ! -f "$SCRIPT_DIR/.env" ]; then
        echo -e "${RED}❌ .env file not found at: $SCRIPT_DIR/.env${NC}"
        echo -e "${YELLOW}💡 Create a .env file with:${NC}"
        echo -e "   PERPLEXITY_API_KEY=your_key_here"
        echo -e "   LINKEDIN_ACCESS_TOKEN=your_token_here"
        echo -e "   LINKEDIN_PERSON_URN=urn:li:person:xxxxx"
        echo -e "   PIXABAY_API_KEY=your_key_here"
        return 1
    fi
    return 0
}

check_main_script() {
    if [ ! -f "$MAIN_SCRIPT" ]; then
        echo -e "${RED}❌ main.py not found at: $MAIN_SCRIPT${NC}"
        return 1
    fi
    return 0
}

run_immediate_mode() {
    echo -e "${GREEN}🚀 Running in IMMEDIATE mode...${NC}"
    echo -e "${YELLOW}Generating and publishing post now${NC}\n"
    
    # Source activate script
    source "$VENV_DIR/bin/activate" 2>/dev/null
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to activate virtual environment${NC}"
        return 1
    fi
    
    # Run the script
    "$PYTHON_EXECUTABLE" "$MAIN_SCRIPT" now
    
    local exit_code=$?
    
    # Deactivate venv
    deactivate 2>/dev/null
    
    if [ $exit_code -eq 0 ]; then
        echo -e "\n${GREEN}✅ Post published successfully!${NC}"
    else
        echo -e "\n${RED}❌ Error publishing post (exit code: $exit_code)${NC}"
    fi
    
    return $exit_code
}

run_scheduled_mode() {
    echo -e "${GREEN}🕐 Running in SCHEDULED mode...${NC}"
    echo -e "${YELLOW}Daemon will publish every 3.5 days at 10:00${NC}\n"
    
    # Source activate script
    source "$VENV_DIR/bin/activate" 2>/dev/null
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to activate virtual environment${NC}"
        return 1
    fi
    
    # Run the script (will loop indefinitely)
    "$PYTHON_EXECUTABLE" "$MAIN_SCRIPT"
    
    # Deactivate venv
    deactivate 2>/dev/null
}

show_help() {
    echo -e "\n${BLUE}Usage:${NC}"
    echo -e "  zsh linkedinposter.sh now       ${YELLOW}# Publish immediately${NC}"
    echo -e "  zsh linkedinposter.sh daemon    ${YELLOW}# Run scheduled daemon${NC}"
    echo -e "  zsh linkedinposter.sh help      ${YELLOW}# Show this help${NC}"
    echo -e "\n${BLUE}macOS Shortcut Setup:${NC}"
    echo -e "  1. Open Shortcuts.app"
    echo -e "  2. Create new shortcut"
    echo -e "  3. Add 'Run Shell Script' action"
    echo -e "  4. Change shell to: ${YELLOW}zsh${NC}"
    echo -e "  5. Paste: ${YELLOW}zsh /full/path/to/linkedinposter.sh now${NC}"
    echo -e "  6. Run shortcut to test"
    echo -e "\n${BLUE}Setup:${NC}"
    echo -e "  1. Create venv:     ${YELLOW}python3 -m venv venv${NC}"
    echo -e "  2. Install deps:    ${YELLOW}pip install -r requirements.txt${NC}"
    echo -e "  3. Configure .env   ${YELLOW}(add API keys)${NC}"
    echo -e "  4. Run script:      ${YELLOW}zsh linkedinposter.sh now${NC}"
}

# ========== MAIN EXECUTION ==========

print_header

# Validate prerequisites
if ! check_venv; then
    exit 1
fi

if ! check_env_file; then
    exit 1
fi

if ! check_main_script; then
    exit 1
fi

# Parse arguments
case "${1:-help}" in
    now)
        run_immediate_mode
        exit $?
        ;;
    daemon)
        run_scheduled_mode
        exit $?
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}❌ Unknown command: $1${NC}"
        show_help
        exit 1
        ;;
esac
