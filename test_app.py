#!/usr/bin/env python3
"""Test script to verify app imports work correctly."""

import sys
import os

# Add app directory to path
sys.path.insert(0, '/app')

try:
    import app
    print("✅ app package imported successfully")
    print(f"   app.app = {app.app}")
    print(f"   app.name = {getattr(app, 'name', 'N/A')}")
    print()
    
    from app.main import app
    print("✅ app.main.app imported successfully")
    print(f"   app.main.app = {app}")
    print()
    print("=== All imports successful! ===")
    
except Exception as e:
    print(f"❌ Import failed: {type(e).__name__}")
    print(f"   Error: {e}")
    print()
    import traceback
    traceback.print_exc()
