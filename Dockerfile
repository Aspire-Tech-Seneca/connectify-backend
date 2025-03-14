# Use Node.js base image
FROM node:18

# Create app directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json .
RUN npm install

# Copy source files
COPY . .

# Expose port
EXPOSE 5000

# Start the application
CMD ["node", "server.js"]
