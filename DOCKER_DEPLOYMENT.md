# 🐳 Docker Deployment Guide

This guide will help you deploy the Payment Gateway API using Docker and Docker Compose.

## 📋 Prerequisites

- Docker Desktop installed and running
- Docker Compose available
- At least 2GB of available RAM
- Ports 8000, 27017, 80, and 443 available

## 🚀 Quick Start

### 1. Automatic Deployment (Recommended)

```bash
# Deploy in production mode
./deploy.sh

# Deploy in development mode (with volume mounts)
./deploy.sh dev

# Show help
./deploy.sh help
```

### 2. Manual Deployment

```bash
# Build and start all services
docker-compose up --build -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

## 🏗️ Architecture

The deployment includes the following services:

### Services
- **API**: FastAPI application (Port 8000)
- **MongoDB**: Database (Port 27017)
- **Nginx**: Reverse proxy with SSL (Ports 80, 443)

### Networks
- **payment_network**: Internal network for service communication

### Volumes
- **mongodb_data**: Persistent MongoDB data storage
- **logs**: Application logs

## 🔧 Configuration

### Environment Variables

Set these environment variables before deployment:

```bash
# Razorpay Configuration
export RAZORPAY_KEY_ID=your_razorpay_key_id
export RAZORPAY_KEY_SECRET=your_razorpay_key_secret

# JWT Configuration
export SECRET_KEY=your-secret-key-here-make-it-long-and-secure
```

### Docker Compose Files

- **docker-compose.yml**: Production configuration
- **docker-compose.dev.yml**: Development configuration with volume mounts

## 📊 Service Information

### API Service
- **Image**: Built from local Dockerfile
- **Port**: 8000
- **Health Check**: `/health` endpoint
- **Dependencies**: MongoDB

### MongoDB Service
- **Image**: mongo:6.0
- **Port**: 27017
- **Authentication**: admin/password123
- **Database**: Payment-Gateway
- **Initialization**: mongo-init.js

### Nginx Service
- **Image**: nginx:alpine
- **Ports**: 80 (HTTP), 443 (HTTPS)
- **SSL**: Self-signed certificates
- **Rate Limiting**: Configured for API protection

## 🧪 Testing the Deployment

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. Test Credentials
- **Email**: test@example.com
- **Password**: testpass123

### 4. API Testing
```bash
# Test authentication
curl -X POST "http://localhost:8000/auth/signin" \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"testpass123"}'

# Test payment creation (requires JWT token)
curl -X POST "http://localhost:8000/payments/create-payment" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"amount":1000,"currency":"INR","description":"Test payment"}'
```

## 🔍 Monitoring and Logs

### View Service Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f mongodb
docker-compose logs -f nginx
```

### Service Status
```bash
# Check service health
docker-compose ps

# Check container resources
docker stats
```

### Database Access
```bash
# Connect to MongoDB
docker-compose exec mongodb mongosh -u admin -p password123

# Backup database
docker-compose exec mongodb mongodump --out /backup
```

## 🛠️ Development Mode

For development with live code reloading:

```bash
# Deploy in development mode
./deploy.sh dev

# Or manually
docker-compose -f docker-compose.dev.yml up --build -d
```

**Development Features:**
- Volume mounts for live code changes
- Hot reloading
- Development-specific environment variables
- Easier debugging

## 🔒 Security Considerations

### Production Deployment
1. **Change Default Passwords**:
   - MongoDB admin password
   - JWT secret key
   - API secret keys

2. **SSL Certificates**:
   - Replace self-signed certificates with real ones
   - Configure proper domain names

3. **Environment Variables**:
   - Use proper Razorpay production keys
   - Set strong JWT secrets
   - Configure proper CORS settings

4. **Network Security**:
   - Configure firewall rules
   - Use proper network segmentation
   - Enable rate limiting

### Security Checklist
- [ ] Change MongoDB admin password
- [ ] Set strong JWT secret key
- [ ] Use production Razorpay keys
- [ ] Configure proper SSL certificates
- [ ] Set up proper logging
- [ ] Configure backup strategy
- [ ] Set up monitoring and alerting

## 🚨 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Check what's using the port
lsof -i :8000

# Stop conflicting services
sudo systemctl stop conflicting-service
```

#### 2. MongoDB Connection Issues
```bash
# Check MongoDB logs
docker-compose logs mongodb

# Restart MongoDB
docker-compose restart mongodb
```

#### 3. API Not Starting
```bash
# Check API logs
docker-compose logs api

# Check environment variables
docker-compose exec api env
```

#### 4. SSL Certificate Issues
```bash
# Regenerate SSL certificates
rm -rf ssl/
./deploy.sh
```

### Debug Commands
```bash
# Enter API container
docker-compose exec api bash

# Check MongoDB connection
docker-compose exec api python -c "from app.database import connect_to_mongo; import asyncio; asyncio.run(connect_to_mongo())"

# Test API endpoints
docker-compose exec api curl http://localhost:8000/health
```

## 📈 Scaling

### Horizontal Scaling
```bash
# Scale API service
docker-compose up --scale api=3 -d

# Scale with load balancer
docker-compose -f docker-compose.yml -f docker-compose.scale.yml up -d
```

### Performance Optimization
1. **Database Indexing**: Already configured in mongo-init.js
2. **Connection Pooling**: Configured in database.py
3. **Caching**: Consider adding Redis
4. **Load Balancing**: Nginx configured for multiple API instances

## 🔄 Backup and Recovery

### Database Backup
```bash
# Create backup
docker-compose exec mongodb mongodump --out /backup/$(date +%Y%m%d_%H%M%S)

# Restore backup
docker-compose exec mongodb mongorestore /backup/backup_name
```

### Volume Backup
```bash
# Backup MongoDB data
docker run --rm -v payment_gateway_mongodb_data:/data -v $(pwd):/backup alpine tar czf /backup/mongodb_backup.tar.gz -C /data .

# Restore MongoDB data
docker run --rm -v payment_gateway_mongodb_data:/data -v $(pwd):/backup alpine tar xzf /backup/mongodb_backup.tar.gz -C /data
```

## 🧹 Cleanup

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Remove Everything
```bash
# Remove containers, networks, volumes, and images
docker-compose down --rmi all --volumes --remove-orphans
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)

---

**Deployment Status**: ✅ Ready for production deployment  
**Last Updated**: January 2024
