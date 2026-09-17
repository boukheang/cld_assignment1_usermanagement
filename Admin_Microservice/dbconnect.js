// STEP-1 : IMPORT MONGOOSE PACKAGE
const mongoose = require('mongoose');
require('dotenv').config();

// Database Connection URL
const uri = process.env.MONGODB_URI || "mongodb://fromheaventohelliamthegod_db_user:kp0m6aZ5uUhLiuoo@ac-v0qr9ql-shard-00-00.bziazoz.mongodb.net:27017,ac-v0qr9ql-shard-00-01.bziazoz.mongodb.net:27017,ac-v0qr9ql-shard-00-02.bziazoz.mongodb.net:27017/clusterdb?ssl=true&replicaSet=atlas-cvnewq-shard-0&authSource=admin&appName=Cluster0";

const clientOptions = { 
  serverApi: { version: '1', strict: true, deprecationErrors: true },
  serverSelectionTimeoutMS: 5000 
};

// STEP-2 : ESTABLISH CONNECTION WITH MONGODB DATABASE THROUGH MONGOOSE
async function connectDB() {
  try {
    await mongoose.connect(uri, clientOptions);
    await mongoose.connection.db.admin().command({ ping: 1 });
    console.log("Pinged your deployment. You successfully connected to MongoDB!");
  } catch (error) {
    console.error("MongoDB connection error:", error.message);
  }
}

connectDB();

// STEP-3 : EXPORT MODULE mongoose
module.exports = mongoose;
