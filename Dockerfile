# Use an official Node.js runtime as a base image
FROM node:14

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock) from the front-end subdirectory
COPY front-end/package.json front-end/package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code from the front-end subdirectory
COPY front-end/ ./

# Expose port 3000 for the application
EXPOSE 3000

# Command to run the app
CMD ["npm", "start"]
