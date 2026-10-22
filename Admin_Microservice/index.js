const express = require('express');
const app = express();

const jwt = require('jsonwebtoken');
require('dotenv').config();

app.use(express.json());

const JWT_SECRET = process.env.JWT_SECRETE;

const PersonModel = require('./person_schema.js');
const dbconnect = require('./dbconnect.js');

// ============================================
// JWT + ADMIN AUTHORIZATION MIDDLEWARE
// ============================================

function verifyAdmin(req, res, next) {

// Get Authorization header
const authHeader = req.headers.authorization;

// Check if token exists
if (!authHeader) {
    return res.status(401).json({
        message: "Access denied. Token is required."
    });
}


// Expected format:
// Authorization: Bearer TOKEN

const token = authHeader.split(' ')[1];


if (!token) {
    return res.status(401).json({
        message: "Invalid token format."
    });
}


try {

    // Verify JWT
    const decoded = jwt.verify(
        token,
        JWT_SECRET
    );


    // Check role
    if (decoded.role !== 'admin') {

        return res.status(403).json({
            message: "Access denied. Admin only."
        });

    }


    // Save logged-in user information
    req.user = decoded;


    // Continue to API
    next();

}
catch (err) {

    return res.status(401).json({
        message: "Invalid or expired token."
    });

}

}

// ============================================
// SEARCH USER API
// GET /searchuser?email=a@gmail.com
// ============================================

app.get('/searchuser', verifyAdmin, async (req, res) => {

try {

    const email = req.query.email;


    if (!email) {

        return res.status(400).json({
            message: "Email is required."
        });

    }


    // Search user by email
    const user = await PersonModel.findOne({
        email: email
    });


    if (!user) {

        return res.status(404).json({
            message: "User not found."
        });

    }


    return res.status(200).json({
        user: user
    });

}
catch (err) {

    return res.status(500).json({
        message: err.message || "Error searching user."
    });

}

});

// ============================================
// VIEW ALL USERS API
// GET /viewalluser
// ============================================

app.get('/viewalluser', verifyAdmin, async (req, res) => {

try {

    const users = await PersonModel.find();


    return res.status(200).json({
        totalUsers: users.length,
        users: users
    });

}
catch (err) {

    return res.status(500).json({
        message: err.message || "Error retrieving users."
    });

}

});

// ============================================
// DELETE USER API
// DELETE /deluser
// ============================================

app.delete('/deluser', verifyAdmin, async (req, res) => {

try {

    const email = req.body.email;


    if (!email) {

        return res.status(400).json({
            message: "Email is required."
        });

    }


    // Delete user
    const deletedUser =
        await PersonModel.findOneAndDelete({
            email: email
        });


    // User does not exist
    if (!deletedUser) {

        return res.status(404).json({
            message: "User not found."
        });

    }


    return res.status(200).json({

        message: "User deleted successfully."

    });

}
catch (err) {

    return res.status(500).json({
        message: err.message || "Error deleting user."
    });

}

});

// ============================================
// START EXPRESS SERVER
// ============================================

app.listen(5003, () =>

console.log(
    'ADMIN Service Started at Port No: 5003'
)

);
