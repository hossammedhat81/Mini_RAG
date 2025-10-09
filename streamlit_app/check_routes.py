"""
Check what routes are available in the backend
"""
import requests

API_BASE_URL = "http://127.0.0.1:8000"

print("=" * 60)
print("Checking Available Routes")
print("=" * 60)

# Try to get OpenAPI spec
try:
    response = requests.get(f"{API_BASE_URL}/openapi.json")
    if response.status_code == 200:
        spec = response.json()
        paths = spec.get('paths', {})
        
        print(f"\n✅ Total routes: {len(paths)}")
        print("\n📋 Available routes:")
        
        sql_routes = []
        other_routes = []
        
        for path in sorted(paths.keys()):
            if '/sql/' in path:
                sql_routes.append(path)
            else:
                other_routes.append(path)
        
        if sql_routes:
            print("\n✅ SQL Routes (NEW):")
            for route in sql_routes:
                methods = list(paths[route].keys())
                print(f"   {route} [{', '.join(m.upper() for m in methods)}]")
        else:
            print("\n❌ NO SQL Routes found!")
            print("   Backend needs restart to load SQL routes")
        
        print(f"\n📝 Other Routes ({len(other_routes)}):")
        for route in other_routes[:5]:
            methods = list(paths[route].keys())
            print(f"   {route} [{', '.join(m.upper() for m in methods)}]")
        if len(other_routes) > 5:
            print(f"   ... and {len(other_routes) - 5} more")
            
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("Action Required:")
print("=" * 60)
if not sql_routes:
    print("🔴 Backend is running OLD CODE")
    print("   → Stop backend (Ctrl+C)")
    print("   → Restart: python main.py")
else:
    print("✅ Backend has SQL routes loaded!")
    print("   Upload should work now")
