const express = require('express');
const cors = require('cors');
require('dotenv').config();

const dbconnect = require('./dbconnect.js');
const User = require('./user_schema.js');

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.USER_PORT || 5004;

// TASK 9.1: GET /user/viewprofile - View own profile
app.get(['/user/viewprofile', '/viewprofile'], async (req, res) => {
  console.log("--> USER MICROSERVICE: View profile request received");
  try {
    // Authenticated user identity from API Gateway header, query, or body
    const userEmail = req.headers['x-user-email'] || req.query.email;
    const userId = req.headers['x-user-id'] || req.query.id;

    if (!userEmail && !userId) {
      return res.status(400).json({
        success: false,
        message: "User identifier missing from authenticated session."
      });
    }

    const query = userId ? { _id: userId } : { email: userEmail.toLowerCase().trim() };
    const user = await User.findOne(query).select('-password');

    if (!user) {
      return res.status(404).json({
        success: false,
        message: "User profile not found in the database."
      });
    }

    return res.status(200).json({
      success: true,
      message: "User profile retrieved successfully.",
      user: user
    });
  } catch (error) {
    console.error("Error viewing user profile:", error.message);
    return res.status(500).json({
      success: false,
      message: error.message || "Internal server error while fetching profile."
    });
  }
});

// TASK 9.2: PUT /user/updateprofile - Update own profile
app.put(['/user/updateprofile', '/updateprofile'], async (req, res) => {
  console.log("--> USER MICROSERVICE: Update profile request received", req.body);
  try {
    const userEmail = req.headers['x-user-email'] || (req.body && req.body.email);
    const userId = req.headers['x-user-id'] || (req.body && req.body.id);

    if (!userEmail && !userId) {
      return res.status(400).json({
        success: false,
        message: "User identifier missing from authenticated session."
      });
    }

    const query = userId ? { _id: userId } : { email: userEmail.toLowerCase().trim() };

    const { name, phone } = req.body;
    const updateData = {};
    if (name) updateData.name = name.trim();
    if (phone !== undefined) updateData.phone = phone.trim();

    if (Object.keys(updateData).length === 0) {
      return res.status(400).json({
        success: false,
        message: "No fields provided to update. Allowed fields: 'name', 'phone'."
      });
    }

    const updatedUser = await User.findOneAndUpdate(
      query,
      { $set: updateData },
      { new: true, runValidators: true }
    ).select('-password');

    if (!updatedUser) {
      return res.status(404).json({
        success: false,
        message: "User profile not found to update."
      });
    }

    return res.status(200).json({
      success: true,
      message: "User profile updated successfully.",
      user: updatedUser
    });
  } catch (error) {
    console.error("Error updating user profile:", error.message);
    return res.status(500).json({
      success: false,
      message: error.message || "Internal server error while updating profile."
    });
  }
});

// Health check endpoint
app.get(['/', '/health'], (req, res) => {
  res.json({ status: "User Microservice is running", port: PORT });
});

app.listen(PORT, () => {
  console.log(`User Microservice Server Started at Port No: ${PORT}`);
});
