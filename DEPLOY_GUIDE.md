# 🎯 Portainer Deployment Guide

## Issue: Container can't import `app.main`

The error `Could not import module app.main` means the container is using an old/cached version WITHOUT `__init__.py`.

## Solution: Build Fresh on Your Portainer Host

---

## Step 1: Copy Code to Portainer Host

SSH into your Portainer host (Docker server), then:

```bash
# On Portainer host, SSH as root or user with sudo
mkdir -p /path/to/your/docker/host/PCO-MCP-v1.1

# Copy the entire repo to that path from your local machine
# Or clone from GitHub if it's your repo
git clone https://github.com/chilimac02/PCO-MCP-v1.1.git /path/to/your/docker/host/PCO-MCP-v1.1

# If you're copying from another machine, use scp
# scp -r /home/justin/.openclaw/workspace-super_coder/PCO_MCP_v1.1 /path/to/your/docker/host/PCO-MCP-v1.1
```

---

## Step 2: Build Docker Image Locally

```bash
cd /path/to/your/docker/host/PCO-MCP-v1.1
docker build -t pco-mcp-v1.1 .
```

This builds the image from the Dockerfile, including `__init__.py`.

---

## Step 3: Deploy in Portainer

1. **Stacks → Create new stack**
2. **Stack name:** `pco-mcp`
3. **Compose file:** Point to `docker-compose.yml`
4. **Environment:** Add your PCO credentials
5. **Create stack**

Portainer will use the image you built locally.

---

## Step 4: Verify

Check logs:

```bash
docker logs -f pco-mcp-server
```

**Expected:**
```
INFO: Uvicorn running on http://0.0.0.0:8000
```

---

## Alternative: Use Volume Mounts

This ensures the container always reads the latest `__init__.py`:

```yaml
volumes:
  - ./app:/app/app
```

In Portainer compose settings:
- **volumes**
  - `./app:/app/app`

This mounts the local `app/` directory (with `__init__.py`) into the container.

---

## Why You're Still Seeing the Error

GitHub doesn't build Docker images. When you pull `chilimac02/pco-mcp-v1.1:latest`, Portainer doesn't pull from GitHub Container Registry - it's looking for an image that doesn't exist or is cached.

**Fix:** Build locally on Portainer host (Step 2 above), then use that image or volume mount local code.

---

## Quick Fix Commands

On Portainer host:

```bash
cd /path/to/PCO-MCP-v1.1
docker-compose down           # Stop old container
docker build -t pco-mcp .    # Build fresh
docker-compose up -d          # Start new container with fresh image
```

---

## Need Help?

Let me know the path where you copied the repo and I can help you run the commands!
