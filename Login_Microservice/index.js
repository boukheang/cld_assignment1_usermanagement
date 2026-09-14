const express = require('express');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
require('dotenv').config();

const dbconnect = require('./dbconnect.js');
const User = require('./user_schema.js');

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.LOGIN_PORT || 5002;
const JWT_SECRET = process.env.JWT_SECRET || '347186591486#^%%ABCF*##GHE';

// TASK 6: POST /auth/login
// Accepts { email, password, role }
app.post(['/auth/login', '/login'], async (req, res) => {
  console.log("--> LOGIN MICROSERVICE: Login attempt received");
  try {
    const { email, password, role } = req.body;

    // Validate presence of required fields
    if (!email || !password || !role) {
      return res.status(400).json({
        success: false,
        message: "Missing required fields: email, password, and role must be provided."
      });
    }

    const normalizedEmail = email.toLowerCase().trim();
    const normalizedRole = role.toLowerCase().trim();

    // 1. Find user by email in MongoDB
    const user = await User.findOne({ email: normalizedEmail });
    if (!user) {
      console.log(`Login failed: Email '${normalizedEmail}' not found in database.`);
      return res.status(401).json({
        success: false,
        message: "Invalid credentials: User with this email does not exist."
      });
    }

    // 2. Validate password with bcrypt
    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
      console.log(`Login failed: Incorrect password for '${normalizedEmail}'.`);
      return res.status(401).json({
        success: false,
        message: "Invalid credentials: Password does not match."
      });
    }

    // 3. Validate role
    if (user.role.toLowerCase() !== normalizedRole) {
      console.log(`Login failed: Role mismatch for '${normalizedEmail}'. Provided: ${normalizedRole}, Actual: ${user.role}`);
      return res.status(403).json({
        success: false,
        message: `Invalid role: Access denied. Account is registered as '${user.role}', but login requested as '${normalizedRole}'.`
      });
    }

    // 4. Generate JWT Token (payload: id, email, role) valid for 24 hours
    const token = jwt.sign(
      {
        id: user._id,
        email: user.email,
        role: user.role
      },
      JWT_SECRET,
      { expiresIn: '24h' }
    );

    console.log(`Login successful for user: ${user.email} [role: ${user.role}]`);

    return res.status(200).json({
      success: true,
      message: "Login successful. JWT token generated.",
      token: token,
      user: {
        _id: user._id,
        name: user.name,
        email: user.email,
        role: user.role,
        phone: user.phone
      }
    });
  } catch (error) {
    console.error("Login error:", error.message);
    return res.status(500).json({
      success: false,
      message: error.message || "Internal server error during login."
    });
  }
});

// Health check endpoint
app.get(['/', '/health'], (req, res) => {
  res.json({ status: "Login Microservice is running", port: PORT });
});

app.listen(PORT, () => {
  console.log(`Login Microservice Server Started at Port No: ${PORT}`);
});
