const schema_mongoose = require('mongoose');

const PersonSchema = schema_mongoose.Schema(
    {
       _id: {type: Number},
       name: { type: String },
       email: { type: String },
       password: { type: String },
       role: { type: String },
       phone: { type: Number },
    }, 
    {
       timestamps: true
    }
    );

module.exports = schema_mongoose.model('person_collections', PersonSchema);