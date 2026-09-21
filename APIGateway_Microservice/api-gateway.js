const express = require('express');
const cors = require('cors');
const httpProxy = require('http-proxy');
const jwt = require('jsonwebtoken');
require('dotenv').config();

const app = express();
app.use(cors());

// USE PROXY SERVER TO REDIRECT THE INCOMING REQUEST
const proxy = httpProxy.createProxyServer();

// Handle proxy errors gracefully
proxy.on('error', (err, req, res) => {
    console.error("API Gateway Proxy Error:", err.message);
    if (!res.headersSent) {
        res.status(502).json({ message: "Bad Gateway: Target microservice is unavailable.", error: err.message });
    }
});

const PORT = process.env.PORT || 4000;
const JWT_SECRETE = process.env.JWT_SECRETE || '347186591486#^%%ABCF*##GHE';

// TASK 7: Token Validation Middleware
function authToken(req, res, next) {
    const authHeader = req.headers['authorization'];
    if (!authHeader) {
        return res.status(401).json({ message: "Please send token" });
    }

    let token = authHeader;
    if (authHeader.startsWith('Bearer ') || authHeader.startsWith('bearer ')) {
        token = authHeader.substring(7).trim();
    } else if (authHeader.includes(' ')) {
        token = authHeader.split(' ')[1].trim();
    }

    if (!token) {
        return res.status(401).json({ message: "Please send token" });
    }

    jwt.verify(token, JWT_SECRETE, (err, user) => {
        if (err) {
            if (err.name === 'TokenExpiredError') {
                return res.status(401).json({ message: "Expired token", error: err.message });
            }
            return res.status(403).json({ message: "Invalid token", error: err.message });
        }
        req.user = user;

        // Forward verified user identity in proxy request headers
        req.headers['x-user-id'] = user.id || user._id;
        req.headers['x-user-email'] = user.email;
        req.headers['x-user-role'] = user.role;
        next();
    });
}

// TASK 7: Role-Based Access Control (RBAC) Middleware
function authRole(role) {
    return (req, res, next) => {
        if (!req.user || req.user.role !== role) {
            return res.status(403).json({ message: "Unauthorized: Access denied for this role" });
        }
        next();
    };
}

// ==========================================
// TASK 4: API GATEWAY ROUTING DEFINITIONS
// Single entry point (:4000) for all clients
// ==========================================

// REDIRECT TO THE REGISTRATION MICROSERVICE (Port 5001)
app.use(['/register', '/reg'], (req, res) => {
    console.log(`--> API GATEWAY: Routing ${req.method} ${req.originalUrl} to Registration Microservice (Port 5001)`);
    proxy.web(req, res, { target: 'http://localhost:5001' });
});

// REDIRECT TO THE LOGIN (Authentication) MICROSERVICE (Port 5002)
app.use(['/auth', '/login'], (req, res) => {
    console.log(`--> API GATEWAY: Routing ${req.method} ${req.originalUrl} to Authentication Microservice (Port 5002)`);
    proxy.web(req, res, { target: 'http://localhost:5002' });
});

// REDIRECT TO THE ADMIN MICROSERVICE (Port 5003) - Role 'admin' ONLY
app.use('/admin', authToken, authRole('admin'), (req, res) => {
    console.log(`--> API GATEWAY: Routing ${req.method} ${req.originalUrl} to Admin Microservice (Port 5003)`);
    proxy.web(req, res, { target: 'http://localhost:5003' });
});

// REDIRECT TO THE USER MICROSERVICE (Port 5004) - Role 'user' ONLY
app.use('/user', authToken, authRole('user'), (req, res) => {
    console.log(`--> API GATEWAY: Routing ${req.method} ${req.originalUrl} to User Microservice (Port 5004)`);
    proxy.web(req, res, { target: 'http://localhost:5004' });
});

app.listen(PORT, () => {
    console.log("API Gateway Service is running on PORT NO : " + PORT);
});