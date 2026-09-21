const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

let bcrypt;
try {
  bcrypt = require('bcrypt');
} catch (e) {
  bcrypt = require('bcryptjs');
}

const dbconnect = require('./dbconnect.js');
const PersonModel = require('./person_schema.js');

function uniqueid(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min);
}

// REGISTRATION HANDLER
const handleRegistration = async (req, res) => {
  try {
    console.log("REG API EXECUTED");
    const {
      firstname,
      name,
      email,
      password,
      mobile,
      phone,
      role
    } = req.body;

    const userName = (name || firstname || '').trim();
    const userEmail = (email || '').toLowerCase().trim();
    const userPhone = phone || mobile || '';

    // 1. VALIDATE REQUIRED FIELDS
    if (!userName || !userEmail || !password || !role) {
      return res.status(400).json({
        message: "Missing required fields. Name, email, password, and role are required."
      });
    }

    // 2. VALIDATE ROLE
    const allowedRoles = ['admin', 'user'];
    const normalizedRole = role.toLowerCase().trim();
    if (!allowedRoles.includes(normalizedRole)) {
      return res.status(400).json({
        message: "Invalid role. Only admin or user is allowed."
      });
    }

    // 3. CHECK IF EMAIL ALREADY EXISTS
    const existingUser = await PersonModel.findOne({ email: userEmail });
    if (existingUser) {
      return res.status(400).json({
        message: "Duplicate email not accepted. A user with this email address already exists."
      });
    }

    // 4. HASH PASSWORD
    const saltRounds = 10;
    const hashedPassword = await bcrypt.hash(password, saltRounds);

    // 5. CREATE USER
    const pobj = new PersonModel({
      _id: uniqueid(1000, 9999),
      name: userName,
      email: userEmail,
      password: hashedPassword,
      phone: userPhone,
      role: normalizedRole
    });

    // 6. SAVE USER
    await pobj.save();

    return res.status(201).json({
      message: "User registered successfully",
      user: {
        _id: pobj._id,
        name: pobj.name,
        email: pobj.email,
        role: pobj.role
      }
    });
  } catch (err) {
    console.error("Registration Error:", err);
    return res.status(500).json({
      message: err.message || "Error in User Save"
    });
  }
};

// Expose clean endpoints without prefix duplication
app.post('/reg', handleRegistration);
app.post('/userregister', handleRegistration);

const PORT = process.env.PORT || 5001;
app.listen(PORT, () => {
  console.log(`Registration Microservice Server Started at Port No: ${PORT}`);
});
