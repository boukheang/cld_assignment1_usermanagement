const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
require('dotenv').config();

let bcrypt;
try {
    bcrypt = require('bcrypt');
} catch (e) {
    bcrypt = require('bcryptjs');
}

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 5004;
const JWT_SECRET = process.env.JWT_SECRETE || process.env.JWT_SECRET || '347186591486#^%%ABCF*##GHE';

const PersonModel = require('./person_schema.js');
const dbconnect = require('./dbconnect.js');

// ============================================
// JWT AUTHENTICATION MIDDLEWARE
// ============================================
function verifyUser(req, res, next) {
    // 1. Check if user identity was already verified and passed by API Gateway
    const gatewayEmail = req.headers['x-user-email'];
    const gatewayRole = req.headers['x-user-role'];
    if (gatewayEmail && gatewayRole) {
        req.user = { email: gatewayEmail, role: gatewayRole, id: req.headers['x-user-id'] };
        return next();
    }

    // 2. Otherwise verify incoming Bearer token directly
    const authHeader = req.headers['authorization'];
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
        req.user = decoded;
        next();
    } catch (err) {
        return res.status(401).json({
            message: "Invalid or expired token."
        });
    }
}

// ============================================
// TASK 9.1: VIEW MY PROFILE API (Clean single endpoint)
// GET /viewprofile
// ============================================
app.get('/viewprofile', verifyUser, async (req, res) => {
    try {
        const email = (req.user && req.user.email) ? req.user.email.toLowerCase().trim() : '';

        if (!email) {
            return res.status(400).json({
                message: "User identifier missing from authenticated session."
            });
        }

        const user = await PersonModel.findOne({ email: email }).select('-password');

        if (!user) {
            return res.status(404).json({
                message: "User not found."
            });
        }

        return res.status(200).json({
            message: "User profile retrieved successfully.",
            user: user
        });
    } catch (err) {
        return res.status(500).json({
            message: err.message || "Error viewing profile."
        });
    }
});

// ============================================
// TASK 9.2: UPDATE MY PROFILE API (Clean single endpoint)
// PUT /updateprofile
// ============================================
app.put('/updateprofile', verifyUser, async (req, res) => {
    try {
        const email = (req.user && req.user.email) ? req.user.email.toLowerCase().trim() : '';

        if (!email) {
            return res.status(400).json({
                message: "User identifier missing from authenticated session."
            });
        }

        const { firstname, name, mobile, phone, password } = req.body;
        const updateData = {};

        const updatedName = name || firstname;
        if (updatedName) updateData.name = updatedName.trim();

        const updatedPhone = phone || mobile;
        if (updatedPhone !== undefined) updateData.phone = updatedPhone;

        if (password) {
            const saltRounds = 10;
            updateData.password = await bcrypt.hash(password, saltRounds);
        }

        if (Object.keys(updateData).length === 0) {
            return res.status(400).json({
                message: "No profile information provided to update."
            });
        }

        const updatedUser = await PersonModel.findOneAndUpdate(
            { email: email },
            { $set: updateData },
            { new: true, runValidators: true }
        ).select('-password');

        if (!updatedUser) {
            return res.status(404).json({
                message: "User not found."
            });
        }

        return res.status(200).json({
            message: "Profile updated successfully.",
            user: updatedUser
        });
    } catch (err) {
        return res.status(500).json({
            message: err.message || "Error updating profile."
        });
    }
});

app.listen(PORT, () => {
    console.log(`USER Service Started at Port No: ${PORT}`);
});
