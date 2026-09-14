const express = require('express');
const httpProxy = require('http-proxy');
const jwt = require('jsonwebtoken');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());

// Create HTTP Proxy instance
const proxy = httpProxy.createProxyServer();

// Handle proxy errors gracefully
proxy.on('error', (err, req, res) => {
  console.error("API Gateway Proxy Error:", err.message);
  if (!res.headersSent) {
    res.status(502).json({
      success: false,
      message: "Bad Gateway: Target microservice is unavailable or connection was refused.",
      error: err.message
    });
  }
});

const PORT = process.env.GATEWAY_PORT || 4000;
const JWT_SECRET = process.env.JWT_SECRET || '347186591486#^%%ABCF*##GHE';

// TASK 7: Token Validation and Role-Based Access Control (RBAC) Middleware
function verifyTokenAndRole(allowedRole) {
  return (req, res, next) => {
    const authHeader = req.headers['authorization'];

    // 1. Check if token is present
    if (!authHeader) {
      console.log(`[AUTH REJECTED - NO TOKEN] ${req.method} ${req.originalUrl}`);
      return res.status(401).json({
        success: false,
        message: "Access Denied: No token provided. Authorization header is missing."
      });
    }

    // Extract Bearer token
    let token = authHeader;
    if (authHeader.startsWith('Bearer ') || authHeader.startsWith('bearer ')) {
      token = authHeader.substring(7).trim();
    }

    if (!token) {
      console.log(`[AUTH REJECTED - EMPTY BEARER] ${req.method} ${req.originalUrl}`);
      return res.status(401).json({
        success: false,
        message: "Access Denied: No token provided in Bearer authorization header."
      });
    }

    // 2. Verify token signature and expiration
    jwt.verify(token, JWT_SECRET, (err, decoded) => {
      if (err) {
        if (err.name === 'TokenExpiredError') {
          console.log(`[AUTH REJECTED - EXPIRED TOKEN] ${req.method} ${req.originalUrl}`);
          return res.status(401).json({
            success: false,
            message: "Access Denied: Expired token."
          });
        }
        console.log(`[AUTH REJECTED - INVALID TOKEN] ${req.method} ${req.originalUrl}: ${err.message}`);
        return res.status(403).json({
          success: false,
          message: "Access Denied: Invalid token."
        });
      }

      // 3. Role-Based Access Control (RBAC)
      // Requirement: User must NEVER access Admin APIs; Admin must NEVER access User APIs
      const userRole = (decoded.role || '').toLowerCase();

      if (userRole !== allowedRole.toLowerCase()) {
        console.log(`[ROLE FORBIDDEN] User role '${userRole}' denied access to '${allowedRole}' API: ${req.originalUrl}`);
        if (allowedRole.toLowerCase() === 'admin') {
          return res.status(403).json({
            success: false,
            message: "Access Denied: Admin privileges required. Ordinary users are not permitted to access Admin APIs."
          });
        } else {
          return res.status(403).json({
            success: false,
            message: "Access Denied: User privileges required. Administrators are not permitted to access User APIs."
          });
        }
      }

      // Attach decoded user identity to request headers for microservices
      req.headers['x-user-id'] = decoded.id;
      req.headers['x-user-email'] = decoded.email;
      req.headers['x-user-role'] = decoded.role;

      console.log(`[AUTH SUCCESS] '${userRole}' (${decoded.email}) authorized for ${req.originalUrl}`);
      next();
    });
  };
}

// ==========================================
// TASK 4: API GATEWAY ROUTING DEFINITIONS
// Single entry point for all client requests
// ==========================================

// 1. PUBLIC ROUTE: Registration Microservice (Port 5001)
app.use('/register', (req, res) => {
  console.log(`--> API GATEWAY: Routing ${req.method} ${req.originalUrl} to Registration Microservice (Port 5001)`);
  proxy.web(req, res, { target: 'http://localhost:5001' });
});

// 2. PUBLIC ROUTE: Login Microservice (Port 5002)
app.use('/auth', (req, res) => {
  console.log(`--> API GATEWAY: Routing ${req.method} ${req.originalUrl} to Login Microservice (Port 5002)`);
  proxy.web(req, res, { target: 'http://localhost:5002' });
});

// 3. PROTECTED ROUTE: Admin Microservice (Port 5003) - Role 'admin' ONLY
app.use('/admin', verifyTokenAndRole('admin'), (req, res) => {
  console.log(`--> API GATEWAY: Routing ${req.method} ${req.originalUrl} to Admin Microservice (Port 5003)`);
  proxy.web(req, res, { target: 'http://localhost:5003' });
});

// 4. PROTECTED ROUTE: User Microservice (Port 5004) - Role 'user' ONLY
app.use('/user', verifyTokenAndRole('user'), (req, res) => {
  console.log(`--> API GATEWAY: Routing ${req.method} ${req.originalUrl} to User Microservice (Port 5004)`);
  proxy.web(req, res, { target: 'http://localhost:5004' });
});

// Gateway Status / Health
app.get('/', (req, res) => {
  res.json({
    gateway: "Central Identity & User Management Platform API Gateway",
    status: "Active",
    port: PORT,
    routes: {
      public: ["/register/userregister", "/auth/login"],
      adminProtected: ["/admin/searchuser", "/admin/viewalluser", "/admin/deluser"],
      userProtected: ["/user/viewprofile", "/user/updateprofile"]
    }
  });
});

app.listen(PORT, () => {
  console.log(`API Gateway Microservice is running on PORT NO : ${PORT}`);
});
