const express = require('express');
const cors = require('cors');
require('dotenv').config();

const dbconnect = require('./dbconnect.js');
const User = require('./user_schema.js');

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.ADMIN_PORT || 5003;

// TASK 8.1: GET /admin/searchuser - Search user by name or email
app.get(['/admin/searchuser', '/searchuser'], async (req, res) => {
  console.log("--> ADMIN MICROSERVICE: Search user request received", req.query);
  try {
    const { name, email } = req.query;

    if (!name && !email) {
      return res.status(400).json({
        success: false,
        message: "Search query required: please provide 'name' or 'email' as a query parameter."
      });
    }

    const query = {};
    if (email) {
      query.email = email.toLowerCase().trim();
    } else if (name) {
      query.name = { $regex: name.trim(), $options: 'i' }; // case-insensitive regex
    }

    const users = await User.find(query).select('-password');

    if (!users || users.length === 0) {
      return res.status(404).json({
        success: false,
        message: "User not found with the specified search criteria."
      });
    }

    return res.status(200).json({
      success: true,
      message: `Found ${users.length} user(s).`,
      count: users.length,
      users: users
    });
  } catch (error) {
    console.error("Error searching user:", error.message);
    return res.status(500).json({
      success: false,
      message: error.message || "Internal server error during search."
    });
  }
});

// TASK 8.2: GET /admin/viewalluser - View all users' information
app.get(['/admin/viewalluser', '/viewalluser'], async (req, res) => {
  console.log("--> ADMIN MICROSERVICE: View all users request received");
  try {
    const users = await User.find().select('-password').sort({ createdAt: -1 });

    return res.status(200).json({
      success: true,
      message: "Retrieved all users information successfully.",
      totalUsers: users.length,
      users: users
    });
  } catch (error) {
    console.error("Error viewing all users:", error.message);
    return res.status(500).json({
      success: false,
      message: error.message || "Internal server error while retrieving users."
    });
  }
});

// TASK 8.3: DELETE /admin/deluser - Delete a user by emailid
app.delete(['/admin/deluser', '/deluser'], async (req, res) => {
  console.log("--> ADMIN MICROSERVICE: Delete user request received", req.query, req.body);
  try {
    const email = req.query.email || (req.body && req.body.email);

    if (!email) {
      return res.status(400).json({
        success: false,
        message: "User email is required to delete a user (provide via ?email=... query or JSON body)."
      });
    }

    const normalizedEmail = email.toLowerCase().trim();
    const deletedUser = await User.findOneAndDelete({ email: normalizedEmail });

    if (!deletedUser) {
      return res.status(404).json({
        success: false,
        message: `Cannot delete: User with email '${normalizedEmail}' not found.`
      });
    }

    return res.status(200).json({
      success: true,
      message: `User '${normalizedEmail}' has been successfully deleted from the database.`,
      deletedUser: {
        _id: deletedUser._id,
        name: deletedUser.name,
        email: deletedUser.email,
        role: deletedUser.role
      }
    });
  } catch (error) {
    console.error("Error deleting user:", error.message);
    return res.status(500).json({
      success: false,
      message: error.message || "Internal server error during user deletion."
    });
  }
});

// Health check endpoint
app.get(['/', '/health'], (req, res) => {
  res.json({ status: "Admin Microservice is running", port: PORT });
});

app.listen(PORT, () => {
  console.log(`Admin Microservice Server Started at Port No: ${PORT}`);
});
