# System Design Documentation
## Email Notification System for Web Application

---

## 📋 **System Overview**

The Email Notification System is a REST API-based backend service that handles user registration and automatically sends welcome emails using SendGrid. The system stores user data in a simple JSON file-based database and provides endpoints for user management.

### **Primary Goals:**
- Automatically send welcome emails to new users upon registration
- Store user registration data persistently
- Provide API endpoints for user management
- Maintain simple, scalable architecture

---

## 🏗️ **Architecture Diagram**

```
┌─────────────────┐    HTTP/HTTPS     ┌─────────────────┐
│                 │    Requests       │                 │
│   Client Apps   │◄─────────────────►│   FastAPI       │
│                 │    JSON           │   Backend       │
│ • Web Frontend  │    Responses      │                 │
│ • Mobile App    │                   │ • REST API      │
│ • Postman       │                   │ • Request       │
│ • curl          │                   │   Validation    │
└─────────────────┘                   │ • Error         │
                                       │   Handling      │
                                       └─────────────────┘
                                                │
                                                │
                    ┌───────────────────────────┼───────────────────────────┐
                    │                           │                           │
                    ▼                           ▼                           ▼
        ┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
        │                 │         │                 │         │                 │
        │  User Storage   │         │ Email Service   │         │   SendGrid      │
        │                 │         │                 │         │     API         │
        │ • JSON File     │         │ • Template      │         │                 │
        │   Database      │         │   Generation    │         │ • Email         │
        │ • CRUD Ops      │         │ • Email         │         │   Delivery      │
        │ • File I/O      │         │   Formatting    │         │ • Status        │
        │                 │         │ • SendGrid      │         │   Tracking      │
        │ data/users.json │         │   Integration   │         │ • Bounce        │
        │                 │         │                 │         │   Handling      │
        └─────────────────┘         └─────────────────┘         └─────────────────┘
```

---

## 🔄 **System Flow Diagrams**

### **User Registration Flow**
```
┌─────────┐    POST /user-signup     ┌─────────────┐
│ Client  │──────────────────────────►│   FastAPI   │
│         │  {email, name}           │             │
└─────────┘                          └─────────────┘
                                              │
                                              ▼
                                     ┌─────────────┐
                                     │Check if user│
                                     │   exists    │
                                     └─────────────┘
                                              │
                              ┌───────────────┴───────────────┐
                              │                               │
                              ▼                               ▼
                    ┌─────────────┐                 ┌─────────────┐
                    │User exists? │                 │  New user   │
                    │Return error │                 │             │
                    └─────────────┘                 └─────────────┘
                                                            │
                                                            ▼
                                                   ┌─────────────┐
                                                   │Save to JSON │
                                                   │    file     │
                                                   └─────────────┘
                                                            │
                                                            ▼
                                                   ┌─────────────┐
                                                   │Send welcome │
                                                   │   email     │
                                                   └─────────────┘
                                                            │
                                                            ▼
                                                   ┌─────────────┐
                                                   │Return user  │
                                                   │    data     │
                                                   └─────────────┘
```

### **Email Sending Flow**
```
┌─────────────┐    Email Request     ┌─────────────┐
│Email Service│◄─────────────────────│   FastAPI   │
│             │                      │ Controller  │
└─────────────┘                      └─────────────┘
       │
       ▼
┌─────────────┐
│Load Email   │
│Template     │
└─────────────┘
       │
       ▼
┌─────────────┐
│Generate HTML│
│Content      │
└─────────────┘
       │
       ▼
┌─────────────┐    HTTPS API Call    ┌─────────────┐
│Send to      │─────────────────────►│  SendGrid   │
│SendGrid     │                      │    API      │
└─────────────┘                      └─────────────┘
       │                                     │
       ▼                                     ▼
┌─────────────┐                      ┌─────────────┐
│Return       │◄─────────────────────│Email Status │
│Response     │                      │   Code      │
└─────────────┘                      └─────────────┘
```

---

## 🗄️ **Database Schema (JSON File Structure)**

### **File Location:** `backend/data/users.json`

### **Schema Structure:**
```json
{
  "users": [
    {
      "id": "string (UUID)",
      "name": "string",
      "email": "string (email format)",
      "registration_date": "string (ISO datetime)",
      "email_sent": "boolean",
      "email_sent_at": "string (ISO datetime)",
      "status": "string (active/inactive)",
      "created_at": "string (ISO datetime)",
      "updated_at": "string (ISO datetime)"
    }
  ],
  "metadata": {
    "total_users": "number",
    "last_updated": "string (ISO datetime)",
    "schema_version": "string"
  }
}
```

### **Sample Data:**
```json
{
  "users": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "name": "John Doe",
      "email": "john.doe@example.com",
      "registration_date": "2024-01-15T10:30:45.123456Z",
      "email_sent": true,
      "email_sent_at": "2024-01-15T10:30:46.789012Z",
      "status": "active",
      "created_at": "2024-01-15T10:30:45.123456Z",
      "updated_at": "2024-01-15T10:30:45.123456Z"
    }
  ],
  "metadata": {
    "total_users": 1,
    "last_updated": "2024-01-15T10:30:45.123456Z",
    "schema_version": "1.0"
  }
}
```

### **Data Constraints:**
- **id**: Unique UUID for each user
- **email**: Must be valid email format, unique across all users
- **name**: Non-empty string, max 255 characters
- **registration_date**: ISO 8601 datetime format
- **status**: Enum values: "active", "inactive", "suspended"
- **email_sent**: Boolean tracking welcome email delivery

---

## 📡 **API Specification Document**

### **Base URL:** `http://localhost:8000`

### **Authentication:** None (for demo purposes)

### **Content-Type:** `application/json`

---

## 🔗 **API Endpoints Specification**

### **1. Health Check**
```http
GET /health
```
**Description:** Check if API is running  
**Parameters:** None  
**Response:**
```json
{
  "status": "healthy"
}
```

---

### **2. User Registration**
```http
POST /user-signup
```
**Description:** Register new user and send welcome email  
**Request Body:**
```json
{
  "to_email": "user@example.com",
  "user_name": "John Doe"
}
```
**Validation Rules:**
- `to_email`: Required, valid email format
- `user_name`: Required, 1-255 characters

**Success Response (201):**
```json
{
  "success": true,
  "message": "User John Doe signed up successfully! Welcome email sent.",
  "user_email": "user@example.com",
  "user_id": "550e8400-e29b-41d4-a716-446655440001",
  "signup_time": "2024-01-15T10:30:45.123456Z",
  "stored_in_file": true,
  "email_result": {
    "status_code": 202,
    "body": "",
    "headers": {}
  }
}
```

**Error Response - User Exists (409):**
```json
{
  "success": false,
  "message": "User with email user@example.com already exists!",
  "user_email": "user@example.com",
  "existing_user_id": "550e8400-e29b-41d4-a716-446655440001",
  "registered_date": "2024-01-15T10:30:45.123456Z"
}
```

---

### **3. Get All Users**
```http
GET /users
```
**Description:** Retrieve all registered users  
**Parameters:** None

**Success Response (200):**
```json
{
  "success": true,
  "message": "Retrieved all users successfully",
  "total_users": 2,
  "users": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "name": "John Doe",
      "email": "john.doe@example.com",
      "registration_date": "2024-01-15T10:30:45.123456Z",
      "status": "active"
    }
  ]
}
```

---

### **4. Send Custom Email**
```http
POST /send-email
```
**Description:** Send custom email to any recipient  
**Request Body:**
```json
{
  "to_email": "recipient@example.com",
  "subject": "Email Subject",
  "message": "Email content here",
  "from_name": "Sender Name"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Email sent successfully",
  "result": {
    "status_code": 202,
    "body": "",
    "headers": {}
  }
}
```

---

### **5. Send Welcome Email**
```http
POST /send-welcome-email
```
**Description:** Send welcome email template to user  
**Request Body:**
```json
{
  "to_email": "user@example.com",
  "user_name": "John Doe"
}
```

---

### **6. Send Notification Email**
```http
POST /send-notification-email
```
**Description:** Send notification email with priority levels  
**Request Body:**
```json
{
  "to_email": "user@example.com",
  "notification_type": "Account Activity",
  "message": "Notification content",
  "priority": "Medium"
}
```
**Priority Levels:** Low, Medium, High, Critical

---

## 🔧 **System Components**

### **1. FastAPI Application (app.py)**
- **Purpose:** Main application server and API routing
- **Responsibilities:**
  - Handle HTTP requests/responses
  - Request validation using Pydantic models
  - Route management and middleware
  - Error handling and exception management
  - CORS configuration

### **2. Email Service (utils/email_service.py)**
- **Purpose:** Email template generation and delivery
- **Responsibilities:**
  - HTML email template creation
  - SendGrid API integration
  - Email formatting and styling
  - Delivery status tracking
  - Error handling for email failures

### **3. User Storage Service (utils/user_storage.py)**
- **Purpose:** File-based user data management
- **Responsibilities:**
  - JSON file read/write operations
  - User data validation and storage
  - Duplicate user checking
  - Data retrieval and filtering
  - File locking for concurrent access

### **4. Configuration Management**
- **Environment Variables (.env):**
  - `SENDGRID_API_KEY`: SendGrid authentication
  - `FROM_EMAIL`: Verified sender email address
- **Application Settings:**
  - CORS origins configuration
  - File paths and directory structure
  - Email template settings

---

## 🔄 **Data Flow Architecture**

### **Request Processing Pipeline:**
```
Client Request → FastAPI Router → Request Validation → Business Logic → External APIs → Response
```

### **User Registration Pipeline:**
```
POST Request → Validate Input → Check Duplicates → Save to JSON → Send Email → Return Response
```

### **Email Sending Pipeline:**
```
Email Request → Template Selection → HTML Generation → SendGrid API → Status Response
```

---

## 🛡️ **Security Considerations**

### **Current Security Measures:**
- Input validation using Pydantic models
- Email format validation
- Error handling without exposing sensitive data

### **Security Recommendations for Production:**
- API rate limiting
- Request authentication/authorization
- Input sanitization for XSS prevention
- HTTPS enforcement
- Environment variable encryption
- File access permissions
- Request logging and monitoring

---

## 📈 **Scalability Considerations**

### **Current Limitations:**
- File-based storage not suitable for high concurrency
- No caching mechanism
- Single server deployment
- No load balancing

### **Scalability Improvements:**
- Database migration (PostgreSQL/MongoDB)
- Redis caching layer
- Queue system for email processing (Celery/RQ)
- Horizontal scaling with load balancers
- CDN for static assets
- Microservices architecture

---

## 🔍 **Monitoring and Logging**

### **Current Logging:**
- Basic error logging to console
- SendGrid API response tracking

### **Recommended Monitoring:**
- Application performance monitoring (APM)
- Email delivery rate tracking
- Error rate and response time metrics
- User registration analytics
- File system monitoring
- SendGrid webhook integration

---

## 🚀 **Deployment Architecture**

### **Development Environment:**
```
Local Machine → Python Virtual Environment → FastAPI Dev Server → Local File Storage
```

### **Production Recommendations:**
```
Load Balancer → Docker Containers → FastAPI + Gunicorn → Database Cluster → Email Service
```

This system design provides a solid foundation for the email notification system while maintaining simplicity and room for future growth.