# MongoDB Database Setup with Beanie ODM

This directory contains the MongoDB database configuration and models using Beanie ODM for the AI service.

## Files

- `database.py` - MongoDB connection management and initialization
- `models.py` - Beanie document models for User, BlackListToken, and Article
- `example_usage.py` - Example code showing how to use the database and models

## Features

### Database Connection

- Async MongoDB connection using Motor
- Connection health checks
- Proper error handling and timeouts
- Beanie ODM initialization

### Authentication Models

#### User Model

- Email-based authentication with unique constraint
- Password hashing using bcrypt
- User roles and permissions
- Account activation status
- Timestamps for creation and updates

#### BlackListToken Model

- JWT token blacklisting for logout functionality
- Automatic cleanup of expired tokens
- Token expiration management

#### Article Model

- Full-text search capabilities
- Author relationship
- Publishing status
- Tags and metadata
- Content management

## Usage

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Make sure your `.env` file contains:

```
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=ai_service
```

### 3. Connect to Database

```python
from app.infraestructure.db.mongo_db.database import connect_to_mongo

# In your FastAPI startup event
await connect_to_mongo()
```

### 4. Use Models

```python
from app.infraestructure.db.mongo_db.models import User

# Create a user
user = await User.create_user(
    email="user@example.com",
    full_name="John Doe",
    password="secure_password"
)

# Authenticate user
authenticated_user = await User.authenticate("user@example.com", "secure_password")
```

## Example

See `example_usage.py` for a complete example of how to use all the models and database functionality.

## Database Indexes

The models automatically create the following indexes for optimal performance:

- **Users**: email (unique), is_active, created_at
- **BlackListTokens**: token (unique), expire, created_at
- **Articles**: author_id, text search (title, content), created_at, is_published
