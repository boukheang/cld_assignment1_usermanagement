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

const PORT = process.env.LOGIN_PORT || process.env.AUTH_PORT || 5002;
const JWT_SECRETE = process.env.JWT_SECRETE || '347186591486#^%%ABCF*##GHE';

const PersonModel = require('./person_schema.js');
const dbconnect = require('./dbconnect.js');

// LOGIN API
app.post("/login", async (req, res) => {
  try {
    console.log("LOGIN API EXECUTED");
    const { email, password, role } = req.body;

    if (!email || !password || !role) {
      return res.status(400).json({
        message: "Missing required fields: email, password, and role must be provided."
      });
    }

    const normalizedEmail = email.toLowerCase().trim();
    const normalizedRole = role.toLowerCase().trim();

    // ============================================
    // 1. FIND USER BY EMAIL IN MONGODB
    // ============================================
    const user = await PersonModel.findOne({ email: normalizedEmail });

    // USER NOT FOUND
    if (!user) {
      return res.status(401).json({
        message: "Invalid credentials: User with this email does not exist."
      });
    }

    // ============================================
    // 2. COMPARE PLAINTEXT PASSWORD WITH HASH
    // ============================================
    const passwordMatch = await bcrypt.compare(password, user.password);

    // PASSWORD DOES NOT MATCH
    if (!passwordMatch) {
      return res.status(401).json({
        message: "Invalid credentials: Password does not match."
      });
    }

    // ============================================
    // 3. CHECK REGISTERED ROLE MATCHES REQUESTED ROLE
    // ============================================
    if (user.role.toLowerCase() !== normalizedRole) {
      return res.status(403).json({
        message: `Invalid role: Access denied. Account is registered as '${user.role}', but login requested as '${role}'.`
      });
    }

    // ============================================
    // 4. GENERATE 24H SIGNED JWT TOKEN
    // ============================================
    const token = jwt.sign(
      {
        id: user._id,
        email: user.email,
        role: user.role
      },
      JWT_SECRETE,
      {
        expiresIn: '24h'
      }
    );

    // ============================================
    // 5. RETURN TOKEN
    // ============================================
    return res.status(200).json({
      message: "Login successful",
      token: token,
      user: {
        _id: user._id,
        name: user.name,
        email: user.email,
        role: user.role
      }
    });
  } catch (err) {
    console.error("Login Error:", err);
    return res.status(500).json({
      message: err.message || "Internal server error during login."
    });
  }
});

app.listen(PORT, () => {
  console.log(`Authentication Service Server is running on PORT NO: ${PORT}`);
});
