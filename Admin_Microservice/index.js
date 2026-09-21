const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.ADMIN_PORT || 5003;
const JWT_SECRET = process.env.JWT_SECRETE || process.env.JWT_SECRET || '347186591486#^%%ABCF*##GHE';

const PersonModel = require('./person_schema.js');
const dbconnect = require('./dbconnect.js');

// ============================================
// JWT + ADMIN AUTHORIZATION MIDDLEWARE
// ============================================
function verifyAdmin(req, res, next) {
    const authHeader = req.headers.authorization;
    if (!authHeader) {
        return res.status(401).json({
            message: "Access denied. Token is required."
        });
    }

    let token = authHeader;
    if (authHeader.startsWith('Bearer ') || authHeader.startsWith('bearer ')) {
        token = authHeader.substring(7).trim();
    } else if (authHeader.includes(' ')) {
        token = authHeader.split(' ')[1].trim();
    }

    if (!token) {
        return res.status(401).json({
            message: "Invalid token format."
        });
    }

    try {
        const decoded = jwt.verify(token, JWT_SECRET);
        if (decoded.role !== 'admin') {
            return res.status(403).json({
                message: "Access denied. Admin only."
            });
        }
        req.user = decoded;
        next();
    } catch (err) {
        return res.status(401).json({
            message: "Invalid or expired token."
        });
    }
}

// ============================================
// TASK 8.1: SEARCH USER API (Clean single endpoint)
// GET /searchuser?email=... or ?name=...
// ============================================
app.get('/searchuser', verifyAdmin, async (req, res) => {
    try {
        const { email, name } = req.query;

        if (!email && !name) {
            return res.status(400).json({
                message: "Email or Name query parameter is required."
            });
        }

        const query = {};
        if (email) {
            query.email = email.toLowerCase().trim();
        } else if (name) {
            query.name = { $regex: name.trim(), $options: 'i' };
        }

        const user = await PersonModel.find(query).select('-password');

        if (!user || user.length === 0) {
            return res.status(404).json({
                message: "User not found."
            });
        }

        return res.status(200).json({
            message: "User found successfully",
            count: user.length,
            user: user.length === 1 ? user[0] : user
        });
    } catch (err) {
        return res.status(500).json({
            message: err.message || "Error searching user."
        });
    }
});

// ============================================
// TASK 8.2: VIEW ALL USERS API (Clean single endpoint)
// GET /viewalluser
// ============================================
app.get('/viewalluser', verifyAdmin, async (req, res) => {
    try {
        const users = await PersonModel.find().select('-password').sort({ createdAt: -1 });

        return res.status(200).json({
            message: "Retrieved all users information successfully.",
            totalUsers: users.length,
            users: users
        });
    } catch (err) {
        return res.status(500).json({
            message: err.message || "Error retrieving users."
        });
    }
});

// ============================================
// TASK 8.3: DELETE USER API (Clean single endpoint)
// DELETE /deluser?email=... or JSON body { email: ... }
// ============================================
app.delete('/deluser', verifyAdmin, async (req, res) => {
    try {
        const email = req.query.email || (req.body && req.body.email);

        if (!email) {
            return res.status(400).json({
                message: "Email is required to delete a user."
            });
        }

        const normalizedEmail = email.toLowerCase().trim();
        const deletedUser = await PersonModel.findOneAndDelete({ email: normalizedEmail });

        if (!deletedUser) {
            return res.status(404).json({
                message: `User '${normalizedEmail}' not found.`
            });
        }

        return res.status(200).json({
            message: "User deleted successfully.",
            deletedUser: {
                _id: deletedUser._id,
                name: deletedUser.name,
                email: deletedUser.email,
                role: deletedUser.role
            }
        });
    } catch (err) {
        return res.status(500).json({
            message: err.message || "Error deleting user."
        });
    }
});

app.listen(PORT, () => {
    console.log(`ADMIN Service Started at Port No: ${PORT}`);
});
