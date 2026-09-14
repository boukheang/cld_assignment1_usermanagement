const express = require('express');
const cors = require('cors');
const bcrypt = require('bcryptjs');
require('dotenv').config();

const dbconnect = require('./dbconnect.js');
const User = require('./user_schema.js');

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.REGISTRATION_PORT || 5001;

// TASK 5: POST /register/userregister
// Supports both direct path and Gateway routed path
app.post(['/register/userregister', '/userregister'], async (req, res) => {
  console.log("--> REGISTRATION MICROSERVICE: Registration request received");
  try {
    const { name, email, password, role, phone } = req.body;

    // Validate required fields
    if (!name || !email || !password || !role) {
      return res.status(400).json({
        success: false,
        message: "Missing required fields: name, email, password, and role are required."
      });
    }

    // Validate role
    const normalizedRole = role.toLowerCase().trim();
    if (!['admin', 'user'].includes(normalizedRole)) {
      return res.status(400).json({
        success: false,
        message: "Invalid role specified. Allowed roles: 'admin' or 'user'."
      });
    }

    // Check if email already exists (Duplicate Email Check)
    const normalizedEmail = email.toLowerCase().trim();
    const existingUser = await User.findOne({ email: normalizedEmail });
    if (existingUser) {
      console.log(`Registration failed: Duplicate email detected for ${normalizedEmail}`);
      return res.status(400).json({
        success: false,
        message: "Duplicate email not accepted. A user with this email address already exists."
      });
    }

    // Hash the password with bcrypt (10 salt rounds)
    const saltRounds = 10;
    const hashedPassword = await bcrypt.hash(password, saltRounds);

    // Create and save new user in MongoDB
    const newUser = new User({
      name: name.trim(),
      email: normalizedEmail,
      password: hashedPassword,
      role: normalizedRole,
      phone: phone ? phone.trim() : ""
    });

    const savedUser = await newUser.save();
    console.log(`User registered successfully: ${savedUser.email} [${savedUser.role}]`);

    // Return success response (omitting password hash)
    return res.status(201).json({
      success: true,
      message: "User registered successfully in MongoDB database.",
      user: {
        _id: savedUser._id,
        name: savedUser.name,
        email: savedUser.email,
        role: savedUser.role,
        phone: savedUser.phone,
        createdAt: savedUser.createdAt,
        updatedAt: savedUser.updatedAt
      }
    });
  } catch (error) {
    console.error("Error during registration:", error.message);
    return res.status(500).json({
      success: false,
      message: error.message || "Internal server error during registration."
    });
  }
});

// Health check endpoint
app.get(['/', '/health'], (req, res) => {
  res.json({ status: "Registration Microservice is running", port: PORT });
});

app.listen(PORT, () => {
  console.log(`Registration Microservice Server Started at Port No: ${PORT}`);
});
