#!/bin/bash
# restart-dev.sh - Restart MedBrief development servers using tmux

# Resolve project root dynamically
# Assuming script is in <root>/scripts/
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🔄 Restarting MedBrief dev servers..."
echo "   Project Root: $PROJECT_ROOT"

# Kill existing tmux sessions for medbrief
tmux kill-session -t medbrief-backend 2>/dev/null
tmux kill-session -t medbrief-frontend 2>/dev/null

# Also kill any stray processes
pkill -f "uvicorn main:app" 2>/dev/null
pkill -f "vite" 2>/dev/null
sleep 1

# Detect Python interpreter
# Prefer python3.10 if available (matches system python with dependencies), else python3
if command -v python3.10 &> /dev/null; then
    PYTHON_EXEC="python3.10"
else
    PYTHON_EXEC="python3"
fi
echo "   Using Python: $PYTHON_EXEC"

# Start backend in tmux
echo "   Starting backend (uvicorn)..."
tmux new-session -d -s medbrief-backend -c "$PROJECT_ROOT/backend" \
    "$PYTHON_EXEC -m uvicorn main:app --reload --port 8000"

# Start frontend in tmux  
echo "   Starting frontend (vite)..."
# Check if nvm script exists, source it if so, otherwise just run npm
if [ -f "$HOME/.nvm/nvm.sh" ]; then
    FRONTEND_CMD="source $HOME/.nvm/nvm.sh && npm run dev"
else
    FRONTEND_CMD="npm run dev"
fi

tmux new-session -d -s medbrief-frontend -c "$PROJECT_ROOT/frontend" \
    "$FRONTEND_CMD"

sleep 2
echo ""
echo "✅ Dev servers restarted!"
echo "   Backend:  http://localhost:8000  (tmux: medbrief-backend)"
echo "   Frontend: http://localhost:5173  (tmux: medbrief-frontend)"
echo ""
echo "   View logs:  tmux attach -t medbrief-backend"
echo "               tmux attach -t medbrief-frontend"
echo "   Detach:     Ctrl+B, then D"
