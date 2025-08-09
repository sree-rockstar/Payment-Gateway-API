@echo off
echo ========================================
echo    Payment Gateway API - Windows Setup
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed or not running!
    echo Please install Docker Desktop for Windows from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not available!
    echo Please ensure Docker Desktop is running and includes Docker Compose.
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose are available
echo.

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

REM Stop and remove existing containers
echo 🧹 Cleaning up existing containers...
docker-compose -f docker-compose.dev.yml down --remove-orphans

REM Build and start services
echo 🚀 Starting Payment Gateway API...
docker-compose -f docker-compose.dev.yml up --build -d

REM Wait for services to be healthy
echo ⏳ Waiting for services to be ready...
timeout /t 10 /nobreak >nul

REM Show status
echo.
echo 📊 Service Status:
docker-compose -f docker-compose.dev.yml ps

echo.
echo 🌐 API URLs:
echo   • API Base: http://localhost:8000
echo   • Swagger UI: http://localhost:8000/docs
echo   • ReDoc: http://localhost:8000/redoc
echo   • Test Frontend: http://localhost:8000/test_frontend.html
echo   • Health Check: http://localhost:8000/health
echo.

echo 📝 Useful Commands:
echo   • View logs: docker-compose -f docker-compose.dev.yml logs -f
echo   • Stop services: docker-compose -f docker-compose.dev.yml down
echo   • Restart API: docker-compose -f docker-compose.dev.yml restart api
echo   • Rebuild: docker-compose -f docker-compose.dev.yml up --build -d
echo.

echo ✅ Setup complete! The API should be running at http://localhost:8000
pause
