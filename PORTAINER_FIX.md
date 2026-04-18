# 🚀 Quick Fix: Force Rebuild PCO MCP Server in Portainer

## Issue: Container is using cached/old image (without __init__.py)

## Solution: Force Rebuild

### Step 1: Edit Stack in Portainer
1. Go to **Stacks** → Click **pco-mcp**
2. Click **"Edit"**
3. **Replace the compose file** (or update the build context)

### Step 2: Use This Compose Configuration

```yaml
version: '3.8'

services:
  pco-mcp:
    # Option 1: Build fresh from GitHub (Recommended)
    build:
      context: .
      dockerfile: Dockerfile
      args:
        PYTHONDONTWRITEBYTECODE=1
        PYTHONUNBUFFERED=1
    
    # Option 2: Use pre-built image (if available)
    # image: chilimac02/pco-mcp-v1.1:latest
    # build disabled, use image instead above
    
    container_name: pco-mcp-server
    ports:
      - "8000:8000"
    environment:
      - PCO_APP_ID=<YOUR_APP_ID_HERE>
      - PCO_SECRET=<YOUR_SECRET_HERE>
      - PORT=8000
    volumes:
      - ./app:/app/app
      - ./.env:/app/.env
    restart: unless-stopped
    
    # Optional: Limit resources
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### Step 3: Save Changes

Portainer will:
1. Detect new compose configuration
2. **Rebuild the Docker image** from `Dockerfile`
3. **Recreate the container** with new code
4. Start fresh with `__init__.py` included

### Step 4: Wait for Rebuild

Portainer will show:
- **Recreating container...**
- **Building Docker image...**

Wait ~2-3 minutes for build to complete.

### Step 5: Verify

Check logs:
```bash
docker logs -f pco-mcp-server
```

**Expected output:**
```
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Connected to MCP server
```

---

## If Still Not Working:

### Delete and Recreate Container

Sometimes Portainer cache persists. In Portainer:

1. Go to **Stacks** → **pco-mcp**
2. Click **"Remove stack"** (⚠️ data will be recreated)
3. **OR** click **"Update"** → **"Delete and recreate service"**
4. Re-add with new compose file

---

## Alternative: Use Docker Volume Mounts

This ensures Docker always pulls latest code:

```yaml
volumes:
  - ./app:/app/app
  - ./.env:/app/.env
```

This mounts your local `./app` directory (with `__init__.py`) into the container, so every restart reads the latest code.

---

## Verify Files Exist

Before deploying, ensure these files exist locally:

```bash
ls PCO-MCP-v1.1/
```

Should show:
- ✅ `Dockerfile`
- ✅ `docker-compose.yml`
- ✅ `app/` (with `__init__.py`)
- ✅ `app/main.py`
- ✅ `.env.example`

---

## Need Help?

Share the logs from Portainer and I'll debug further!
