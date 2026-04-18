#!/bin/bash
# Script to prepare your PCO MCP Server for Portainer deployment

echo "=== PCO MCP Server Portainer Setup ==="
echo ""

# 1. Clone repository if not already done
if [ ! -d "PCO-MCP-v1.1" ]; then
    echo "Cloning from GitHub..."
    git clone https://github.com/chilimac02/PCO-MCP-v1.1.git
else
    echo "Repository already cloned."
fi

# 2. Create .env file for configuration
echo ""
echo "Creating .env file..."
if [ ! -f "PCO-MCP-v1.1/.env" ]; then
    cp PCO-MCP-v1.1/.env.example PCO-MCP-v1.1/.env
fi

# 3. Edit .env with your credentials
echo ""
echo "Edit PCO-MCP-v1.1/.env with your PCO credentials:"
echo "  PCO_APP_ID=your_app_id_here"
echo "  PCO_SECRET=your_secret_here"
echo ""
echo "Example using nano:"
echo "  nano PCO-MCP-v1.1/.env"
echo ""
echo "Example using vim:"
echo "  vim PCO-MCP-v1.1/.env"

# 4. Export the environment for docker-compose
echo ""
echo "=== Environment Configuration ==="
echo "Set the following environment variables in .env file:"
echo "  PCO_APP_ID       - Your PCO API App ID"
echo "  PCO_SECRET       - Your PCO API Secret"
echo ""
echo "After editing, restart the stack:"
echo "  portainer-cli stack reload -n pco-mcp"
echo "  OR manually in Portainer UI:"
echo "    Click stack -> Services -> pco-mcp -> Update"

echo ""
echo "=== Next Steps ==="
echo "1. Review and edit PCO-MCP-v1.1/.env"
echo "2. Copy PCO-MCP-v1.1 to your Portainer host (if needed)"
echo "3. Create stack in Portainer with the docker-compose.yml"
echo "4. Add PCO credentials to .env"
echo "5. Import stack to Portainer"
echo ""
echo "Or use Portainer's direct upload:"
echo "  - Go to Stacks -> Create new stack"
echo "  - Upload the PCO-MCP-v1.1 directory"
echo "  - Edit environment variables in Portainer UI"
echo ""
echo "For Docker volume mounting, set:"
echo "  - DATA_PATH=/tmp/pco-mcp-data"
echo "  (Data will persist across container restarts)"
