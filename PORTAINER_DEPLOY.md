# Portainer Deployment Guide

## Deploy from GitHub Container Registry

After GitHub Actions builds the image (wait ~2-3 minutes after push), you can deploy directly to Portainer.

---

## Steps:

1. **Wait for Image Build**
   - After pushing code with:
     ```bash
     git push origin main
     ```
   - GitHub Actions will build and push the image to:
     ```
     ghcr.io/chilimac02/PCO-MCP-v1.1:latest
     ```

2. **Deploy to Portainer**
   
   Go to Portainer:
   - **Stacks** → **Create new stack**
   - **Stack name:** `pco-mcp`
   - **Compose file:** Use the content from `docker-compose-simple.yml`
   - **Image:** `ghcr.io/chilimac02/PCO-MCP-v1.1:latest`
   - **Environment variables:**
     ```
     PCO_APP_ID=your_app_id_here
     PCO_SECRET=your_secret_here
     PORT=8000
     LOG_LEVEL=info
     ```
   - **Ports:**
     ```
     8000:8000
     ```
   - **Volumes:** (Optional, for code reloading)
     ```
     ./app:/app/app
     ```

3. **Deploy**
   - Click **Create stack**
   - Portainer will pull the image from GitHub Container Registry
   - Wait for container to start (~1-2 minutes)

4. **Verify**
   - Check logs in Portainer
   - Test endpoint at: `http://YOUR_SERVER:8000`

---

## Re-deploy Updates

After code changes in the repo:

1. **Commit and push**
   ```bash
   git add .
   git commit -m "update"
   git push origin main
   ```

2. **GitHub Actions builds new image** (auto)

3. **In Portainer:**
   - Stack → pco-mcp → Edit → Pull
   - OR Update stack to rebuild

That's it! No need to build images locally or set up Docker Hub.

---

## Useful Commands

View GitHub Actions build status:
```bash
github.com/chilimac02/PCO-MCP-v1.1/actions
```

Pull image locally for testing:
```bash
docker pull ghcr.io/chilimac02/PCO-MCP-v1.1:latest
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/app:/app/app \
  -e PCO_APP_ID=$PCO_APP_ID \
  -e PCO_SECRET=$PCO_SECRET \
  ghcr.io/chilimac02/PCO-MCP-v1.1:latest
```

---

## Troubleshooting

**Image not found?**
- Wait 2-5 minutes for GitHub Actions to complete
- Check GitHub Actions tab for errors
- Ensure you have push permissions to the repository

**Container won't start?**
- Check logs: Stack → pco-mcp → Services → Logs
- Verify PCO environment variables are set correctly
