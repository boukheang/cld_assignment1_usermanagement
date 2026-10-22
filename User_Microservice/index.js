const express = require('express');
const app = express();

const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

require('dotenv').config();

app.use(express.json());

const JWT_SECRET = process.env.JWT_SECRETE;

const PersonModel = require('./person_schema.js');
const dbconnect = require('./dbconnect.js');

// ============================================
// JWT AUTHENTICATION MIDDLEWARE
// ============================================

function verifyUser(req, res, next) {

const authHeader = req.headers.authorization;


// Check if Authorization header exists
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


    // Save user information from token
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
// VIEW MY PROFILE API
// GET /viewprofile
// ============================================

app.get('/viewprofile', verifyUser, async (req, res) => {

try {

    // Get email from JWT token
    const email = req.user.email;


    // Find user's own profile
    // Exclude password hash
    const user = await PersonModel
        .findOne({
            email: email
        })
        .select('-password');


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
        message: err.message || "Error viewing profile."
    });

}

});

// ============================================
// UPDATE MY PROFILE API
// PUT /updateprofile
// ============================================

app.put('/updateprofile', verifyUser, async (req, res) => {

try {

    // Get logged-in user's email from JWT
    const email = req.user.email;


    const {
        firstname,
        mobile,
        password
    } = req.body;


    // Object to store only fields being updated
    const updateData = {};


    // ============================================
    // UPDATE NAME
    // ============================================

    if (firstname) {

        updateData.name = firstname;

    }


    // ============================================
    // UPDATE MOBILE
    // ============================================

    if (mobile) {

        updateData.phone = mobile;

    }


    // ============================================
    // UPDATE PASSWORD
    // ============================================

    if (password) {

        const saltRounds = 10;


        // Hash new password
        updateData.password =
            await bcrypt.hash(
                password,
                saltRounds
            );

    }


    // Check if there is anything to update
    if (Object.keys(updateData).length === 0) {

        return res.status(400).json({
            message: "No profile information provided to update."
        });

    }


    // ============================================
    // UPDATE ONLY LOGGED-IN USER
    // ============================================

    const updatedUser =
        await PersonModel.findOneAndUpdate(

            {
                email: email
            },

            {
                $set: updateData
            },

            {
                new: true,
                runValidators: true
            }

        )
        .select('-password');


    if (!updatedUser) {

        return res.status(404).json({
            message: "User not found."
        });

    }


    return res.status(200).json({

        message: "Profile updated successfully.",

        user: updatedUser

    });

}
catch (err) {

    return res.status(500).json({
        message: err.message || "Error updating profile."
    });

}

});

// ============================================
// START EXPRESS SERVER
// ============================================

app.listen(5004, () =>

console.log(
    'USER Service Started at Port No: 5004'
)

);
