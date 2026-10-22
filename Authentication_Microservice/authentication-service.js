const express = require('express');
const app = express();

const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

require('dotenv').config();

app.use(express.json());

const JWT_SECRETE = process.env.JWT_SECRETE;

const PersonModel = require('./person_schema.js');
const dbconnect = require('./dbconnect.js');

/*
In Postman use:

localhost:5002/login

{
"email": "a@gmail.com",
"password": "abc",
"role": "student"
}
*/

// LOGIN API
app.post("/login", async (req, res) => {

try {

console.log("LOGIN API EXECUTED");

const {
  email,
  password,
  role
} = req.body;


// ============================================
// 1. FIND USER BY EMAIL AND ROLE
// ============================================
const user = await PersonModel.findOne({
  email: email,
  role: role
});


// USER NOT FOUND
if (!user) {
  return res.status(401).send({
    message: "Invalid email, password, or role"
  });
}


// ============================================
// 2. COMPARE PLAINTEXT PASSWORD WITH HASH
// ============================================
const passwordMatch = await bcrypt.compare(
  password,        // Plaintext password from user
  user.password    // Hashed password from MongoDB
);


// PASSWORD DOES NOT MATCH
if (!passwordMatch) {
  return res.status(401).send({
    message: "Invalid email, password, or role"
  });
}


// ============================================
// 3. GENERATE JWT TOKEN
// ============================================
const token = jwt.sign(

  {
    email: user.email,
    role: user.role
  },

  JWT_SECRETE,

  {
    expiresIn: '24h'
  }

);


// ============================================
// 4. RETURN TOKEN
// ============================================
return res.status(200).json({

  message: "Login successful",

  token: token

});

}

catch (err) {

console.error(err);

return res.status(500).send({

  message: err.message || "Authentication error"

});

}

});

// START SERVER
app.listen(5002, () => {

console.log(
'Authentication Service Server is running on PORT NO: 5002'
);

});
