const express = require('express');
const app = express();

// USE PROXY SERVER TO REDIRECT THE INCOMING REQUEST
const httpProxy = require('http-proxy');
const proxy = httpProxy.createProxyServer();

const jwt = require('jsonwebtoken');
require('dotenv').config();
const JWT_SECRETE = process.env.JWT_SECRETE;

// Microservice URLs (Configurable via environment variables for multi-EC2 setup)
const ADMIN_SERVICE_URL = process.env.ADMIN_SERVICE_URL || 'http://localhost:5003';
const USER_SERVICE_URL = process.env.USER_SERVICE_URL || 'http://localhost:5004';
const REG_SERVICE_URL = process.env.REG_SERVICE_URL || 'http://localhost:5001/reg';
const LOGIN_SERVICE_URL = process.env.LOGIN_SERVICE_URL || 'http://localhost:5002/login';

// Error handler to prevent API Gateway crash if target service is unreachable
proxy.on('error', (err, req, res) => {
    console.error('[API Gateway] Proxy Error:', err.message);
    if (!res.headersSent) {
        res.status(502).json({
            message: "Bad Gateway. Target microservice is unreachable.",
            error: err.message
        });
    }
});

function authToken(req, res, next) {
    console.log(req.headers.authorization);
    const header = req?.headers.authorization;
    const token = header && header.split(' ')[1];

    if (token == null) return res.status(401).json("Please send token");

    jwt.verify(token, JWT_SECRETE, (err, user) => {
        if (err) return res.status(403).json("Invalid token", err);
        req.user = user;
        next();
    });
}

function authRole(role) {
    return (req, res, next) => {
        if (req.user.role !== role) {
            return res.status(403).json("Unauthorized");
        }
        next();
    };
}

// REDIRECT TO THE REGISTRATION MICROSERVICE (EC2 #1 Localhost:5001)
app.use('/reg', (req, res) => {
    proxy.web(req, res, { target: REG_SERVICE_URL });
});

// REDIRECT TO THE LOGIN (Authentication) MICROSERVICE (EC2 #1 Localhost:5002)
app.use('/login', (req, res) => {
    proxy.web(req, res, { target: LOGIN_SERVICE_URL });
});

// REDIRECT TO THE ADMIN MICROSERVICE (EC2 #2 Port 5003)
app.use('/admin', authToken, authRole('admin'), (req, res) => {
    console.log("INSIDE API GATEWAY ADMIN ROUTE -> Forwarding to Admin Service at:", ADMIN_SERVICE_URL);
    proxy.web(req, res, { target: ADMIN_SERVICE_URL });
});

// REDIRECT TO THE USER MICROSERVICE (EC2 #3 Port 5004)
app.use('/user', authToken, authRole('user'), (req, res) => {
    console.log("INSIDE API GATEWAY USER ROUTE -> Forwarding to User Service at:", USER_SERVICE_URL);
    proxy.web(req, res, { target: USER_SERVICE_URL });
});

app.listen(4000, () => {
    console.log("API Gateway Service is running on PORT NO : 4000");
    console.log("Admin Target URL:", ADMIN_SERVICE_URL);
    console.log("User Target URL:", USER_SERVICE_URL);
});
