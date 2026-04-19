"""
PCO MCP Server
Exposes Planning Center People/Groups API via MCP JSON-RPC
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
from dotenv import load_dotenv

load_dotenv()

from pco_client import PCOClient

app = FastAPI(title="PCO MCP Server", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    pco_client = PCOClient()
except ValueError as e:
    print(f"Warning: PCO client not initialized: {e}")
    pco_client = None


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


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "PCO MCP Server v2.0"}


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
    
    # --- People ---
    if method == "get_people":
        people = pco_client.get_people(
            per_page=params.get("per_page", 100),
            offset=params.get("offset", 0)
        )
        return [
            {
                "id": p["id"],
                "first_name": p["attributes"].get("first_name"),
                "last_name": p["attributes"].get("last_name"),
                "email": p["attributes"].get("email"),
                "phone": p["attributes"].get("phone_number"),
            }
            for p in people
        ]
    
    elif method == "search_people":
        if not params.get("query"):
            raise ValueError("query is required")
        people = pco_client.search_people(params["query"])
        return [
            {
                "id": p["id"],
                "first_name": p["attributes"].get("first_name"),
                "last_name": p["attributes"].get("last_name"),
                "email": p["attributes"].get("email"),
            }
            for p in people
        ]
    
    elif method == "get_person":
        if not params.get("person_id"):
            raise ValueError("person_id is required")
        person = pco_client.get_person(params["person_id"])
        return person
    
    elif method == "get_person_fields":
        if not params.get("person_id"):
            raise ValueError("person_id is required")
        return pco_client.get_person_field_values(params["person_id"])
    
    # --- Groups ---
    elif method == "get_groups":
        groups = pco_client.get_groups(per_page=params.get("per_page", 100))
        return [
            {
                "id": g["id"],
                "name": g["attributes"].get("name"),
                "group_type": g["attributes"].get("group_type_id"),
            }
            for g in groups
        ]
    
    elif method == "get_group":
        if not params.get("group_id"):
            raise ValueError("group_id is required")
        return pco_client.get_group(params["group_id"])
    
    elif method == "get_group_members":
        if not params.get("group_id"):
            raise ValueError("group_id is required")
        members = pco_client.get_group_members(params["group_id"])
        return [
            {
                "id": m["id"],
                "person_id": m["relationships"]["person"]["data"]["id"],
                "status": m["attributes"].get("person_status"),
            }
            for m in members
        ]
    
    elif method == "get_group_types":
        types = pco_client.get_group_types()
        return [
            {"id": t["id"], "name": t["attributes"].get("name")}
            for t in types
        ]
    
    # --- Tags ---
    elif method == "get_tags":
        tags = pco_client.get_tags()
        return [{"id": t["id"], "name": t["attributes"].get("name")} for t in tags]
    
    elif method == "get_people_with_tag":
        if not params.get("tag_id"):
            raise ValueError("tag_id is required")
        people = pco_client.get_people_with_tag(params["tag_id"])
        return [
            {"id": p["id"], "name": f"{p['attributes'].get('first_name')} {p['attributes'].get('last_name')}"}
            for p in people
        ]
    
    # --- Households ---
    elif method == "get_households":
        households = pco_client.get_households(per_page=params.get("per_page", 100))
        return [
            {"id": h["id"], "name": h["attributes"].get("name")}
            for h in households
        ]
    
    elif method == "get_household":
        if not params.get("household_id"):
            raise ValueError("household_id is required")
        return pco_client.get_household(params["household_id"])
    
    elif method == "get_household_members":
        if not params.get("household_id"):
            raise ValueError("household_id is required")
        return pco_client.get_household_members(params["household_id"])
    
    # --- List available methods ---
    elif method == "list":
        return {
            "methods": [
                # People
                "get_people",
                "search_people",
                "get_person",
                "get_person_fields",
                # Groups
                "get_groups",
                "get_group",
                "get_group_members",
                "get_group_types",
                # Tags
                "get_tags",
                "get_people_with_tag",
                # Households
                "get_households",
                "get_household",
                "get_household_members",
                # Utility
                "list",
            ]
        }
    
    else:
        raise ValueError(f"Unknown method: {method}")


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
