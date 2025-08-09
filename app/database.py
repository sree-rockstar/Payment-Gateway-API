from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings
import asyncio


class Database:
    client: AsyncIOMotorClient = None
    database = None


db = Database()


async def check_and_create_database():
    """Check if database exists and create it if needed."""
    try:
        # List all databases
        database_list = await db.client.list_database_names()
        
        if settings.database_name not in database_list:
            print(f"Database '{settings.database_name}' not found. Creating...")
            # Create database by inserting a document
            await db.database.create_collection("_init")
            await db.database._init.insert_one({"created": True})
            await db.database._init.delete_one({"created": True})
            print(f"✅ Database '{settings.database_name}' created successfully!")
        else:
            print(f"✅ Database '{settings.database_name}' already exists.")
            
        # Check and create collections if they don't exist
        collections = await db.database.list_collection_names()
        
        if "users" not in collections:
            print("Creating 'users' collection...")
            await db.database.create_collection("users")
            print("✅ 'users' collection created.")
        else:
            print("✅ 'users' collection already exists.")
            
        if "payments" not in collections:
            print("Creating 'payments' collection...")
            await db.database.create_collection("payments")
            print("✅ 'payments' collection created.")
        else:
            print("✅ 'payments' collection already exists.")
            
    except Exception as e:
        print(f"❌ Error checking/creating database: {str(e)}")
        raise


async def connect_to_mongo():
    """Create database connection with automatic database creation."""
    try:
        print("🔌 Connecting to MongoDB...")
        db.client = AsyncIOMotorClient(settings.mongodb_url)
        
        # Test the connection
        await db.client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # Set the database
        db.database = db.client[settings.database_name]
        
        # Check and create database/collections
        await check_and_create_database()
        
        print("🎉 Database setup completed successfully!")
        
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {str(e)}")
        print("💡 Make sure MongoDB is running on localhost:27017")
        print("   You can start MongoDB with: mongod")
        raise


async def close_mongo_connection():
    """Close database connection."""
    if db.client:
        db.client.close()
        print("🔌 Disconnected from MongoDB.")


def get_database():
    """Get database instance."""
    return db.database


async def test_connection():
    """Test database connection and return status."""
    try:
        await db.client.admin.command('ping')
        return {"status": "connected", "database": settings.database_name}
    except Exception as e:
        return {"status": "disconnected", "error": str(e)}
