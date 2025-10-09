"""
Test FastAPI app startup to see any errors
"""
import sys
sys.path.insert(0, '.')

print("=" * 60)
print("Testing FastAPI App with SQL Routes")
print("=" * 60)

try:
    print("\n1. Importing FastAPI...")
    from fastapi import FastAPI
    print("   ✅ FastAPI imported")
    
    print("\n2. Importing routes...")
    from routes import base, data, nlp, sql
    print("   ✅ All routes imported")
    print(f"   SQL router has {len(sql.router.routes)} routes")
    
    print("\n3. Creating FastAPI app...")
    app = FastAPI()
    print("   ✅ App created")
    
    print("\n4. Including routers...")
    app.include_router(base.base_router)
    print("   ✅ base router included")
    
    app.include_router(data.data_router)
    print("   ✅ data router included")
    
    app.include_router(nlp.nlp_router)
    print("   ✅ nlp router included")
    
    app.include_router(sql.router, prefix="/api/v1/sql", tags=["SQL"])
    print("   ✅ SQL router included")
    
    print("\n5. Checking all routes...")
    all_routes = []
    for route in app.routes:
        if hasattr(route, 'path'):
            all_routes.append(route.path)
    
    print(f"   Total routes: {len(all_routes)}")
    
    sql_routes = [r for r in all_routes if '/sql/' in r]
    print(f"\n📋 SQL Routes ({len(sql_routes)}):")
    for route in sql_routes:
        print(f"   {route}")
    
    if sql_routes:
        print("\n✅ SUCCESS! SQL routes are working!")
        print("   The issue must be with how the backend is running")
    else:
        print("\n❌ SQL routes not found after including!")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Diagnosis:")
print("=" * 60)
print("If SQL routes appear above, the code is correct.")
print("Issue: Backend might not be running the right main.py")
print("Solution: Make sure you're running from src/ directory")
