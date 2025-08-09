#!/usr/bin/env python3
"""
Database Connection Test Script
Tests MongoDB connection and database setup
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import connect_to_mongo, close_mongo_connection, test_connection
from app.config import settings


async def test_database_setup():
    """Test database connection and setup."""
    print("🧪 Testing Database Connection and Setup")
    print("=" * 50)
    
    try:
        # Test connection
        print("1. Testing MongoDB connection...")
        await connect_to_mongo()
        
        # Test database status
        print("\n2. Testing database status...")
        status = await test_connection()
        print(f"   Status: {status['status']}")
        print(f"   Database: {status.get('database', 'N/A')}")
        
        # Test database info
        print("\n3. Getting database information...")
        from app.database import db
        
        collections = await db.database.list_collection_names()
        print(f"   Collections: {collections}")
        
        # Test database stats
        try:
            db_stats = await db.database.command("dbStats")
            print(f"   Total collections: {db_stats.get('collections', 0)}")
            print(f"   Data size: {db_stats.get('dataSize', 0)} bytes")
            print(f"   Storage size: {db_stats.get('storageSize', 0)} bytes")
        except Exception as e:
            print(f"   Error getting stats: {e}")
        
        print("\n✅ Database setup test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Database test failed: {str(e)}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Make sure MongoDB is running: mongod")
        print("   2. Check if MongoDB is accessible on localhost:27017")
        print("   3. Verify your .env file configuration")
        return False
    
    finally:
        await close_mongo_connection()


async def main():
    """Main function to run the database test."""
    print("🚀 Payment Gateway API - Database Connection Test")
    print("=" * 60)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  .env file not found. Using default configuration.")
        print("   You can create one with: cp env.example .env")
    
    # Run the test
    success = await test_database_setup()
    
    if success:
        print("\n🎉 All tests passed! Your database is ready.")
        print("   You can now start the API with: python run.py")
    else:
        print("\n💥 Tests failed. Please fix the issues before running the API.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
