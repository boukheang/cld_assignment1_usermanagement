# University Central User Management Platform

**Course:** CLD 376 Cloud Native Development  
**Student:** Goat Ronaldo (ID: 2024476)  
**Semester:** Fall 2026  

---

## 1. System Architecture

A distributed identity and user management platform built with NodeJS microservices, an Express API Gateway, and MongoDB Atlas persistence.

```
                  +----------------------------------------------+
                  |           Client / Postman (:4000)          |
                  +----------------------------------------------+
                                         |
                                         v
                         +-------------------------------+
                         |     API Gateway (Port 4000)   |
                         |  - JWT Verification (authToken)|
                         |  - RBAC Enforcement (authRole)|
                         |  - Header Injection (x-user-*)|
                         +-------------------------------+
                                         |
         +--------------------+----------+----------+--------------------+
         |                    |                     |                    |
         v                    v                     v                    v
+------------------+ +------------------+ +------------------+ +------------------+
|   Registration   | |  Authentication  | | Admin Service    | | User Service     |
|   (Port 5001)    | |   (Port 5002)    | | (Port 5003)      | | (Port 5004)      |
|  - Bcrypt Hashing| |  - Credential Auth| | - verifyAdmin    | | - verifyUser     |
|  - Unique Email  | |  - 24h JWT Issue | | - /searchuser    | | - /viewprofile   |
|  - Unique Num ID | |  - Role Match Chk| | - /viewalluser   | | - /updateprofile |
|  - /userregister | |  - /login        | | - /deluser       | |                  |
+------------------+ +------------------+ +------------------+ +------------------+
         |                    |                     |                    |
         +--------------------+----------+----------+--------------------+
                                         |
                                         v
                      +-------------------------------------+
                      |      MongoDB Atlas (UserData)       |
                      |       (person_collections)          |
                      +-------------------------------------+
```

---

## 2. Microservice Port & Route Mapping

| Microservice | Port | Gateway Public Route | Internal Microservice Route | Protection Level |
|---|---|---|---|---|
| **API Gateway** | `4000` | `http://localhost:4000` | Single Entry Point | Reverse Proxy & Gatekeeper |
| **Registration** | `5001` | `POST /register/userregister`<br>`POST /register/reg` | `POST /userregister`<br>`POST /reg` | Public (Validation & Bcrypt) |
| **Authentication** | `5002` | `POST /auth/login`<br>`POST /login` | `POST /login` | Public (Issues 24h JWT) |
| **Admin Service** | `5003` | `GET /admin/searchuser`<br>`GET /admin/viewalluser`<br>`DELETE /admin/deluser` | `GET /searchuser`<br>`GET /viewalluser`<br>`DELETE /deluser` | **Two-Tier Protected**<br>(Gateway `admin` + `verifyAdmin`) |
| **User Service** | `5004` | `GET /user/viewprofile`<br>`PUT /user/updateprofile` | `GET /viewprofile`<br>`PUT /updateprofile` | **Two-Tier Protected**<br>(Gateway `user` + `verifyUser`) |

---

## 3. Key Enhancements Addressing Professor Feedback

### A. Clean Internal Route Resolution
- Microservices strictly expose clean, single endpoints (`/viewprofile`, `/updateprofile`, `/searchuser`, `/viewalluser`, `/deluser`, `/reg`, `/login`).
- Eliminates dual-array alias confusion (`['/user/viewprofile', '/viewprofile']`).
- Express mount prefixes (`app.use('/admin', ...)`) in the API Gateway strip the path prefix before forwarding (`proxy.web`), allowing downstream microservices to maintain standard, clean routes.

### B. Two-Tier Authentication Defense (Proxy Protection)
- **Tier 1 (API Gateway Tier):**
  - `authToken` intercepts incoming requests, verifies JWT validity and 24h expiration, and rejects unauthenticated calls (401/403).
  - `authRole('admin')` and `authRole('user')` enforce strict mutual exclusion (User cannot access Admin; Admin cannot access User).
  - Gateway injects verified identity headers (`x-user-id`, `x-user-email`, `x-user-role`).
- **Tier 2 (Microservice Defense-in-Depth Tier):**
  - Backend services enforce `verifyAdmin` (Port 5003) and `verifyUser` (Port 5004).
  - If an attacker attempts to bypass the API Gateway by querying internal ports directly, the microservice inspects the Bearer token and rejects unauthorized calls with `401 Unauthorized`.

---

## 4. Database Schema (`person_schema.js`)

Each user document in MongoDB Atlas `UserData.person_collections` contains:
```javascript
{
  _id: Number,         // Unique numeric ID (e.g. 7593)
  name: String,        // Full name
  email: String,       // Unique email address
  password: String,    // Bcrypt salted hash
  role: String,        // 'admin' or 'user'
  phone: Number,       // Contact number
  createdAt: Date,     // Auto-generated timestamp
  updatedAt: Date      // Auto-generated timestamp
}
```

---

## 5. Getting Started

### Prerequisites
- Node.js (v18+)
- MongoDB Atlas cluster or local MongoDB instance

### Installation
```bash
npm install
```

### Starting Services
To start all 5 services simultaneously:
```bash
node start_all.js
```

Or start individual services independently:
```bash
npm run start:gateway
npm run start:register
npm run start:auth
npm run start:admin
npm run start:user
```

### Running Automated Test Suite
```bash
node test_suite.js
```
