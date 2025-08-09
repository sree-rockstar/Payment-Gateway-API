// MongoDB initialization script
// This script runs when the MongoDB container starts for the first time

// Switch to the Payment-Gateway database
db = db.getSiblingDB('Payment-Gateway');

// Create collections with validation
db.createCollection('users', {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["email", "full_name", "hashed_password", "created_at", "updated_at"],
            properties: {
                email: {
                    bsonType: "string",
                    pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
                },
                full_name: {
                    bsonType: "string",
                    minLength: 1,
                    maxLength: 100
                },
                hashed_password: {
                    bsonType: "string"
                },
                created_at: {
                    bsonType: "date"
                },
                updated_at: {
                    bsonType: "date"
                }
            }
        }
    }
});

db.createCollection('payments', {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["order_id", "amount", "currency", "status", "user_id", "created_at", "updated_at"],
            properties: {
                order_id: {
                    bsonType: "string"
                },
                amount: {
                    bsonType: "number",
                    minimum: 0
                },
                currency: {
                    bsonType: "string",
                    minLength: 3,
                    maxLength: 3
                },
                status: {
                    enum: ["pending", "completed", "failed"]
                },
                user_id: {
                    bsonType: "string"
                },
                description: {
                    bsonType: ["string", "null"]
                },
                created_at: {
                    bsonType: "date"
                },
                updated_at: {
                    bsonType: "date"
                }
            }
        }
    }
});

// Create indexes for better performance
db.users.createIndex({ "email": 1 }, { unique: true });
db.users.createIndex({ "created_at": 1 });

db.payments.createIndex({ "order_id": 1 }, { unique: true });
db.payments.createIndex({ "user_id": 1 });
db.payments.createIndex({ "status": 1 });
db.payments.createIndex({ "created_at": 1 });

// Insert a test user if it doesn't exist
const testUser = {
    email: "test@example.com",
    full_name: "Test User",
    hashed_password: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3bp.gS.Oi", // password: testpass123
    created_at: new Date(),
    updated_at: new Date()
};

// Check if test user exists
const existingUser = db.users.findOne({ email: testUser.email });
if (!existingUser) {
    db.users.insertOne(testUser);
    print("Test user created: test@example.com / testpass123");
} else {
    print("Test user already exists");
}

print("MongoDB initialization completed successfully!");
print("Database: Payment-Gateway");
print("Collections: users, payments");
print("Indexes created for better performance");
