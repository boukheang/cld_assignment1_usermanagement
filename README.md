# Role-Based User Management System Using Microservices API Gateway, NodeJS & MongoDB

**Course:** CLD 376 - Cloud Native Development  
**Student:** Try Boukheang (ID: 2024476)  
**Assignment:** 01. Role-Based User Management System Using Microservices API Gateway NodeJS MongoDB  

---

## 🏛️ Project Overview & Scenario
A university Central Identity and User Management Platform developed as independent microservices communicating through an API Gateway with MongoDB persistence.

The platform distinguishes two types of users:
1. **User (Student/Staff):** Manage their own personal profile (`/user/*`).
2. **Admin (University Administrator):** Manage student/staff user accounts (`/admin/*`).

### 🛡️ Security Requirement
- **Ordinary users can NEVER access administrative APIs** (enforced with `403 Forbidden`).
- **Administrators can NEVER access user-only APIs** (enforced with `403 Forbidden`).
- **Unauthenticated requests are strictly rejected** at the API Gateway before reaching internal microservices.

---

## 🏗️ System Architecture & Microservices

| Microservice | Port | Route via Gateway (`:4000`) | Description |
| :--- | :--- | :--- | :--- |
| **API Gateway** | `4000` | `http://localhost:4000/` | Single entry point, JWT validation, role-based access guard, reverse proxy |
| **Registration Microservice** | `5001` | `POST /register/userregister` | Validates input, enforces unique email, bcrypt password hash, saves to MongoDB |
| **Login Microservice** | `5002` | `POST /auth/login` | Validates email/password/role, generates 24-hour signed JWT token |
| **Admin Microservice** | `5003` | `GET /admin/searchuser`<br>`GET /admin/viewalluser`<br>`DELETE /admin/deluser` | Administrative user search, viewing all users, and deleting accounts |
| **User Microservice** | `5004` | `GET /user/viewprofile`<br>`PUT /user/updateprofile` | Viewing own profile and updating personal profile details |

```
Client (Postman)
       ↓
API GATEWAY (:4000) ──[JWT & Role Verification]
  ├── POST /register/* ──────────► Registration Microservice (:5001) ──► MongoDB
  ├── POST /auth/* ──────────────► Login Microservice (:5002) ────────► MongoDB
  ├── [Admin Only] /admin/* ─────► Admin Microservice (:5003) ────────► MongoDB
  └── [User Only] /user/* ───────► User Microservice (:5004) ─────────► MongoDB
```

---

## 🗄️ MongoDB User Model Schema
```json
{
  "_id": "ObjectId(...)",
  "name": "Try Boukheang",
  "email": "student@university.edu",
  "password": "$2a$10$hashed_password_with_bcrypt...",
  "role": "user",
  "phone": "+85512345678",
  "createdAt": "2026-09-14T08:29:30.779Z",
  "updatedAt": "2026-09-14T08:29:36.223Z"
}
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Node.js (v18+)
- MongoDB Atlas cluster or local MongoDB instance

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/boukheang/cld_assignment1_usermanagement.git
cd cld_assignment1_usermanagement

# Install dependencies
npm install
```

### 3. Environment Configuration
Create a `.env` file in the root directory (or copy from `.env.example`):
```env
MONGODB_URI=your_mongodb_connection_string
JWT_SECRET=your_jwt_secret
GATEWAY_PORT=4000
REGISTRATION_PORT=5001
LOGIN_PORT=5002
ADMIN_PORT=5003
USER_PORT=5004
```

### 4. Start All 5 Microservices
Run the unified orchestrator script:
```bash
node start_all.js
```

### 5. Run the Automated End-to-End Test Suite
```bash
node test_suite.js
```

---

## 📡 API Reference

### 1. Registration (`POST /register/userregister`)
- **URL:** `http://localhost:4000/register/userregister`
- **Method:** `POST`
- **Body:**
```json
{
  "name": "Try Boukheang",
  "email": "student@university.edu",
  "password": "SecurePassword123!",
  "role": "user",
  "phone": "+85512345678"
}
```
- **Response (201 Created):** Returns user object (password omitted). Rejects duplicate emails with `400 Bad Request`.

### 2. Authentication (`POST /auth/login`)
- **URL:** `http://localhost:4000/auth/login`
- **Method:** `POST`
- **Body:**
```json
{
  "email": "student@university.edu",
  "password": "SecurePassword123!",
  "role": "user"
}
```
- **Response (200 OK):** Returns 24-hour signed JWT token and user info.

### 3. Admin Operations (Requires Admin Bearer Token)
- **View All Users:** `GET http://localhost:4000/admin/viewalluser`
- **Search User by Query:** `GET http://localhost:4000/admin/searchuser?email=student@university.edu` or `?name=Boukheang`
- **Delete User:** `DELETE http://localhost:4000/admin/deluser?email=student@university.edu`

### 4. User Profile Operations (Requires User Bearer Token)
- **View Profile:** `GET http://localhost:4000/user/viewprofile`
- **Update Profile:** `PUT http://localhost:4000/user/updateprofile`
  - Body: `{ "name": "Updated Name", "phone": "+85599887766" }`

---

## 🔒 Security Gatekeeper Verification (Task 10)
| Test Case | Request | Result | Status |
| :--- | :--- | :--- | :--- |
| **10.a** | Access protected route without token | Rejected: "No token provided" | `401 Unauthorized` |
| **10.b** | Access protected route with invalid token | Rejected: "Invalid token" | `403 Forbidden` |
| **10.c** | Admin token accessing `/user/viewprofile` | Rejected: "Admins cannot access User APIs" | `403 Forbidden` |
| **10.d** | User token accessing `/admin/viewalluser` | Rejected: "Users cannot access Admin APIs" | `403 Forbidden` |

---

## 📄 Submission Documents
- Word Report: `Role_Based_User_Management_Submission.docx`
- Canvas Submission PDF: `Role_Based_User_Management_Submission.pdf` (19 pages with 22 captioned screenshots and headings)
