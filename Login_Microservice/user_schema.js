const mongoose = require('./dbconnect.js');

// TASK 3: MongoDB User Model Schema
const userSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, 'Name is required'],
      trim: true
    },
    email: {
      type: String,
      required: [true, 'Email is required'],
      unique: true,
      lowercase: true,
      trim: true
    },
    password: {
      type: String,
      required: [true, 'Password is required']
    },
    role: {
      type: String,
      required: [true, 'Role is required (admin or user)'],
      enum: ['admin', 'user'],
      lowercase: true,
      trim: true
    },
    phone: {
      type: String,
      required: false,
      trim: true
    }
  },
  {
    timestamps: true // Automatically manages createdAt and updatedAt
  }
);

const User = mongoose.models.User || mongoose.model('User', userSchema);

module.exports = User;
