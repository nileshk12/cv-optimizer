# Stage 1: Build the React app
FROM node:16 AS builder

WORKDIR /app

# Copy package files first to leverage Docker caching
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React app
RUN npm run build

# Stage 2: Serve the app with a lightweight server
FROM node:16-slim

WORKDIR /app

# Install a lightweight server to serve the static files
RUN npm install -g serve

# Copy the build output from the builder stage
COPY --from=builder /app/build ./build

# Expose the port for the frontend
EXPOSE 3000

# Command to serve the React app
CMD ["serve", "-s", "build", "-l", "3000"]
