#!/bin/bash
# restart-dev.sh - Restart MedBrief development servers
# Usage: wsl bash /mnt/d/Github/med-brief/scripts/restart-dev.sh

echo "🔄 Restarting MedBrief dev servers..."

# Kill existing dev servers
echo "   Stopping existing servers..."
pkill -f "uvicorn main:app" 2>/dev/null
pkill -f "vite" 2>/dev/null
sleep 1

# Create logs directory
mkdir -p /mnt/d/Github/med-brief/logs/dev

# Start backend with nohup
echo "   Starting backend (uvicorn)..."
cd /mnt/d/Github/med-brief/backend
nohup python3 -m uvicorn main:app --reload --port 8000 > /mnt/d/Github/med-brief/logs/dev/backend.log 2>&1 &

# Start frontend with nohup
echo "   Starting frontend (vite)..."
cd /mnt/d/Github/med-brief/frontend
source ~/.nvm/nvm.sh
nohup npm run dev > /mnt/d/Github/med-brief/logs/dev/frontend.log 2>&1 &

sleep 2
echo ""
echo "✅ Dev servers restarted!"
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:5173"
echo ""
echo "   Logs: logs/dev/backend.log, logs/dev/frontend.log"
