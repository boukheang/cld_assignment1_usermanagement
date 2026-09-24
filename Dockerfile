# Use official Node.js LTS image
FROM node:24-alpine

# Set working directory inside the container
WORKDIR /app

# Copy dependency files first to leverage Docker layer caching
COPY package*.json ./

# Install application dependencies
RUN npm install

# Copy application source code
COPY . .

# Expose API Gateway (4000) and internal microservice ports (5001-5004)
EXPOSE 4000 5001 5002 5003 5004

# Start all microservices in the background and the API Gateway in the foreground
CMD ["sh", "-c", "node Registration_Microservice/registration.js & node Authentication_Microservice/authentication-service.js & node Admin_Microservice/index.js & node User_Microservice/index.js & exec node APIGateway_Microservice/api-gateway.js"]
