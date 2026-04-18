"""
PCO MCP Server
Exposes Planning Center Online API via MCP JSON-RPC
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import PCO client
import sys
sys.path.append('/home/justin/.openclaw/workspace-super_coder/pco-dashboard')
from app.pco_client import PCOClient

app = FastAPI(title="PCO MCP Server v1.1", version="1.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize PCO client
try:
    pco_client = PCOClient()
except ValueError as e:
    print(f"Warning: PCO client not initialized: {e}")
    pco_client = None

# MCP Request/Response Models
class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: Optional[Dict[str, Any]] = None
    id: Optional[Any] = None

class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[Any] = None

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "PCO MCP Server v1.1"}

# MCP endpoint
@app.post("/mcp")
async def handle_mcp_request(request: MCPRequest):
    if not pco_client:
        raise HTTPException(status_code=503, detail="PCO client not configured")
    
    try:
        result = await process_mcp_method(request.method, request.params or {})
        return MCPResponse(result=result, id=request.id)
    except Exception as e:
        return MCPResponse(
            error={"code": -32603, "message": str(e)},
            id=request.id
        )

async def process_mcp_method(method: str, params: Dict[str, Any]) -> Any:
    """Process MCP JSON-RPC methods"""
    
    if method == "get_service_types":
        service_types = pco_client.get_service_types()
        return [
            {"id": st["id"], "name": st["attributes"]["name"]}
            for st in service_types
        ]
    
    elif method == "get_plans":
        service_type_id = params.get("service_type_id")
        start_date = params.get("start_date")
        end_date = params.get("end_date")
        
        if not service_type_id:
            raise ValueError("service_type_id is required")
            
        plans = pco_client.get_plan_times(service_type_id, start_date, end_date)
        return [
            {
                "id": pt["id"],
                "starts_at": pt["attributes"]["starts_at"],
                "ends_at": pt["attributes"]["ends_at"],
                "name": pt["attributes"]["title"],
                "service_type_id": pt["relationships"]["service_type"]["data"]["id"]
            }
            for pt in plans
        ]
    
    elif method == "get_headcounts":
        plan_time_id = params.get("plan_time_id")
        if not plan_time_id:
            raise ValueError("plan_time_id is required")
            
        headcounts = pco_client.get_headcounts(plan_time_id)
        return [
            {
                "id": hc["id"],
                "count": hc["attributes"]["count"],
                "created_at": hc["attributes"]["created_at"]
            }
            for hc in headcounts
        ]
    
    elif method == "get_aggregated_attendance":
        service_type_ids = params.get("service_type_ids", [])
        start_date = params.get("start_date")
        end_date = params.get("end_date")
        
        if not service_type_ids:
            raise ValueError("service_type_ids is required")
        if not start_date or not end_date:
            raise ValueError("start_date and end_date are required")
            
        attendance = pco_client.get_aggregated_attendance(
            service_type_ids, start_date, end_date
        )
        return attendance
    
    elif method == "get_year_over_year_comparison":
        service_type_ids = params.get("service_type_ids", [])
        reference_date = params.get("reference_date")
        lookback_days = params.get("lookback_days", 90)
        
        if not service_type_ids:
            raise ValueError("service_type_ids is required")
        if not reference_date:
            raise ValueError("reference_date is required")
            
        comparison = pco_client.get_year_over_year_comparison(
            service_type_ids, reference_date, lookback_days
        )
        return comparison
    
    elif method == "list":
        # Return available methods
        return {
            "methods": [
                "get_service_types",
                "get_plans", 
                "get_headcounts",
                "get_aggregated_attendance",
                "get_year_over_year_comparison",
                "list"
            ]
        }
    
    else:
        raise ValueError(f"Unknown method: {method}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)