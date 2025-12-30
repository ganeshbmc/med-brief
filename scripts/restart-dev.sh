#!/bin/bash
# restart-dev.sh - Restart MedBrief development servers
# Usage: wsl bash /mnt/d/Github/med-brief/scripts/restart-dev.sh

echo "🔄 Restarting MedBrief dev servers..."

# Kill existing dev servers
echo "   Stopping existing servers..."
pkill -f "uvicorn main:app" 2>/dev/null
pkill -f "vite" 2>/dev/null
sleep 1

# Start backend
echo "   Starting backend (uvicorn)..."
cd /mnt/d/Github/med-brief/backend
python3 -m uvicorn main:app --reload --port 8000 &

# Start frontend
echo "   Starting frontend (vite)..."
cd /mnt/d/Github/med-brief/frontend
source ~/.nvm/nvm.sh
npm run dev &

echo ""
echo "✅ Dev servers restarted!"
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:5173"
