# Verification Script for SQL Routes after Docker Rebuild
# This script checks if the SQL routes are properly loaded in the backend

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   SQL Routes Verification Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if backend is running
Write-Host "[1/5] Checking if backend is responding..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/" -Method Get
    Write-Host "✅ Backend is running" -ForegroundColor Green
    Write-Host "    App: $($response.app_name) v$($response.app_version)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Backend is not responding!" -ForegroundColor Red
    Write-Host "   Please wait for Docker containers to start" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 2: Check SQL routes availability
Write-Host "[2/5] Checking SQL routes..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/sql/tables" -Method Get
    Write-Host "✅ SQL routes are loaded!" -ForegroundColor Green
    Write-Host "    Response: $($response.Count) tables" -ForegroundColor Gray
} catch {
    if ($_.Exception.Response.StatusCode.value__ -eq 404) {
        Write-Host "❌ SQL routes NOT found (404)" -ForegroundColor Red
        Write-Host "   The Docker image needs to be rebuilt" -ForegroundColor Red
        exit 1
    } else {
        Write-Host "✅ SQL routes endpoint exists (got non-404 error)" -ForegroundColor Green
    }
}

Write-Host ""

# Step 3: Check OpenAPI docs
Write-Host "[3/5] Checking OpenAPI documentation..." -ForegroundColor Yellow
try {
    $openapi = Invoke-RestMethod -Uri "http://127.0.0.1:8000/openapi.json" -Method Get
    $paths = $openapi.paths.PSObject.Properties.Name
    $sqlPaths = $paths | Where-Object { $_ -like "/api/v1/sql/*" }
    
    if ($sqlPaths.Count -gt 0) {
        Write-Host "✅ Found $($sqlPaths.Count) SQL endpoints in OpenAPI spec" -ForegroundColor Green
        Write-Host "    SQL Endpoints:" -ForegroundColor Gray
        foreach ($path in $sqlPaths) {
            Write-Host "      - $path" -ForegroundColor Gray
        }
    } else {
        Write-Host "❌ No SQL endpoints in OpenAPI spec" -ForegroundColor Red
    }
} catch {
    Write-Host "⚠️  Could not fetch OpenAPI spec" -ForegroundColor Yellow
}

Write-Host ""

# Step 4: Check if SQL files exist in container
Write-Host "[4/5] Checking SQL files in Docker container..." -ForegroundColor Yellow
try {
    $result = docker exec fastapi ls -la /app/controllers/SQLController.py 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ SQLController.py exists in container" -ForegroundColor Green
    } else {
        Write-Host "❌ SQLController.py NOT found in container" -ForegroundColor Red
    }
    
    $result = docker exec fastapi ls -la /app/routes/sql.py 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ sql.py exists in container" -ForegroundColor Green
    } else {
        Write-Host "❌ sql.py NOT found in container" -ForegroundColor Red
    }
} catch {
    Write-Host "⚠️  Could not check files in container" -ForegroundColor Yellow
}

Write-Host ""

# Step 5: Test SQL imports in container
Write-Host "[5/5] Testing SQL imports in container..." -ForegroundColor Yellow
try {
    $result = docker exec fastapi python -c "from routes import sql; print(len(sql.router.routes))" 2>&1
    if ($result -match "\d+") {
        $routeCount = [int]($result -replace '\D', '')
        if ($routeCount -eq 8) {
            Write-Host "✅ SQL routes import correctly: $routeCount routes" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Unexpected route count: $routeCount (expected 8)" -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "⚠️  Could not test imports in container" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Verification Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Open browser: http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "  2. Look for 'SQL' section with 8 endpoints" -ForegroundColor White
Write-Host "  3. Start Streamlit: streamlit run app_sql_chat.py" -ForegroundColor White
Write-Host "  4. Upload sample_data/customers.csv" -ForegroundColor White
Write-Host ""
