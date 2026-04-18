# PCO MCP Server - Portainer Deployment

## Ready to Deploy! 🚀

All setup is complete. GitHub will automatically build and push the Docker image when you push code.

---

## Deployment Steps (Quick):

1. **Wait ~5 minutes** after pushing for GitHub Actions to build

2. **In Portainer:**
   - Go to **Stacks** → **Create new stack**
   
3. **Fill in:**
   - **Stack name:** `pco-mcp`
   - **Compose file:** Use content from `docker-compose-simple.yml`
   - **Image:** `ghcr.io/chilimac02/PCO-MCP-v1.1:latest`
   - **Environment variables:**
     ```
     PCO_APP_ID=your_pc_api_key_here
     PCO_SECRET=your_pc_secret_here
     ```
   - Click **Create stack**

4. **Done!** Container will pull image from GitHub Container Registry

---

## Compose Content (Copy/Paste):

```yaml
version: '3.8'

services:
  pco-mcp:
    image: ghcr.io/chilimac02/PCO-MCP-v1.1:latest
    ports:
      - "8000:8000"
    environment:
      - PCO_APP_ID=your_app_id_here
      - PCO_SECRET=your_secret_here
      - PORT=8000
      - LOG_LEVEL=info
    volumes:
      - ./app:/app/app
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
    labels:
      - "app=pco-mcp"
```

---

## Re-deploy After Updates:

Just change code in repo and push:

```bash
git add .
git commit -m "your changes"
git push origin main
```

GitHub Actions builds and pushes automatically. In Portainer, either:
- Pull the new image, OR
- Update stack with new compose file

That's it!

---

## Access:

Once running, access at:
- `http://YOUR_SERVER:8000`
- `http://YOUR_SERVER:8000/mcp`

---

## Files Created:

✅ `docker-compose-simple.yml` - Portainer-friendly compose
✅ GitHub Actions workflow - Auto-builds Docker images
✅ `.dockerignore` - Clean builds in Portainer
✅ Documentation - Complete deployment guides
