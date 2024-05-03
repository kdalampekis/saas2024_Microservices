# Use an official Node.js runtime as a base image
FROM node:16-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock) from the front-end subdirectory
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code from the front-end subdirectory
COPY . .

# Expose port 3000 for the application
EXPOSE 3000

# Command to run the app
CMD ["npm", "start"]