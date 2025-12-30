#!/bin/bash
# restart-dev.sh - Restart MedBrief development servers using tmux
# Usage: wsl bash /mnt/d/Github/med-brief/scripts/restart-dev.sh

echo "🔄 Restarting MedBrief dev servers..."

# Kill existing tmux sessions for medbrief
tmux kill-session -t medbrief-backend 2>/dev/null
tmux kill-session -t medbrief-frontend 2>/dev/null

# Also kill any stray processes
pkill -f "uvicorn main:app" 2>/dev/null
pkill -f "vite" 2>/dev/null
sleep 1

# Start backend in tmux
echo "   Starting backend (uvicorn)..."
tmux new-session -d -s medbrief-backend -c /mnt/d/Github/med-brief/backend \
    "python3 -m uvicorn main:app --reload --port 8000"

# Start frontend in tmux  
echo "   Starting frontend (vite)..."
tmux new-session -d -s medbrief-frontend -c /mnt/d/Github/med-brief/frontend \
    "source ~/.nvm/nvm.sh && npm run dev"

sleep 2
echo ""
echo "✅ Dev servers restarted!"
echo "   Backend:  http://localhost:8000  (tmux: medbrief-backend)"
echo "   Frontend: http://localhost:5173  (tmux: medbrief-frontend)"
echo ""
echo "   View logs:  tmux attach -t medbrief-backend"
echo "               tmux attach -t medbrief-frontend"
echo "   Detach:     Ctrl+B, then D"
