# Dev Scripts

## restart-dev.sh

Restarts the MedBrief backend and frontend development servers using tmux.

### Usage

**From PowerShell:**
```powershell
wsl bash /mnt/d/Github/med-brief/scripts/restart-dev.sh
```

**From Ubuntu/WSL terminal:**
```bash
bash /mnt/d/Github/med-brief/scripts/restart-dev.sh
```

### Managing Servers

**View server logs:**
```bash
tmux attach -t medbrief-backend
tmux attach -t medbrief-frontend
```

**Detach from tmux:** `Ctrl+B`, then `D`

**Kill servers manually:**
```bash
tmux kill-session -t medbrief-backend
tmux kill-session -t medbrief-frontend
```

### Notes
- Servers persist even after closing the terminal (tmux keeps them running)
- Both servers hot-reload on file changes
- Backend: http://localhost:8000
- Frontend: http://localhost:5173
