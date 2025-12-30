# Railway Deployment Guide

## 🚨 One-Time Fix for Existing Databases

If you are deploying this code to a **production database that already contains data** (tables like `users`, `profiles` already exist), the new auto-migration script might fail with "Table already exists".

To fix this, you need to tell the migration system that the database is already up-to-date.

### Method: Temporary Start Command

1.  Open your **Railway Dashboard**.
2.  Click on your **Backend Service**.
3.  Go to **Settings** -> **Deploy**.
4.  Find **Custom Start Command**.
5.  Set it to this command (one line):
    ```bash
    python -m alembic stamp head && python -m alembic upgrade head && gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
    ```
6.  **Redeploy** the service.
    *   This will force the database to be "stamped" as current, then run upgrades, then start the server.
7.  **IMPORTANT:** Once the deploy is successful and the app is running:
    *   **Clear** the Custom Start Command in settings (make it empty).
    *   Redeploy one last time.
    *   Now your service will use the default Dockerfile command (which only does "upgrade", not "stamp").

## Standard Deployment

For all future updates, you don't need to do anything. Just push your code. The `Dockerfile` handles migrations automatically (`alembic upgrade head`).
